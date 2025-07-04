### **5.6.7 Grafana 설치**

---

Grafana 패키지는 vSphere Supervisor

- grafana 패키지 설치 리스트를 확인합니다.

```bash
$ tanzu package available list grafana.tanzu.vmware.com
```

- grafana 패키지 설치 구성 파일을 생성합니다.

```bash
$ tanzu package available get grafana.tanzu.vmware.com/10.0.1+vmware.1-tkg.3 --default-values-file-output grafana-data-values.yaml
```

- grafana-data-values.yaml 파일을 vi 편집기로 알맞은 값으로 변경합니다.
    - 템플릿에는 기본 데이터소스로 설치되는 TKC에 prometheus-server 주소가 구성되어 있습니다.
    - 추가 datasource가 필요한 경우, grafana 배포 이후에 UI에서 추가할 수 있습니다.
    - storageClass을 정의합니다.
    - 초기 admin user & password는 모두 ‘admin’ 입니다. password를 변경하려면 base64 인코딩된 값을 필요로 하니, 아래 명령문을 참고하시기 바랍니다. ‘mypassword’ 항목을 원하는 문자열로 치환 후, 출력되는 base64 인코딩 값을 사용합니다.
    - 외부 노출이 필요한 경우에는 .grafana.service.type 항목을 NodePort → LoadBalancer로 변경합니다.

```bash
#! The namespace in which to deploy grafana.
namespace: tanzu-system-dashboards

grafana:
  #! The grafana configuration.
  config:
    #! Refer to https://grafana.com/docs/grafana/latest/administration/provisioning/#example-data-source-config-file
    datasource_yaml: |-
      apiVersion: 1
      datasources:
        - name: Prometheus
          type: prometheus
          # prometheus namespace
          url: http://prometheus-server.tanzu-system-monitoring.svc.cluster.local
          access: proxy
          tlsSkipVerify: true
          isDefault: true
  pvc:
    storageClassName: tanzu-storage-policy
    accessMode: ReadWriteOnce
    storage: 20Gi
  secret:
    admin_password: YWRtaW4=
    admin_user: YWRtaW4=
    type: Opaque
  service:
    port: 80
    targetPort: 3000
    type: NodePort
ingress:
  enabled: true
  prefix: /
  servicePort: 80
  virtual_host_fqdn: grafana.vks.tanzu.lab
  tlsCertificate:
    tls:
      crt:
      key:
    ca:
      crt:

```

- 계정 패스워드 변경

```bash
$ echo -n 'mypassword' | base64 -w0
```

- grafana 패키지 설치를 위한 namespace을 생성합니다.(이름 변경 금지)

```bash
$ kubectl create namespace tanzu-system-dashboards
$ kubectl label --overwrite ns tanzu-system-dashboards pod-security.kubernetes.io/enforce=privileged
```

- grafana 패키지 설치를 진행합니다.

```bash
$ tanzu package install prometheus -p grafana.tanzu.vmware.com -v 10.0.1+vmware.1-tkg.3 --values-file grafana-data-values.yaml -n tanzu-system-dashboards
```

- 설치 패키지 상태를 확인합니다.

```bash
$ tanzu package installed list -n tanzu-system-dashbaords

$ kubectl get all -n tanzu-system-dashbaords
```

- ingress(httpproxy) 정보를 확인합니다.

```bash
# contour ingress 배포 시
$ kubectl get ingress -n tanzu-system-dashbaords
# contour ingress를 httpproxy mode 배포 시
$ kubectl get httpproxy -n tanzu-system-dashbaords
```

- 모든 namespace에서 존재하는 ingress 인스턴스를 확인

```bash
$ kubectl get httpproxy -A

NAMESPACE NAME FQDN TLS SECRET STATUS STATUS DESCRIPTION

tanzu-system-dashboards grafana-httpproxy grafana.vks.tanzu.lab grafana-tls valid Valid HTTPProxy

tanzu-system-monitoring prometheus-httpproxy prometheus.vks.tanzu.lab prometheus-tls valid Valid HTTPProxy
```

