from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
from functools import wraps
import psycopg2
from psycopg2 import sql
import threading
import time
import json
from datetime import datetime
from collections import defaultdict

# InsecureRequestWarning 경고를 무시하도록 설정
warnings.simplefilter('ignore', InsecureRequestWarning)

# Flask 애플리케이션 초기화
app = Flask(__name__)

# 세션 관리를 위한 비밀 키 설정
app.secret_key = 'sdklfsdfhewoiwe3242234f'

# 가상의 사용자 데이터베이스 (테스트용)
USERS = {
    "admin": "admin"
}

# Avi Controller 정보 (환경 변수에서 가져옴)
AVI_CONTROLLER_IP = os.environ.get("AVI_CONTROLLER_IP")
AVI_USERNAME = os.environ.get("AVI_USERNAME")
AVI_PASSWORD = os.environ.get("AVI_PASSWORD")
API_VERSION = "30.1.1"

# PostgreSQL 데이터베이스 정보 (환경 변수에서 가져옴)
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")

# 데이터베이스 연결
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"데이터베이스 연결 실패: {e}")
        return None

# 데이터베이스 테이블 생성
def create_table_if_not_exists():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS vs_performance (
                        id SERIAL PRIMARY KEY,
                        vs_uuid VARCHAR(255) NOT NULL,
                        vs_name VARCHAR(255),
                        metric_id VARCHAR(255) NOT NULL,
                        value_type VARCHAR(255),
                        value FLOAT,
                        timestamp TIMESTAMPTZ DEFAULT NOW()
                    );
                """)
                conn.commit()
            print("데이터베이스 테이블이 성공적으로 생성되었거나 이미 존재합니다.")
        except Exception as e:
            print(f"테이블 생성 실패: {e}")
        finally:
            conn.close()

# 세션 관리용 전역 변수 (스레드 간 공유)
session_token = None
session_id = None
avisession_id = None

# 로그인 데코레이터
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

# 로그인 상태 확인 API
@app.route('/api/check_login_status', methods=['GET'])
def check_login_status():
    if 'username' in session:
        return jsonify({'is_logged_in': True}), 200
    else:
        return jsonify({'is_logged_in': False}), 200

# AVI Controller 로그인 API
@app.route('/api/login', methods=['POST'])
def login():
    global session_token, session_id, avisession_id

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

        response = requests.post(login_url, json=data, headers=headers, verify=False)
        response.raise_for_status()

        if username in USERS and USERS[username] == password:

            if session_id:
                session['logged_in'] = True
                session['username'] = username
                session['avi_api_sessionid'] = session_id
                session['avi_api_token'] = session_token
                return jsonify({"success": True, "message": "로그인 성공"}), 200
            else:
                return jsonify({"error": "로그인 실패: 세션 ID를 가져올 수 없습니다."}), 401
        else:
            return jsonify({"success": False, "message": "잘못된 자격 증명"}), 401

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "로그인 실패: 컨트롤러 정보가 올바르지 않습니다."}), 401

# 로그아웃 API
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    global session_token, session_id, avisession_id

    session.pop('avi_api_token', None)
    session.pop('avi_api_sessionid', None)
    session.pop('logged_in', None)
    session.pop('username', None)

    session_token = None
    session_id = None
    avisession_id = None

    try:
        session.clear()
        return jsonify({"success": True, "message": "로그아웃 성공"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": "로그아웃 중 오류 발생"}), 500

# VS 목록 조회 API
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

# 백그라운드에서 주기적으로 AVI Controller로부터 성능 데이터 가져와 DB에 저장
def fetch_and_save_performance_data():
    while True:
        try:
            # 세션 토큰이 없으면 로그인 시도
            if not session_id:
                print("세션 ID가 없어 로그인 시도 중...")
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
                    session_id = response.cookies.get('sessionid')
                    session_token = response.cookies.get('csrftoken')
                    print("로그인 성공, 세션 ID 및 토큰 획득.")
                except requests.exceptions.RequestException as e:
                    print(f"자동 로그인 실패: {e}")
                    time.sleep(5)
                    continue

            headers = {
                "X-Avi-Version": API_VERSION,
                "X-CSRFToken": session_token
            }
            cookies = dict(sessionid=session_id)
            
            # VS 목록 가져오기
            vs_list_url = f"https://{AVI_CONTROLLER_IP}/api/virtualservice"
            vs_response = requests.get(vs_list_url, headers=headers, cookies=cookies, verify=False)
            vs_response.raise_for_status()
            vs_data = vs_response.json()
            vs_name_map = {vs['uuid']: vs['name'] for vs in vs_data.get('results', [])}

            # 성능 데이터 가져오기
            performance_url = f"https://{AVI_CONTROLLER_IP}/api/analytics/metrics/virtualservice?metric_id=l4_client.avg_bandwidth,l4_server.avg_open_conns&limit=1"
            response = requests.get(performance_url, headers=headers, cookies=cookies, verify=False)
            response.raise_for_status()
            performance_data = response.json()

            conn = get_db_connection()
            if conn:
                try:
                    with conn.cursor() as cur:
                        for item in performance_data.get('results', []):
                            vs_uuid = item.get('entity_uuid')
                            vs_name = vs_name_map.get(vs_uuid, 'name')
                            for series in item.get('series', []):
                                metric_id = series.get('metric_id')
                                for data_point in series.get('data', []):
                                    value = data_point.get('value')
                                    value_type = 'float'
                                    if value is not None:
                                        cur.execute(
                                            sql.SQL("""
                                                INSERT INTO vs_performance (vs_uuid, vs_name, metric_id, value_type, value)
                                                VALUES (%s, %s, %s, %s, %s)
                                            """),
                                            (vs_uuid, vs_name, metric_id, value_type, value)
                                        )
                        conn.commit()
                        print("AVI 성능 데이터가 데이터베이스에 성공적으로 저장되었습니다.")
                except Exception as e:
                    print(f"데이터베이스 저장 실패: {e}")
                finally:
                    conn.close()

        except requests.exceptions.RequestException as e:
            print(f"AVI Controller에서 데이터 가져오기 실패: {e}")
        except Exception as e:
            print(f"백그라운드 스레드 오류: {e}")

        # 5초마다 실행
        time.sleep(5)

# API: DB에서 성능 데이터 조회 (모든 VS)
@app.route('/api/performance')
@login_required
def get_performance_data():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "데이터베이스에 연결할 수 없습니다."}), 500

    try:
        with conn.cursor() as cur:
            # 최근 1시간 동안의 데이터를 가져옵니다.
            cur.execute("""
                SELECT vs_uuid, vs_name, metric_id, value, timestamp
                FROM vs_performance
                WHERE timestamp >= NOW() - INTERVAL '1 hour'
                ORDER BY vs_uuid, metric_id, timestamp;
            """)
            results = cur.fetchall()
            
            # 데이터를 VS 및 지표별로 그룹화합니다.
            vs_data_map = defaultdict(lambda: {'series': defaultdict(list)})
            
            for row in results:
                vs_uuid, vs_name, metric_id, value, timestamp = row
                
                # VS 메타데이터를 저장합니다.
                vs_data_map[vs_uuid]['entity_uuid'] = vs_uuid
                vs_data_map[vs_uuid]['metric_entity_name'] = vs_name
                
                # 지표별 시계열 데이터를 추가합니다.
                vs_data_map[vs_uuid]['series'][metric_id].append({
                    'value': value,
                    'timestamp': timestamp.isoformat()
                })
            
            # 최종 출력 형식에 맞게 변환합니다.
            final_results = []
            for vs_uuid, vs_data in vs_data_map.items():
                vs_item = {
                    'entity_uuid': vs_data['entity_uuid'],
                    'metric_entity_name': vs_data['metric_entity_name'],
                    'series': []
                }
                for metric_id, data_points in vs_data['series'].items():
                    vs_item['series'].append({
                        'header': {'name': metric_id},
                        'data': data_points
                    })
                final_results.append(vs_item)
            
            return jsonify({"results": final_results}), 200
    except Exception as e:
        return jsonify({"error": f"데이터베이스 조회 실패: {e}"}), 500
    finally:
        conn.close()

# API: 특정 VS의 성능 데이터 조회
@app.route('/api/performance/<string:vs_uuid>')
@login_required
def get_vs_performance_data(vs_uuid):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "데이터베이스에 연결할 수 없습니다."}), 500

    try:
        with conn.cursor() as cur:
            # 특정 VS의 최근 1시간 동안의 데이터를 가져옵니다.
            cur.execute(
                sql.SQL("""
                    SELECT vs_uuid, vs_name, metric_id, value, timestamp
                    FROM vs_performance
                    WHERE vs_uuid = %s AND timestamp >= NOW() - INTERVAL '1 hour'
                    ORDER BY metric_id, timestamp;
                """),
                (vs_uuid,)
            )
            results = cur.fetchall()

            # 데이터를 지표별로 그룹화합니다.
            vs_data_map = defaultdict(list)
            vs_name = ""
            for row in results:
                vs_uuid, vs_name_from_db, metric_id, value, timestamp = row
                vs_name = vs_name_from_db # 마지막 값으로 VS 이름 설정
                vs_data_map[metric_id].append({
                    'value': value,
                    'timestamp': timestamp.isoformat()
                })

            # 최종 출력 형식에 맞게 변환합니다.
            final_results = [{
                'entity_uuid': vs_uuid,
                'metric_entity_name': vs_name,
                'series': [
                    {
                        'header': {'name': metric_id},
                        'data': data_points
                    } for metric_id, data_points in vs_data_map.items()
                ]
            }]
            
            return jsonify({"results": final_results}), 200
    except Exception as e:
        return jsonify({"error": f"데이터베이스 조회 실패: {e}"}), 500
    finally:
        conn.close()


@app.route('/api/pool')
@login_required
def get_pool_data():
    token = session.get('avi_api_token')
    apisessionid = session.get('avi_api_sessionid')
    headers = {
        "X-Avi-Version": API_VERSION,
        "X-CSRFToken": token
    }
    url = f"https://{AVI_CONTROLLER_IP}/api/pool"
    try:
        response = requests.get(url, headers=headers, cookies=dict(sessionid=apisessionid), verify=False)
        response.raise_for_status()
        data = response.json()
        if "count" in data:
            count_data = data["count"]
            return jsonify(count_data)
        else:
            return jsonify({"error": "응답에 'count' 필드가 없습니다."}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "JSON 응답을 파싱하는 데 실패했습니다."}), 500

# 애플리케이션 시작 시 DB 테이블 생성 및 백그라운드 스레드 시작
if __name__ == '__main__':
    create_table_if_not_exists()
    
    # 백그라운드 스레드 시작
    fetch_thread = threading.Thread(target=fetch_and_save_performance_data)
    fetch_thread.daemon = True # 메인 스레드 종료 시 함께 종료
    fetch_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True)

