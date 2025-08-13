# web_info_server.py
from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# HTML 템플릿 정의
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>클라이언트 정보 (VKS SME Group in KR)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }
        .container { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 800px; margin: 0 auto; }
        h1 { color: #0056b3; }
        h2 { color: #007bff; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-top: 20px; }
        p { margin-bottom: 5px; }
        pre { background-color: #e9e9e9; padding: 10px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; }
        strong { color: #555; }
    </style>
</head>
<body>
    <div class="container">
        <h1>클라이언트 정보</h1>
        
        <h2>기본 정보</h2>
        <p><strong>접속 IP 주소:</strong> {{ ip_address }}</p>
        <p><strong>User-Agent:</strong> {{ user_agent }}</p>
        <p><strong>서버 호스트 이름:</strong> {{ server_hostname }}</p>
        <p><strong>요청 경로:</strong> {{ request_path }}</p>
        <p><strong>메서드:</strong> {{ request_method }}</p>
        
        <h2>요청 헤더</h2>
        <pre>{{ headers }}</pre>
    </div>
</body>
</html>
"""

@app.route('/')
def client_info():
    """클라이언트의 IP 주소, User-Agent, 및 모든 HTTP 헤더를 표시합니다."""
    # 클라이언트의 IP 주소 가져오기
    # Kubernetes 환경에서 실제 클라이언트 IP는 보통 'X-Forwarded-For'에 있습니다.
    # 클라이언트 IP의 신뢰성은 Ingress 컨트롤러 또는 LoadBalancer 설정에 따라 달라집니다.
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # 클라이언트의 User-Agent 가져오기
    user_agent = request.headers.get('User-Agent', '정보 없음')
    
    # 서버가 실행 중인 호스트 이름 (Pod 이름이 될 가능성이 높음)
    server_hostname = os.getenv('HOSTNAME', '알 수 없음')

    # 요청 경로 및 메서드
    request_path = request.path
    request_method = request.method

    # 모든 요청 헤더를 보기 좋게 문자열로 변환
    headers_str = ""
    for key, value in request.headers.items():
        headers_str += f"{key}: {value}\n"
    
    # HTML 템플릿에 데이터 렌더링
    return render_template_string(
        HTML_TEMPLATE,
        ip_address=ip_address,
        user_agent=user_agent,
        server_hostname=server_hostname,
        request_path=request_path,
        request_method=request_method,
        headers=headers_str
    )

if __name__ == '__main__':
    # Flask 앱은 5000번 포트에서 실행됩니다.
    # K8s 환경에서는 컨테이너 내부 포트입니다.
    app.run(host='0.0.0.0', port=5000, debug=False)
