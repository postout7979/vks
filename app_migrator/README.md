# VKS YAML Migrator

퍼블릭 클라우드(EKS / AKS / GKE / OpenShift)에서 export한 Kubernetes 매니페스트를 온프레미스 **VCF 9.1 VKS** 환경용으로 변환하는 단일 HTML 도구입니다.

- 설치/서버 불필요: `vks-yaml-migrator.html` 을 브라우저에서 열기만 하면 됩니다.
- 모든 처리는 브라우저 안에서 수행되며 외부로 전송되지 않습니다 (폐쇄망/오프라인 동작, 외부 CDN 없음).
- **여러 개의 소스 YAML을 동시에 업로드**하고, 소스별로 분리해서 분석 결과를 확인한 뒤 **개별 또는 전체 export** 할 수 있습니다.

## 3단계 워크플로

### 0. 사전 준비: 소스 YAML 수집

도구에 넣을 소스 YAML 은 **소스 클러스터(EKS / AKS / GKE / OpenShift)에서 `kubectl get -o yaml` 로 export** 한 파일입니다. **네임스페이스(또는 앱) 단위로 파일 1개**씩 만들면, 도구에서 소스별로 구분해서 분석하고 개별 export 할 수 있습니다.

#### 수집 대상 리소스와 도구에서 쓰는 정보

| 리소스 | 수집되는 정보 (소스 YAML 에 들어가는 내용) | 도구가 하는 일 |
|---|---|---|
| Deployment / StatefulSet / DaemonSet / CronJob / Job | 컨테이너 `image`, `nodeSelector`, `annotations`, `securityContext`, volumes, replicas, strategy, apiVersion | 이미지 경로를 Harbor 로 변경, 클라우드 annotation / nodeSelector 제거, deprecated API 변환 |
| Service | `type`, `loadBalancerIP`, 클라우드 LB annotation(`aws-load-balancer-*`, `azure-load-balancer-*`) | annotation 제거, LoadBalancer(NSX/Avi) 검토 경고 |
| Ingress (OpenShift: Route) | host, path, backend, TLS, ingress class / `alb.*` / `appgw.*` annotation | `networking.k8s.io/v1` 변환, Route → Ingress 변환, ingress class 검토 경고 |
| PersistentVolumeClaim | `storageClassName`, `accessModes`, 요청 용량 | StorageClass 를 vSAN 으로 매핑, RWX 경고 |
| ConfigMap / Secret | 이름, 키, 값 (값은 그대로 복사) | ConfigMap 안의 클라우드 참조 문자열 경고, Secret 재생성 안내 |
| ServiceAccount | IRSA / Workload Identity annotation, `imagePullSecrets` | 클라우드 IAM annotation 제거 |
| HPA / PodDisruptionBudget / NetworkPolicy / Role / RoleBinding | 스펙 전체 | `autoscaling/v2`, `policy/v1` 등 GA API 로 변환 |
| Namespace (OpenShift: Project) | 이름, label | Namespace 로 변환 |
| (OpenShift) DeploymentConfig | 스펙 전체, triggers, strategy | `Deployment` 로 변환 |

`status`, `uid`, `resourceVersion`, `managedFields`, `clusterIP` 같은 서버 생성 필드와 Pod / ReplicaSet / Endpoints / Event 는 YAML 에 섞여 있어도 도구가 자동으로 제거하므로 따로 걸러낼 필요가 없습니다.

#### 단일 네임스페이스 export (Kubernetes: EKS / AKS / GKE)

```bash
kubectl config use-context <source-cluster-context>
NS=production
RES=deployments,statefulsets,daemonsets,cronjobs,jobs,services,ingress,configmaps,secrets,persistentvolumeclaims,serviceaccounts,poddisruptionbudgets,horizontalpodautoscalers,networkpolicies,roles,rolebindings

{ kubectl get namespace "$NS" -o yaml; echo '---'; kubectl get "$RES" -n "$NS" -o yaml; } > "$NS.yaml"
```

간단하게 시작하려면 `kubectl get all,cm,secret,pvc,ingress,sa,pdb,hpa -n <ns> -o yaml > <ns>.yaml` 도 사용할 수 있습니다. 다만 `all` 에는 Pod / ReplicaSet 이 포함되고 NetworkPolicy, Role, RoleBinding 은 빠집니다.

#### 여러 네임스페이스를 한 번에 (네임스페이스별 파일 1개)

```bash
mkdir -p export
for NS in production staging payments; do
  { kubectl get namespace "$NS" -o yaml; echo '---'; kubectl get "$RES" -n "$NS" -o yaml; } > "export/$NS.yaml"
done
```

만들어진 `export/` 폴더를 도구의 **Select folder…** 로 한 번에 올리면 파일마다 하나의 소스가 됩니다.

#### OpenShift export

```bash
oc login <source-cluster>
NS=production
RES=deployments,statefulsets,daemonsets,cronjobs,jobs,services,configmaps,secrets,persistentvolumeclaims,serviceaccounts,poddisruptionbudgets,horizontalpodautoscalers,networkpolicies,roles,rolebindings

{ oc get project "$NS" -o yaml; echo '---'; oc get deploymentconfigs,routes,"$RES" -n "$NS" -o yaml; } > "$NS.yaml"
```

`ImageStream` / `BuildConfig` 는 VKS 에 대응 리소스가 없어 도구가 제외하므로 export 하지 않아도 됩니다. DeploymentConfig 가 참조하는 이미지는 YAML 의 `image` 필드(이미 resolve 된 값)에서 읽습니다.

#### 추가로 확인하면 좋은 정보 (YAML 에 넣을 필요는 없음)

```bash
# 사용 중인 이미지 전체 목록 → 마이그레이션 전에 Harbor 로 미러링할 대상 사전 점검
kubectl get pods -n "$NS" -o jsonpath='{range .items[*]}{range .spec.initContainers[*]}{.image}{"\n"}{end}{range .spec.containers[*]}{.image}{"\n"}{end}{end}' | sort -u

# PVC 의 StorageClass / 용량 / 접근 모드 → StorageClass 매핑표(gp3=vsan-default-storage-policy 등) 작성용
kubectl get pvc -n "$NS"
kubectl get storageclass

# 사용 중인 Ingress class → 설정의 "Ingress class name" 결정용
kubectl get ingressclass

# 네임스페이스에 어떤 리소스 종류가 있는지 확인 (CRD / 커스텀 리소스 누락 점검)
for r in $(kubectl api-resources --verbs=list --namespaced -o name); do
  kubectl get "$r" -n "$NS" --ignore-not-found -o name 2>/dev/null
done
```

#### 수집 시 주의사항

- **Secret 에는 민감한 값(base64)이 그대로 들어갑니다.** export 파일은 안전하게 보관하고 작업 후 삭제하세요. Secret 을 YAML 로 옮기지 않고 Vault / External Secrets 로 재구성하려면 `RES` 목록에서 `secrets` 를 빼면 됩니다.
- **CRD / 커스텀 리소스**(cert-manager, Istio, Operator 등)는 위 목록에 없습니다. 도구는 이들을 검증하지 않으므로 필요한 것만 별도로 export 하고 결과를 직접 검토하세요.
- **Helm 으로 배포한 앱**은 `helm get manifest <release> -n <ns> > <release>.yaml` 로 렌더링된 매니페스트를 받아도 됩니다. Helm release Secret 은 도구가 자동 제외합니다.
- `kubectl get` 은 서버가 제공하는 최신 API 버전으로 출력하므로, deprecated API(`extensions/v1beta1` 등)는 오래된 클러스터나 저장해 둔 YAML 에서만 나타납니다.
- **데이터는 YAML 로 옮겨지지 않습니다.** PV 의 데이터(Velero 등), 클라우드 관리형 서비스(RDS, S3, Azure SQL 등), 애플리케이션 코드 안의 SDK 호출은 별도로 마이그레이션해야 합니다.
- 클러스터 범위 리소스(ClusterRole, ClusterRoleBinding, StorageClass, PersistentVolume, IngressClass)는 대상 클러스터에서 새로 구성하는 것을 권장하며, 위 export 에는 포함하지 않습니다.

### 1. Sources & settings
- YAML 파일을 드래그&드롭 / **Select files…** / **Select folder…** 로 여러 개 추가합니다. 각 파일은 하나의 "소스"로 유지됩니다.
- 붙여넣기 영역에 이름을 지정해 소스를 추가할 수도 있습니다. 같은 이름은 자동으로 `name (2).yaml` 처럼 구분됩니다.
- 소스별로 감지된 플랫폼 배지(EKS / AKS / GKE / OCP)가 표시됩니다. **Load samples** 는 EKS / AKS / OpenShift 샘플 3개를 한 번에 불러옵니다.
- 왼쪽에서 Harbor FQDN / Project, 정리 규칙, 대상 Namespace / StorageClass, VKS `kubectl context`, OpenShift 변환(Ingress controller / class) 을 설정합니다. (설정은 브라우저에 저장)
- **Run analysis** 를 누르면 모든 소스를 각각 분석합니다. 소스나 설정을 바꾸면 다시 분석해야 합니다.

### 2. Analysis (소스별 가시성)
- 왼쪽 목록: **All sources** + 소스별 카드. 카드 왼쪽 색상은 상태(초록=정상, 노랑=검토 필요, 빨강=오류)이고, 체크박스로 export 포함 여부를 정합니다.
- **All sources** 보기
  - *Summary*: 소스별 리소스 수, 삭제 수, 이미지/annotation/API 변경 수, 경고/오류 수 비교표 (행 클릭 → 해당 소스로 이동)
  - *Review items*: 전체 소스의 검토 필요 항목 모음 (소스 이름 클릭 → 해당 소스의 Changes)
  - *Images*: 이미지 매핑과 사용된 소스 목록
- **개별 소스** 보기
  - *Resources*: 리소스 인벤토리 (Kind / Name / Namespace / 원본 apiVersion / 결과 DROPPED·CREATED·CHANGED·REVIEW·OK). Route 에서 생성된 TLS Secret 은 CREATED 로 표시됩니다. 행 클릭 → 해당 리소스의 변경 내역만 필터링
  - *Changes*: 변경(FIXED) / 경고(WARN) / 정보(INFO) 목록, 필터와 검색
  - *Diff*: 원본 대비 변환 결과 (추가/삭제 라인 강조)
  - *Output YAML*: 변환 결과, 복사 / 다운로드
  - *Images*: 해당 소스의 이미지 매핑

### 3. Export (VKS 클러스터 기준)
- 소스별 **⬇ YAML**(변환 파일 1개) / **⬇ ZIP**(해당 소스만 담은 번들) 버튼으로 개별 export
- **Export selected (ZIP)** : 체크한 소스만 한 번에 export
- **Export all sources (ZIP)** : 전체 소스를 한 번에 export
- **Selected as one combined YAML** : 선택한 소스를 하나의 YAML 로 합쳐서 다운로드

ZIP 구성:

```
manifests/<source>.vks.yaml     소스별 변환 결과 (소스 파일명 1:1)
reports/summary.md              전체 요약 (여러 소스일 때)
reports/<source>.report.md      소스별 변경/검토 리포트
images/image-map.csv            원본 → Harbor 이미지 매핑 (소스 간 중복 제거)
images/image-mirror.sh          skopeo 기반 이미지 미러링 스크립트
apply.sh                        VKS 클러스터에 적용 (dry-run / apply)
README.txt
```

적용 순서:

```bash
bash images/image-mirror.sh     # Harbor 로 이미지 미러링 (skopeo + 레지스트리 로그인 필요)
bash apply.sh dry-run           # kubectl apply --dry-run=server
bash apply.sh apply             # 실제 적용
```

`apply.sh` 는 설정한 `kubectl context` 를 사용합니다 (비우면 현재 context). 네임스페이스가 없으면 server dry-run 이 실패하므로 Namespace 매니페스트를 먼저 적용하세요.

## 변환 규칙 (기본값)

### 1. Image registry 경로 변경
| 원본 | 변환 결과 (project=`migration`) |
|---|---|
| `123456789012.dkr.ecr.ap-northeast-2.amazonaws.com/team/web:1.4.2` | `harbor.corp.local/migration/team/web:1.4.2` |
| `myacr.azurecr.io/backend/api:v2` | `harbor.corp.local/migration/backend/api:v2` |
| `gcr.io/google-containers/pause:3.2` | `harbor.corp.local/migration/google-containers/pause:3.2` |
| `nginx:1.25` (Docker Hub 암묵 경로) | `harbor.corp.local/migration/library/nginx:1.25` |

- `containers`, `initContainers`, `ephemeralContainers`, CronJob 템플릿 등 모든 `image:` 필드가 대상입니다. tag / digest 는 유지됩니다.
- 경로 방식: 전체 경로 유지 또는 이미지 이름만 사용(flatten). 레지스트리별 매핑(`*.dkr.ecr.*.amazonaws.com => harbor.corp.local/ecr-mirror`)과 제외 목록(`registry.k8s.io`) 지원.
- ConfigMap 등 문자열 블록 안의 텍스트는 변경하지 않고, 남은 클라우드 참조로 경고만 합니다.

### 2. 퍼블릭 클라우드 전용 annotation 제거
`eks.amazonaws.com/*`, `service.beta.kubernetes.io/aws-*`, `alb.ingress.kubernetes.io/*`, `service.beta.kubernetes.io/azure-*`, `azure.workload.identity/*`, `appgw.ingress.kubernetes.io/*`, `cloud.google.com/*`, `iam.gke.io/*`, `openshift.io/*`, `kubectl.kubernetes.io/last-applied-configuration`, `pv.kubernetes.io/*` 등. 규칙은 화면에서 편집할 수 있습니다 (`*` 와일드카드, `key =~ 정규식`).

### 3. 더 이상 필요 없는 / 제거된 API
| 원본 | 변환 |
|---|---|
| `extensions/v1beta1`, `networking.k8s.io/v1beta1` Ingress | `networking.k8s.io/v1` (`serviceName/servicePort` → `service.name/port`, `pathType` 추가, `backend` → `defaultBackend`) |
| `extensions/v1beta1`, `apps/v1beta*` Deployment 등 | `apps/v1` |
| `batch/v1beta1` CronJob | `batch/v1` |
| `policy/v1beta1` PodDisruptionBudget | `policy/v1` |
| `autoscaling/v2beta1` HPA | `autoscaling/v2` (`targetAverageUtilization` → `target.type/averageUtilization`) |
| RBAC / Storage / PriorityClass 등 beta | GA 버전 |

CRD, Webhook, CSR 은 스키마가 달라 경고만 표시합니다.

### 4. 그 외 정리
- 서버가 채우는 필드 제거: `status`, `uid`, `resourceVersion`, `managedFields`, `clusterIP(s)`, PVC `volumeName` 등
- 클라우드 `nodeSelector` 라벨 제거 (`eks.amazonaws.com/*`, `kubernetes.azure.com/*`, `agentpool` 등)
- 이식 불가 / 자동 생성 리소스 제외: `PodSecurityPolicy`, `PersistentVolume`, `StorageClass`, `Endpoints`, ownerReferences 가 있는 Pod, SA token Secret 등
- (옵션) 대상 Namespace 일괄 변경, StorageClass 일괄/매핑 변경 (`gp3=vsan-default-storage-policy`)

### 5. 검토 필요 항목 (자동 변환하지 않고 경고)
Secret, `LoadBalancer`(NSX/Avi), `loadBalancerIP`, `ReadWriteMany` PVC, `kubernetes.io/ingress.class` 제거 후 `ingressClassName` 지정, `hostPath`, `privileged`, `hostNetwork`, 변환 후에도 남은 클라우드 참조 문자열 (`amazonaws.com`, `azurecr.io` 등), OpenShift 변환 시 남는 항목(위 OpenShift 절 참고).

## OpenShift → VKS 전환

설정의 **4 · OpenShift conversion** 에서 켜고 끌 수 있습니다 (기본 ON). VKS 에서 사용할 Ingress controller(Generic·Avi AKO / NGINX / Contour)와 `ingressClassName` 을 지정하면 Route 변환에 반영됩니다.

| OpenShift | 변환 결과 |
|---|---|
| `Project` (project.openshift.io) | `Namespace` (`spec`/`status` 제거) |
| `DeploymentConfig` (apps.openshift.io) | `Deployment` (`apps/v1`). `selector` 맵 → `selector.matchLabels` (없으면 template label 에서 생성), `strategy` Rolling/Recreate 매핑(`maxSurge`/`maxUnavailable` 유지), `triggers`/`test` 제거 |
| `Route` (route.openshift.io) | `Ingress` (`networking.k8s.io/v1`): host / path / backend Service·port / `ingressClassName` / TLS. `edge`·`reencrypt` 의 inline 인증서·키는 `kubernetes.io/tls` **Secret 을 자동 생성**(CA 는 체인에 추가) |
| `ImageStream`, `BuildConfig`, `Build`, `SecurityContextConstraints` | 제외 (VKS 에 대응 리소스 없음) |
| `builder`/`deployer` ServiceAccount, `system:image-*` RoleBinding, `*-dockercfg-*` Secret, `openshift-service-ca.crt` | 자동 생성 리소스로 제외 |
| ServiceAccount `imagePullSecrets` 의 `*-dockercfg-*` | 제거 |
| Pod/컨테이너 `securityContext.seLinuxOptions` | 제거 |
| 내부 레지스트리 `image-registry.openshift-image-registry.svc:5000/...`, `registry.redhat.io`, `quay.io` | Harbor FQDN 경로로 변경 (이미지 매핑 + 미러 스크립트에 포함) |

Route annotation 매핑 (자동 변환, 나머지는 검토 항목으로 표시):

| Route annotation | NGINX | Contour |
|---|---|---|
| `haproxy.router.openshift.io/timeout` | `proxy-read-timeout`, `proxy-send-timeout` (초) | `projectcontour.io/response-timeout` |
| `haproxy.router.openshift.io/ip_whitelist` | `whitelist-source-range` | (검토 항목) |
| `haproxy.router.openshift.io/rewrite-target` | `rewrite-target` | (검토 항목) |
| `tls.insecureEdgeTerminationPolicy: Redirect/Allow` | `ssl-redirect` true/false | `ingress.kubernetes.io/force-ssl-redirect` (Redirect) |
| `tls.termination: passthrough` | `ssl-passthrough` (controller 옵션 필요) | (검토 항목: HTTPProxy 필요) |
| `tls.termination: reencrypt` | `backend-protocol: HTTPS` | (검토 항목) |

자동 변환하지 않고 **경고**로 표시하는 항목: `alternateBackends`(가중치 분산), wildcard host, re-encrypt 의 backend CA, Route 의 pod `targetPort`(Ingress 는 Service port 필요), OpenShift apps 도메인 host, `service.beta.openshift.io/serving-cert-secret-name`(service CA → cert-manager 필요), `runAsUser` 가 SCC 범위(10자리 UID) 인 경우, 그 외 변환되지 않은 `*.openshift.io` 리소스(예: `Template`).

> 생성된 TLS Secret 에는 개인 키가 평문(`stringData`)으로 들어갑니다. 적용 전에 시크릿 저장소(Vault 등)로 옮기는 것을 권장합니다.

## 제한 사항

- JSON 입력은 지원하지 않습니다 (`-o yaml` 사용). 폴더 선택 시 `.yaml` / `.yml` / `.txt` 파일만 읽습니다.
- AKS Workload Identity 의 **label**(`azure.workload.identity/use`)은 annotation 이 아니라서 제거되지 않습니다. 필요하면 수동 삭제하세요.
- 애플리케이션 코드 내부의 AWS/Azure SDK 호출은 감지하지 못합니다.
- 들여쓰기 기반으로 텍스트를 직접 수정하므로 주석/순서/따옴표는 보존되지만, 비정상적인 flow-style(`{a: b}`) YAML 은 일부 규칙이 적용되지 않을 수 있습니다.
- CRD / Operator 리소스는 검토가 필요합니다. 적용 전 `--dry-run=server` 검증은 필수입니다.
