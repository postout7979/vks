# Ubuntu 22.04 LTS 이미지를 사용합니다.
FROM ubuntu:22.04

# apt 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    stress-ng \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Flask 및 psutil 설치
RUN pip3 install Flask psutil

# 애플리케이션 파일 추가
RUN mkdir -p /app
COPY app.py /app/app.py
COPY index.html /app/templates/index.html
COPY index.html /app/index.htm
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# 컨테이너가 80번 포트를 노출하도록 설정
EXPOSE 80

# 컨테이너 시작 시 start.sh 스크립트 실행
CMD ["/app/start.sh"]
