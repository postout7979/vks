# **1.1 TKG 서비스 클러스터 생성하기**

TMC-SM 배포에 사용할 TKG Cluster 생성

사전 준비 사항: vSphere Namespace을 생성 및 사용자 권한 할당

```bash
kubectl vsphere login --server=https://{{IP ADDRESS}} --insecure-skip-tls-verify --vsphere-username={{Account Name}} --tanzu-kubernetes-cluster-namespace={{vSphere Namespace}}

kubectl vsphere login --server=https://10.10.152.1 --insecure-skip-tls-verify --vsphere-username=administrator@vsphere.local --tanzu-kubernetes-cluster-namespace=ns-demo
```

**Trusted CA 생성**

사설 인증서을 사용하는 Private Registry에 대한 인증서 정보 내보내기한 다음 .pem 정보를 base64 더블 인코딩으로 전환해서 TKG 서비스 클러스터 배포 시, 신뢰받는 인증서로 추가합니다.

```bash
base64 -w0 harbor.crt | base64 -w0 > harbor-double-encoding
```

tmc-cluster-secret.yaml

```bash
apiVersion: v1
data:
  # 하기 name은 TKC yaml 배포파일에서 인증서 이름으로 동일하게 사용됩니다. 이름과 인증서 base64 인코딩 된 값을 붙여 넣습니다.
  additional-ca-1: TFMwdExTMUNSVWRKVGlCRFJWSlVTVVpKUTBGVVJTMHRMUzB0Q2sxSlNVWnNla05EUVRNclowRjNTVUpCWjBsVll6aHZXakZDZUU5T1ZFVlBTa04xU0ZkUVREaERWMng2UjNrNGQwUlJXVXB ---- 생략 ----OU9Wa2RMWTBGek5EUnFMMWRwUWk4eFZWQmtUVWhCUFQwS0xTMHRMUzFGVGtRZ1EwVlNWRWxHU1VOQlZFVXRMUzB0TFFvSw==
kind: Secret
metadata:
  # {tkc name}-user-trusted-ca-secret & tkc name은 tkc yaml 배포파일에서 지정한 이름으로 사용합니다. -user.. 이후 구문은 고정 값입니다.
  name: tmc-cluster-user-trusted-ca-secret
  # vsphere namespace: TKC yaml 파일에서 지정한 vSphere namespace 대상 이름입니다.
  namespace: cis-ns
type: Opaque
```

Trusted CA 정보를 담은 secret 파일을 생성

```bash
kubectl apply -f tmc-cluster-secret.yaml
```

TKG 서비스 클러스터를 생성(ClusterClass: builtin-generic-v3.3.0)

- tmc-cluster.yaml (tmc-sm 설치에는 6 worker nodes가 요구됩니다.)

```bash
apiVersion: cluster.x-k8s.io/v1beta1
kind: Cluster
metadata:
  name: tmc-cluster
  namespace: ns-cis
spec:
  clusterNetwork:
    pods:
      cidrBlocks:
      - 172.200.0.0/16
    serviceDomain: cluster.local
    services:
      cidrBlocks:
      - 172.18.0.0/16
  topology:
    class: builtin-generic-v3.3.0
    controlPlane:
      replicas: 3
    variables:
    - name: osConfiguration
      value:
        trust:
          additionalTrustedCAs:
          - caCert:
              secretRef:
                key: additional-ca-1
                name: tmc-cluster-user-trusted-ca-secret
    - name: vmClass
      value: best-effort-medium
    - name: storageClass
      value: tanzu-storage-policy
    - name: vsphereOptions
      value:
        persistentVolumes:
          availableStorageClasses:
          - tanzu-storage-policy
          availableVolumeSnapshotClasses: []
          defaultStorageClass: tanzu-storage-policy
          defaultVolumeSnapshotClass: 
    - name: volumes
      value:
      - capacity: 40Gi
        mountPath: /var/lib/containerd
        name: containerd-override
        storageClass: tanzu-storage-policy
      - capacity: 40Gi
        mountPath: /var/lib/kubelet
        name: kubelet-override
        storageClass: tanzu-storage-policy
    - name: kubernetes
      value:
        certificateRotation:
          enabled: true
          renewalDaysBeforeExpiry: 90
    version: v1.31.4+vmware.1-fips
    workers:
      machineDeployments:
      - class: node-pool
        name: node-pool-1
        replicas: 6
        variables:
          overrides:
          - name: vmClass
            value: best-effort-large
```

tmc-cluster yaml 파일 적용

```bash
kubectl apply -f tmc-cluster.yaml
```

**TMC-SM 구성을 환경 변수 및 namespace 생성**

```bash
## harbor path
export TKG_CUSTOM_IMAGE_REPOSITORY=harbor.tanzu.lab/tmc-sm-1.4
export TKG_CUSTOM_IMAGE_REPOSITORY_SKIP_TLS_VERIFY=true
## harbor ca 추가 - base64 인코딩
export TKG_CUSTOM_IMAGE_REPOSITORY_CA_CERTIFICATE=TFMwdExTMUNSVWRKVGB0Q2
...............
4eFZWQmtUVWhCUFQwS0xTMHRMUzFGVGtRZ1EwVlNWRWxHU1VOQlZFVXRMUzB0TFFvSw==
```

**사전 준비 사항: Carvel 패키지 도구가 작업용 호스트에 설치되어 있어야 합니다.**

옵션: Carvel 도구 설치

```bash
wget -O- https://carvel.dev/install.sh > install.sh 
sudo bash install.sh  
## 혹은 실행 파일을 브로드컴 사이트에서 다운 받아 권한 부여 후, /usr/local/bin 폴더로 이동
## admin 호스트에서 Carvel 패키지 명령어 도구를 필요로 함으로 admin 호스트로 실행 파일을 복사합니다.
```

생성한 tanzu 서비스 클러스터에 로그인 합니다.

```bash
kubectl vsphere login --server=https://10.10.152.1 --insecure-skip-tls-verify --vsphere-username=cis@vsphere.local --tanzu-kubernetes-cluster-name=tmc-cluster --tanzu-kubernetes-cluster-namespace=cis-ns

kubectl config current-context
```

kubectx 파일 설치(Air-gapped 환경의 admin 호스트에서는 바이너리 파일을 다운로드 및 이동하여 설치를 진행합니다.)

```bash
sudo apt install kubectx ## kubectx 도구는 namespace 리스트를 쉽게 확인할 수 있는 도구입니다.
```

### 1.2 Tanzu Standard Package 설치

- 실제 에어갭 환경에서 인터넷이 되는 Bastion 호스트에서 실행 후, 다운로드한 파일을 에어갭 영역의 Admin 호스트로 이동 시킨 후, 업로드를 진행합니다.

Public Registry로부터 패키지 이미지를 다운로드

```bash
# 이미지패키지 리스트를 확인할 수 있습니다.
imgpkg tag list -i projects.registry.vmware.com/tkg/packages/standard/repo

ulimit -S -n 4096 

# 이미지 패키지를 파일로 저장합니다.
imgpkg copy -b projects.registry.vmware.com/tkg/packages/standard/repo:v2025.6.17 --to-tar ./images.tar

```

vSphere용 tanzu plugin 파일도 다운로드합니다.

```bash
tanzu plugin download-bundle --group vmware-vsphere/default --to-tar ./vsphere-plugin-bundle.tar
```

Private Registry의 인증서를 Admin 호스트의 신뢰 저장소에 저장

```bash
## Ubuntu 예제
sudo cp harbor.crt /usr/local/share/ca-certificates
sudo update-ca-certificates
```

작업 전에 Harbor Registry에 Project 'tmc-sm'를 생성합니다. Admin 호스트에서 다운로드한 파일을 옮긴 후, Private Registry에 업로드를 필요로 합니다.(이 가이드에서는 “tmc-sm-1.4”를 project name으로 사용함)

올바른 harbor 인증서 경로 및 계정 정보를 입력하고서 패키지 압축 파일을 private registry에 push 합니다.

```bash
imgpkg copy --tar ./images.tar \
--to-repo tzharbor.tanzu.lab/library/packages/standard/repo \
--registry-username 'cis' \
--registry-password 'VMware1!' \
--registry-ca-cert-path=/home/viadmin/tkgs/tzharbor.crt
```

Bastion 호스트에서 다운로드한 Tanzu plugin bundle 파일을 Admin 호스트로 옮긴 후, private registry에 업로드 합니다.

```bash
tanzu config cert add --host tzharbor.tanzu.lab:443 --ca-cert tzharbor.crt

docker login harbor.tanzu.lab

tanzu plugin upload-bundle --tar ./vsphere-plugin-bundle.tar --to-repo tzharbor.tanzu.lab/library/tanzu/plugins
```

tanzu plugin의 source를 private harbor registry로 지정합니다.

```bash
tanzu plugin source update default --uri harbor.tanzu.lab/tmc-sm-1.4/plugins/plugin-inventory:latest
```

Tanzu 패키지 리포지토리를 Private Registry 경로로 지정합니다.

```bash
tanzu package repository add tanzu-standard --url harbor.tanzu.lab/tmc-sm-1.4/498533941640.dkr.ecr.us-west-2.amazonaws.com/packages/standard/repo:v2025.6.17 -n tkg-system
```

패키지 리스트 확인

```bash
tanzu package repository list -A
```

### 1.3 Cert-Manager 배포

- 다음 일부 작업에서는 인증서 생성을 돕는 Cert-Manager를 필요로 합니다.
- Production 환경에서는 고객사 CA 인증서를 활용해서, 추가 필요한 도메인들에 대한 인증서를 Cert-Manager를 통해서 생성하거나, 사전에 모든 도메인에 대한 검증된 공인 인증서를 준비해서 수동으로 secret을 생성하여 적용할 수 있습니다. 여기서는 Cert-Manager를 통한 사설 CA 인증서를 사용하여 진행합니다.

Cert-Manager 배포를 위한 namespace를 생성(On tmc-cluster)

```bash
kubectl create ns cert-manager
kubectl label --overwrite ns cert-manager pod-security.kubernetes.io/enforce=privileged
```

패키지 리스트를 확인합니다.

```bash
tanzu package available list cert-manager.tanzu.vmware.com
```

패키지 설치를 진행합니다.

```bash
tanzu package install cert-manager -p cert-manager.tanzu.vmware.com -n cert-manager -v 1.12.2+vmware.2-tkg.2
```

설치된 패키지를 확인합니다.

```bash
tanzu package installed list -n cert-manager

kubectl -n cert-manager get all
```

-

### 1.4 사설 인증서 작업

root CA 인증서를 생성하기

```bash
openssl genrsa -out rootCA.key 4096

openssl req -x509 -new -nodes -sha512 -days 3650 \
 -subj "/C=KR/ST=Seoul/L=Seoul/O=example/OU=Personal/CN=tanzu" \
 -key rootCA.key \
 -out rootCA.crt
```

base64 인코딩으로 전환

```bash
cat rootCA.crt | base64 -w0 > rootCA-crt.enc

cat rootCA.key | base64 -w0 > rootCA-key.enc
```

root 인증서에 대한 key pair를 가진 secret를 생성합니다.

- tls.crt & tls.key 항목은 인코딩된 값으로 입력합니다.

```bash
cat << EOF > ca-key-pair.yaml
apiVersion: v1
kind: Secret
metadata:
  name: ca-key-pair
  namespace: cert-manager
data:
  tls.crt: LS0tLS1CRUdJTiBDRVJ....## 여기에 올바른 인코딩 된 값을 입력
  tls.key: LS0tLS1CRUdJTiBQUkl....## 여기에 올바른 인코딩 된 값을 입력
EOF
```

secret yaml 파일을 적용합니다.

```bash
kubectl apply -f ca-key-pair.yaml
```

ClusterIssuer를 위한 yaml 파일을 생성합니다.

```bash
cat << EOF > tmc-caissuer.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: tmc-local
spec:
  ca:
    secretName: ca-key-pair
EOF

```

ClusterIssuer을 발행합니다.

```bash
kubectl apply -f tmc-caissuer.yaml
```

발행된 clusterissuer를 확인할 수 있습니다.

```bash
kubectl get clusterissuers.cert-manager.io
```

### **1.5 keycloak 배포**

Keycloak 배포를 위한 신규 TKC 클러스터 생성

- tmc-cluster 를 만든 것과 같이 동일한 vSphere Namespace에 keycloak 배포에 사용할 comm-cluster를 생성합니다.(worker node: 3)

comm-cluster-secret.yaml 파일을 작성합니다.

```bash
apiVersion: v1
data:
  # 하기 name은 TKC yaml 배포파일에서 인증서 이름으로 동일하게 사용됩니다. 이름과 인증서 base64 더블 인코딩 된 값을 붙여 넣습니다.
  additional-ca-1: TFMwdExTMUNSVWRKVGlCRFJWSlVTVVpKUTBGVVJTMHRMUzB0Q2sxSlNVWnNla05EUVRNclowRjNTVUpCWjBsVll6aHZXakZDZUU5T1ZFVlBTa04xU0ZkUVREaERWMng2UjNrNGQwUlJXVXB ---- 생략 ----OU9Wa2RMWTBGek5EUnFMMWRwUWk4eFZWQmtUVWhCUFQwS0xTMHRMUzFGVGtRZ1EwVlNWRWxHU1VOQlZFVXRMUzB0TFFvSw==
kind: Secret
metadata:
  # {tkc name}-user-trusted-ca-secret & tkc name은 tkc yaml 배포파일에서 지정한 이름으로 사용합니다. -user.. 이후 구문은 고정 값입니다.
  name: comm-cluster-user-trusted-ca-secret
  # vsphere namespace: TKC yaml 파일에서 지정한 vSphere namespace 대상 이름입니다.
  namespace: cis-ns
type: Opaque
```

Trusted CA 정보를 담은 secret 파일을 생성합니다.

```bash
kubectl apply -f comm-cluster-secret.yaml
```

comm-cluster.yaml 파일을 작성합니다.

```bash
apiVersion: cluster.x-k8s.io/v1beta1
kind: Cluster
metadata:
  name: comm-cluster
  namespace: ns-cis
spec:
  clusterNetwork:
    pods:
      cidrBlocks:
      - 172.200.0.0/16
    serviceDomain: cluster.local
    services:
      cidrBlocks:
      - 172.18.0.0/16
  topology:
    class: builtin-generic-v3.3.0
    controlPlane:
      replicas: 3
    variables:
    - name: osConfiguration
      value:
        trust:
          additionalTrustedCAs:
          - caCert:
              secretRef:
                key: additional-ca-1
                name: comm-cluster-user-trusted-ca-secret
    - name: vmClass
      value: best-effort-medium
    - name: storageClass
      value: tanzu-storage-policy
    - name: vsphereOptions
      value:
        persistentVolumes:
          availableStorageClasses:
          - tanzu-storage-policy
          availableVolumeSnapshotClasses: []
          defaultStorageClass: tanzu-storage-policy
          defaultVolumeSnapshotClass: 
    - name: volumes
      value:
      - capacity: 40Gi
        mountPath: /var/lib/containerd
        name: containerd-override
        storageClass: tanzu-storage-policy
      - capacity: 40Gi
        mountPath: /var/lib/kubelet
        name: kubelet-override
        storageClass: tanzu-storage-policy
    - name: kubernetes
      value:
        certificateRotation:
          enabled: true
          renewalDaysBeforeExpiry: 90
    version: v1.31.4+vmware.1-fips
    workers:
      machineDeployments:
      - class: node-pool
        name: node-pool-1
        replicas: 3
        variables:
          overrides:
          - name: vmClass
            value: best-effort-large
```

생성한 클러스터로 알맞은 명령어를 사용하여 로그인 및 context를 변경/확인 합니다.

```bash
kubectl config use-context comm-cluster
```

keycloak 배포를 위한 namespace를 생성하고, 권한을 부여합니다.

```bash
kubectl create ns keycloak
kubectl label --overwrite ns keycloak pod-security.kubernetes.io/enforce=privileged
```

keycloak key를 생성하고, csr을 요청 파일을 생성합니다.

```bash
openssl genrsa -out keycloak.key 4096

openssl req -sha512 -new \ -subj "/C=KR/ST=Seoul/L=Seoul/O=example/OU=Personal/CN=keycloak.tanzu.lab" \ -key keycloak.key \ -out keycloak.csr
```

인증서 x509 v3 확장을 파일을 생성합니다.

```bash
cat > v3-keycloak.ext <<-EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1=keycloak.tanzu.lab
DNS.2=*.keycloak.tanzu.lab
EOF
```

인증서 x509 확장 정보와 csr 파일 사용해서, rooCA 인증서를 통한 keycloak 인증서를 생성합니다.

```bash
#v3.ext를 이용해서 csr 및 Crt 파일을 keycloak hostname과 함께 변경  
openssl x509 -req -sha512 -days 3650 \
    -extfile v3-keycloak.ext \
    -CA rootCA.crt -CAkey rootCA.key -CAcreateserial \
    -in keycloak.csr \
    -out keycloak.crt
```

keycloak 인증서 파일과 key를 사용해서 secret을 생성합니다.(On comm-cluster)

```bash
kubectl create secret tls keycloak-tls --cert=keycloak.crt --key=keycloak.key -n keycloak
```

keycloak에 대한 Helm chart를 Private harbor registry에 복사합니다.

```bash
# Bastion 호스트에서 작업
helm repo add bitnami https://charts.bitnami.com/bitnami 
helm repo update 
helm pull bitnami/keycloak

helm show values bitnami/keycloak > keycloak-values.yaml
helm search repo | grep keycloak

# 다운로드한 keycloak 패키지 이미지 파일을 확인합니다.

## PoC 및 Prod 환경에서는 인터넷 연결된 Bastion 호스트에서 파일을 다운로드 후, 내부 Admin 호스트로 복사한 후 push 합니다.
helm push keycloak-26.2.3.tgz oci://harbor.tanzu.lab/bitnami

```

keycloak 설치에 필요한 image를 Private harbor registry에 복사합니다.

```bash
# keycloak chart에서 사용할 이미지를 pull하고서, 파일로 저장 한 다음 해당 파일을 Admin 호스트로 이동시킵니다. 
docker pull bitnami/postgresql:17.4.0-debian-12-r17 
docker pull bitnami/keycloak:26.2.3-debian-12-r0 
docker pull bitnami/keycloak-config-cli:6.4.0-debian-12-r5  

## 파일로 압축 다운로드
docker save -o postgresql-17.4.0.tar bitnami/postgresql:17.4.0-debian-12-r17
docker save -o keycloak.26.2.3.tar bitnami/keycloak:26.2.3-debian-12-r0
docker save -o keycloak-config-cli.6.4.0.tar bitnami/keycloak-config-cli:6.4.0-debian-12-r5

## PoC 과정에서는 외부 Bastion 호스트에서 파일을 다운로드 후, 내부 Admin 호스트로 복사합니다.
## Admin 호스트에서 Docker login 명령어로로 private registry에 로그인 합니다.
docker login harbor.tanzu.lab

## 이미지 파일을 Admin 호스트에서 불러오기 합니다.
docker load -i postgresql-17.4.0.tar
docker load -i keycloak.26.2.3.tar
docker load -i keycloak-config-cli.6.4.0.tar

## 불러온 이미지를 TAG를 Private Registry로 지정합니다.
docker tag bitnami/postgresql:17.4.0-debian-12-r17 harbor.tanzu.lab/bitnami/postgresql:17.4.0-debian-12-r17

docker tag bitnami/keycloak:26.2.3-debian-12-r0 harbor.tanzu.lab/bitnami/keycloak:26.2.3-debian-12-r0

docker tag bitnami/keycloak-config-cli:6.4.0-debian-12-r5 harbor.tanzu.lab/bitnami/keycloak:keycloak-config-cli:6.4.0-debian-12-r5

## docker push 명령어로 Private registry로 업로드를 진행합니다.
docker push harbor.tanzu.lab/bitnami/postgresql:17.4.0-debian-12-r17
docker push harbor.tanzu.lab/bitnami/keycloak:26.2.3-debian-12-r0
docker push harbor.tanzu.lab/bitnami/keycloak-config-cli:6.4.0-debian-12-r5
```

이미지 파일의 docker pull & push 방식은 불편함을 가질 수 있습니다.

DMZ 영역이나 Public 영역의 Registry와 Internal 영역의 Registry 간의 Harbor Replication 기능을 이용해서, 이미지를 가져올 수 있습니다.

Public Registry -> DMZ Harbor Registry -> Internal Harbor Registry

Bastion 호스트에서 받은 keycloak-values.yaml 파일을 복사하여, 환경 설정을 진행합니다.

values.yaml 파일을 배포 환경에 맞게 설정

- Production 환경에서는 Ingress 배포를 사용하거나, Prod에 맞게 scale 및 외부 Postgres DB등을 사용하는 것과 같은 환경 변수를 조정이 필요할 수 있습니다.
- keycloak용으로 앞서 생성한 tls secret name을 지정하고, LoadBalancer 고정 IP를 설정합니다.
- 글로벌 이미지 레지스트리 경로를 Private Harbor로 변경합니다.

```bash
global:
  imageRegistry: "harbor.tanzu.lab"
  imagePullSecrets: []
  defaultStorageClass: "tanzu-storage-policy"
  storageClass: "tanzu-storage-policy"
  security:
    allowInsecureImages: true
image:
  registry: docker.io
  repository: bitnami/keycloak
  tag: 26.2.2
  digest: ""
auth:
  adminUser: user
  adminPassword: "VMware1!" ## adminuser의 임시 패스워드를 설정합니다.
tls:
  enabled: true  ## tls 사용을 활성화 합니다.
  autoGenerated: false  ## true일 경우, 자동으로 인증서를 cert-manager를 통한 생성을 진행합니다.
  existingSecret: "keycloak-tls"  ## 앞서 생성한 tls를 적용한 secret을 사용합니다.
  usePem: true
service:
  type: LoadBalancer
  loadBalancerIP: "10.10.152.201"
  http:
    enabled: true
  https:
    enabled: true
postgresql:
  enabled: true  ## 외부의 postgresql을 사용 시에는 false로 전환 후, 외부 DB 정보를 구성합니다.
  auth:
    postgresPassword: "VMware1!"
    username: bn_keycloak
    password: "VMware1!"
    database: "bitnami_keycloak"
    existingSecret: ""
    architecture: standalone
  persistence:
    enabled: "true"

```

옵션: 고객이 Helm을 사용한 사용자 앱을 패키징하여 배포하는 경우, Helm repository를 에어갭 환경에 별도 구성되어 있거나, 신규 구성을 할 수 있습니다. web server, GitLab, Chartmuseum등 다양한 방식을 지원하고 있음으로, 자세한 사항은 Helm 홈페이지를 참고하시기 바랍니다.

- 이 가이드에서는 기존 Harbor repository에 helm package image을 upload하여, 직접 oci:// 구문을 통한 helm repository 추가 없이 image path를 직접 지정하여 사용하고 있습니다.

```bash
Helm repository에서 keycloak 이미지를 사용하여, 설치를 진행합니다.(comm-cluster)

## Install & Upgrade  -  Upgrade 명령어로 수행 시, 미설치 상태일 경우에는 신규 설치를 진행합니다.
helm upgrade -i keycloak oci://harbor.tanzu.lab/bitnami/keycloak -f keycloak-values.yaml --set volumePermissions.enabled=true
```

설치된 정보를 확인하고, external IP로 Web 접속을 시도합니다.

```bash
kubectl get pod -n keycloak

kubectl get svc -n keycloak

kubectl get pv,pvc -n keycloak
```

https://keycloak.tanzu.lab 사이트에 접속하여, 임시 사용자 user로 접속해서 다음 작업을 진행합니다.
