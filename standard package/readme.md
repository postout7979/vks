TKG Service Cluster에 Tanzu Standard Package를 사용해서 Kubernetes Cluster 운영에 필요한 오픈소스 기반 도구를 사용할 수 있습니다.

TKG Service Cluster를 지원하는 지원 패키지

- Cert Manager: Certificate management
- Contour with Envoy: Kubernetes ingress controller and reverse proxy
- ExternalDNS: DNS lookup of Kubernetes services
- Fluent Bit: Log forwarding
- Prometheus with Alertmanager: Monitoring and alerting
- Harbor: Container registry
- External CSI Snapshot Validation Webhook & vSphere PV CSI Webhook: Persistent storage snapshotting
- Cluster Autoscaler: Cluster autoscaling
- Windows gMSA Webhook: Identity management
- Telegraf: Monitoring and metrics collection

### 3.6.1 패키지 설치를 위한 일반 요구 사항

---

vSphere 7.x와 vSphere 8.x의 패키지 설치 요구 사항은 상이하며, 여기서는 vSphere 8.x에 대한 설치 과정을 다룹니다.

**Repository 요구 사항**

vSphere 8 TKR에는 Kapp Controller로 잘 알려진 Carvel 도구가 패키징 되어 있습니다.

**클라이언트 요구 사항**

TKrs for vSphere 8.x로 프로비저닝된 TKG 클러스터에 표준 패키지를 설치하려면 Kubectl 및 kubectl용 vSphere 플러그인을 포함한 Kubernetes CLI Tools for vSphere와 Tanzu CLI가 필요합니다. 이러한 도구를 설치하려면 TKG 서비스 클러스터용 CLI 도구 설치를 참조하세요.

---

**Tanzu CLI 설치(v1.1)**

- APT(Debian or Ubuntu)

```bash
sudo apt update

sudo apt install -y ca-certificates curl gpg

sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://storage.googleapis.com/tanzu-cli-installer-packages/keys/TANZU-PACKAGING-GPG-RSA-KEY.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/tanzu-archive-keyring.gpg

echo "deb [signed-by=/etc/apt/keyrings/tanzu-archive-keyring.gpg] https://storage.googleapis.com/tanzu-cli-installer-packages/apt tanzu-cli-jessie main" | sudo tee /etc/apt/sources.list.d/tanzu.list

sudo apt update

sudo apt list tanzu-cli -a

sudo apt install -y tanzu-cli=1.1.0
```

Windows, RHEL 및 MAC OS에서의 설치는 아래 링크를 참조하시기 바랍니다.

[https://github.com/vmware-tanzu/tanzu-cli/blob/main/docs/quickstart/install.md](https://www.google.com/url?q=https://github.com/vmware-tanzu/tanzu-cli/blob/main/docs/quickstart/install.md&sa=D&source=editors&ust=1749716239602914&usg=AOvVaw1jFgA5bzhGC-UhKlPCpWuI)

**Tanzu CLI Plugin**

Tanzu CLI 플러그인은 CLI 명령 그룹을 패키징하는 실행 가능한 바이너리입니다. 핵심 CLI에는 일부 명령 그룹이 내장되어 있으며, CLI 플러그인은 추가 명령 그룹으로 CLI를 확장합니다.

특정 플러그인은 컨텍스트 유형에 따라 CLI를 연결하는 다양한 제품과 다양한 컨텍스트와 관련이 있습니다. 각 제품은 CLI Core, 플러그인, 플러그인 그룹 및 제품에 설명된 대로 관련 플러그인을 독립 실행형 또는 컨텍스트 범위로 지정합니다.

컨텍스트 범위 플러그인: 제품에 연결하기 위해 Tanzu CLI 컨텍스트를 만들면 컨텍스트 범위 플러그인이 아직 설치되지 않은 경우 자동으로 설치됩니다. 백업으로 플러그인이 자동으로 설치되지 않으면 원하는 컨텍스트로 CLI를 설정한 상태에서 tanzu plugin sync를 실행하여 플러그인을 설치할 수 있습니다.

독립 실행형 플러그인: 일부 제품의 경우 아래에 설명된 대로 tanzu plugin install을 실행하여 독립 실행형 플러그인을 설치해야 합니다.

위의 Tanzu CLI 설치 단계를 완료한 후 다음 지침에 따라 독립형 Tanzu CLI 플러그인을 설치할 수 있습니다. 하나의 명령을 사용하여 플러그인 그룹의 모든 플러그인을 설치하거나 각 플러그인을 개별적으로 설치할 수 있습니다.

설치 가능한 플러그인 그룹 목록을 확인합니다.

```bash
tanzu plugin group search

GROUP                       DESCRIPTION                          LATEST
vmware-tap/default          Plugins for TAP                      v1.6.3
vmware-tkg/default          Plugins for TKG                      v2.4.0
vmware-vsphere/default          Plugins for vSphere                      v8.0.3
```

vSphere Supervisor의 TKG를 위한 vmware-tkg에 대한 plugin group을 설치합니다.

```bash
$ tanzu plugin install --group vmware-vsphere/default
```

옵션: 다른 버전의 플러그인 버전을 설치를 원할 경우에는 모든 가능 버전을 확인할 수 있습니다.

```bash
$ tanzu plugin group search -n vmware-vsphere/default --show-details
```

옵션: 다른 버전의 플러그인 설치는 아래와 같이 특정 버전을 정의해야 합니다.

```bash
$ tanzu plugin install --group vmware-vsphere/default:v8.0.3
```

설치된 플러그인을 확인합니다.

```bash
$ tanzu plugin group get vmware-vsphere/default
$ tanzu plugin list
```

![](attachment:d0a6d9c5-d7a0-40ca-95a4-3d985f5f49a3:imagesimage85.png)

Air-Gapped 환경에서의 설치 과정은 아래 링크를 통해서 확인하시기 바랍니다.

[https://techdocs.broadcom.com/us/en/vmware-tanzu/cli/tanzu-cli/1-1/cli/index.html](https://www.google.com/url?q=https://techdocs.broadcom.com/us/en/vmware-tanzu/cli/tanzu-cli/1-1/cli/index.html&sa=D&source=editors&ust=1749716239610632&usg=AOvVaw0Nyp6J6oymqO9JPiNoDVk3)

**Carvel Package tool 설치**

Carvel 패키지 도구는 이미지를 패키징 및 배포 도구로 Tanzu CLI 명령어와 함께 활용됩니다. 아래 링크를 통해서 설치 가이드를 확인할 수 있습니다. (kapp, ytt, imgpkg, kwt, kbld, kctrl)

[https://carvel.dev/kapp/docs/v0.64.x/install/](https://www.google.com/url?q=https://carvel.dev/kapp/docs/v0.64.x/install/&sa=D&source=editors&ust=1749716239611925&usg=AOvVaw2HY7OO3jcjyHLDlR_a3ma6)

**script 기반 설치**

```bash
$ wget -O- https://carvel.dev/install.sh > [install.sh](https://www.google.com/url?q=http://install.sh&sa=D&source=editors&ust=1749716239612938&usg=AOvVaw3whZdfQwgQb846DAhLeGSa) --no-

# Inspect install.sh before running...

$ sudo bash install.sh

$ kapp version
```

### 3.6.2 Package Repository 추가

---

Tanzu Package Repository를 TKG Cluster에 추가

Tanzu standard package version을 공식 홈페이지를 통해서 확인할 수 있습니다.

- 이 작업은 tkg-demo-cl 클러스터로 context를 이동하여 진행됩니다.

```bash
kubectl config use-context tkg-demo-cl
```

tanzu CLI 명령어를 사용해서 목표 패키지 버전에 맞춰서 repository를 ‘tkg-system’ namespace에 추가합니다.

```bash
tanzu package repository add standard-repo --url projects.registry.vmware.com/tkg/packages/standard/repo:v2025.4.29 -n tkg-system
```

** 내부 Repository를 이용할 경우, 올바른 내부 Repository 경로를 사용해서 설치를 진행합니다.

---

- 사용 가능한 패키지 리스트를 확인합니다.

```bash
$ tanzu package available list -n tkg-system
```

사용 가능한 패키지별 버전 리스트를 확인할 수 있습니다.

```bash
$ tanzu package available get cert-manager.tanzu.vmware.com -n tkg-system

$ tanzu package available get contour.tanzu.vmware.com -n tkg-system

$ tanzu package available get external-dns.tanzu.vmware.com -n tkg-system

$ tanzu package available get fluent-bit.tanzu.vmware.com -n tkg-system

$ tanzu package available get prometheus.tanzu.vmware.com -n tkg-system
```

패키지 리포지토리내 모든 리스트를 확인할 수 있습니다.

tanzu package repository list 명령을 사용하여 대상 TKG 서비스 클러스터에서 사용할 수 있는 모든 패키지 저장소를 나열합니다. 이 목록에는 tanzu package repository add 명령을 실행하여 대상 클러스터에 추가된 패키지 저장소가 포함됩니다.

```bash
$ tanzu package repository list -n tkg-system
```

![](attachment:a4a80a87-2035-45d6-b5c6-108a39cb9703:imagesimage15.png)

패키지 리포지토리에 대한 상세 정보를 확인할 수 있습니다.

```bash
$ tanzu package repository get REPOSITORY-NAME -n tkg-system
```

**패키지 리포지토리 업데이트**

```bash
$ tanzu package repository update REPOSITORY-NAME --url REPOSITORY-URL -n tkg-system
```

**패키지 리포지토리 삭제**

```bash
$ tanzu package repository delete REPOSITORY-NAME -n tkg-system
```

+++
