## Ubuntu OS에 Harbor script로 설치 하기 ##

sudo ./harbor.sh 파일을 실행합니다.

docker, docker-compose를 배포하고, harbor 오프라인 installer 파일을 다운로드 후, 폴더 압축 그리고 harbor 구성을 활성화 합니다.

1. Harbor가 활성화 되면, 최초 HTTP로 되어 있음으로, HTTPs 구성을 위해서는 사용할 harbor domain FQDN 혹은 IP를 포함한 인증서를 생성합니다.
2. Harbor 서비스를 docker compose 명령어를 사용하여, down 시킵니다.
   -- sudo docker-compose down -v
3. 생성한 인증서를 harbor.yml 파일 내에 지정할 경로 폴더에 저장합니다.
   
   port: 443 <br>
   The path of cert and key files for nginx <br>
   certificate: /your/certificate/path <br>
   private_key: /your/private/key/path <br>
   insecure: true
   
5. ./prepare 파일을 실행하면, harbor 설정을 재구성을 진행합니다.
6. sudo docker-compose up -d 명령어로 다시 harbor 서비스를 시작합니다.

docker client에서 docker login 명령어로 로그인 시, https에 대한 비공인 인증서로 인하여, 오류 발생 시에는 해당 클라이언트에 인증서를 저장해야 합니다.
자세한 사항은 Harbor 공식 페이지를 참고해주세요.
