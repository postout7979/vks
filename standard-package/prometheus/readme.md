### 3.6.6 Prometheus 설치(With Alertmanager)

---

Prometheus는 Kubernetes 플랫폼 내에서 발생하는 메트릭 정보를 수집하여, 시계열 정보로 저장하여, 활용할 수 있도록 서비스를 제공합니다.

1. 리포지토리로부터 패키지 가용 여부를 확인합니다.

```bash
$ tanzu package available get prometheus.tanzu.vmware.com -n tkg-system

$ kubectl -n tkg-system get packages | grep prometheus
```

패키지로부터 설치에 필요한 기본 prometheus-data-values 파일을 생성합니다.

백업 파일을 생성하고, 주석문을 제거한 다음 신규 파일을 생성합니다.

```bash
$ tanzu package available get prometheus.tanzu.vmware.com/2.45.0+vmware.1-tkg.2 --default-values-file-output prometheus-data-values.yaml

$ mv prometheus-data-values.yaml prometheus-data-values.yaml.bak

$ sed 's/# //g' prometheus-data-values.yaml.bak > prometheus-data-values.yaml
```

prometheus-data-values 파일을 수정합니다.

```bash
$ vi prometheus-data-values.yaml
```

| Parameter | Description |
| --- | --- |
| ingress.tlsCertificate.tls.crt | 셀프 TLS 인증서를 인그레스를 위해서 생성됨. 소유 인증서 정보를 직접 추가할 수 있습니다. |
| ingress.tlsCertificate.tls.key | 셀프 TLS 인증서 Private Key를 인그레스를 위해서 생성됨. 소유 인증서 정보를 직접 추가할 수 있습니다. |
| ingress.enabled | default: false - Ingress 서비스를 활성화합니다. |
| ingress.virtual_host_fqdn | default: prometheus.system.tanzu - your own is  prometheus.<your.domain> |
| alertmanager.pvc.storageClassName | vSphere Storage Policy를 입력합니다. |
| prometheus.pvc.storageClassName | vSphere Storage Policy를 입력합니다. |

**Prometheus 구성 요소**

| Container | Resource Type | Replicas | 용도 |
| --- | --- | --- | --- |
| prometheus-alertmanager | Deployment | 1 | Prometheus 서버와 같은 클라이언트 애플리케이션에서 보낸 알림을 처리합니다. |
| prometheus-cadvisor | DaemonSet | 5 | 실행 중인 컨테이너에서 리소스 사용 및 성능 데이터를 분석하고 공개합니다. |
| prometheus-kube-state-metrics | Deployment | 1 | 노드 상태 및 용량, 복제본 세트 규정 준수, Pod, 작업 및 Cronjob 상태, 리소스 요청 및 제한을 모니터링합니다. |
| prometheus-node-exporter | DaemonSet | 5 | 커널에 의해 노출된 하드웨어 및 OS 메트릭을 내보내는 프로그램입니다. |
| prometheus-pushgateway | Deployment | 1 | 스크래핑할 수 없는 작업의 메트릭을 푸시할 수 있는 서비스입니다. |
| prometheus-server | Deployment | 1 | 스크래핑, 규칙 처리, 알림 등의 핵심 기능을 제공합니다. |

**Prometheus Data Values**

아래 링크는 prometheus-data-values.yaml 파일의 예입니다.

[Prometheus Data Values](https://www.google.com/url?q=https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere-supervisor/8-0/using-tkg-service-with-vsphere-supervisor/installing-standard-packages-on-tkg-service-clusters/standard-package-reference/prometheus-package-reference.html&sa=D&source=editors&ust=1749716239673221&usg=AOvVaw0XwKn3zfYEmStjXqUTS_3t)

다음 사항에 유의하세요.

- Ingress가 활성화(ingress: enabled: true).
- Ingress는 /alertmanager/(alertmanager_prefix:) 및 /(prometheus_prefix:)로 끝나는 URL에 대해 구성되었습니다.
- Prometheus의 FQDN은 prometheus.system.tanzu(virtual_host_fqdn:)입니다.
- Ingress 섹션(tls.crt, tls.key, ca.crt)에 사용자 지정 인증서를 제공합니다.(이 예제에서는 insecure로 동작을 위해서 tls 구문은 모두 # 주석 처리를 합니다.)
- alertmanager의 pvc는 2GiB입니다. 기본 스토리지 정책에 대한 storageClassName을 제공합니다.
- prometheus의 pvc는 20GiB입니다. vSphere 스토리지 정책에 대한 storageClassName을 제공합니다.

**Prometheus-Data-Values.yaml**

```bash
alertmanager:
  config:
    alertmanager_yml: |
      global:
      receivers:
      - name: default-receiver
      templates:
      - '/etc/alertmanager/templates/*.tmpl'
      route:
        group_interval: 5m
        group_wait: 10s
        receiver: default-receiver
        repeat_interval: 3h
  deployment:
    replicas: 1
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    updateStrategy: Recreate
  pvc:
    accessMode: ReadWriteOnce
    storage: 2Gi
    storageClassName: tanzu-storage-policy
  service:
    port: 80
    targetPort: 9093
    type: ClusterIP
ingress:
  alertmanager_prefix: /alertmanager/
  alertmanagerServicePort: 80
  enabled: true
  prometheus_prefix: /
  prometheusServicePort: 80
  #! [Required] the tlsCertificate if you want your own certificate.
#  tlsCertificate:
#    ca.crt:
#    tls.crt:
#    tls.key:
  virtual_host_fqdn: prometheus.vks.holo.lab
kube_state_metrics:
  deployment:
    replicas: 1
  service:
    port: 80
    targetPort: 8080
    telemetryPort: 81
    telemetryTargetPort: 8081
    type: ClusterIP
namespace: tanzu-system-monitoring
node_exporter:
  daemonset:
    hostNetwork: false
    updatestrategy: RollingUpdate
  service:
    port: 9100
    targetPort: 9100
    type: ClusterIP
--- 이하 생략 ---

```

- -- 이하 생략 ---

data-values.yaml 파일 내에는 총 2개의 storageClassName 항목이 존재하고 있습니다. 해당 문구를 검색한 후, 올바른 storageClass name을 입력해야 합니다.

패키지 설치를 위한 namespace을 생성합니다.

```bash
$ kubectl create namespace tanzu-system-monitoring

$ kubectl label --overwrite ns tanzu-system-monitoring pod-security.kubernetes.io/enforce=privileged
```

tanzu package 명령어를 사용한 패키지 설치를 진행합니다.

```bash
$ tanzu package install prometheus -p prometheus.tanzu.vmware.com -v 2.45.0+vmware.1-tkg.2 --values-file prometheus-data-values.yaml -n tanzu-system-monitoring
```

설치 패키지 리스트를 검증합니다.

```bash
$ tanzu package installed list -n my-packages

  or

$ kubectl -n tanzu-system-monitoring get pvc

NAME                STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
alertmanager        Bound    pvc-a53f7091-9823-4b70-a9b4-c3d7a1e27a4b   2Gi        RWO            k8s-policy     2m30s
prometheus-server   Bound    pvc-41745d1d-9401-41d7-b44d-ba430ecc5cda   20Gi       RWO            k8s-policy     2m30s

```

prometheus를 위한 ingress 혹은 httpproxy 배포 상태를 확인합니다.

```bash
$ kubectl get ingress -A
  or
$ kubectl get httpproxy -A

```

+++
