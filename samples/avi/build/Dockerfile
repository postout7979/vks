# 1단계: Python 3.9 slim-buster 이미지를 기반으로 사용
FROM python:3.9-slim-buster

# pip 경고를 피하고 깨끗한 환경을 위해 권장됩니다.
RUN python -m venv /opt/venv

# 2단계: 컨테이너 내부의 작업 디렉토리를 설정
WORKDIR /app

# 3단계: 애플리케이션 실행을 위한 'appuser' 생성
RUN useradd -m appuser

# 4단계: 'appuser'에게 /app 디렉토리 소유권 부여
RUN chown -R appuser:appuser /app

# 5단계: 'appuser'로 전환
USER appuser

# 6단계: PATH 환경 변수 업데이트
# pip가 설치한 바이너리 경로를 PATH에 추가합니다.
ENV PATH="/home/appuser/.local/bin:$PATH"

# 7단계: 의존성 파일 복사 및 설치
COPY requirements.txt .

# 8단계: 'appuser' 권한으로 pip 설치
RUN pip install -r requirements.txt
# 9단계: 나머지 소스 코드 복사
COPY . .
COPY templates/index.html /app/templates/index.html
COPY templates/login.html /app/templates/login.html
COPY templates/dashboard.html /app/templates/dashboard.html


# 10단계: 포트 노출
EXPOSE 5000

CMD ["python", "app.py"]

