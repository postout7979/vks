FROM ubuntu
RUN apt update && apt install -y stress && apt install -y nginx
WORKDIR /home/ubuntu
COPY stress.sh /home/ubuntu
EXPOSE 80
CMD ["systemctl", "start", "nginx"]
