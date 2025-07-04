TMC-SM 배포 전에 DNS 서버에 TMC-SM에 사용될 Static VIP에 대한 DNS 레코드 등록을 필요로 합니다.

```bash
DNS type A records:
━━━━━━━━━━━━━━━━━━━━━━━━━━━

             DNS RECORD                 IP
  tmc.broadcom.com                      10.10.152.101
  alertmanager.tmc.broadcom.com         10.10.152.101
  auth.tmc.broadcom.com                 10.10.152.101
  blob.tmc.broadcom.com                 10.10.152.101
  console.s3.tmc.broadcom.com           10.10.152.101
  gts-rest.tmc.broadcom.com             10.10.152.101
  gts.tmc.broadcom.com                  10.10.152.101
  landing.tmc.broadcom.com              10.10.152.101
  pinniped-supervisor.tmc.broadcom.com  10.10.152.101
  prometheus.tmc.broadcom.com           10.10.152.101
  s3.tmc.broadcom.com                   10.10.152.101
  tmc-local.tmc.broadcom.com            10.10.152.101

```

tmc-cluster로 context를 이동한 후, namespace를 생성합니다.

```bash
kubectl config use-context tmc-cluster

kubectl create ns tmc-local
kubectl label --overwrite ns tmc-local pod-security.kubernetes.io/enforce=privileged
```

tmc-sm 파일을 브로드컴 홈페이지에서 다운 받아, Admin 호스트로 옮긴 후, 압축을 해제 합니다.

```bash
mkdir tanzumc
tar -xf tmc-self-managed-1.4.1.tar -C ./tmcsm

# Add the root CA cert for Harbor to the /etc/ssl/certs path of the jumpbox for system-wide use. This enables the image push to the Harbor repository.  

sudo cp harbor.crt /etc/ssl/certs/

```

tmcsm 폴더로 이동 후, tmc-sm 커맨드를 사용하여, image를 private registry의 project name에 맞게 수정하여 업로드 합니다.

```bash
cd tmcsm

./tmc-sm push-images harbor --help

./tmc-sm push-images harbor --project tzharbor.tanzu.lab/library/tmc --username admin --password VMware1!

```

tanzu-mission-control-packages의 경로 repository를 추가합니다.

```bash
tanzu package repository add tanzu-mission-control-packages --url "harbor.tanzu.lab/tmc-sm-1.4/package-repository:1.4.1" --namespace tmc-local
```

## **CA 인증서를 사용한 TMC용 사설 인증서 발행 secret yaml 파일 생성**

– 이 단계는 앞서 tmc-cluster  배포 시, 이미 사설 인증서 발행 작업을 마친 경우, 건너뛰기 합니다.

rootCA.crt, rootCA.key 값의 base64 인코딩된 값으로 아래 tls.crt & tls.key 항목에 붙여넣기

**CA 인증서의 base64 인코딩 값으로 secret을 생성**

secret-ca.yaml

```bash
cat > secret-ca.yaml << EOF
apiVersion: v1
kind: Secret
metadata:
  name: ca-key-pair
  namespace: cert-manager
data:
  tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUZyVENDQTVXZ0F3SUJBZ0lVWEpJaWFYT
.................. 생략
25vUWhyVElMCm0vSzltNDZRRzc3NkRhVUcramJ1TklJPQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
  tls.key: LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUpRZ0lCQURBTkJna3Foa2lHOXcwQkFR
.................. 생략
UsyMHFvQkx1U3VxaCt3PT0KLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLQo=
EOF

```

secret 적용

```bash
kubectl apply -f secret-ca.yaml
```

**ClusterIssuer 발행**

- tmc-sm에 대한 셀프 인증서를 발행하기 위한 ClusterIssuer를 생성

```bash
cat > tmc-caissuer.yaml << EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: tmc-local
spec:
  ca:
    secretName: ca-key-pair
EOF
```

```bash
kubectl apply -f tmc-caissuer.yaml
```

```bash
kubectl get clusterissuers.cert-manager.io
```

## tmc-sm의 환경 설정 파일 수정

tmc 설치 values.yaml 파일을 생성합니다.

- harbor 경로, dnsZone name, ClusterIssuer name, loadBalancerIP 입력을 주의 합니다.
- oidc 정보를 입력합니다.
- keycloak 주소와 realms 정보를 입력하고, cleintID 및 노트패드에 복사한 Secret을 입력합니다.
- idpGroupRoles을 설정합니다.(앞서 keycloak에서 여러 그룹을 생성 시, 그룹은 admin, 혹은 member role중 하나에 매핑이 되어 있습니다.)
- size를 조정합니다.(PoC 환경에서 리소스가 부족할 경우에는 small로 진행합니다.)
- tanzu standard package의 path 경로를 명확한 private registry로 지정합니다.

```bash
harborProject: harbor.tanzu.lab/tmc-sm-1.4
dnsZone: tmc.tanzu.lab
clusterIssuer: tmc-local
postgres:
  userPassword: 'VMware1!'
  maxConnections: 300
minio:
  username: root
  password: 'VMware1!'
contourEnvoy:
  serviceType: LoadBalancer
  loadBalancerIP: 10.10.152.101
oidc:
  issuerType: pinniped
  issuerURL: https://keycloak.tanzu.lab/realms/master
  clientID: tmc-sm
  clientSecret: FjROnlZylPstRbSFJuIFWpF48ldSlDhY
idpGroupRoles:
  admin: tmc:admin
  member: tmc:member
trustedCAs:
# Harbor registry의 CA 추가
  harbor-ca: |-
    -----BEGIN CERTIFICATE-----
    MIIFlzCCA3+gAwIBAgIUc8oZ1BxONTEOJCuHWPL8CWlzGy8wDQYJKoZIhvcNAQEL
    .................
    eoAR0tASQqdChkbCTsGLyf/WqpDmsI4tytloNVGKcAs44j/WiB/1UPdMHA==
    -----END CERTIFICATE-----
# keycloak의 CA 추가
  idp-ca: |-
    -----BEGIN CERTIFICATE-----
    MIIDnTCCAoWgAwIBAgIUV5ZJO8s++XDpsV+99rFZMdXOZjMwDQYJKoZIhvcNAQEL
    .................
    EbuB3ZKjNj8GIwfcC7JCfKM=
    -----END CERTIFICATE-----
#alertmanager: "" # needed only if you want to turn on alerting
#  criticalAlertReceiver:
#    slack_configs:
#    - send_resolved: false
#      api_url: https://hooks.slack.com/services/...
#      channel: '#<slack-channel-name>'
#telemetry:
#  ceipAgreement: false
#  ceipOptIn: false
#  eanNumber: ""
size: small
tanzuStandard: 
  imageRegistry: harbor.tanzu.lab
  relativePath: tmc-sm-1.4/498533941640.dkr.ecr.us-west-2.amazonaws.com/packages/standard/repo:v2025.04.29
```

옵션: yq 명령어 도구가 설치되어 있는 경우 인증서 텍스트를 쉽게 열 맞춤을 통한 추가 방법

- 아래 영역의 인증서 값을 비워 놓습니다.

```bash
trustedCAs:
# Harbor registry의 CA 추가
  harbor-ca:
# keycloak의 CA 추가
  idp-ca:
```

yq 명령어 도구를 사용해서, 인증서 파일의 .pem 정보를 삽입하여, 새로운 파일을 생성합니다.

```bash
yq eval '.trustedCAs.harbor-ca ="'"$(< harbor.crt)"'"' tmc-values.yaml > temp1.yaml

yq eval '.trustedCAs.idp-ca ="'"$(< keycloak.crt)"'"' temp1.yaml > temp2.yaml
```

인증서 삽입이 잘 완료되었다면, temp3.yaml 파일명을 tmc-values.yaml로 변경해서 사용합니다.

export 환경 변수 값을 설정합니다.

```bash
export TKG_CUSTOM_IMAGE_REPOSITORY=harbor.tanzu.lab/tmc-sm-1.4
export TKG_CUSTOM_IMAGE_REPOSITORY_SKIP_TLS_VERIFY=true
## 올바른 harbor.crt의 base64 encoding된 정보를 입력
export TKG_CUSTOM_IMAGE_REPOSITORY_CA_CERTIFICATE=LS0t[...]tLS0tLQ==

```

tanzu mission control self-managed 설치를 진행합니다.

```bash
tanzu package install tanzu-mission-control -p tmc.tanzu.vmware.com --version "1.4.1" --values-file ./tmc-values.yaml --namespace tmc-local
```

- 정상적인 배포 완료를 하지 못한 경우 중단 시에는 원인을 수정하고, tmc-local namespace를 삭제 후, 다시 namespace 생성부터 진행합니다.

---

## tanzu package 삭제

```bash
tanzu package installed delete tanzu-mission-control --namespace tmc-local
```

```bash
tanzu package repository delete tanzu-mission-control-packages --namespace tmc-local
```

### 남아 있는 것

- persistent volumes
- internal TLS certificates
- configmaps

## Delete namespace

```bash
kubectl delete ns tmc-local
```

```bash
kubectl get namespace "tmc-local" -o json \
  | tr -d "\n" | sed "s/\"finalizers\": \[[^]]\+\]/\"finalizers\": []/" \
  | kubectl replace --raw /api/v1/namespaces/"tmc-local"/finalize -f -
```

-
