프로젝트 구조
```Bash
client-info-app/
├── web_info_server.py
├── requirements.txt
├── Dockerfile
└── k8s/
    ├── client-info-deployment.yaml
    └── client-info-service.yaml
```

### 배포 및 실행 방법
Docker 이미지 빌드 및 푸시:
client-info-app/ 디렉토리로 이동하여 Docker 이미지를 빌드하고 Docker Hub(또는 다른 컨테이너 레지스트리)에 푸시합니다. **your-dockerhub-username**을 여러분의 실제 Docker Hub 사용자 이름으로 변경해야 합니다.

```Bash
cd client-info-app
docker build -t your-dockerhub-username/client-info-web:latest .
docker push your-dockerhub-username/client-info-web:latest
```

Kubernetes 클러스터 준비:
Minikube, Kind, Docker Desktop의 Kubernetes 기능, 또는 클라우드 제공업체(EKS, GKE, AKS 등)의 클러스터가 필요합니다. kubectl이 설치되어 있고 클러스터에 연결되어 있는지 확인합니다.

YAML 파일 배포:
k8s/ 디렉토리로 이동하여 다음 명령어를 실행합니다.

```Bash
cd k8s
kubectl apply -f .
```

배포 확인:
다음 명령어를 사용하여 Pod, Service, Deployment의 상태를 확인합니다.

```Bash
kubectl get deployments
kubectl get pods
kubectl get services
```
모든 Pod가 Running 상태이고 서비스가 올바르게 생성되었는지 확인합니다.

애플리케이션 접속:
web-service의 외부 접근 URL 또는 IP 주소를 확인합니다.

```Bash
kubectl get service client-info-web-service
```
출력 결과에서 client-info-web-service의 PORT(S) 컬럼을 보면 80:NodePort번호/TCP와 같은 형식으로 나타납니다.

Minikube/Kind의 경우: minikube service client-info-web-service 명령어를 사용하면 자동으로 브라우저가 열리거나 접속 URL을 알려줍니다.

Docker Desktop Kubernetes: http://localhost:NodePort번호 (NodePort번호는 kubectl get service client-info-web-service 결과에서 확인)

클라우드 Kubernetes (LoadBalancer 타입인 경우): kubectl get service client-info-web-service에서 EXTERNAL-IP를 확인하고 해당 IP로 접속합니다.

웹 브라우저를 통해 접속하면 현재 클라이언트의 IP 주소와 기타 요청 정보가 웹 페이지에 표시될 것입니다. X-Forwarded-For 헤더에 표시되는 IP는 여러분의 실제 공인 IP일 수도 있고, Kubernetes Ingress/LoadBalancer의 IP일 수도 있으며, 환경에 따라 다르게 나타납니다.
