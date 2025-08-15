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
import uuid

# InsecureRequestWarning 경고를 무시하도록 설정
warnings.simplefilter('ignore', InsecureRequestWarning)

# Flask 애플리케이션 초기화
app = Flask(__name__)

# 세션 관리를 위한 비밀 키 설정. 실제 운영 환경에서는 더 안전하게 관리해야 합니다.
app.secret_key = 'sdklfsdfhewoiwe3242234f'

# Avi Controller 정보 (환경 변수에서 가져옴)
# 컨테이너 환경에서 실행될 때 이 변수들이 설정되어야 합니다.
AVI_CONTROLLER_IP = os.environ.get("AVI_CONTROLLER_IP")
AVI_USERNAME = os.environ.get("AVI_USERNAME")
AVI_PASSWORD = os.environ.get("AVI_PASSWORD")
API_VERSION = "30.1.1"

username="admin"
password="admin"

# PostgreSQL 데이터베이스 정보 (환경 변수에서 가져옴)
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")

# 로그인 세션 정보 저장
session_id = None
session_token = None

# DB 연결 함수
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"데이터베이스 연결 실패: {e}")
        return None

# DB 테이블 생성 함수
def create_table_if_not_exists():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                # 테이블이 이미 존재하면 삭제합니다.
                # 이는 ON CONFLICT 구문이 요구하는 PRIMARY KEY가 정확히 설정되도록 보장합니다.
                cur.execute("DROP TABLE IF EXISTS vs_performance CASCADE;")
                
                cur.execute("""
                    CREATE TABLE vs_performance (
                        vs_uuid VARCHAR(255),
                        vs_name VARCHAR(255),
                        metric_id VARCHAR(255),
                        value REAL,
                        timestamp TIMESTAMP WITH TIME ZONE,
                        PRIMARY KEY (vs_uuid, metric_id, timestamp)
                    );
                """)
                conn.commit()
            print("vs_performance 테이블이 성공적으로 삭제 및 재생성되었습니다.")
        except Exception as e:
            print(f"테이블 생성 중 오류 발생: {e}")
        finally:
            conn.close()

# 로그인 확인 데코레이터
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# --- 라우팅 설정 ---
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

# 로그인 API
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # 환경 변수로 설정된 사용자명과 비밀번호로 로그인 처리
    if username == AVI_USERNAME and password == AVI_PASSWORD:
        session['logged_in'] = True
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "사용자 이름 또는 비밀번호가 올바르지 않습니다."}), 401

# 로그아웃 API
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({"message": "Logged out"}), 200

# 세션 확인 API
@app.route('/api/check_session', methods=['GET'])
def check_session():
    if session.get('logged_in'):
        return jsonify({"logged_in": True}), 200
    else:
        return jsonify({"logged_in": False}), 401

# --- AVI API 상호작용 함수 ---
def get_avi_session():
    """Avi Controller에 로그인하여 세션 ID와 토큰을 가져옵니다."""
    global session_id, session_token
    try:
        if session_id and session_token:
            return True, session_id, session_token
        
        login_url = f"https://{AVI_CONTROLLER_IP}/login"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "username": AVI_USERNAME,
            "password": AVI_PASSWORD
        }
        
        response = requests.post(login_url, headers=headers, json=payload, verify=False, timeout=10)
        response.raise_for_status()

        session_id = response.cookies.get('sessionid')
        session_token = response.cookies.get('csrftoken')
        
        if session_id and session_token:
            print("AVI Controller 로그인 성공!")
            return True, session_id, session_token
        else:
            print("AVI Controller 로그인 실패: 세션 ID 또는 토큰을 가져올 수 없습니다.")
            return False, None, None

    except requests.exceptions.RequestException as e:
        print(f"AVI Controller 연결 오류: {e}")
        return False, None, None

def get_avi_data(api_path):
    """지정된 AVI API 경로로부터 데이터를 가져옵니다."""
    success, session_id, session_token = get_avi_session()
    if not success:
        return None

    api_url = f"https://{AVI_CONTROLLER_IP}/api/{api_path}"
    headers = {
        'X-CSRFToken': session_token,
        'Content-Type': 'application/json',
        'Referer': f"https://{AVI_CONTROLLER_IP}"
    }
    cookies = {
        'csrftoken': session_token,
        'sessionid': session_id
    }
    
    try:
        response = requests.get(api_url, headers=headers, cookies=cookies, verify=False, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"AVI 데이터 조회 오류 (URL: {api_url}): {e}")
        return None

def get_virtual_services():
    """모든 가상 서비스 목록을 가져옵니다."""
    data = get_avi_data(f"virtualservice/?page_size=100&fields=name,uuid")
    if data:
        return data.get('results', [])
    return []

def get_vs_metrics(vs_uuid):
    """
    특정 가상 서비스의 성능 지표를 가져옵니다.
    """
    metric_ids = [
        "l4_client.max_open_conns",
        "l4_client.avg_bandwidth",
        "l4_client.avg_new_established_conns",
        "l4_client.avg_total_rtt"
    ]
    
    metric_query_string = ",".join(metric_ids)
    
    api_path = f"analytics/metrics/virtualservice?metric_id={metric_query_string}&entity_uuid={vs_uuid}&group_by=entity_uuid&limit=1"
    
    data = get_avi_data(api_path)

    # API 응답을 더 상세하게 확인하고 올바르게 파싱하는 로직 추가
    if not data or 'results' not in data or not data['results']:
        print(f"[{vs_uuid}] AVI Controller로부터 데이터를 가져오지 못했거나 'results' 키가 비어있습니다.")
        return []
    
    # 'results' 리스트의 첫 번째 항목에서 'series'를 가져옴
    result_item = data['results'][0]
    if 'series' not in result_item or not result_item['series']:
        print(f"[{vs_uuid}] 'results'의 첫 번째 항목에서 'series' 키를 찾을 수 없거나 'series' 배열이 비어있습니다.")
        return []
        
    series_data = result_item['series']
    return series_data

# 백그라운드에서 데이터를 주기적으로 수집하는 스레드
def data_collection_thread():
    print("백그라운드 데이터 수집 스레드 시작...")
    while True:
        try:
            vs_list = get_virtual_services()
            if not vs_list:
                print("수집할 가상 서비스가 없습니다. 5초 후 재시도합니다.")
                time.sleep(5)
                continue

            conn = get_db_connection()
            if conn:
                try:
                    with conn.cursor() as cur:
                        total_inserted_rows = 0
                        for vs in vs_list:
                            vs_uuid = vs.get('uuid')
                            vs_name = vs.get('name')
                            
                            metrics = get_vs_metrics(vs_uuid)
                            if metrics:
                                for metric_data in metrics:
                                    metric_id = metric_data.get('header', {}).get('name')
                                    data_points = metric_data.get('data')
                                    
                                    if metric_id and data_points:
                                        latest_data = data_points[0]
                                        value = latest_data.get('value')
                                        # API timestamp는 ISO 8601 형식 문자열이므로 datetime으로 변환
                                        timestamp_str = latest_data.get('timestamp')
                                        if timestamp_str:
                                            timestamp = datetime.fromisoformat(timestamp_str)
                                        else:
                                            timestamp = datetime.now()


                                        if value is not None and timestamp is not None:
                                            cur.execute("""
                                                INSERT INTO vs_performance (vs_uuid, vs_name, metric_id, value, timestamp)
                                                VALUES (%s, %s, %s, %s, %s)
                                                ON CONFLICT (vs_uuid, metric_id, timestamp) DO NOTHING;
                                            """, (str(vs_uuid), str(vs_name), str(metric_id), value, timestamp))
                                            total_inserted_rows += cur.rowcount
                            
                        if total_inserted_rows > 0:
                            print(f"데이터베이스에 {total_inserted_rows}개의 행이 성공적으로 저장되었습니다.")
                        else:
                            print("새로운 데이터가 없습니다. (0개 행 저장)")
                            
                        conn.commit()
                except Exception as e:
                    print(f"데이터베이스 저장 중 오류 발생: {e}")
                finally:
                    if conn:
                        conn.close()
        except Exception as e:
            print(f"데이터 수집 스레드 오류: {e}")

        time.sleep(5)

# --- API 엔드포인트 ---
@app.route('/api/vslist', methods=['GET'])
@login_required
def vs_list():
    vs_data = get_virtual_services()
    return jsonify(vs_data)

@app.route('/api/vs_metrics_by_time', methods=['GET'])
@login_required
def get_vs_metrics_by_time():
    vs_uuid = request.args.get('vs_uuid')
    metric_id = request.args.get('metric_id')
    
    if not vs_uuid or not metric_id:
        return jsonify({"error": "vs_uuid와 metric_id가 필요합니다."}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "데이터베이스 연결 실패"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT timestamp, value
                FROM vs_performance
                WHERE vs_uuid = %s AND metric_id = %s
                ORDER BY timestamp ASC;
            """, (vs_uuid, metric_id))
            results = cur.fetchall()

            data = [{'timestamp': row[0].isoformat(), 'value': row[1]} for row in results]
            
            return jsonify({"results": data}), 200
    except Exception as e:
        return jsonify({"error": f"데이터베이스 조회 실패: {e}"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/recent_data', methods=['GET'])
@login_required
def get_recent_data():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "데이터베이스 연결 실패"}), 500
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT vs_uuid, vs_name, metric_id, value, timestamp
                FROM vs_performance
                ORDER BY timestamp DESC
                LIMIT 10;
            """)
            results = cur.fetchall()

            column_names = [desc[0] for desc in cur.description]
            data = []
            for row in results:
                row_dict = dict(zip(column_names, row))
                if 'timestamp' in row_dict and isinstance(row_dict['timestamp'], datetime):
                    row_dict['timestamp'] = row_dict['timestamp'].isoformat()
                data.append(row_dict)

            return jsonify({"results": data}), 200
    except Exception as e:
        return jsonify({"error": f"데이터베이스 조회 실패: {e}"}), 500
    finally:
        if conn:
            conn.close()

# 애플리케이션 시작 시 DB 테이블 생성 및 백그라운드 스레드 시작
if __name__ == '__main__':
    create_table_if_not_exists()

    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        print("백그라운드 데이터 수집 스레드 시작 중...")
        thread = threading.Thread(target=data_collection_thread, daemon=True)
        thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True)

