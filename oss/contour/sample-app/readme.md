# 추가 Contour 배포를 통한 Ingress 및 httpproxy 적용 테스트 샘플 앱

### 앱 구조
```
client-info-web sample
|-client-info-web-deployment.yaml
|-client-info-web-service.yaml
|-ingress.yaml
|-httpproxy.yaml
```

이 애플리케이션은 ingress 및 httpproxy 테스트를 위해서 service type: ClusterIP로 배포됩니다.

Namespace을 생성합니다.
```
kubectl create namespace webinfo
kubectl label namespace webinfo pod-security.kubernetes.io/enforce=privileged
```

client-info-web 배포
```
kubectl apply -f client-info-web-deployment.yaml -n webinfo
kubectl apply -f client-info-web-service.yaml -n webinfo
```

### ingress 배포할 경우
```bash
kubectl apply -f ingress.yaml -n webinfo
```


### httpproxy 배포할 경우
```bash
kubectl apply -f proxy.yaml -n webinfo
```

httpproxy 배포 후, web url 접속 시 화면
- Avi controller에 접속 후, envoy가 할당된 Virtual Service의 system application 속성에 대한 TCP Proxy를 활성화 하여, X-Forwared-For를 받을 수 있도록 수정합니다.


![image](https://github.com/user-attachments/assets/f180737d-80a4-4c57-bd30-63fef21f615c)
