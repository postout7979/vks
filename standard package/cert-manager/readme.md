### Cert Manager 설치

---

Cert Manager는 Kubernetes내 애플리케이션에 사용 되어지는 인증서에 대한 셀프 인증서 발급 및 관리를 제공합니다.

표준 패키지에서 Contour, ExternalDNS, Prometheus 및 Harbor 패키지를 이용 시, 사전에 Cert Manager가 제공되야 합니다.

TKG Service Cluster에 로그인한 후

패키지 사용 여부를 확인합니다.

```bash
$ tanzu package available get cert-manager.tanzu.vmware.com -n tkg-system
```

패키지 설치 대상 namespace을 생성합니다.

```bash
$ kubectl create ns cert-manager
$ kubectl label --overwrite ns cert-manager pod-security.kubernetes.io/enforce=privileged
```

Cert Manager를 대상 namespace에 설치 명령어를 수행합니다.

```bash
$ tanzu package install cert-manager -p cert-manager.tanzu.vmware.com --namespace cert-manager --version 1.13.3+vmware.1=tkg.1
```

대상 namespace에 설치된 패키지 리스트를 확인합니다.

```bash
$ tanzu package installed list -n package-installed

$ tanzu package installed get cert-manager -n package-installed
```

Cert Manager namespace에 생성된 인스턴스를 확인합니다.

```bash
$ kubectl -n cert-manager get all

NAME                                          READY   STATUS    RESTARTS   AGE

pod/cert-manager-b5675b75f-flkjp              1/1     Running   0          6m14s

pod/cert-manager-cainjector-f8dc756cf-f7xsv   1/1     Running   0          6m14s

pod/cert-manager-webhook-6c888c8ddd-5xlnb     1/1     Running   0          6m14s

NAME                           TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE

service/cert-manager           ClusterIP   10.97.254.59     <none>        9402/TCP   6m14s

service/cert-manager-webhook   ClusterIP   10.105.225.156   <none>        443/TCP    6m14s

NAME                                      READY   UP-TO-DATE   AVAILABLE   AGE

deployment.apps/cert-manager              1/1     1            1           6m14s

deployment.apps/cert-manager-cainjector   1/1     1            1           6m14s

deployment.apps/cert-manager-webhook      1/1     1            1           6m14s

NAME                                                DESIRED   CURRENT   READY   AGE

replicaset.apps/cert-manager-b5675b75f              1         1         1       6m14s

replicaset.apps/cert-manager-cainjector-f8dc756cf   1         1         1       6m14s

replicaset.apps/cert-manager-webhook-6c888c8ddd     1         1         1       6m14s
```

**Upgrade Cert Manager**

패키지 업데이트를 tanzu package installed update 명령어를 사용해서 진행할 수 있습니다.

```bash
$ tanzu package installed update cert-manager -v 1.13.3+vmware.1-tkg.1 --namespace cert-manager
```

**Delete Cert Manager**

패키지 삭제를 tanzu package installed delete 명령어를 사용해서 진행할 수 있습니다.

```bash
$ tanzu package installed delete cert-manager -n package-installed -y
```

**Troubleshoot**

패키지 설치 문제가 발생 시, 설치 상태를 확인할 수 있습니다.

```bash
$ kubectl get pkgi -A

$ kubectl describe pkgi cert-manager -n package-installed
```

+++
