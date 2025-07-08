# 배포 및 실행 방법

DB 비밀번호 인코딩:
k8s/db-secret.yaml 파일의 POSTGRES_PASSWORD 값을 여러분의 실제 비밀번호를 base64로 인코딩한 값으로 대체합니다. (예: echo -n "my_strong_password" | base64)

Docker 이미지 빌드 및 푸시:
ap 및 web 디렉토리의 Dockerfile을 사용하여 Docker 이미지를 빌드하고 Docker Hub(또는 다른 컨테이너 레지스트리)에 푸시해야 합니다. your-dockerhub-username을 실제 Docker Hub 사용자 이름으로 변경하세요.

```Bash

# ap 이미지 빌드 및 푸시
cd three-tier-postgresql-app/ap
docker build -t your-dockerhub-username/three-tier-ap:latest .
docker push your-dockerhub-username/three-tier-ap:latest
```

# web 이미지 빌드 및 푸시
```cd ../web
docker build -t your-dockerhub-username/three-tier-web:latest .
docker push your-dockerhub-username/three-tier-web:latest
PostgreSQL 이미지는 공식 이미지를 사용하므로 따로 빌드할 필요 없습니다.
```

Kubernetes 클러스터 준비:
kubectl이 설치되어 있고 Kubernetes 클러스터에 연결되어 있는지 확인합니다.

YAML 파일 배포:
k8s/ 디렉토리로 이동하여 다음 명령어를 순서대로 실행합니다. Secret과 PVC를 먼저 생성해야 합니다.

```Bash

cd three-tier-postgresql-app/k8s
```

# Secret과 PVC 먼저 생성
```kubectl apply -f db-secret.yaml
kubectl apply -f db-pvc.yaml
```
# Deployment 및 Service 생성 (의존성 순서 고려)
```kubectl apply -f db-deployment.yaml
kubectl apply -f db-service.yaml

kubectl apply -f ap-deployment.yaml
kubectl apply -f ap-service.yaml

kubectl apply -f web-deployment.yaml
kubectl apply -f web-service.yaml
```
또는 모든 파일을 한 번에 적용할 수도 있지만, 순서가 중요한 경우 위에처럼 명시적으로 적용하는 것이 좋습니다.

```Bash

kubectl apply -f .
```
배포 확인:
모든 파드가 Running 상태인지, 서비스가 올바르게 생성되었는지 확인합니다.

```Bash

kubectl get deployments
kubectl get pods
kubectl get services
kubectl get pvc
kubectl get secret
```

애플리케이션 접속:
web-service의 외부 접근 URL을 확인합니다.

```Bash

kubectl get service web-service
```

출력에서 web-service의 PORT(S) 컬럼에 표시된 NodePort 번호를 확인합니다. (예: 5000:30XXX/TCP)

Minikube/Kind의 경우: minikube service web-service 명령어를 사용하면 됩니다.

Docker Desktop Kubernetes: http://localhost:NodePort번호 (예: http://localhost:30000)

클라우드 Kubernetes (LoadBalancer 타입인 경우): kubectl get service web-service에서 EXTERNAL-IP를 확인하고 해당 IP로 접속합니다.


---

AP 계층 이미지 재빌드 및 푸시:
3ta-app-v1/ap 디렉토리에서:

```Bash

docker build -t [your-dockerhub-username]/3ta-ap:latest .
docker push [your-dockerhub-username]/3ta-ap:latest
```

WEB 계층 이미지 재빌드 및 푸시:
3ta-app-v1/web 디렉토리에서:

```Bash

docker build -t [your-dockerhub-username]/3ta-web:latest .
docker push [your-dockerhub-username]/3ta-web:latest
```
**your-dockerhub-username**을 여러분의 실제 Docker Hub 사용자 이름 혹은 내부 repostiry path로 변경하세요.

Kubernetes Deployment 신규 배포:


Kubernetes Deployment 업데이트:
이미지 푸시가 완료된 후, Kubernetes 클러스터에서 Deployment를 업데이트하여 새로운 이미지를 사용하도록 합니다. 가장 간단한 방법은 각 Deployment에 대해 롤링 업데이트를 시작하는 것입니다:

```Bash

kubectl rollout restart deployment ap-deployment
kubectl rollout restart deployment web-deployment
```
이 명령은 ap-deployment와 web-deployment의 Pod들을 새로운 이미지 버전으로 점진적으로 교체합니다.

확인 및 접속:

```Bash

kubectl get pods
kubectl get services
```
모든 Pod가 Running 상태인지 확인하고, web-service의 외부 접근 URL로 브라우저에 접속합니다. 이제 웹 페이지의 아이템 목록 옆에 "삭제" 버튼이 나타날 것입니다. 버튼을 클릭하여 아이템이 올바르게 삭제되는지 테스트할 수 있습니다.

이로써 Three-Tier 애플리케이션에 아이템 삭제 기능이 성공적으로 추가되었습니다! 사용자가 웹 UI에서 삭제 요청을 하면, 웹 서버가 이 요청을 AP 서버로 전달하고, AP 서버가 최종적으로 PostgreSQL 데이터베이스와 통신하여 데이터를 삭제하는 완벽한 흐름을 갖추게 됩니다.
