# Python 3.10 공식 이미지를 기반으로 사용합니다.
FROM python:3.10-slim

# 필요한 환경 변수를 설정합니다.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 컨테이너에 애플리케이션 코드를 저장할 작업 디렉토리를 생성합니다.
WORKDIR /app

# 애플리케이션 의존성 파일을 컨테이너로 복사합니다.
COPY requirements.txt /app/

# pip를 최신 버전으로 업그레이드하고, requirements.txt에 명시된 패키지를 설치합니다.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 현재 디렉토리의 모든 파일을 컨테이너의 /app 디렉토리로 복사합니다.
COPY . /app/

# Flask 애플리케이션이 실행될 포트를 노출합니다.
EXPOSE 5000

# 컨테이너가 시작될 때 app.py를 실행합니다.
CMD ["python", "app.py"]

# Flask 애플리케이션 실행
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

