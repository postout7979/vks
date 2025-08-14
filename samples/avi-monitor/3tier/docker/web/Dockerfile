# Nginx 최신 버전 사용
FROM nginx:latest

# 기본 Nginx 설정 파일 제거
RUN rm /etc/nginx/conf.d/default.conf

# 커스텀 Nginx 설정 파일과 웹 페이지 파일 복사
COPY nginx.conf /etc/nginx/conf.d/
COPY templates /app/templates

# 복사된 파일 및 디렉터리의 소유권을 nginx 사용자로 변경하여 권한 문제 해결
RUN chown -R nginx:nginx /app/templates

# 컨테이너의 80 포트를 외부에 노출
EXPOSE 80

# Nginx 실행
CMD ["nginx", "-g", "daemon off;"]

