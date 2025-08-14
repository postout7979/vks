from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os,requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
from functools import wraps

# InsecureRequestWarning 경고를 무시하도록 설정
warnings.simplefilter('ignore', InsecureRequestWarning)

# Flask 애플리케이션을 API 전용으로 초기화합니다.
# 템플릿 및 정적 파일 경로를 지정하지 않습니다.
app = Flask(__name__)

# 세션 관리를 위한 비밀 키를 설정합니다.
# 실제 환경에서는 이 키를 환경 변수나 별도의 설정 파일에 저장해야 합니다.
app.secret_key = 'sdklfsdfhewoiwe3242234f'

# 가상의 사용자 데이터베이스
USERS = {
    "admin": "admin"
}

# Avi Controller 정보 (환경 변수에서 가져옴)
AVI_CONTROLLER_IP = os.environ.get("AVI_CONTROLLER_IP")
AVI_USERNAME = os.environ.get("AVI_USERNAME")
AVI_PASSWORD = os.environ.get("AVI_PASSWORD")
# 인증에 필요한 API 버전
API_VERSION = "30.1.1"

session_token = None
session_id = None
avisession_id = None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'avi_api_sessionid' not in session:
            # 로그인 되지 않았을 경우 401 Unauthorized 응답을 반환합니다.
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

# 새로 추가된 API 엔드포인트: 로그인 상태를 JSON으로 반환
@app.route('/api/check_login_status', methods=['GET'])
def check_login_status():
    # 세션에 'user' 정보가 있으면 로그인 상태
    if 'avi_api_sessionid' in session:
        return jsonify({'is_logged_in': True}), 200
    else:
        return jsonify({'is_logged_in': False}), 200


@app.route('/api/login', methods=['POST'])
def login():
    """
    로그인 요청을 처리하는 API입니다.
    요청 본문에서 사용자 이름과 비밀번호를 받아 인증을 수행합니다.
    인증에 성공하면 세션에 'logged_in' 플래그를 설정하고 성공 메시지를 반환합니다.
    """
    global session_token
    global session_id
    global avisession_id
    
    username = request.json.get('username')
    password = request.json.get('password')

    login_url = f"https://{AVI_CONTROLLER_IP}/login"

    headers = {
        "Content-Type": "application/json",
        "X-Avi-Version": API_VERSION
    }
    data = {
        "username": AVI_USERNAME,
        "password": AVI_PASSWORD
    }

    try:
        response = requests.post(login_url, json=data, headers=headers, verify=False)
        response.raise_for_status()

        avisession_id = response.cookies.get('avi-sessionid')
        session_id = response.cookies.get('sessionid')
        session_token = response.cookies.get('csrftoken')

        # 가상의 사용자 데이터베이스와 비교하여 인증합니다.
        if username in USERS and USERS[username] == password:
            # 인증 성공 시, 세션에 로그인 상태를 기록합니다.
            session['logged_in'] = True
            session['username'] = username
            print(f"User {username} logged in successfully.")
            if session_id:
                # 세션에 인증 정보를 저장하고 성공 응답을 반환합니다.
                session['avi_api_sessionid'] = session_id
                session['avi_api_token'] = session_token
                return jsonify({"success": True}), 200
            else:
                return jsonify({"error": "로그인 실패: 세션 ID를 가져올 수 없습니다."}), 401
        else:
            # 인증 실패 시, 실패 메시지를 반환합니다.
            print(f"Login failed for user {username}.")
            return jsonify({"success": False, "message": "Invalid credentials"}), 401

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "로그인 정보가 올바르지 않습니다."}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    global session_token
    global session_id
    global avisession_id

    session.pop('avi_api_token', None)
    session.pop('avi_api_sessionid', None)

    session_token = None
    session_id = None

    """
    로그아웃 요청을 처리하는 API입니다.
    사용자의 세션 데이터를 모두 삭제하고 성공 메시지를 반환합니다.
    """
    try:
        # 세션에서 모든 데이터를 삭제하여 로그아웃합니다.
        session.clear()
        print("User logged out successfully.")
        return jsonify({"success": True, "message": "Logged out successfully"}), 200
    except Exception as e:
        # 로그아웃 중 예외가 발생하면 오류를 반환합니다.
        print(f"Error during logout: {e}")
        return jsonify({"success": False, "message": "Server error during logout"}), 500

@app.route('/api/vs_list')
@login_required
def get_vs_list():
    token = session.get('avi_api_token')
    apisessionid = session.get('avi_api_sessionid')
    headers = {
        "X-Avi-Version": API_VERSION,
        "X-CSRFToken": token
    }
    
    url = f"https://{AVI_CONTROLLER_IP}/api/virtualservice"

    try:
        response = requests.get(url, headers=headers, cookies=dict(sessionid=apisessionid), verify=False)
        response.raise_for_status()
        vs_data = response.json()
        
        vs_list = [{'name': vs['name'], 'uuid': vs['uuid']} for vs in vs_data.get('results', [])]
        return jsonify(vs_list)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/performance')
@login_required
def get_performance_data():
    token = session.get('avi_api_token')
    apisessionid = session.get('avi_api_sessionid')
    headers = {
        "X-Avi-Version": API_VERSION,
        "X-CSRFToken": token
    }

    url = f"https://{AVI_CONTROLLER_IP}/api/analytics/metrics/virtualservice?metric_id=l4_client.avg_bandwidth,l4_server.avg_open_conns&limit=10"

    try:
        vs_list_url = f"https://{AVI_CONTROLLER_IP}/api/virtualservice"
        vs_response = requests.get(vs_list_url, headers=headers, cookies=dict(sessionid=apisessionid), verify=False)
        vs_response.raise_for_status()
        vs_data = vs_response.json()

        vs_name_map = {vs['uuid']: vs['name'] for vs in vs_data.get('results', [])}

        response = requests.get(url, headers=headers, cookies=dict(sessionid=apisessionid), verify=False)
        response.raise_for_status()
        performance_data = response.json()

        if performance_data.get('results'):
            for item in performance_data['results']:
                metric_entity_uuid = item.get('entity_uuid')
                item['metric_entity_name'] = vs_name_map.get(metric_entity_uuid, 'name')

        return jsonify(performance_data)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/performance/<string:vs_uuid>')
@login_required
def get_vs_performance_data(vs_uuid):
    token = session.get('avi_api_token')
    apisessionid = session.get('avi_api_sessionid')
    headers = {
        "X-Avi-Version": API_VERSION,
        "X-CSRFToken": token
    }
    
    url = f"https://{AVI_CONTROLLER_IP}/api/analytics/metrics/virtualservice?metric_id=l4_client.avg_bandwidth&entity_uuid={vs_uuid}&limit=10"

    try:
        vs_list_url = f"https://{AVI_CONTROLLER_IP}/api/virtualservice"
        vs_response = requests.get(vs_list_url, headers=headers, cookies=dict(sessionid=apisessionid), verify=False)
        vs_response.raise_for_status()
        vs_data = vs_response.json()

        vs_name_map = {vs['uuid']: vs['name'] for vs in vs_data.get('results', [])}

        response = requests.get(url, headers=headers, cookies=dict(sessionid=apisessionid), verify=False)
        response.raise_for_status()
        performance_data = response.json()

        if performance_data.get('results'):
            for item in performance_data['results']:
                metric_entity_uuid = item.get('entity_uuid')
                item['metric_entity_name'] = vs_name_map.get(metric_entity_uuid, 'name')

        return jsonify(performance_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Flask app run
    app.run(host='0.0.0.0', port=5000, debug=True)

