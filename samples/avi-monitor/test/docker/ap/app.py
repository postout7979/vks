from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os,requests
import warnings
import threading
import time
from urllib3.exceptions import InsecureRequestWarning
from functools import wraps
import json

# InsecureRequestWarning 경고를 무시하도록 설정
warnings.simplefilter('ignore', InsecureRequestWarning)

# Flask 애플리케이션을 API 전용으로 초기화합니다.
# 템플릿 및 정적 파일 경로를 지정하지 않습니다.
app = Flask(__name__)

# 세션 관리를 위한 비밀 키를 설정합니다.
# 실제 환경에서는 이 키를 환경 변수나 별도의 설정 파일에 저장해야 합니다.
app.secret_key = 'sdklfsdfhewoiwe3242234f'

# Avi Controller 정보 (환경 변수에서 가져옴)
AVI_CONTROLLER_IP = os.environ.get("AVI_CONTROLLER_IP")
AVI_USERNAME = os.environ.get("AVI_USERNAME")
AVI_PASSWORD = os.environ.get("AVI_PASSWORD")
# 인증에 필요한 API 버전
API_VERSION = "30.1.1"

# 전역 세션 관리 변수
avi_session_cookie = None
avi_csrftoken = None
avi_sessionid = None
lock = threading.Lock()

def session_renewal_task():
    """
    주기적으로 Avi Controller 세션을 갱신하는 백그라운드 작업입니다.
    """
    while True:
        login_to_avi_controller()
        # 1시간(3600초)마다 세션 갱신
        time.sleep(3600)

def login_to_avi_controller():
    """
    Avi Controller에 로그인하고 세션 쿠키를 갱신합니다.
    """
    global avi_session_cookie, avi_sessionid, avi_csrftoken
    login_url = f"https://{AVI_CONTROLLER_IP}/login"
    payload = {
        "username": AVI_USERNAME,
        "password": AVI_PASSWORD
    }
    
    with lock:
        try:
            response = requests.post(login_url, json=payload, verify=False)
            response.raise_for_status()

            # 응답 헤더에서 Set-Cookie 값 추출
            if 'Set-Cookie' in response.headers:
                avi_session_cookie = response.headers['Set-Cookie']
                avi_sessionid = response.cookies.get('sessionid')
                avi_csrftoken = response.cookies.get('csrftoken')
                print("Avi Controller 세션이 성공적으로 갱신되었습니다.")
            else:
                print("Avi Controller 로그인 실패: 세션 쿠키를 찾을 수 없습니다.")
                avi_session_cookie = None
        except requests.exceptions.RequestException as e:
            print(f"Avi Controller 로그인 오류: {e}")
            avi_session_cookie = None
            avi_sessionid = None
            avi_csrftoken = None

def get_avi_session_info():
    """
    Avi Controller 세션 정보를 딕셔너리로 반환합니다.
    """
    with lock:
        return {
            'sessionid': avi_sessionid,
            'csrftoken': avi_csrftoken
        }

@app.route('/api/vs_list')
def get_vs_list():
    avi_session = get_avi_session_info()
    if not avi_session['sessionid'] or not avi_session['csrftoken']:
        return jsonify({"error": "Avi Controller 세션을 가져올 수 없습니다. 잠시 후 다시 시도하십시오."}), 503

    headers = {
        "X-Avi-Version": API_VERSION,
        "X-CSRFToken": avi_session['csrftoken']
    }
    url = f"https://{AVI_CONTROLLER_IP}/api/virtualservice"

    try:
        response = requests.get(url, headers=headers, cookies=dict(sessionid=avi_session['sessionid']), verify=False)
        response.raise_for_status()
        vs_data = response.json()
        vs_list = [{'name': vs['name'], 'uuid': vs['uuid']} for vs in vs_data.get('results', [])]
        return jsonify(vs_list)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/performance')
def get_performance_data():
    avi_session = get_avi_session_info()
    if not avi_session['sessionid'] or not avi_session['csrftoken']:
        return jsonify({"error": "Avi Controller 세션을 가져올 수 없습니다. 잠시 후 다시 시도하십시오."}), 503

    headers = {
        "X-Avi-Version": API_VERSION,
        "X-CSRFToken": avi_session['csrftoken']
    }
    
    url = f"https://{AVI_CONTROLLER_IP}/api/analytics/metrics/virtualservice?metric_id=l4_client.avg_bandwidth,l4_client.max_open_conns&limit=10"

    try:
        vs_list_url = f"https://{AVI_CONTROLLER_IP}/api/virtualservice"
        vs_response = requests.get(vs_list_url, headers=headers, cookies=dict(sessionid=avi_session['sessionid']), verify=False)
        vs_response.raise_for_status()
        vs_data = vs_response.json()
        vs_name_map = {vs['uuid']: vs['name'] for vs in vs_data.get('results', [])}
        
        response = requests.get(url, headers=headers, cookies=dict(sessionid=avi_session['sessionid']), verify=False)
        response.raise_for_status()
        performance_data = response.json()

        if performance_data.get('results'):
            for item in performance_data['results']:
                metric_entity_uuid = item.get('entity_uuid')
                item['metric_entity_name'] = vs_name_map.get(metric_entity_uuid, 'name')
        
        return jsonify(performance_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/pool')
def get_pool_data():
    avi_session = get_avi_session_info()
    if not avi_session['sessionid'] or not avi_session['csrftoken']:
        return jsonify({"error": "Avi Controller 세션을 가져올 수 없습니다. 잠시 후 다시 시도하십시오."}), 503

    headers = {
        "X-Avi-Version": API_VERSION,
        "X-CSRFToken": avi_session['csrftoken']
    }
    url = f"https://{AVI_CONTROLLER_IP}/api/pool"

    try:
        response = requests.get(url, headers=headers, cookies=dict(sessionid=avi_session['sessionid']), verify=False)
        response.raise_for_status()
        data = response.json()

        if "count" in data:
            count_data = data["count"]
            return jsonify(count_data)
        else:
            print("응답에 'count' 필드가 없습니다.")
            return jsonify({"error": "No 'count' field in response"}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except json.JSONDecodeError:
        print("JSON 응답을 파싱하는 데 실패했습니다.")
        return jsonify({"error": "Failed to parse JSON response"}), 500

@app.route('/api/performance/<string:vs_uuid>')
def get_vs_performance_data(vs_uuid):
    avi_session = get_avi_session_info()
    if not avi_session['sessionid'] or not avi_session['csrftoken']:
        return jsonify({"error": "Avi Controller 세션을 가져올 수 없습니다. 잠시 후 다시 시도하십시오."}), 503

    headers = {
        "X-Avi-Version": API_VERSION,
        "X-CSRFToken": avi_session['csrftoken']
    }

    url = f"https://{AVI_CONTROLLER_IP}/api/analytics/metrics/virtualservice?metric_id=l4_client.avg_bandwidth&entity_uuid={vs_uuid}&limit=10"

    try:
        vs_list_url = f"https://{AVI_CONTROLLER_IP}/api/virtualservice"
        vs_response = requests.get(vs_list_url, headers=headers, cookies=dict(sessionid=avi_session['sessionid']), verify=False)
        vs_response.raise_for_status()
        vs_data = vs_response.json()
        vs_name_map = {vs['uuid']: vs['name'] for vs in vs_data.get('results', [])}

        response = requests.get(url, headers=headers, cookies=dict(sessionid=avi_session['sessionid']), verify=False)
        response.raise_for_status()
        performance_data = response.json()

        if performance_data.get('results'):
            for item in performance_data['results']:
                metric_entity_uuid = item.get('entity_uuid')
                item['metric_entity_name'] = vs_name_map.get(metric_entity_uuid, 'name')

        return jsonify(performance_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Flask 애플리케이션 컨텍스트를 사용하여 스레드 시작
with app.app_context():
    thread = threading.Thread(target=session_renewal_task)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

