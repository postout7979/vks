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

# 세션 관리를 위한 비밀 키 설정. 실제 운영 환경에서는 더 안전하게 관리해야 합니다.
app.secret_key = 'sdklfsdfhewoiwe3242234f'

# 가상의 사용자 데이터베이스 (테스트용)
USERS = {
    "admin": "admin"
}

session_id = None
session_token = None

# Avi Controller 정보 (환경 변수에서 가져옴)
# 컨테이너 환경에서 실행될 때 이 변수들이 설정되어야 합니다.
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
    """데이터베이스 연결을 설정하고 반환합니다."""
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
    """VS 성능 데이터를 저장할 테이블이 없으면 생성합니다."""
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

# 로그인 데코레이터
def login_required(f):
    """API 엔드포인트에 대한 사용자 인증을 확인하는 데코레이터입니다."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            # 로그인되어 있지 않으면 401 Unauthorized 응답을 반환합니다.
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

# 로그인 상태 확인 API
@app.route('/api/check_login_status', methods=['GET'])
def check_login_status():
    """현재 사용자가 로그인되어 있는지 여부를 반환합니다."""
    if 'username' in session:
        return jsonify({'is_logged_in': True}), 200
    else:
        return jsonify({'is_logged_in': False}), 200

# AVI Controller 로그인 API
@app.route('/api/login', methods=['POST'])
def login():
    """
    사용자 자격 증명을 확인하고 Avi Controller에 로그인하여 세션을 설정합니다.
    """
    username = request.json.get('username')
    password = request.json.get('password')

    # 가상 사용자 데이터베이스에서 자격 증명 확인
    if username not in USERS or USERS[username] != password:
        return jsonify({"success": False, "message": "잘못된 자격 증명"}), 401

    # Avi Controller에 로그인
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

        # 세션 쿠키 추출
        session_id = response.cookies.get('sessionid')
        session_token = response.cookies.get('csrftoken')
        avisession_id = response.cookies.get('avi-sessionid')

        if session_id:
            # Flask 세션에 Avi API 세션 정보 저장
            session['logged_in'] = True
            session['username'] = username
            session['avi_api_sessionid'] = session_id
            session['avi_api_token'] = session_token
            session['avisessionid'] = avisession_id

            return jsonify({"success": True, "message": "로그인 성공"}), 200
        else:
            return jsonify({"error": "로그인 실패: 세션 ID를 가져올 수 없습니다."}), 401

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"로그인 실패: 컨트롤러 정보가 올바르지 않습니다. ({e})"}), 401

# 로그아웃 API
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """사용자 세션을 제거하여 로그아웃합니다."""
    try:
        session.pop('avi_api_token', None)
        session.pop('avi_api_sessionid', None)
        session.pop('logged_in', None)
        session.pop('username', None)
        session.pop('avisessionid', None)
        session.clear()
        return jsonify({"success": True, "message": "로그아웃 성공"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": "로그아웃 중 오류 발생"}), 500

# VS 목록 조회 API
@app.route('/api/vs_list')
@login_required
def get_vs_list():
    """Avi Controller에서 Virtual Service 목록을 가져옵니다."""
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
    """
    백그라운드 스레드에서 주기적으로 Avi Controller API를 호출하여 성능 데이터를 수집하고
    PostgreSQL 데이터베이스에 저장합니다.
    """
    global session_token, session_id, avisession_id

    while True:
        conn = None
        try:
            # 세션 토큰이 없으면 로그인 시도
            if not session_id or not session_token:
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
                    avisession_id = response.cookies.get('avi-sessionid')
                    print("로그인 성공, 세션 ID 및 토큰 획득.")
                except requests.exceptions.RequestException as e:
                    print(f"자동 로그인 실패: {e}")
                    time.sleep(15)
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
            if not vs_name_map:
                print("경고: Avi Controller에서 Virtual Service 목록을 가져오지 못했습니다. 데이터 수집을 건너뜁니다.")
                time.sleep(5)
                continue

            # 성능 데이터 가져오기
            performance_url = f"https://{AVI_CONTROLLER_IP}/api/analytics/metrics/virtualservice?metric_id=l4_client.avg_bandwidth,l4_server.avg_open_conns&limit=1"
            response = requests.get(performance_url, headers=headers, cookies=cookies, verify=False)
            response.raise_for_status()
            performance_data = response.json()
            
            # 성능 데이터가 없는 경우 로깅
            if not performance_data.get('results', []):
                print("경고: Avi Controller API에서 성능 데이터를 가져오지 못했습니다. 데이터 수집을 건너뜁니다.")
                time.sleep(5)
                continue

            conn = get_db_connection()
            if conn:
                try:
                    with conn.cursor() as cur:
                        inserted_rows = 0
                        for item in performance_data.get('results', []):
                            vs_uuid = item.get('entity_uuid')
                            vs_name = vs_name_map.get(vs_uuid, 'name')
                            for series in item.get('series', []):
                                metric_id = series['header'].get('name')
                                for data_point in series.get('data', []):
                                    value = data_point.get('value')
                                    timestamp_str = data_point.get('timestamp')
                                    
                                    if value is not None and timestamp_str:
                                        # Avi API에서 제공하는 timestamp를 사용
                                        timestamp = datetime.fromisoformat(timestamp_str)
                                        cur.execute(
                                            sql.SQL("""
                                                INSERT INTO vs_performance (vs_uuid, vs_name, metric_id, value, timestamp)
                                                VALUES (%s, %s, %s, %s, %s)
                                            """),
                                            (vs_uuid, vs_name, metric_id, value, timestamp)
                                        )
                                        inserted_rows += 1
                        conn.commit()
                        print(f"AVI 성능 데이터가 데이터베이스에 성공적으로 저장되었습니다. 총 {inserted_rows}개 행 삽입됨.")
                except Exception as e:
                    print(f"데이터베이스 저장 중 오류 발생: {e}")
                finally:
                    if conn:
                        conn.close()

        except requests.exceptions.RequestException as e:
            print(f"AVI Controller에서 데이터 가져오기 실패: {e}")
            # 인증 실패 시 세션을 재설정하여 다음 루프에서 재로그인 시도
            if response.status_code == 401:
                session_id = None
                session_token = None
        except Exception as e:
            print(f"백그라운드 스레드에서 예상치 못한 오류 발생: {e}")

        # 5초마다 실행
        time.sleep(5)

# API: DB에서 성능 데이터 조회 (모든 VS)
@app.route('/api/performance')
@login_required
def get_performance_data():
    conn = get_db_connection()
    if not conn:
        print("API: 데이터베이스에 연결할 수 없습니다.")
        return jsonify({"error": "데이터베이스에 연결할 수 없습니다."}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT vs_uuid, vs_name, metric_id, value, timestamp
                FROM vs_performance
                WHERE timestamp >= NOW() - INTERVAL '1 minutes'
                ORDER BY vs_uuid, metric_id, timestamp;
            """)
            results = cur.fetchall()

            if not results:
                print("API: 데이터베이스에 최근 1분 데이터가 없습니다.")
                return jsonify({"results": []}), 200

            vs_data_map = defaultdict(lambda: {'series': defaultdict(list)})
            
            for row in results:
                vs_uuid, vs_name, metric_id, value, timestamp = row

                vs_data_map[vs_uuid]['entity_uuid'] = vs_uuid
                vs_data_map[vs_uuid]['metric_entity_name'] = vs_name
                
                vs_data_map[vs_uuid]['series'][metric_id].append({
                    'value': value,
                    'timestamp': timestamp.isoformat()
                })

            final_results = []
            for vs_uuid, vs_data in vs_data_map.items():
                vs_item = {
                    'entity_uuid': vs_data['entity_uuid'],
                    'metric_entity_name': vs_data['metric_entity_name'],
                    'series': []
                }
                for metric_id, data_points in vs_data['series'].items():
                    header = {'name': metric_id}
                    if metric_id == 'l4_client.avg_bandwidth':
                        header['units'] = 'bps'
                    elif metric_id == 'l4_server.avg_open_conns':
                        header['units'] = 'connections'

                    vs_item['series'].append({
                        'header': header,
                        'data': data_points
                    })
                final_results.append(vs_item)

            return jsonify({"results": final_results}), 200
    except Exception as e:
        print(f"API: 데이터베이스 조회 실패: {e}")
        return jsonify({"error": f"데이터베이스 조회 실패: {e}"}), 500
    finally:
        conn.close()

# API: 특정 VS의 성능 데이터 조회
@app.route('/api/performance/<string:vs_uuid>')
@login_required
def get_vs_performance_data(vs_uuid):
    """특정 VS의 최근 10분 성능 데이터를 DB에서 조회하여 반환합니다."""
    conn = get_db_connection()
    if not conn:
        print("API: 데이터베이스에 연결할 수 없습니다.")
        return jsonify({"error": "데이터베이스에 연결할 수 없습니다."}), 500

    try:
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("""
                    SELECT vs_uuid, vs_name, metric_id, value, timestamp
                    FROM vs_performance
                    WHERE vs_uuid = %s AND timestamp >= NOW() - INTERVAL '1 minutes'
                    ORDER BY metric_id, timestamp;
                """),
                (vs_uuid,)
            )
            results = cur.fetchall()

            if not results:
                print(f"API: 특정 VS (UUID: {vs_uuid})에 대한 최근 1분 데이터가 없습니다.")
                return jsonify({"results": []}), 404

            vs_data_map = defaultdict(list)
            vs_name = ""
            for row in results:
                vs_uuid_from_db, vs_name_from_db, metric_id, value, timestamp = row
                vs_name = vs_name_from_db
                vs_data_map[metric_id].append({
                    'value': value,
                    'timestamp': timestamp.isoformat()
                })

            final_results = [{
                'entity_uuid': vs_uuid,
                'metric_entity_name': vs_name,
                'series': [
                    {
                        'header': {'name': metric_id, 'units': 'bps' if metric_id == 'l4_client.avg_bandwidth' else 'connections'},
                        'data': data_points
                    } for metric_id, data_points in vs_data_map.items()
                ]
            }]

            return jsonify({"results": final_results}), 200
    except Exception as e:
        print(f"API: 데이터베이스 조회 실패: {e}")
        return jsonify({"error": f"데이터베이스 조회 실패: {e}"}), 500
    finally:
        conn.close()


@app.route('/api/pool')
@login_required
def get_pool_data():
    """Avi Controller에서 풀(Pool)의 총 개수를 가져옵니다."""
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
        # Avi API는 'count' 대신 'results' 배열을 반환합니다.
        # 따라서 'results' 배열의 길이를 반환합니다.
        if "results" in data and isinstance(data["results"], list):
            count = len(data["results"])
            return jsonify(count)
        else:
            print("API: 풀 개수 API 응답에 유효한 'results' 필드가 없습니다.")
            return jsonify({"error": "응답에 유효한 'results' 필드가 없습니다."}), 500
    except requests.exceptions.RequestException as e:
        print(f"API: 풀 개수 API 호출 실패: {e}")
        return jsonify({"error": str(e)}), 500
    except json.JSONDecodeError:
        print("API: JSON 응답 파싱 실패.")
        return jsonify({"error": "JSON 응답을 파싱하는 데 실패했습니다."}), 500

@app.route('/api/check_db_data')
@login_required
def check_db_data():
    """데이터베이스의 vs_performance 테이블에서 최근 데이터를 조회합니다."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "데이터베이스에 연결할 수 없습니다."}), 500

    try:
        with conn.cursor() as cur:
            # 최근 10개 데이터를 최신순으로 정렬하여 조회
            cur.execute("""
                SELECT vs_uuid, vs_name, metric_id, value, timestamp
                FROM vs_performance
                ORDER BY timestamp DESC
                LIMIT 10;
            """)
            results = cur.fetchall()

            # 조회 결과를 JSON으로 변환
            column_names = [desc[0] for desc in cur.description]
            data = []
            for row in results:
                row_dict = dict(zip(column_names, row))
                # datetime 객체를 ISO 형식 문자열로 변환
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

    # Flask의 디버그 리로더는 코드를 두 번 실행합니다.
    # WERKZEUG_RUN_MAIN 환경 변수가 'true'일 때만 스레드를 시작하여
    # 백그라운드 스레드가 한 번만 실행되도록 합니다.
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        print("백그라운드 데이터 수집 스레드 시작...")
        fetch_thread = threading.Thread(target=fetch_and_save_performance_data)
        fetch_thread.daemon = True # 메인 스레드 종료 시 함께 종료
        fetch_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True)

