### 3.6.4 Contour 설치

---

Contour는 TKG 서비스 클러스터 내에서 Envoy Reverse Proxy설치와 함께 쿠버네티스 클러스터 환경으로 인입 서비스 트래픽에 대한 L7 HTTP 및 HTTPs 트래픽 처리를 지원합니다.

tanzu package 가용 리스트를 확인합니다.

```bash
$ tanzu package available get contour.tanzu.vmware.com -n tkg-system
$ kubectl -n tkg-system get packages | grep contour
```

contour 배포 시, 환경 값으로 사용될 기본 환경 정보 파일을 생성합니다.(파일명: contour-data-values.yaml)

백업 파일을 생성하고, sed 명령어로 주석문을 제거한 신규 파일을 생성합니다.

```bash
$ tanzu package available get contour.tanzu.vmware.com/1.28.2+vmware.1-tkg.1 --default-values-file-output contour-data-values.yaml

$ mv contour-data-values.yaml contour-data-values.yaml.bak

$ sed 's/# //g' contour-data-values.yaml.bak > contour-data-values.yaml
```

편집기를 사용하여, contour-data-values.yaml 파일을 수정합니다.

```bash
$ vi contour-data-values.yaml
```

```bash
---
infrastructure_provider: vsphere
namespace: tanzu-system-ingress
contour:
  configFileContents: {}
  useProxyProtocol: true
  replicas: 2
  pspNames: "vmware-system-restricted"
  logLevel: info
envoy:
  service:
    type: LoadBalancer
#    LoadBalancerIP: 10.10.152.14  # set static IP if you want
    annotations: {}
    externalTrafficPolicy: Cluster
    disableWait: false
  hostPorts:
    enable: true
    http: 80
    https: 443
  hostNetwork: false
  terminationGracePeriodSeconds: 300
  logLevel: info
certificates:
  duration: 8760h
  renewBefore: 360h

```

Contour 패키지를 설치를 위한 namespace를 생성합니다.

```bash
$ kubectl create ns tanzu-system-ingress

$ kubectl label --overwrite ns tanzu-system-ingress pod-security.kubernetes.io/enforce=privileged
```

Contour 패키지를 설치를 진행합니다.

```bash
$ tanzu package install contour -p contour.tanzu.vmware.com -v 1.28.2+vmware.1-tkg.1 --values-file contour-data-values.yaml -n tanzu-system-ingress
```

Contour 설치 상태 정보를 확인합니다.

```bash
$ tanzu package installed list -n tanzu-system-ingress

NAME     PACKAGE-NAME              PACKAGE-VERSION        STATUS

contour  contour.tanzu.vmware.com  1.28.2+vmware.1-tkg.1  Reconcile succeeded
```

Namespace 내에 Contour 설치 상태 정보를 확인합니다.

```bash
$ kubectl -n tanzu-system-ingress get all
```

```bash
NAME                           READY   STATUS    RESTARTS   AGE
pod/contour-777bdddc69-fqnsp   1/1     Running   0          102s
pod/contour-777bdddc69-gs5xv   1/1     Running   0          102s
pod/envoy-d4jtt                2/2     Running   0          102s
pod/envoy-g5h72                2/2     Running   0          102s
pod/envoy-pjpzc                2/2     Running   0          102s

NAME              TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)                      AGE
service/contour   ClusterIP      10.105.242.46   <none>          8001/TCP                     102s
service/envoy     LoadBalancer   10.103.245.57   10.197.154.69   80:32642/TCP,443:30297/TCP   102s

NAME                   DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
daemonset.apps/envoy   3         3         3       3            3           <none>          102s

NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/contour   2/2     2            2           102s

NAME                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/contour-777bdddc69   2         2         2       102s

```

+++
