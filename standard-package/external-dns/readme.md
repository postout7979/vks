### 3.6.5 ExternalDNS

---

ExternalDNS를 사용하면 Envoy가 포함된 Contour와 같은 인그레스 구성 요소가 있는 Kubernetes 서비스에 대해 DNS 레코드를 자동으로 만들 수 있습니다. ExternalDNS 패키지는 다음 DNS 공급자로 검증되었습니다. AWS Route 53, Azure DNS 및 RFC2136 호환 DNS 서버(예: BIND).

ExternalDNS를 사용할 경우, Kubernetes에서 Contour를 사용한 Ingress 혹은 HTTPProxy 사용 시, FQDN에 대해서 지정된 DNS 서버에 A record를 자동으로 생성/업데이트/삭제를 진행합니다.

리포지토리로부터 패키지 가용 여부를 확인합니다.

```bash
$ tanzu package available get external-dns.tanzu.vmware.com -n tkg-system
```

external dns 서비스에 대한 환경 설정 파일을 생성합니다.

```bash
$ tanzu package available get external-dns.tanzu.vmware.com/0.14.2+vmware.3-tkg.1 --default-values-file-output external-dns-data-values.yaml
```

external dns 서비스에 대한 환경 설정 파일을 편집합니다.

```bash
$ vi external-dns-data-values.yaml
```

참고링크: [external-dns-values.yaml](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere-supervisor/8-0/using-tkg-service-with-vsphere-supervisor/installing-standard-packages-on-tkg-service-clusters/standard-package-reference/externaldns-package-reference.html)

- 여기서는 insecure 통신으로 MS DNS 서버와 통신을 하도록 준비합니다.
- MS DNS 서버에서의 설정
    - DNS Zone을 생성합니다.(이미 생성되어 있다면 PASS)
    - secure dynamic updates for the zone을 활성화합니다.
    - 모든 서버로 zone transfer를 활성화 합니다.
    - Zone에 create/update/delete record 권한 계정을 부여합니다.

```bash
---
# Namespace in which to deploy ExternalDNS pods and this namespace name cannot be replaced to user defined
namespace: tanzu-system-service-discovery
# Deployment-related configuration
deployment:
  args:
     - --registry=txt
     - --txt-owner-id=cis
     - --txt-prefix=external-dns- #! Disambiguates TXT records from CNAME records
     - --provider=rfc2136
     - --rfc2136-host=172.18.10.101 #! Replace with IP of RFC2136-compatible DNS server, such as 192.168.0.1
     - --rfc2136-port=53
     - --rfc2136-zone=tanzu.lab #! Replace with zone where services are deployed, such as my-zone.example.org 
#     - --rfc2136-tsig-secret=TSIG-SECRET #! Replace with TSIG key secret authorized to update DNS server
#     - --rfc2136-tsig-secret-alg=hmac-sha256
#     - --rfc2136-tsig-keyname=TSIG-KEY-NAME #! Replace with TSIG key name, such as externaldns-key
     - --rfc2136-insecure
     - --rfc2136-tsig-axfr
     - --source=service
     - --source=ingress
     - --source=contour-httpproxy  #! Only Enables Contour HTTPProxy need set
     - --domain-filter=tanzu.lab #! Zone where services are deployed, such as my-zone.example.org
     - --log-level=debug   # for debugging to get more log information

```

external dns 서비스를 설치할 namespace을 생성하고, 권한을 부여 합니다.

```bash
$ kubectl create ns tanzu-system-service-discovery
$ kubectl label namespace tanzu-system-service-discovery pod-security.kubernetes.io/enforce=privileged
```

external dns 서비스를 설치를 진행합니다.

```bash
$ tanzu package install external-dns -p external-dns.tanzu.vmware.com --version 0.14.2+vmware.3-tkg.1 --namespace tanzu-system-service-discovery --dangerous-allow-use-of-shared-namespace --values-file external-dns-data-values.yaml
```

설치된 external dns Pod를 확인합니다.

```bash
$ kubectl get pod -n tanzu-system-service-discovery

NAME					READY	STATUS		RESTARTS	AGE
external-dns-b7475b8bf-5nzhj	1/1	Running	0		28m

```

설치된 external dns Pod의 logs 정보를 확인합니다.

```bash
$ kubectl logs external-dns-b7475b8bf-5nzhj -n tanzu-system-service-discovery
```

![](attachment:13ac8835-0e02-4b8c-985c-54708b0affae:imagesimage194.png)

+++
