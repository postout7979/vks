
<img width="1972" height="1724" alt="image" src="https://github.com/user-attachments/assets/8f9c27c1-5504-4460-a26e-884e2e56ba65" />


Avi controllers were deployed on two site for GSLB service.

Primary AVI controllers were placed across two sites.(1+2)

Primary AVI controllers managed SE group for ingress service.

- Main AKO configuration is used to Site-A for primary SE group.
- Aviinfrasetting configuration is used to Site-B for another SE group.

```smalltalk
primary SE Group
- VIP network: 172.20.10.0/24  # Primary VIP network will be registered to IPAM profile.

Secondary SE Group
- VIP network: 172.19.20.0/24  # Secondary VIP network isn't used IPAM profile.

Node Network
- VPC private network name in VKS cluster.(vpc private network name is generated as vpc subnet automatically.
```

**Key**

- It supports Active-Active(DR) in terms an infrastructure layer.
- Workload will be deployed on Site-A
- When site-A has failure, workload will be failover to site-B

**T0 EDGE:** Active-Standby

**CTGW:** Active-Standby

**AKO support**

Supervisor + NSX classic LB(VPC) as default LB

- Supervisor and VKS api use with NSX vpc LB, and AKO(vCenter cloud) will be deployed independently into VKS Cluster.
- L4 and L7 service for applications uses loadbalancerClass and ingressclass with AKO, not using the cloud provider LB(NSX classic LB).

**values.yaml information**

- avi controller 설정
- Local harbor image registry or Broadcom public registry(require broadcom site token)
- primaryInstance: true
- clusterName: '{vks cluster name}'
- namespaceSelector:  # empty label watch all namespace.  Label and key watches particular namespace as injection of metadata in namespace.
    labelKey: ''
    labelValue: ''
- nodeNetworkList:
    - networkName: "avi-vks-cl-9knkx-c7f58947_c623z"  # node network is vpc private network name.
      cidrs:
        - 172.10.0.32/27
- vipNetworkList:
   - networkName: "MGMT-PG-172.20.10.x"
     cidr: 172.20.10.0/24
- L7Settings:
  defaultIngController: 'true'     # True is used for Ingress service.
  serviceType: 'NodePort'
- L4Settings:
  defaultLBController: 'false'     # false is used for Load Balancer service with loadbalancerClass.
- serviceEngineGroupName: Default-Group    # First service engine group.
  controllerVersion: '32.1.2'
  cloudName: Default-Cloud
  controllerHost: '172.18.10.201'
  tenantName: admin

### AKO 기본 배포 시, values.yaml 파일

values.yaml

**AviInfraSetting**

- AviInfraSetting CRD supports deploying additional SE Group for different LB configuration.

```yaml
apiVersion: ako.vmware.com/v1beta1
kind: AviInfraSetting
metadata:
  name: vip-infrasetting
spec:
  seGroup:
    name: second-Group
  network:
    vipNetworks:
      - networkName: wd-hcs-cl01-vds-01-pg-vmotion
        cidr: 172.19.20.0/24
    enableRhi: false
      #    nodeNetworks:
      #      - networkName: 2051
      #        cidr: 10.200.51.0/24
```

---

## L4 Service

Default AKO Segroup에서 L4 LB 서비스 생성(172.20.10.x 범위)

- loadBalancerClass

```yaml
apiVersion: v1
kind: Service
metadata:
  name: guestbook-frontend-first
  namespace: guestbook
  labels:
    app: guestbook
    tier: frontend
spec:
  type: LoadBalancer
  loadBalancerClass: ako.vmware.com/avi-lb
  ports:
    - port: 80
  selector:
    app: guestbook
    tier: frontend
```

추가 SE Group에 대한 L4 LB 서비스 생성(172.19.20.x 범위)

- loadBalancerClass and annotation

```yaml
apiVersion: v1
kind: Service
metadata:
  annotations:
    aviinfrasetting.ako.vmware.com/name: "vip-infrasetting"
  name: guestbook-frontend-second
  namespace: guestbook
  labels:
    app: guestbook
    tier: frontend
spec:
  type: LoadBalancer
  loadBalancerClass: ako.vmware.com/avi-lb
  ports:
    - port: 80
  selector:
    app: guestbook
    tier: frontend
```

---

## L7 Ingress

Create two L7 Ingresses using different VIP networks and SE groups within the same VKS cluster.

Ingress 배포를 위한 백엔드 service - clusterIP 생성

```yaml
apiVersion: v1
kind: Service
metadata:
  name: guestbook-frontend
  namespace: guestbook
  labels:
    app: guestbook
    tier: frontend
spec:
  # ⭐️ L7 배포를 위해 내부 통신용(ClusterIP)으로 전환합니다 (생략 시 기본값 ClusterIP)
  type: ClusterIP 
  ports:
    - port: 80
      targetPort: 80 # 실제 팟 컨테이너가 열고 있는 포트 번호와 일치시킵니다.
  selector:
    app: guestbook
    tier: frontend

```

First ingress 생성

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: guestbook-ingress-first
  namespace: guestbook
spec:
  # AKO 컨트롤러가 감지할 수 있도록 인그레스 클래스를 필수 지정합니다.
  ingressClassName: avi-lb # AKO 배포 시, 기본 ignressclass는 avi-lb로 정의됨.
  rules:
    # 요청하신 FQDN 도메인을 기입합니다.
    - host: gslb-a.app.vcf.local 
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                # 위에서 ClusterIP로 수정한 서비스 이름을 매핑합니다.
                name: guestbook-frontend 
                port:
                  number: 80

```

Create additional IngressClass

```yaml
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  annotations:
    ingressclass.kubernetes.io/is-default-class: "false"
  name: avi-lb-second # 추가 ingressClass name 정의
spec:
  controller: ako.vmware.com/avi-lb
  parameters:
    apiGroup: ako.vmware.com
    kind: AviInfraSetting
    name: "vip-infrasetting" # aviinfrasetting으로 생성한 이름 정의
```

output: ingressclass 추가 생성됨.

```yaml
viadmin@HCSVDI-28:~/guestbook$ kubectl get ingressclass
NAME            CONTROLLER              PARAMETERS                                        AGE
avi-lb          ako.vmware.com/avi-lb   <none>                                            50s
avi-lb-second   ako.vmware.com/avi-lb   AviInfraSetting.ako.vmware.com/vip-infrasetting   15m
```

Second ingress 생성

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: guestbook-ingress-second
  namespace: guestbook
spec:
  # AKO 컨트롤러가 감지할 수 있도록 인그레스 클래스를 필수 지정합니다.
  ingressClassName: avi-lb-second
  rules:
    # 요청하신 FQDN 도메인을 기입합니다.
    - host: gslb-b.app.vcf.local 
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                # 위에서 ClusterIP로 수정한 서비스 이름을 매핑합니다.
                name: guestbook-frontend 
                port:
                  number: 80

```

Output: Ingress service in k8s namespace

```yaml
viadmin@HCSVDI-28:~/guestbook$ kubectl get ingress -n guestbook
NAME                       CLASS           HOSTS                  ADDRESS         PORTS   AGE
guestbook-ingress-first    avi-lb          gslb-a.app.vcf.local   172.20.10.201   80      8s
guestbook-ingress-second   avi-lb-second   gslb-b.app.vcf.local   172.19.20.201   80      26s
```
