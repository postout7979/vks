# Dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

# 가상 환경 생성 및 활성화
# pip 경고를 피하고 깨끗한 환경을 위해 권장됩니다.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 필요한 Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY web_info_server.py .

# Flask 앱이 리스닝할 포트 노출
EXPOSE 5000

# 환경 변수를 설정하여 Flask 개발 서버에서 버퍼링 없이 로그 출력
ENV PYTHONUNBUFFERED=1

# 웹 서버 실행
CMD ["python", "web_info_server.py"]
