

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
