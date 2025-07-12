## 사용법 ##
VKS standard package 설치 이후 추가 contour 및 envoy 설치를 위한 작업을 안내합니다.
VKS standard package의 contour에 대해서 브로드컴의 기술 지원은 다음과 같으며, 패키지가 아닌 contour 설치 및 문제 해결에 대한 권한은 일반 contour 배포 소유주에게 있습니다.
```
- 설치 오류에 대한 설치 환경 정보 값 확인
- 설치 이후, 업그레이드 버전에 대한 패키지 제공
- 설치 및 업그레이드 시, 발생하는 문제 해결을 위한 기술 지원
```

### 구성파일
```
contour
|-01-crds.txt
|-run.sh
```

run.sh 파일과 01-crds.txt 파일을 로컬 리눅스 머신에 다운로드 혹은 생성하시기 바랍니다.
- run.sh 파일은 몇 가지 변수 값을 사전 정의하기 위해, 생성한 스크립트입니다. 해당 스크립트의 yaml 파일을 채우는 값들은 공식 projectcontour의 git page에 있는 examples/contour 폴더의 파일 내용을 참조합니다.

run.sh 파일을 실행하면 대화형 진행을 하게됩니다.
![image](https://github.com/user-attachments/assets/8bcf9d9e-e0a1-45f6-95b4-50efbf87d3b2)

기본적으로 contour는 기본 설치 모드와 avi LB를 사용하도록 ako에 대한 loadBalancerClass를 지정과 ingress-class-name을 지정하는 모드로 구분됩니다.
- 첫 번째 질문에서 숫자 1을 입력 시, ingress-class-name을 사용하는 모드이며, 숫자 2를 입력시에는 기본 모드로 배포됩니다.
- 이 스크립트는 수퍼바이저에서 제공하는 기본 로드밸런서를 사용하지 않으며, 개별 TKC에 배포한 AKO를 사용하는 것을 전제로 합니다. 사전에 AKO를 배포하여, 추가 로드밸런서 사용이 준비되어 있어야 합니다.
- AKO 배포에 대해서 다른 루트 폴더에 있는 AKO 폴더를 참고 바랍니다.
```
Number 1 - ingress-class을 정의합니다.
Number 2 - 기본 설정 contour를 배포합니다.
```

## 숫자 1을 선택하여, ingress-class-name을 사용할 경우 ##
![image](https://github.com/user-attachments/assets/ff859776-a30c-423c-9bed-0c992404d4a7)

1번을 입럭하고서, contour 배포를 위한 namespace 이름을 입력합니다.(예: contour)

![image](https://github.com/user-attachments/assets/d6eb4ba5-77f0-4ff1-ab03-16199fbe10a7)

이 항목에서 앞으로 ingress 혹은 httpproxy 배포 시, 사용할 ingress class name을 입력합니다.
- 이는 생성되는 03-contour.yaml 파일의 deployment 항목의 container runtime의 servce 영역의 마지막 줄로 --ingress-class-name={your class name} 전달자를 envoy에 전달하여 사용하도록 합니다.
- 입력된 ingress-class-name은 ingressClass.yaml을 생성하여, cluster에 contour controller에 대한 ingressclass를 생성합니다.

![image](https://github.com/user-attachments/assets/fe51e1ed-5ad9-4921-b317-9ab0c5343d34)

이 항목은 사전에 배포한 ako 환경 설정에서 정의한 namespace label에 해당합니다. 이 label이 namespace에 할당된 경우에 배포된 ako를 통해서 Virtual Service를 제공받을 수 있습니다.
- ako 환경 설정 values.yaml 파일 내, namespace에 대한 label key 및 value 값에 해당합니다.(이 예제에서는 label이 avi: ako 의 형태로 namespace에 추가됩니다.)
- 해당 label은 contour가 배포되는 namespace에 추가되어, contour가 배포된 namespace의 envoy가 external LoadBalancer(여기서는 AKO로 구성된 Avi LB)로부터 IP를 가져오고, 네트워크 서비스를 제공합니다.

ingress class는 ingress 혹은 httpproxy 배포 시, 해당 되는 yaml 값의 spec.ingressClassName={your ingress name}으로 ingress.yaml 혹은 httpproxy.yaml 파일에 추가되어, service가 어떤 인그레스를 사용할지 선택하도록 제공합니다.
- httpproxy를 배포할 경우에는 추가 annotation을 필요로 합니다.

스크립트 실행 생성 파일
```
run.sh
|-00-common.yaml
|-00-ingressclass.yaml
|-01-contour-config.yaml
|-01-crds.yaml
|-02-job-certgen.yaml
|-02-rbac.yaml
|-02-role-contour.yaml
|-02-service-contour.yaml
|-02-service-envoy.yaml
|-03-contour.yaml
|-03-envoy.yaml
```

kubectl 실행 구문 순서
- contour.yaml 및 envoy.yaml의 image path에서 cluster의 k8s version에 맞는 image 배포 version이 올바른지 확인하시기 바랍니다.
```
kubectl apply -f 00-common.yaml
kubectl apply -f 00-ingressclass.yaml
kubectl apply -f 01-contour-config.yaml
kubectl apply -f 01-crds.yaml
kubectl apply -f 02-job-certgen.yaml
kubectl apply -f 02-rbac.yaml
kubectl apply -f 02-role-contour.yaml
kubectl apply -f 02-service-contour.yaml
kubectl apply -f 02-service-envoy.yaml
kubectl apply -f 03-contour.yaml
kubectl apply -f 03-envoy.yaml
```

httpproxy로 배포하기 위해서는 03-contour.yaml파일의 arg 구문에 추가 설정이 필요합니다. kubectl 배포 이전에 설정하기 바랍니다.
- ` - --use-proxy-protocol ` 구문이 포함되어야 함.
```
      containers:
      - args:
        - serve
        - --incluster
        - --xds-address=0.0.0.0
        - --xds-port=8001
        - --contour-cafile=/certs/ca.crt
        - --contour-cert-file=/certs/tls.crt
        - --contour-key-file=/certs/tls.key
        - --config-path=/config/contour.yaml
        - --ingress-class-name=ingress-contour
        - --use-proxy-protocol
```

ingress.yaml 예제
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: client-info-ingress
  namespace: webinfo
spec:
  ingressClassName: ingress-contour
  rules:
  - host: webinfo.tanzu.lab
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: client-info-web-service
            port:
              number: 80
```

httpproxy.yaml 예제
```yaml
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: client-info-proxy
  namespace: webinfo
  annotations:
    projectcontour.io/ingress.class: ingress-contour
spec:
  ingressClassName: ingress-contour
  routes:
  - conditions:
    - prefix: /
    requestHeadersPolicy:
      set:
      - name: X-Client-IP
        value: '%DOWNSTREAM_REMOTE_ADDRESS_WITHOUT_PORT%'
    services:
    - name: client-info-web-service
      port: 80
  virtualhost:
    fqdn: webinfo.tanzu.lab
```
