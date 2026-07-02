![](images/f78e004fa07154ae2b7527d74e5bfac06cb03c033541ff9f06603c7c51533889.jpg)

# HOL-2702-01-V CF-L

# 목차

VCF 9.1의 필수 업데이트 및 기능: Hands-On with Kubernetes (HOL-2702-01-VCF-L) 4

랩 안내 .. 5

핸즈온 랩을 처음 사용하시나요? . 7

모듈 1 - VMware vSphere 쿠버네티스 서비스(VKS), VM 서비스, 컨테이너의 새로운 기능VCF 9.1의 서비스 및 슈퍼바이저 서비스 (30분) 초급 9

모듈 소개 .. 10

VCF 9.1의 vSphere 쿠버네티스 서비스 신규 기능 12

VM 서비스 개선사항 .. 21

컨테이너 서비스 . 27

vSphere 슈퍼바이저 개선사항 28

결론 . 32

모듈 2 - VMware vSphere 쿠버네티스 서비스(VKS) 클러스터 생성 및 신규 기능 (45분) 중급 .... 33

모듈 소개 .. 34

VKS 클러스터 생성 35

다중 네트워크 지원 . 52

외부 애플리케이션으로서의 LCI . 58

모듈 결론 . 66

모듈 3 - VM 서비스 신규 기능 및 운영 (45 분) 중급 67

모듈 소개 ... 68

Canonical 구독 . 69

VM 빠른 배포 v9.1 . 84

대량 작업을 위한 VM 그룹화 . 97

UI를 사용하여 VM의 스냅샷 생성 119

네트워크 가변성 . 137

모듈 결론 . 147

모듈 4 - 새로운 컨테이너 서비스 (15분) 중급 . 148

모듈 소개 .. 149

컨테이너 서비스 소개 .. 150

모듈 결론 . 185

# 쿠버네티스 핸즈온:

# VCF 9.1의 필수 업데이트 및

# 기능

# (HOL-2702-01-VCF-L)

HOL-2702-01-VCF-L

페이지 4

# 랩 안내

VMware Cloud Foundation 9.1에서 vSphere Kubernetes Service (VKS), VM 서비스, 컨테이너서비스 및 슈퍼바이저에서 도입된 향상된 기능을 탐색합니다. 네 개의 집중 모듈을 통해 참가자들은 이러한서비스 전반에 걸친 최신 개선 사항을 발견하고 실제 환경에서 Kubernetes 워크로드를 배포하고관리하는 실무 경험을 얻습니다.

모듈 1은 VKS, VM 서비스, 컨테이너 서비스 및 슈퍼바이저 전반에 걸쳐 새로운 내용에 대한 명확한 개요를제공하여 참가자들이 이후의 모든 연습에서 최대한의 효과를 얻을 수 있도록 합니다. 모듈 2부터 4까지는개념에서 실습으로 이동하며, 참가자들이 각 서비스의 클러스터, 가상 머신 및 컨테이너를 배포하는과정을 안내하고, 각각의 이틀째 운영을 탐색합니다.

이 랩이 끝날 때쯤, 참가자들은 VMware Cloud Foundation 9.1이 현대 애플리케이션 플랫폼공간에서 제공하는 것에 대한 확고한 이해를 갖게 되며, 통합 UI 및 API를 통해 Kubernetes 클러스터,VM 및 컨테이너를 배포, 구성 및 관리할 수 있는 자신감을 얻게 됩니다.

전제 조건: Kubernetes 개념 및 VMware vSphere 인프라에 대한 기본적인 이해.

<table><tr><td>모듈</td><td>제목</td><td>시간</td><td>수준</td></tr><tr><td>1</td><td>VCF 9.1에서 VMware vSphere 쿠버네티스 서비스(VKS) 및슈퍼바이저 서비스의 새로운 기능</td><td>30분</td><td>초급</td></tr><tr><td>2</td><td>VMware vSphere 쿠버네티스 서비스(VKS) 클러스터 생성및 신규 기능</td><td>45분</td><td>중급</td></tr><tr><td>3</td><td>VM 서비스 - 새로운 기능 및 운영</td><td>45분</td><td>중급</td></tr><tr><td>4</td><td>새로운 컨테이너 서비스</td><td>15분</td><td>초급</td></tr></table>

모듈의 길이는 15, 30, 45 또는 60분일 수 있습니다. 모듈 수준은 초급, 중급 또는 고급일 수 있습니다.

랩 저자:

HOL-2702-01-VCF-L

페이지 5

• 모듈 1 -

케빈 브래디, 수석/수석 아키텍트-파트너, 미국

랜디 카슨, 대위/직원 기술 채택 관리자, 미국

• 모듈 2 -

어니스트 니콜스, 캡틴/클라이언트 서비스 컨설턴트, 미국

랜디 카슨, 캡틴/직원 기술 채택 관리자, 미국 마이클 플라이셔, 캡틴/선임

직원 솔루션 아키텍트, 미국

• 모듈 3 -

더그 피오레 , 캡틴/솔루션 아키텍트, 미국

랜디 카슨, 캡틴/직원 기술 채택 관리자, 미국 마이클 플라이셔, 캡틴/선임

직원 솔루션 아키텍트, 미국

• 모듈 4 -

랜디 카슨, 캡틴/직원 기술 채택 관리자, 미국 케빈 브래디, 수석/최고

아키텍트-파트너, 미국

조니 자그루, 캡틴/파트너 솔루션 아키텍트, 캐나다

랩 책임자:

• 케빈 브래디 , 수석/최고 아키텍트-파트너, 미국

HOL-2702-01-VCF-L

페이지 6

# 핸즈온 랩을 처음 사용하시나요?

![](images/562395c42fbc86df084e52ed82ffedbae1be16f31d026d502f76aa1c9ee045b5.jpg)

랩 콘솔에 녹색 '준비 완료' 상태가 표시되면 시작 루틴이 완료됩니다.업데이트가 완료될 때까지 기다려 주십시오. 상태가 '준비 완료'로 변경되지 않으면5분 이내에 도움을 요청하십시오.

 신규 사용자: 랩을 시작하기 전에 VMware Lab Platform 인터페이스를 검토하십시오.여기에는 콘솔에 복사/붙여넣기 및 기타 사용자 인터페이스 질문에 대한 도움이 포함됩니다.

HOL-2702-01-VCF-L

페이지 7

# 텍스트 드래그 앤 드롭

![](images/a73440697472306d67fd8e20e35d28f239ee27846877aaaca778599618aa63ad.jpg)

# Click to enlarge

1.At the Login Method dropdown,select Local Account.
2. At the username field, type admin,
3.At the password field, type
4. Click LOG IN.

![](images/5eb1045770dad815a7b7dd2b2e6843d89bfef50e7f4e9fa1cadec59f729e9ab0.jpg)

![](images/4fd04d37e0ef6c3004ffe9369dfe6341db741255db12d69879496e4d1b148fd8.jpg)

Hil How may I help you?

![](images/18363565b0d36ad2c2308cd79512be257cf5ca159598d7142bcd895a6208e090.jpg)

필요한 텍스트를 매뉴얼에서 랩 콘솔로 직접 드래그 앤 드롭하여 콘솔에 텍스트를 입력하는 시간을절약하십시오.

HOL-2702-01-VCF-L

페이지 8

# 모듈 1 - VCF 9.1에서VMware vSphereKubernetes 서비스(VKS),VM 서비스, 컨테이너서비스 및 슈퍼바이저 서비스의새로운 기능 (30분) 초급

HOL-2702-01-VCF-L

9페이지

# 모듈 소개

이 모듈은 모두 읽기입니다. 실험실과 상호작용할 단계는 없습니다. 이 모듈은 VCF 9.1에서 도입하는 새로운기능을 소개합니다. 이러한 새로운 기능은 모듈 2, 3 및 4에서 상호작용할 수 있습니다.

VMware vSphere Kubernetes Service를 사용하여 VCF 9.1에서 현대 애플리케이션을더 빠르게 배포하고, 더 스마트하게 확장하며, TCO를 낮추세요.

많은 조직에서 Kubernetes 채택은 기술적 이니셔티브로 시작되었지만, 이를 신뢰할 수 있는 기업급플랫폼으로 확장하는 것은 예상보다 훨씬 더 어려운 경우가 많았습니다.혁신으로 시작된 것이 빠르게 복잡해졌습니다.

![](images/4e59328406b18b76f3934ba7eff0a7b5c66e060d3669da4ccda715c5a764f2d3.jpg)

그림 1: VKS는 모든 호환되는 타사 서비스와 함께 포괄적인 클라우드 서비스 세트를 제공합니다.

현대 애플리케이션을 채택하는 것을 살펴보면, 그 이점이 매력적이라는 것은 의심의 여지가 없습니다 - 더 빠른혁신, 확장성 및 민첩성. 그러나 현대 애플리케이션 채택에는 여러 가지 도전 과제가 있습니다.

첫째, 인프라 복잡성과 사일로 - 많은 조직이 하이브리드 환경, 레거시 시스템 및 여러 클라우드플랫폼을 조율하고 있습니다. 이는 도구와 팀이 분리되어 속도 있게 운영하기 어렵게 만듭니다.

HOL-2702-01-VCF-L

10페이지

그 다음으로는 기술 복잡성과 기술 격차 가 있습니다. 기술이 빠르게 발전함에 따라, 쿠버네티스, DevOps클라우드 네이티브 개발에 대한 전문 지식을 가진 인재를 찾고 유지하는 것이 어렵습니다.

보안 및 규정 준수는 또 다른 주요 관심사입니다. 분산 애플리케이션과 더 빠른 릴리스 주기로 인해 안전하고규정을 준수하는 환경을 유지하는 것이 그 어느 때보다 중요하고 복잡해졌습니다.

또한 도구의 확산이 문제로 떠오르고 있습니다. 서로 다른 팀이 유사한 문제에 대해 서로 다른 도구를 채택하여중복되거나 겹치거나 잘 통합되지 않은 솔루션이 발생합니다. 이는 비용을 증가시킬 뿐만 아니라 운영 마찰을증가시킵니다.

마지막으로 레거시 통합은 종종 장애물이 됩니다. 현대 애플리케이션은 기존 시스템과 연결해야 합니다. 고객은통합 문제를 해결하기 위해 올바른 전략과 기술을 선택해야 합니다.

HOL-2702-01-VCF-L

페이지 11

# VCF 9.1의 vSphere 쿠버네티스 서비스 신규 기능

# What's New With Kubernetes in VCF 9.1

![](images/585c58e4fbf6c6c89289bc85e0f64b66c2e37ddc59e71b98de132dbc9dd7386c.jpg)

![](images/e91fd9f179f778201f24341397c5f2ce2df9417c1a8c807aa0d821a9dffb8d68.jpg)

![](images/7227d899523b03cac4c89c9f215c17fd78faf8fb3e9a57a9eb3aec24e13b7ec6.jpg)

![](images/870e9eb21239cde5bc9d08e07166fc6bc4e3e6c80600aa45d78f7c3ca61d27c6.jpg)

![](images/550fc084416d1562e989279a510085b6973f07d0fe0b275acb5af2b5affc2fa0.jpg)

VKS 3.6 Improvements

VM Service Improvements

Container Service

Content distribution

Supervisor Improvements

Kubernetes 1.35

Through Fleet

DTGW Support

Container

Depot and

Faster Deploy and Upgrades

Improved Day 2

Multi-cluster

Instances via

regional Harbor

Operations

Zones

vSphere Pods

BYO CNI

Network mutability

Scale up to

25000 VMs and

Multi-NIC Support

Non-disruptive

500VKS

Import

BYOI RHEL

clusters

vmware

Eroadoom Proprietery end Confidentiel. Copyright @ 202e Broadeom.

by Broadcom

AlIRights Reseved.Theterm"Broadoomrefers to BroadcomIno. and/orits subsidiarles.

VCF 9.1의 새로운 기능은 작업 도메인 생성 과정에서 슈퍼바이저 서비스를 활성화할 수 있는 기능입니다. 이옵션은 슈퍼바이저를 배포하는 의견이 반영된 방법을 제공하며 고객의 최소한의 입력에 의존합니다. 이 배포모델은 드롭다운 메뉴에서 선택할 수 있는 NSX 프로젝트와 VPC를 활용합니다. 이 옵션을 선택하면 작업도메인이 생성된 후 NSX 엣지 배포를 완료해야 합니다.

HOL-2702-01-VCF-L

페이지 12

# VKS 3.6 개선 사항

# VKS 3.6 brings the latest CNCF certified Kubernetes release

Kubernetes 1.35 with 24 months of support

![](images/87e40262df9d4883629e2c2d9e4e1c9822110992bd2d2a7ebdce9f16b4903652.jpg)

Support for CNCF-certified, upstreamalignedKubernetes version 1.35

24 months of Enterprise support

![](images/a063572d1d627094603cae01057d17d819f704ee5d0863719f71641553063ee9.jpg)

Upstream Aligned

CNCF Certified

# Upstream Capabilities in v1.35

# NotableDeprecations in v1.35

24 months support to run workloads on a single Kubernetes version

![](images/683e29915515a20031b04cd4c550358a8b0ae1eb8f1ed335118e6f7cf315f42f.jpg)

Supportfor In-Place updateof Pod Resourcespod estarts

Ocgroupsv1-Allnode images shipped as part of VKSarealready oncgroupsv2

![](images/6fbfca88d92b1c8656641ac6b45722c1e9a11a6a571cd7c449c1f127e92e06a4.jpg)

OCl images as first class VolumeSource

# vmware'

Eroedcom Proprietery end Confidentiel. Copyrigh1 @ 2020 Broedoom. AllRightsReseed.he temrocomers toroaoomIn.ndor tssuides

by Broadcom

VMware는 CNCF Kubernetes 릴리스와 발맞추어 나가겠다는 약속을 지키고 있습니다. VKS 3.6은Kubernetes 버전 1.35의 공식 릴리스 후 단 8주 만에 출시되었으며, 릴리스 날짜로부터 24개월의 지원이포함되어 있습니다. 이 릴리스는 cgroup v2 사용을 표준화했습니다. cgroup v2로의 전환은 단순한"업데이트"가 아니라 커널이 프로세스 격리를 처리하는 방식의 완전한 재설계입니다. 고객에게 또 다른 큰이점은 인플레이스 포드 업데이트입니다. 이전 버전에서는 사용 중인 리소스를 변경하려면 포드를 재생성해야했습니다. 이제는 포드를 재시작하지 않고도 CPU 및/또는 메모리를 증가시킬 수 있습니다.

HOL-2702-01-VCF-L

페이지 13

# 확장성 향상

![](images/61e1419d2754dc1a30c86e27076131e4cd5641e50637e58935ca662bf040569c.jpg)

| Cluster | Value |
|---------|-------|
| Kubernetes Cluster 1 | 190 |
| Kubernetes Cluster 2 | 190 |
| Kubernetes Cluster 3 | 190 |
| Kubernetes Cluster 4 | 190 |
| Kubernetes Cluster 5 | 190 |
| Kubernetes Cluster 6 | 190 |
| Kubernetes Cluster 7 | 190 |
| Kubernetes Cluster 8 | 190 |
| Kubernetes Cluster 9 | 190 |
| Kubernetes Cluster 10 | 190 |
| Kubernetes Cluster 11 | 190 |
| Kubernetes Cluster 12 | 190 |
| Kubernetes Cluster 13 | 190 |
| Kubernetes Cluster 14 | 190 |
| Kubernetes Cluster 15 | 190 |
| Kubernetes Cluster 16 | 190 |
| Kubernetes Cluster 17 | 190 |
| Kubernetes Cluster 18 | 190 |
| Kubernetes Cluster 19 | 190 |
| Kubernetes Cluster 20 | 190 |
| Kubernetes Cluster 21 | 190 |
| Kubernetes Cluster 22 | 190 |
| Kubernetes Cluster 23 | 190 |
| Kubernetes Cluster 24 | 190 |
| Kubernetes Cluster 25 | 190 |
| Kubernetes Cluster 26 | 190 |
| Kubernetes Cluster 27 | 190 |
| Kubernetes Cluster 28 | 190 |
| Kubernetes Cluster 29 | 190 |
| Kubernetes Cluster 30 | 190 |
| Kubernetes Cluster 31 | 190 |
| Kubernetes Cluster 32 | 190 |
| Kubernetes Cluster 33 | 190 |
| Kubernetes Cluster 34 | 190 |
| Kubernetes Cluster 35 | 190 |
| Kubernetes Cluster 36 | 190 |
| Kubernetes Cluster 37 | 190 |
| Kubernetes Cluster 38 | 190 |
| Kubernetes Cluster 39 | 190 |
| Kubernetes Cluster 40 | 190 |
| Kubernetes Cluster 41 | 190 |
| Kubernetes Cluster 42 | 190 |
| Kubernetes Cluster 43 | 190 |
| Kubernetes Cluster 44 | 190 |
| Kubernetes Cluster 45 | 190 |
| Kubernetes Cluster 46 | 190 |
| Kubernetes Cluster 47 | 190 |
| Kubernetes Cluster 48 | 190 |
| Kubernetes Cluster 49 | 190 |
| Kubernetes Cluster 50 | 190 |
| VCF 9.0 | 190 |
| VCF 9.1 | 500 |

고객은 이제 감독자당 최대 500개의 VKS 클러스터로 확장할 수 있으며, 이는 9.0에서의 상당한 증가입니다.이 증가는 다음과 같은 이점을 제공합니다:

• vSphere Kubernetes 서비스에서 대규모 Kubernetes 배포를 위한 더 큰 확장성과 유연성
• 테스트된 차원에 기반한 한계 및 구성 옵션에 대한 명확하고 실행 가능한 안내.
• 대규모 환경에 대한 성능 보장을 통해 운영 신뢰성 향상.
• 환경이 정확히 지원할 수 있는 것을 아는 것으로 최적화된 자원 활용 및 비용 효율성 향상.

이 점프는 기업이 개발, 테스트, 스테이징을 포함한 여러 프로젝트와 여러 조직 내에서 필요할 수 있는 작업 부하격리를 위한 충분한 공간을 제공합니다.

중요한 점은 이 규모가 단일 감독자에서 지원되므로, 클러스터 규모가 부족해져서 새로운 감독자 클러스터를프로비저닝할 필요가 없는 단일 제어 평면의 이점을 누릴 수 있다는 것입니다.

이 스케일은 대규모 쿠버네티스 배포에 매우 유용합니다.

HOL-2702-01-VCF-L

14페이지

# VKS 클러스터를 위한 빠른 배포

Fast Deploy for VKS Clusters Accelerate Cluster Provisioning and Upgrades

![](images/0033c6c1498c2792ec9e6082a5055a7e40410df53c73a6d457949bf73b3db0f7.jpg)

| Category | Time to Deploy Clusters |
| -------- | ------------------------ |
| VCF 9.0  | 37 mins                  |
| VCF 9.1  | 11 mins                  |

![](images/29550a96669ee578e900edb5a790bfde1c695687528cf6d40510b536b702383d.jpg)

| Category | Time to Upgrade Clusters |
| -------- | ------------------------ |
| VCF 9.0  | 414 mins                 |
| VCF 9.1  | 103 mins                 |

# Testing parameters

Hardware: PowerEdge R650·Xeon Gold 6330 @ 2.00GHz·512GB RAM·vSAN NVMe (1.46TB cache,3.49TB
capacity)
Configuration:Zonal WCP(1Mgmt,2Workloadzones)with3CPVMs(medium),Ncking
VKS Clusters:3CPVM100 worker nodes

# vmware

Broadoom Proprietary and Confidential. Copyright @ 2026 Brosdoom. All Rights Reserved. The term *Broadcom refers to Broadcom Inc. snd/or its subsidiaries.

by Broadcom

빠른 배포는 갑작스러운 애플리케이션 작업 부하 급증 시 주요 이점이 될 수 있습니다. 예를 들어, 바쁜 쇼핑시즌 동안의 온라인 소매업체나 바쁜 쇼핑 시즌 동안의 꽃집이 있습니다. 직접 모드와 연결 모드 기술을활용하여 갑작스러운 수요 급증에 대응하고 프로덕션을 완벽하게 반영하는 스테이징 환경을 신속하게 구축할 수있습니다. 이는 관리자의 시간을 되돌려주고 개발자에게 민첩성을 되돌려주는 것입니다.

HOL-2702-01-VCF-L

15페이지

# VKS 다중 네트워크 지원

Unlock high demand workloads with VKS multi network support Multi-NIC Worker Node/ Pods for VKS Clusters

![](images/276a5e2c36a013446e0dfe20a7c2570ec93c928281ec3f8e963f3e9c4db26556.jpg)

vmware

Broadcom Proprietary and Confidential. Copyright @ 2026 Broadcom. AllRights Reserved. The term “Broadcomrefers to Broadcom Inc.and/or its subsidiaries

by Broadcom

역사적으로, Kubernetes는 모든 트래픽—클러스터 관리, API 호출 및 애플리케이션

데이터—를 단일 기본 네트워크 파이프를 통해 라우팅해왔습니다. 이는 표준 웹 애플리케이션에는 작동하지만, 미디어 스트리밍이나 대용량 데이터베이스와 같은 고수요서비스는 종종 성능 병목 현상에 직면하게 됩니다.

이 다중 네트워크 아키텍처는 귀하의 작업 부하에 대해 세 가지 막대한 이점을 제공합니다:

• 네이티브 멀티캐스트 지원: VKS 내에서 원-투-다수 라우팅에 의존하는 스트리밍 및 금융 피드를 네이티브로행할 수 있으며, 실시간 데이터에 대해 서브 밀리초 전달을 보장합니다.
• 트래픽 격리: 중요한 데이터 플레인을 제어 플레인과 물리적으로 분리할 수 있으며,시끄러운 이웃이 클러스터를 다운시키거나 관리 API에 영향을 미치지 않도록 보장합니다.성능.
• 직접 하드웨어 액세스: 가장 극단적인 성능 요구 사항—예를 들어 5G 패킷 처리를 위해—우리는SR-IOV를 지원합니다. 귀하의 포드는 소프트웨어 계층과 오버레이 캡슐화를 완전히 우회하여 물리적프라에 저지연, 선형 속도 연결을 달성할 수 있습니다.

궁극적으로, 우리는 가장 요구가 많은 작업 부하를 그들이 필요로 하는 정확한

네트워크 아키텍처와 결합할 수 있는 유연성을 제공합니다.

HOL-2702-01-VCF-L

16페이지

# VKS 비밀 주입 단순화

![](images/e748b6f71653b155510a91af9b9e99f65a39e536107f45af086d5539854fadb3.jpg)

vSphere 쿠버네티스 서비스(VKS)는 비밀 주입을 자동화하여 보안 작업을 간소화하고, VM과 Pod 모두에서일관되고 통일된 경험을 제공합니다.

보안은 매우 중요하지만 운영 복잡성의 대가로 이루어져서는 안 됩니다. VCF 9.1에서는 이를 완전히 간소화하고있습니다. 비밀 저장소 에이전트 주입기의 자동 생성을 도입했습니다. 이는 비밀 주입 워크플로우가 이제 모든슈퍼바이저 작업 부하에서 일관되게 이루어진다는 것을 의미합니다. Pod 사양에 주석을 사용하기만 하면시스템이 복잡한 작업을 처리합니다. 이는 단순히 시간을 절약할 뿐만 아니라 VM이나 컨테이너에서 실행되는모든 애플리케이션에 대해 감사 가능성과 일관성을 보장하여 보안 태세를 강화합니다.

HOL-2702-01-VCF-L

페이지 17

# 노드 OS에 대한 RHEL 지원

# RHEL now supported for node OS

VKS 3.6 expands your Node OS choices

# VKS Cluster Node OS Options

# Shipped Out of the Box

# Custom Node OS Images

![](images/b000a537c2cd4061e6e9b7a901c05dae511512e2060ab23d8c34a63e1dfc8fdd.jpg)

![](images/ebdd2681495dca75c6552f334e249163654ac647147f60df83b0e57b16f10298.jpg)

Microsoft Windows

Photon OS

Server 2022

Built-inEnterpriseSuportNodditionalicense

Requiresadditionallicensefromvendor

# New in VKS3.6

![](images/e3555d115b110bb39c46a346cb8dd11ca13436167a1ee27cdf89d9779a0c668f.jpg)

![](images/061081108c5ade360c810cc9a2c170d4d518d42739341326cb03ea11dffa159c.jpg)

Red Hat Enterprise

Canonical Ubuntu

Linux

Built-inEnterpriseSupport-NoAdditionalLicense

Requires additional license from vendor

# vmware

Broadoom Proprietary and Confidential. Copyright @ 2028 Broedoom.

by Broadcom

AllRightsReserved. The term"Broadoom”refers to Brosdoom Inc.and/orits subsidiaries

RHEL 9는 이제 VKS 노드의 OS로 지원됩니다. 시작하는 것은 쉽습니다. Red Hat 구독이 있는 고객은 vcfCLI와 통합된 “ImageBaker” 도구를 사용하여 이미지를 빌드하고, 해당 이미지를 콘텐츠 라이브러리에 추가한다음, UI와 CLI 모두에서 향후 클러스터 배포에 사용할 수 있습니다. 이미지 베이커 도구는 개선되었으며, 이제새로운 이미지를 생성하기 위해 라이브 VM이 필요하지 않으며 공기 차단 환경에서도 작동합니다.

HOL-2702-01-VCF-L

페이지 18

# TuneD 프로필을 통한 동적 노드 OS 구성

# Dynamic Node OS Configuration via TuneD Profiles

Profile Inheritance, Continuous Desired State and Nodepool level  granularity

![](images/08fc225e4838347a77526a8e33c1ae65ffca5115e396b186757011397d562351.jpg)

![](images/156bcd0115d97d4dc4d45e313a1d92cda0c82dbc18aa59091639351e2d2d7ed2.jpg)

![](images/5ef2c87516dd215362aa9a60e585a4d8689d7ebadc9684b80c532de0b76063b1.jpg)

FaaS TuneD Profile

Redis TuneD Profile

Elastic Search TuneDProfile

![](images/bbe44ac658bcd8065cb5abcbeca8734bc2d5a716654de306e6a0ab362e028ab2.jpg)

VKS Control Plane

nodeselector. nodepool-1

nodeselector. nodepool-2

nodeselector. nodepool-3

Linux Kernel (Redis TuneD ProfileA)

Linux Kermel (FaaS TuneD Profle)

Linux Kermel (Elastic TuneD Profile)

![](images/62df1d4d796653381a689bb86a7b00f508f704567bfdd2280fb07cd80f80f879.jpg)

![](images/214fde3cbcd414c250dca84ad1019c5c1bc3a62af7d0a7d651f5ca12256e74f9.jpg)

![](images/fe6fe44a3095f1db108a1c67a96cf35eaa1d9963eccc630d65636536d71435ce.jpg)

![](images/ce00c31b182226be1ec8704e91826bdc64e7725475957a01fef6e02d8dec7be6.jpg)

![](images/df8260656f57661b83bcfe255ac2c5031b669dd01b746624796332cccebedf82.jpg)

![](images/6292426d0d52ce57b383818cf9dfafb82ae5049290d0ec0ce56323b295a67c34.jpg)

![](images/7b5d5713067eb7aff63883d974e71f56b0cc8f178043582e5a25d6c458822f2b.jpg)

![](images/60b0dffa10462a99c371cfcc1ffc549167b0cc5dc75ce692a66bffa404b3fec8.jpg)

![](images/c0e3ce04b4e59c6ce7ae1d67376f2e0f84ada30bace55a2d48c61e3663c97a19.jpg)

vm.max_map_count=262144 fs.file-max=2097152 vm.swappiness=1

vm.swappiness=20 /sys/.../ksm/pages_to_scan=100 /sys/kernel/mm/ksm/run=1 Photon OS based Worker Node pool

vm.overcommit_memory=1 vm.swappiness=1

transparent_hugepages=never UbuntuOSbasedWorkerNodepoo

Photon OS based Worker Node pool

WorkerNode Pool 1

Worker Node Pool 2

Worker Node Pool 3

vmware

Broadoom Proprietery and Confidential. Copyright @ 2028 Broadoom. All Rights Reserved. The term “Broadoom* refers to Broadcom Inc. and/or its subsidisries

by Broadcom

선언적 커널 수준 조정이 VKS 노드에서 사용할 수 있습니다.

Elasticsearch 또는 Kafka와 같은 대용량 데이터베이스는 K8s 추상화를 통해 누출되어, 안전하지 않은 sysctl또는 특권이 있는 DaemonSet을 사용하여 조정해야 합니다. 예를 들어, vm.max_map_count를조정하지 않으면, 데이터베이스 부트스트랩 검사가 프로덕션 설정에서 시작 시 즉시 실패합니다. VKS는이제 커널 수준 조정을 위한 선언적 API인 TuneDProfile을 지원합니다. 이를 통해 사용자는 표준 K8s YAML로조정을 정의하고 특정 노드 풀을 대상으로 할 수 있습니다. VKS 3.6에는 내장된

'생산 준비 완료' 프로필은 가장 일반적인 데이터베이스 충돌을 자동으로 방지합니다. TuneD를 사용하는 큰장점은 안전하고, 플랫폼 업그레이드를 견디며, 노드를 깨끗하게 유지한다는 것입니다.

HOL-2702-01-VCF-L

페이지 19

# 선호하는 CNI를 선택하세요

# Choose your preferred CNI

New extensible framework to safely align VKS with your corporate networking strategies

![](images/0b47aeb5b0cbfcb5a768d404fe8126958ca48249cd6f8091cb40ace5b6fa003c.jpg)

PARTNERS CONSUMERS

![](images/4deaa5e536ebbcd1a7749a912b330a26f56780cb51c267b6bfe5063d438e71d5.jpg)

vmware"

Broadcom Proprietary and Confidential. Copyright ③ 2026 Broadcom. All Rights Reserved. The term “Broadoom*refers to Broadcom Inc. and/or its subsidiaries.

by Broadcom

유연성은 새로운 CNI 애드온 프레임워크의 도입으로 네트워크 계층에도 확장됩니다.

Antrea와 Calico는 기본적으로 완전히 지원되지만, 대체 CNI를 지원하기 위해 새로운extensible 프레임워크를 도입하고 있습니다. 우리는 9.1과 함께 Cilium 애드온을 공식 출시합니다.이는 클러스터 생성 전에 표준 패키지 리포지토리를 설치함으로써 활성화됩니다.

거기서부터 애드온 설치를 수동으로 생성하면 됩니다.

클러스터 생성 과정에서 애드온 컨트롤러가 자동으로 Cilium 클러스터 애드온을 생성하고 Cilium CNI를원활하게 설치합니다. 궁극적인 이점은 이 프레임워크가 VKS 관리 클러스터의 수명 주기 및 지원 경계를깨지 않고 귀사의 네트워킹 전략과 일치한다는 것입니다.

HOL-2702-01-VCF-L

페이지 20

# VM 서비스 개선사항

# Delivering Ubuntu Images for direct consumption

# Kick-starting VM Deployment

![](images/4372dc9d6f43cddd682e5036629474617da6eec37694fd609e1145e9bdc1bc95.jpg)

vmware'

Broadcom Proprietary and Confidential. Copyright $ 2026 Broadcom. All Rights Reserved. The term "Broadoom* refers to Broadoom Ino. and/or ts subsidiaries

by Broadcom

VCF는 이제 Canonical과의 파트너십을 통해 직접 사용할 수 있는 검증된 Ubuntu 이미지를 제공합니다.이를 통해 수동 이미지 생성 및 관리의 필요성이 제거됩니다.

Canonical과의 전략적 파트너십을 통해 조직은 이제 버튼 클릭만으로 Canonical 콘텐츠 라이브러리에구독할 수 있습니다. 이러한 이미지는 검증되었으며 VCF에 의해 직접 지원되어 귀하의 환경에 최적화되어있습니다. 공급자가 구독을 허용하면 이러한 이미지는 VM 서비스 내에서 직접 사용할 수 있게 됩니다. 이는 귀하의배포 프로세스를 "시작"하여 제로에서 실행 중인 VM으로 상당히 짧은 시간 안에 이동할 수 있게 합니다.

HOL-2702-01-VCF-L

페이지 21

# 빠른 배포로 VM 배포 가속화

Accelerate VM deployment with Fast Deploy Deploy and Power-on VMs very quickly with minimal storage blueprint using delta disk chains

![](images/90b0bc28eae0c417e66d86eb3264d122c35fde2ef70b49f8b4fbeccca039c825.jpg)

vmware'

Broadoom Proprietary and Confidential. Copyright @ 202e Broedoom. AllRights Reserved. The term “Broadoom refers to Broadcom Inc. and/orits subsidigries.

by Broadcom

VM Fast Deploy는 데이터스토어별 이미지 캐싱 및 델타 디스크 기술을 활용하여 배포 지연 시간을최소화함으로써 워크로드 전달을 가속화합니다. VM 서비스가 이미지를 처리하는 방식을 최적화하여프로비저닝의 가장 큰 병목 현상을 제거했습니다. 네트워크를 통해 전체 이미지를 복사하는 대신, 모든데이터스토어에 로컬 이미지 캐시를 사용합니다.

표준 VM의 경우, 우리는 연결 모드 를 사용합니다. 이는 연결된 클론처럼 작동합니다. 이 모드는 로컬 캐시를참조하는 델타 디스크 를 생성하여 VM이 거의 즉시 전원이 켜지도록 합니다. VKS 클러스터는 이러한 VM위에 구축되기 때문에, 이 최적화는 클러스터 배포 시간을 극적으로 단축할 수 있게 해줍니다. 델타스크를 사용할 수 없는 암호화된 작업 부하의 경우, 직접 모드 를 사용하여 데이터를 가능한 한 효율적으로동하도록 합니다. 이러한 기본적인 VM 수준의 속도가 궁극적으로 전체 플랫폼의 민첩성을 지원합니다.

HOL-2702-01-VCF-L

22페이지

# 집단 작업을 위한 VM 그룹화

# Group VMs together for collective operations

Introducing VM Service Groups

![](images/8c2fdc762bad6377f9a7ab411c8caebe1755dff776701a2c3fae7e6209769f54.jpg)

vmware"

Broadcom Proprietary and Confidential. Copyright @ 2026 Broadcom. All Rights Reserved.The termBroadcomrefers to Broadcom Inc.and/or its subsidiaries.

by Broadcom

환경이 확장됨에 따라 VM을 개별적으로 관리하는 것은 상당한 운영 오버헤드가 될 수 있습니다.이를 해결하기 위해, 우리는 VM 서비스 그룹을 도입하고 있습니다. 이 기능은 집단 작업을 위해 VM을함께 그룹화할 수 있게 해줍니다. 특히 전원 관리에 유용합니다.

대량 전원 작업을 넘어서, VM 그룹은 "웨이브"를 사용하여 특정 시작 순서 시퀀스 를 정의할 수 있게 해줍니다.예를 들어, 웨이브 1에서 데이터베이스 계층이 전원이 켜지고 초기화된 후에 웨이브 2에서 애플리케이션 계층이부팅 프로세스를 시작하도록 보장할 수 있습니다. 이는 네임스페이스를 청사진으로 캡처하려는 모든사람에게 매우 "사용하기 쉬운" 그러나 강력한 도구입니다. 이는 많은 고객들이 VMware CloudDirector(VCD)에서 즐겼던 것과 유사한 오케스트레이션 및 생애 주기 제어 수준을 제공합니다. 초기 배포 중이나환경이 발전함에 따라 배포 후에 이러한 그룹에 VM을 추가할 수 있습니다.

HOL-2702-01-VCF-L

페이지 23

# 스냅샷 작업 수행

# Perform Snapshot Operations

# Introducing Snapshot Management for Consumers

![](images/0f201a95874b7fa26c76e1dbfa7a00e9222065ddd2bab44b23e9b0103e9a2a6d.jpg)

vmware

Bro8dcom Proprietary and Confidential. Copyright @ 2026 Broadcom. AllRights Reserved. The term "Broadoom refers to Broadcom Ino. and/or its subsidiaries.

by Broadcom

VCF 9.1은 소비자에게 셀프 서비스 스냅샷 관리를 제공하여 소비 인터페이스에서 직접 워크로드를 보호하고되돌릴 수 있도록 합니다.

개발자들로부터 가장 빈번하게 요청되는 것 중 하나는 티켓을 열지 않고도 자신의 데이터 보호를 관리할수 있는 능력입니다. 역사적으로 스냅샷 작업은 특권 작업으로, vSphere 관리자가 개입하여 작업을수행해야 했습니다. 이번 업데이트에서는 소비자를 위한 스냅샷 관리를 도입하고 있습니다. 이제 소비인터페이스 내에서 사용자는 자신의 가상 머신에 대해 스냅샷을 생성, 편집, 되돌리기 및 삭제할 수 있습니다.이는 관리자의 운영 부담을 크게 줄이는 동시에 개발자에게 실험, 패치 또는 애플리케이션 업데이트를 위한자율성을 제공합니다. 중개자를 제거하고 팀이 자신의 속도로 진행할 수 있도록 하는 것입니다.

HOL-2702-01-VCF-L

페이지 24

# 배포 후 VM 네트워크 구성 변경

Change VM Network Configuration post deployment Introducing VM Service Day-2 Network Mutability

![](images/4902f59640d321a73da8efc37788f79fbfb5f6af6e9bdcef3a2ab5e95c4376c9.jpg)

vmware'

Broadcom Proprietsry snd Confidentiel. Copyright @ 2026 Brosdoom All Rights Reserved. The term "Brosdcom refers to Broadcom Inc.and/or its subsidisries.

by Broadcom

VM 서비스 Day-2 네트워크 가변성은 사용자가 배포 후 네트워크 구성을 수정할 수 있도록 하여 인프라의민첩성을 향상시킵니다. 이는 애플리케이션 요구 사항이 진화함에 따라 VM 연결성을 조정할 수 있는유연성을 제공합니다.

이전에는 네트워크 구성이 일반적으로 프로비저닝 시점에 정의되었습니다. 이제 우리는 기존 VM에 대해 소비인터페이스를 통해 네트워크 인터페이스를 추가, 제거 또는 편집할 수 있도록 만들었습니다. 이는 전체워크로드를 재배포하지 않고도 연결성을 쉽게 조정하거나 다중 홈 애플리케이션을 확장할 수 있음을 의미합니다.이러한 변경 사항은 게스트 내에서 효과를 발휘하기 위해 간단한 전원 사이클이 필요하지만, 훨씬 더 간소화된경로를 제공합니다.

가상 머신의 장기 수명 주기를 관리합니다.

HOL-2702-01-VCF-L

25페이지

# 비중단 VM 가져오기

![](images/92ac26a65ae1f3d92f24cb046e1a4a9ecb6af9374025f4fe010d34881ecff3f4.jpg)

비중단 VM 가져오기를 사용하면 기존 vSphere 작업 부하를 Supervisor 네임스페이스로 가져오고 VCF자동화 제어 하에 두면서 다운타임이나 네트워크 변경 없이 진행할 수 있습니다. 운영을 현대화하려고 할 때기존 작업 부하를 유지하는 것과 Supervisor 기반 모델로 이동하는 것 사이에서 선택할 필요가 없습니다.우리는 VM 가져오기 프로세스를 완전히 비중단으로 업데이트했습니다.

과거에는 VM을 네임스페이스로 이동하는 데 종종 네트워크 아이덴티티 변경이나 재IP가 필요했으며, 이는자연스럽게 애플리케이션의 다운타임을 의미했습니다. 이제는 기존 상태를 유지하면서 전통적인 vSphere환경에서 Supervisor 네임스페이스로 VM을 마이그레이션할 수 있습니다. 이것은 "비-VM 서비스" VM을VCF 자동화의 중앙 집중식 제어 하에 배치로 가져올 수 있게 하여, 비즈니스를 중단하지 않고 전체 컨테이너 및VM의 일관된 수명 주기 관리를 보장합니다.

HOL-2702-01-VCF-L

26페이지

# 컨테이너 서비스

# Introducing Container Service

Deploy isolated and secure containers

![](images/357dc18bee92fc0be91ea5b809e59ff07c76862cbefa8789fdcfcab88bce33ae.jpg)

vmware

Broadoom Proprietary and Confidential. Copyright @ 2026 Brogdcom. All Rights Reserved. The term “Broadcom* refers to Broadcom Inc. and/or its subsidiaries.

by Broadcom

새로운 컨테이너 서비스는 vSphere 네임스페이스 내에서 격리되고 안전한 컨테이너 인스턴스를 직접 배포할 수있게 하여, 전체 Kubernetes 클러스터의 관리 오버헤드를 제거합니다. vSphere Pods를 활용하여 이 서비스는ESXi 노드에서 1급 작업 부하로 직접 실행되는 격리되고 안전한 컨테이너 인스턴스를 생성합니다.

이 새로운 서비스의 주요 내용은 다음과 같습니다:

• 격리되고 안전한 컨테이너
• 컨테이너 배포를 위한 Kubernetes의 오버헤드 제거
• vSphere 네임스페이스 내에서 컨테이너 인스턴스의 UI 기반 프로비저닝 및 생애 주기 제어
이 서비스의 4가지 주요 기능은 다음과 같습니다:

• vSphere Pods 기반
• 매우 빠른 배포
• 지속적인 볼륨을 연결하여 StatefulSets를 생성할 수 있는 기능
• 다중 컨테이너 지원

모듈 4에서 새로운 컨테이너 서비스와 상호작용할 수 있습니다

HOL-2702-01-VCF-L

27페이지

# vSphere 슈퍼바이저 개선사항

# Unifying Content Distribution in VCF 9.1

Introducing Unified Software Depot through Fleet Depot Service

![](images/99b87893ee857917cb9ecf1a3ecc0ceaf102444079e3c37e7b5b83b0601794b1.jpg)

vmware

Eroadoom Proprietery and Confidential. Copyight @ 202e Broedoom.

by Broadcom

All Rights Reserved. The term "Broadcom* refers to Brosdcom Inc. and/or is subsidiaries

VCF 9.1은 Fleet Depot Service를 도입하여 이진 파일, OCI 아티팩트 및 파트너 콘텐츠의 획득 및 배포를간소화하는 통합 소프트웨어 저장소를 제공합니다.

진정한 통합 클라우드 플랫폼을 지원하기 위해 우리는 콘텐츠를 처리하는 통합된 방법이 필요합니다.우리는 모든 소프트웨어 배달을 위한 중앙 허브 역할을 하는 Fleet Depot Service를 도입하고 있습니다. 이서비스는 vSphere Kubernetes 릴리스(vKRs), OCI 패키지 및 다양한 아티팩트를 포함하여 필요한 이진파일을 수집하는 데 필수적입니다.

이 서비스는 표준 파일, Harbor Proxy Cache를 통한 OCI 아티팩트 및 Canonical의 검증된 Ubuntu 이미지와같은 파트너 저장소의 제3자 콘텐츠를 통합합니다. 운영 내 "빌드" 섹션을 보면 데이터 센터의 보안 요구 사항에맞는 세 가지 유연한 연결 설정이 표시됩니다: 직접 액세스를 위한 Connected, Disconnected, 또는 완전히Offline 모드입니다.

이것은 환경의 제약에 관계없이 전체 시스템에 소프트웨어를 배포하는 일관되고 신뢰할 수 있는 방법을보장합니다.

HOL-2702-01-VCF-L

28페이지

# 기본적으로 로컬 서비스 소비(LCI) 활성화

# Enabling Local Service Consumption by default

Local Consumption Interface (LCl) now deployed as Core Supervisor Service

![](images/0fdfae9d347e19ddf6a33494828b3ab0238d8022c9ba4ccedeefa4c7e4ad8127.jpg)

#

Broedoem Proprietary and Confkdential. Copyrigh1 e 2026 Broedcom

by Broadcom

AlI Rights Reserved. The term *Broedoom” refers to Broedoom Ino. andior its subsidiaries

로컬 소비 인터페이스(LCI)는 이제 핵심 슈퍼바이저 서비스로, 소비자가 VM, 컨테이너 및 쿠버네티스클러스터를 관리할 수 있는 원활한 기본 UI를 제공합니다.

소비자가 자원과 상호작용하는 것을 최대한 쉽게 만들고자 합니다. 이전에는 로컬 소비 인터페이스를 설정하기해 수동 설치 및 구성이 필요했습니다. VCF 9.1에서는 LCI를 핵심 슈퍼바이저 서비스 로 만들어 기본적으로포되고 활성화됩니다.

이 서비스는 vSphere 클라이언트 내에 플러그인을 자동으로 생성하여 사용자가 자신의 네임스페이스의"리소스" 탭에서 직접 접근할 수 있도록 합니다. 이는 가상 머신, 쿠버네티스 클러스터 및 새로운 컨테이너서비스를 관리하기 위한 깔끔하고 집중된 대시보드를 제공합니다. 또한, vSphere 클라이언트에 대한 전체접근이 필요하지 않은 팀의 경우, LCI를 독립형 외부 인터페이스로 실행할 수 있어 개발자에게 자신의환경을 관리하는 데 필요한 정확한 수준의 접근을 제공하기가 쉽습니다.

HOL-2702-01-VCF-L

페이지 29

# DTGW를 이용한 슈퍼바이저 배포

![](images/efb63a1fa0d28372b78c18b77dd703c4044dfbd2f8c71589dc2e1efea7970cd2.jpg)

슈퍼바이저 배포는 이제 분산 전송 게이트웨이(DTGW)를 통해 가상 사설 클라우드(VPC)를 지원하여네트워킹 병목 현상을 제거하고 물리적 패브릭에 대한 연결을 단순화합니다.

네트워킹을 더욱 간소화하기 위해 분산 전송 게이트웨이(DTGW)를 도입하고 있습니다. 이는 ESXi 호스트가물리적 네트워크에 연결하는 방식을 혁신적으로 변화시킵니다. 호스트가 스위치 패브릭에 직접 연결할 수있도록 함으로써 중앙 집중식 전송 게이트웨이의 필요성을 없앱니다.

이 아키텍처 변화는 연결에서 중요한 병목 현상을 제거합니다. 더 이상 중앙 집중식 지점을 통해 트래픽을헤어핀할 필요가 없으므로 지연 시간, 확장성 및 전반적인 네트워크 성능에서 즉각적인 개선을 볼 수있습니다. 운영적으로도 훨씬 간단해졌습니다: 이제 워크로드를 온라인으로 가져오기 위해 전체 NSX 엣지클러스터나 복잡한 BGP 구성이 필요하지 않습니다. 이는 일관된 워크플로우와 새로운 워크로드에 대한 더 빠른온보딩을 제공합니다. 심지어 고급 가상 네트워킹 장치에 대한 깊은 전문 지식이 없어도 가능합니다.

HOL-2702-01-VCF-L

페이지 30

# 다중 클러스터 존으로 존 스프롤 줄이기

Reducing Zone Sprawl with multi-cluster Zones Scale up to 3 ESXi Clusters per Zone without Disruption

![](images/e888d01bb902a1d1d974588c122cdd76042534ab40b9301f37569aee77438942.jpg)

vmware'

Broadoom Proprietary and Confidential. Copyright @ 2026 Broadcom All Rights Reserved. The term “Broadcom* refers to Broadcom Inc. and/or its subsidisries

by Broadcom

VCF 9.1은 다중 클러스터 존을 도입하여 존당 최대 세 개의 ESXi 클러스터를 허용하여 규모를 늘리고비파괴적인 하드웨어 유지 관리를 가능하게 합니다.

고객들이 슈퍼바이저 환경을 확장함에 따라, 존 스프롤 관리가 최우선 과제가 되었습니다. 이전 릴리스에서는존당 하나의 vSphere 클러스터로 제한되었습니다. VCF 9.1에서는 존당 최대 세 개의 클러스터를 지원하여이 장벽을 허물고 있습니다.

이 변화는 단순한 원시 용량 이상의 의미가 있습니다. 운영 연속성에 관한 것입니다. 단일 영역 내에 여러클러스터를 두면 이제 주요 하드웨어 업그레이드, 교체 또는 퇴역을 작업 부하 중단 없이 수행할 수있습니다. 예를 들어, AI 작업 부하에 대한 GPU 드라이버를 업데이트해야 하는 경우, 해당 작업 부하를 동일한영역 내의 다른 클러스터로 간단히 마이그레이션할 수 있습니다. 이를 통해 네임스페이스와 서비스를 재설계 없이유지할 수 있으며, 하드웨어 생애 주기 관리와 일반적으로 관련된 수동 작업과 다운타임을 효과적으로 제거할수 있습니다.

HOL-2702-01-VCF-L

31페이지

# 결론

이 모듈에서는 VCF 9.1에서 도입되는 새로운 기능과 서비스에 대해 검토했습니다.

여기에서 다음을 수행할 수 있습니다:

• 다음 실험 모듈을 계속 진행하십시오.
이

랩의 모든 모듈이나 수업으로 이동하려면 [vlp:table-of-contents|목차 표시]를 클릭하세요.

• 실습을 종료하고 미래에 다시 돌아오세요.

HOL-2702-01-VCF-L

32페이지

# 모듈 2 - VMware vSphere

# 쿠버네티스 서비스(VKS)

# 클러스터 생성 및 신규

# 기능 (45분)

# 중급

HOL-2702-01-VCF-L

페이지 33

# 모듈 소개

이 모듈에서는 VKS 클러스터를 생성할 것입니다. VKS 클러스터를 생성하는 동안 모듈 1에서 설명된새로운 기능과 능력을 보여드릴 것입니다. 이 모듈은 vSphere 슈퍼바이저 서비스 개선 사항을 살펴보며마무리됩니다.

# • VKS 클러스터 생성

• 맞춤 생성
• 클러스터 클래스 및 쿠버네티스 릴리스
• VKS 및 노드 재정의
• 노드 풀 구성
• 다중 네트워크 지원

# • vSphere 슈퍼바이저 서비스

• 외부 애플리케이션으로서의 LCI
• 지역 하버 인스턴스 구성

HOL-2702-01-VCF-L

34페이지

# VKS 클러스터 생성

다음 몇 페이지에서는 VMware vSphere 쿠버네티스 클러스터(VKS)를 생성하는 과정을 안내합니다.

이미 생성된 네임스페이스에서 이 클러스터를 생성할 것입니다. 이 생성 과정에서 몇 가지 새로운 기능을 강조할것입니다.

# Firefox 시작

![](images/3e901d84217f27874af2fb22ae65927ed9eda62d7e2d95b4f09357486e4b30ad.jpg)

Linux 작업 표시줄에서 Firefox 브라우저를 엽니다.

1. 브라우저를 열기 위해 Firefox 아이콘을 클릭합니다.

# VCF 자동화 콘솔 열기

VKS 클러스터를 생성하는 방법은 여러 가지가 있습니다. 일반적으로 vCenter -> 슈퍼바이저 관리경로를 통해 생성하지만, 이번 모듈에서는 VCF 클러스터 관리 내러티브에 더 적합한 다른 방법을 보여드릴것입니다. VCF 자동화에서 이 클러스터를 생성할 것입니다. Firefox 브라우저를 시작하고 VCF 자동화를 시작해보겠습니다.

HOL-2702-01-VCF-L

35페이지

![](images/eb5e1f8f3ea2bc11fe764f47000cefa61cbf538ac660012be328b442d99bb7e2.jpg)

Firefox가 로드되면:

1. 지역 A 북마크 폴더 를 클릭합니다.
2. VCF 자동화 를 클릭합니다.

HOL-2702-01-VCF-L

36페이지

# VCF 자동화 콘솔에 로그인

VMware Cloud Foundation

# Automation

Organization name

![](images/ed7c62719105334ee8733628bd35540286ee3b1d0e9c82e8d2329568303bad18.jpg)

![](images/02efba428cf071ca6afc53ea40673e9fe3871064d14613595a735e7af8668a2f.jpg)

먼저 이 랩을 위해 이전에 생성된 ACME 조직에 로그인해야 합니다.

1. 텍스트 상자에 acme 를 입력합니다.
2. 계속 를 클릭합니다.

HOL-2702-01-VCF-L

37페이지

# 자격 증명

![](images/c35457bf4536726502e0409ccbc84c25afd14fd6b2884f225d7ef9c9d4992c6d.jpg)

관리자에 대한 자격 증명은 이미 브라우저 창에 캐시되어 있어야 합니다.

1. acme-admin의 ACME 조직에 대해 미리 생성된 자격 증명을 선택하십시오.

# 자격 증명 선택

![](images/37c895906136f24ca46d818765e213825bcfc5f9b40ba4f4e2f180bc1c51f480.jpg)

미리 생성된 관리자가 입력되지 않은 경우

HOL-2702-01-VCF-L

페이지 38

1. acme-admin을 입력하십시오.
2. VMware1234!Vmware123!의 비밀번호를 입력하십시오.
3. 로그인 클릭

# Kubernetes 서비스 섹션으로 이동

![](images/31fd5343e0597ca1be1b6c794ac5dfbb8cd0192fbdacdb249939c6c1ec81a01b.jpg)

1

Services

development-3ywn4

![](images/feb9bdaebf1701407885d1a85a4595412d27a0211c2fd9752c6fe8a8e9ad8962.jpg)

Kubernetes

1. 당신의 네임스페이스가 development-3ywn4인지 확인하세요.
2. 선택 Kubernetes

# 새로운 Kubernetes 서비스 생성 시작

# vSphere Kubernetes Service

![](images/5ae8307f2e2b02d1fc5037360c32a49411299f06b9dd9f7afd960a6e759fe8ec.jpg)

CREATE

VKS 클러스터를 생성하려면:

1. 선택 생성 HOL-2702-01-VCF-L

페이지 39

# 구성 유형

Create the cluster with a pre-defined default configuration or a custom configuration

![](images/15e0589df979cacc97764e21771877543e14eda7d43a41d84c3e26e257d64da9.jpg)

![](images/1f29e39f53fae5b8dd4eee02f6f32f709b26a40e079b5c9573299abf77de9f13.jpg)

Configuration Type

1. 선택 사용자 정의 구성
2. 클릭 다음

# 일반 설정

![](images/cd81dd42e6a75db169eb0c388eec165b8d6c3b0989a0e67e308650d735795d22.jpg)

제어 평면 노드를 구성하려면 CPU 및 메모리와 같은 제어 평면 노드 VM에 할당될 리소스를 정의할 VM클래스를 선택해야 합니다.

1. 클러스터 이름: acme-app
2. 클러스터 클래스로 builtin-generic-v3.6.0 선택
3. 쿠버네티스 릴리스로 v1.34.2---vmware.2-vkr.2 선택

HOL-2702-01-VCF-L

페이지 40

4. VM 클래스를 다음으로 변경: best-effort-medium # 스토리지 클래스

![](images/c2f710a0701ed15aa1214c0c0cafacf4ade80b43c368ef513c21d5bcac9c5a74.jpg)

스토리지 클래스를 vsan-default-storage-policy 로 유지합니다.

# 1. 다음 클릭

# 복제본 및 OS

![](images/d6cc24176a1b95b9ed7ad87326c8ed219d5ce2ab381288041b4e3b5e0633d3e1.jpg)

1. 복제본을 1로 설정
2. 선택할 OS 이미지: Photon 5 - 쿠버네티스 서비스 콘텐츠 라이브러리

HOL-2702-01-VCF-L

41페이지

3. 슬라이더를 오른쪽으로 이동하여 초록색으로 변경합니다.

# 오버라이드

![](images/3de5a15e0c7768246131a18bacdb9554d6b6cb518220ea5c6794c0d3acfac292.jpg)

Overrides

VM Class

<table><tr><td></td><td>Name</td><td>CPUs ↑</td><td>CPU request/limit</td><td>Memory</td><td>Memoryrequest/limit</td><td>PCI Devices</td></tr><tr><td>○</td><td>best-effort-xsmall</td><td>2 vCPUs</td><td>No Reservation</td><td>2 GiB</td><td>No Reservation</td><td>0</td></tr><tr><td>○</td><td>best-effort-small</td><td>2 vCPUs</td><td>No Reservation</td><td>4 GiB</td><td>No Reservation</td><td>0</td></tr><tr><td></td><td>best-effort-medium</td><td>2 vCPUs</td><td>No Reservation</td><td>8 GiB</td><td>No Reservation</td><td>0</td></tr><tr><td>○</td><td>best-effort-large</td><td>4 vCPUs</td><td>No Reservation</td><td>16 GiB</td><td>No Reservation</td><td>0</td></tr><tr><td>○</td><td>best-effort-xlarge</td><td>4 vCPUs</td><td>No Reservation</td><td>32 GiB</td><td>No Reservation</td><td>0</td></tr><tr><td colspan="3"></td><td>VM Classes per page</td><td>5 √ 1 - 5 of 8 VM Classes</td><td colspan="2">&lt; &lt; 1 / 2 &gt; |</td></tr></table>

오버라이드를 선택하면 그 위에 여러 항목이 표시됩니다. 첫 번째는 VM 클래스입니다. 이 랩에서는

1. best-effort-medium을 선택합니다.

HOL-2702-01-VCF-L

42페이지

# 노드 볼륨

![](images/479ab548defca1cfddb65d9acb335f1054054063c03460d2b68896e920a9e567.jpg)

그 아래에서 스토리지 클래스를 선택할 수 있는 옵션이 표시됩니다. 우리는 이를 vsan-default-

storage-policy로 두겠습니다.

다음으로 노드 볼륨을 연결할 수 있습니다. 전용 노드 볼륨을 연결하면 containerd 이미지와 kubelet컨테이너 데이터를 다른 곳에 저장할 수 있어 루트 파티션이 가득 차는 것을 방지할 수 있습니다.

1. 설정을 보려면 볼륨 연결을 클릭합니다.

HOL-2702-01-VCF-L

43페이지

# 볼륨 첨부

# Attach Volume

Mount path

![](images/7a6fe5ba0afe4a27df8a1917844bf2d083278cca281308b1a77d742bbc201a16.jpg)

Storage Class

![](images/42c1a1da1b54150f5e5643cf53b39477be247878335c5b0c775149c63830ad44.jpg)

Capaclty

GiB

1

CANCEL

SAVE

여기에서 편집할 수 있는 볼륨의 이름, 마운트 경로, 스토리지 클래스 및

용량을 설정할 수 있습니다. 이 랩의 목적을 위해 노드 볼륨을 생성하지 않을 것입니다.

1. 이전 화면으로 돌아가려면 취소를 클릭하십시오.

# 노드 네트워크

Node Network

You canoverride additional networks.If you plan to use Antrea's additional networks feature,do not override the  Node Network configurations.

![](images/b2fcefb78b9994aa46e345901e8440b7cf187fb2ffd81e95c3d9a9d7a742ae01.jpg)

![](images/2d75b9a7d651b0356f8247682672dedf5c72bc971c04778a30d249a3d9a89ff9.jpg)

1

+ADD ADDITIONAL NETWORK

다음 섹션은 노드 네트워크입니다.

1. HOL-2702-01-VCF-L

추가 설정을 선택하려면 추가 네트워크 추가 를 선택하십시오.

44페이지

# 추가 네트워크

![](images/f8e5af5336abfcdce8e930e5d1abeb3a7e777343eceb00f83a705354e9383b05.jpg)

추가 네트워크 추가 를 선택하면 이제 보조 이더넷 네트워크를 생성할 수 있습니다. 다른 기존 네트워크서브넷 중 하나를 선택하고 MTU를 입력한 다음 필요한 추가 정적 경로를 추가합니다. 이 랩의 이 부분에서는보조가 필요하지 않습니다.

"네트워크".

1. 네트워크 삭제 를 선택하십시오.

HOL-2702-01-VCF-L

45페이지

# 고급 재정의

# Advanced Overrides

Configureadditional setings for the control plane. These settings overrides those defined at cluster level.

> Kubernetes

> Node

Node configures Kubernetes node specific settings.

> os Configuration

OSConfiguration configures the system setings of nodes that are independent of Kubernetes.

> Resource Configuration

supported.

![](images/f2a440e74cf8375fe7bff3590799cd6084844edc35357d2f5da0fd30427fec29.jpg)

1

그런 다음 고급 재정의로 내려갑니다. 여기에서 API 서버 구성, Kubelet 구성, 노드 방화벽 수신 규칙, 비밀번호최대 연령 및 CPU와 메모리에 대한 리소스 예약과 같은 Kubernetes 제어 평면의 기본 설정에서 재정의를수행합니다.

1. 변경 사항을 만들지 않으므로 다음 을 선택하십시오.

HOL-2702-01-VCF-L

46페이지

# 노드풀

![](images/5be4a55e403128eb65c11bba0f121e8f31b65dea10cd4444993faff15c70c294.jpg)

다음 섹션에서는 기존 노드풀을 선택하거나 노드풀을 생성합니다.

Kubernetes 노드 풀은 동일한 구성(예: 머신 유형(CPU, 메모리), 운영 체제 및 디스크 사양)을

공유하는 클러스터 내의 작업자 노드 그룹입니다. 예제에서 이미 생성된 풀을 볼 수 있습니다. 그러나 하나를구성하는 방법을 보려면:

1. 기존 풀 acme-app-np-7mxg의 왼쪽에 있는 3개의 점을 클릭하세요.
2. 구성을 살펴볼 수 있도록 편집 를 선택하세요.

HOL-2702-01-VCF-L

페이지 47

# 노드풀 구성

![](images/cdd587f3a391b92a8c3fbe7f3b23b8d4468478c21a0aae1f82453f57e6597051.jpg)

여기에서 여러 설정이 있음을 볼 수 있습니다. 여기서 주목해야 할 중요한 설정은 OS 이미지로,Photon 또는 Ubuntu일 수 있으며, 자동 확장을 활성화하는 것입니다.

1. 메인 화면으로 돌아가려면 취소를 클릭하세요.

HOL-2702-01-VCF-L

페이지 48

# 고급 클러스터 설정

A nodepool is a group of worker nodes sharing the same resource allcation and storage.

+ ADD NODEPOOL

<table><tr><td></td><td>Name</td><td>Zone</td><td>Replicas</td><td>VM Class</td></tr><tr><td> $\vdots$ </td><td>acme-app-np-7mxg</td><td>z-wld-a Automatic</td><td>1</td><td>best-effort-med</td></tr><tr><td colspan="4">Manage Columns</td><td>1 - 1 of 1 Node pools</td></tr></table>

![](images/0711f998e6d16057213f0558a8db0393cd8957471a207e5c7f4b65748408a419.jpg)

e advanced setings for this cluster

Advanced setings can be used to configure allte variables present on the selected ClusterClass

![](images/3bb66a6ea97604b11a8e04a6423552f3c04535bf7add4cfbda3fdac158ebca4f.jpg)

NEXT

5.Advanced Settings (Optional)

Defineadvanced settingsfor this cluster

# 고급 클러스터 설정 - 2부

1. 노드풀 영역으로 돌아가서, 이 클러스터에 대한 고급 설정 정의 체크박스를 클릭하면 그 아래에 고급설정(선택 사항) 영역이 표시됩니다.
2. 체크박스를 선택한 후 다음 을 클릭하십시오.

HOL-2702-01-VCF-L

페이지 49

# 5. Advanced Settings (Optional)

Defineadvanced settings for thiscluster

![](images/468c7aa900b3f158ff238471a14c958fb2eaba51c24b349f85d58aab44fbb3a0.jpg)

>  Cluster Settings Configure optional setings for the cluster
> Os Settings Define OS level configurations for the cluster nodes
>  Other Settings Configureadditional settings for the cluster

NEXT

![](images/ac6ee7a59e05c1ea6986fff62205a96b457c833247a94369c3ab7a851e13cbda.jpg)

고급 설정에는 클러스터 및 OS, 기타에 대해 설정할 수 있는 구성 요소가 있습니다. 클러스터 예약은 추가 완전한도메인 이름 및 인증서 회전을 설정하는 데 사용됩니다. OS 설정은 NTP 설정 및 HTTP 프록시를 재정의하고,FIPS를 활성화하며 배너를 추가하는 데 사용됩니다. 기타 설정은 Kubernetes와 독립적인 노드와 관련된 항목에대한 것입니다. 이 실습을 위해서는 이러한 설정을 변경할 필요가 없습니다.

1. 계속 진행하려면 다음 을 클릭하십시오.

# 검토 및 확인

6.Review and Confirm

Reviewallthedetailsbefore you deploy thiscluster

![](images/e6fee59491998a4a0aa5646b5c4baf589d2c5455f2edec9ff2a8c39568ab753f.jpg)

Review the configuration and the YAMLfile generated.Then,click FINIsHto startdeploying this cluster.

![](images/9f05efa3e6902a7cfdba348ab4c7fc0c626b1536612fe3051d1b9067e5d3bb4b.jpg)

이 시점에서 우리는 구성의 끝에 있습니다.

HOL-2702-01-VCF-L

페이지 50

1. 완료 를 선택하십시오.

# Kubeconfig 파일과 YAML 파일 가져오기

![](images/a5f432787ad6121d7f38985cda06867fc3f17cedff8083dbb6599e6862de81e7.jpg)

마침을 선택하면 vSphere Kubernetes Service 화면으로 돌아갑니다. 여기에서 왼쪽의 3개의 점을선택하면 몇 가지 옵션이 표시됩니다. 이곳에서 Kubernetes 클러스터에 연결하는 데 필요한 Kubeconfig 파일을다운로드할 수 있습니다. 또한 클러스터를 자동화하여 배포하려는 경우 YAML 파일을 보고 다운로드할 수도있습니다.

HOL-2702-01-VCF-L

51페이지

# 다중 네트워크 지원

기존 Kubernetes 서비스에 다중 네트워크 지원을 추가하는 것은

매우 쉽게 할 수 있습니다.

# 기존 서비스에 다중 네트워크 추가

![](images/997b8974203cd3d770d907f5407ece3b8a3368383f607057017b3384bca709c6.jpg)

# 기존 서비스 찾기 및 선택

VMware Automation에서 개요를 선택합니다.

1. 그런 다음 서비스 영역에서 Kubernetes를 선택합니다.

HOL-2702-01-VCF-L

52페이지

# vSphere Kubernetes Service

![](images/00ec852d3f9b50451a5c1ca52ef84d5ddaccf4f4a3bb25535e7397c25d89ac0c.jpg)

이전 장에서 생성한 기존 acme-app Kubernetes 서비스를 볼 수 있습니다.

1. 이름 acme-app 선택

# 노드 네트워크 영역으로 이동

Persistent Volume Storage

Default Storage Class

![](images/4beb1fbfa35baebaf2fa124c99ce2b898af30a91b34d155295fedc11bdd8ff87.jpg)

![](images/9574bae82d0d7ee663972a49cc5eab6cd43f262b594192d79cf373e379d0844b.jpg)

Node Network

Control plane

EDIT

스크롤을 내려 노드 네트워크 영역에 도달합니다.

1. 편집 을 클릭합니다.

# 네트워크 추가

Node Network

CANCEL

SAVE

![](images/da29a3f74616305cf67c77ce28cd3d0092a7c7a965581829d622d9ae4cedb45d.jpg)

![](images/58e4847f4b27f254d7701501868b607b82ec53cf55d512fdb97f7d6703ff7f4b.jpg)

![](images/0dfc516cdfd3e0ed1302aa193cda1c38f8d7676fcf8d15257f6de031f8126329.jpg)

ADDADDITIONAL NETWORK

HOL-2702-01-VCF-L

페이지 53

추가할 수 있는 네트워크를 보려면.

# 1. 추가 추가 네트워크 를 클릭합니다.

# 새 네트워크 선택

![](images/31c02eed33583465bf1109e6cdf9e6464b783aa370a8f891bb729020f5d3f8af.jpg)

참고 : 이미 선택할 추가 네트워크를 생성했습니다.

1. 네트워크 드롭다운 화살표를 선택하여 추가할 수 있는 네트워크를 확인합니다.

HOL-2702-01-VCF-L

54페이지

# 추가 네트워크 선택

![](images/99b95c0163d8bde6bdc3ee29f9abc862273a0dad67f613d1c0db26970752cc39.jpg)

ACME-APP는 이미 subnet에 할당되어 있습니다. 이 단계에서는 다른 네트워크를택하겠습니다.

1. rc-testnet subnet 선택

# 구성 저장

![](images/6f90ad18ba6b2dad93bb3832134f354a41f117c1e3b402d7fdf9508dccd1472a.jpg)

HOL-2702-01-VCF-L

페이지 55

필요한 경우 MTU를 기본값에서 변경하거나 정적 경로를 추가하는 등의 추가 옵션이 여러 가지 있습니다. 이시나리오에서는 둘 다 수정할 필요가 없습니다.

1. 이 새로운 네트워크를 저장하려면 SAVE 를 선택하십시오. 참고 저장 버튼을 보려면 조금 위로 스크롤해야수 있습니다.

# 새 네트워크가 추가되었는지 확인

![](images/d87fef271d7543226cbf47aa48568c55f02db5b034687c34c43559df4c8e7d6b.jpg)

새 네트워크가 추가되었는지 확인하려면 Wld01 vCenter에 로그인해야 합니다. Firefox 브라우저에서:

1. 새 탭 열기
2. 지역 A 북마크 폴더에서 vc-wld01-a 클라이언트를 선택하십시오.

HOL-2702-01-VCF-L

56페이지

# 추가된 네트워크에 대해 VKS VM을 확인하십시오.

![](images/41843020cadfe99a8c17e6e1f828198b0ec521592936fedd865068bf2092095e.jpg)

vCenter의 인벤토리 보기에서 추가된 네트워크로 재구성되는 제어 계획 VM을 볼 수 있습니다.

1. 클러스터 cluster-wld01-01a 아래에서
2. acme-app VKS 클러스터로 드릴다운하십시오.
3. rc-testnet_6yky5 subnet에서 새로운 IP 주소를 볼 수 있습니다.

# 결론

이 시점에서 클러스터에 추가 네트워크를 성공적으로 추가했습니다.

HOL-2702-01-VCF-L

57페이지

# 외부 애플리케이션으로서의 LCI

VMware 로컬 소비 인터페이스(LCI)는 vCenter 인터페이스를 사용하지 않고도 VM, 쿠버네티스 클러스터및 컨테이너와 같은 리소스에 접근할 수 있는 방법으로, 필요한 접근량을 줄여줍니다. 이 모듈에서는vCenter 내부에서 인터페이스에 접근하는 방법을 보여주고, 직접 로그인할 수 있는지 확인할 것입니다.

# 시작하기

![](images/65a59384146b84a20fa8be4e2861762255b3a78dacc3127c723a89dfeba5aba9.jpg)

1. 먼저 브라우저에

vc-wld01-a.site-

a.vcf.lab 을 입력하거나 미리 로드된 항목에서 선택하여 Workload Domain vSphere에 로그인합니다.

2. 우리는 adminstrator@wld.sso로 로그인합니다.
3. 비밀번호는 자동으로 입력되어야 하지만, 그렇지 않은 경우 VMware123!VMware123!입니다.
4. 로그인 바를 누릅니다.

HOL-2702-01-VCF-L

페이지 58

# 슈퍼바이저 관리

![](images/9bbf1433990f4bec605807d93ad40195cd2fe4bf81947bede26eba81d7d1ebe3.jpg)

1. 왼쪽 상단의 세 개의 막대 를 클릭하세요.
2. 슈퍼바이저 관리 를 선택하세요.

HOL-2702-01-VCF-L

59페이지

# 네임스페이스를 선택하세요.

![](images/9dd1d3cbc4d56ca83c10bca0c31f9a9c8a23275c56ac248abed284cabe10650f.jpg)

슈퍼바이저 관리를 클릭하면 왼쪽에 네임스페이스 목록이 표시됩니다.

이번에 관심 있는 네임스페이스는 svc-cci-ns-nb730 입니다.

1. svc-cci-ns-nb730 네임스페이스를 클릭하세요.

# 리소스

![](images/a4dcd33cd2fc925230549dd0fc7791dcf5d13b2bf9c60e47894b90f531002057.jpg)

HOL-2702-01-VCF-L

60페이지

그렇게 하면 화면 오른쪽이 서비스 표시로 변경되며,

svc-cci-ns-nb730 아래에 선택할 수 있는 여러 탭이 나타납니다.

# 1. 리소스 를 클릭하세요.

LCI 시작하기

![](images/f30fd86091c566b85ac8114d0b9f9de2060abd24548fb3b4fdd306122875dcef.jpg)

# 1. 독립형 클라이언트 시작 를 클릭하십시오.

새 창에서 열기

![](images/f094cbec0b1472216bfb1f2300e39b5e7941f16e536ee860097b18a9b7c2bde7.jpg)

이 옵션을 선택하면 두 가지 옵션이 있는 드롭 메뉴가 표시됩니다.

# 1. 새 창에서 열기를 선택하십시오.

HOL-2702-01-VCF-L

페이지 61

# LCI에 로그인하기

![](images/622737d1fc6e543ce8110a08341394fcd9b2d13b45119ee5854d4c9984a36eff.jpg)

이 링크를 클릭하면 VMware 로컬 소비 인터페이스 로그인 화면으로 이동합니다.

1. 로그인 이름으로 administrator@wld.sso 를 입력하십시오.
2. 비밀번호로 VMware123!VMware123! 를 입력하십시오(또는 사용 가능한 경우

리 채워진 옵션을 사용하십시오).

3. 로그인 클릭

HOL-2702-01-VCF-L

페이지 62

# 네임스페이스 선택

![](images/28c6bd453c97d685770b0e1a82d11a866fc7717c5063f78b23a83858e57db6df.jpg)

1. 이제 LCI 메인 메뉴에 있어야 합니다. 오른쪽 끝, 상단 근처로 가면네임스페이스 를 선택하면 모든 네임스페이스의 드롭다운이 나타납니다.
2. 여기에서 원하는 네임스페이스로 이동할 수 있습니다. 이 예제에서는 development-3ywn4를 선택하세요.

HOL-2702-01-VCF-L

페이지 63

# 쿠버네티스 서비스

![](images/8fb5e19f030c1327ff75660e4af70c7f439eacb625c3e8f13a5929377c4a30cd.jpg)

development-3ywn4를 선택하면 네임스페이스에 대한 더 많은 세부정보가 표시됩니다. 여기에는가상 머신, 이미지, 네트워크 서비스 및 쿠버네티스 클러스터가 포함됩니다.

# 1. 쿠버네티스 클러스터 타일 에서 서비스로 이동 클릭

HOL-2702-01-VCF-L

페이지 64

# 서비스 보기

![](images/17a3ecbbc70c2b90540339240502d7430d79a4da372ab5ff37020c67c1193993.jpg)

여기에서 이전에 생성한 acme-app의 vSphere 쿠버네티스 서비스를 볼 수 있습니다. 더 자세한 내용을려면 클릭할 수 있지만, 이 모듈의 목적을 위해 여기서 마치겠습니다.

# 모듈 종료

이 모듈을 완료했습니다.

HOL-2702-01-VCF-L

페이지 65

# 모듈 결론

이것은 모듈 2의 결론입니다.

여기에서 다음을 수행할 수 있습니다:

• 다음 랩 모듈로 계속 진행하십시오.
이

랩의 모든 모듈이나 수업으로 이동하려면 [vlp:table-of-contents|목차 표시]를 클릭하세요.

• 랩을 종료하고 나중에 돌아오십시오.

HOL-2702-01-VCF-L

페이지 66

# 모듈 3 - VM 서비스 신규 기능및 운영 (45 분) 중급

HOL-2702-01-VCF-L

페이지 67

# 모듈 소개

이 모듈은 참가자들에게 VMware Cloud Foundation 9.1에서 제공되는 강력한 새로운 VM 서비스기능을 소개하며, 더 빠른 배포와 간단한 일상 운영으로 직접 연결되는 실습을 포함합니다. 참가자들은우분투 이미지 관리를 위한 Canonical 구독, 데이터스토어 캐싱 및 델타 디스크 기술을 사용한거의 즉각적인 프로비저닝을 위한 VM Fast Deploy, 그리고 가상 머신 집합 간의 집합 작업 및 부팅 순서전원 관리를 수행하기 위한 VM 그룹화에 대해 탐구할 것입니다. 이 모듈은 또한 VM 스냅샷과 네트워크변동성(Network Mutability)을 다루며, 이는 기존 VM에서 네트워크 인터페이스를 추가, 제거 또는편집할 수 있는 새로운 기능입니다. 재배포 없이도 가능합니다.

HOL-2702-01-VCF-L

68페이지

# Canonical 구독

신뢰할 수 있는 오픈 소스 혁신의 선두주자인 Canonical과 Broadcom의 확장된 파트너십은 현대의컨테이너화된 AI 작업 부하의 배포를 더 효율적이고 안전하게 가속화할 것입니다. IT 팀은 자원 소비를 줄이고라이프사이클 관리를 단순화할 수 있습니다.

VMware는 Canonical의 기술 구성 요소를 VKS에 통합하여 다음 분야에서 새로운 가치를 제공할 것입니다:

• VCF + 기업 지원이 포함된 Ubuntu: VCF는 Ubuntu OS와 Kubernetes 기반 컨테이너를포함하는 통합 전체 스택을 제공하여 운영을 단순화하고 혁신을 가속화할 것입니다. 고객은 안정적인배포를 경험하고, 효율적인 패치 관리를 통해 모니터링, 검토, 우선 순위 지정 및 중요한 고위험 취약점을수정하는 강력한 프로세스를 통해 보장된 유지 관리와 향상된 보안을 누릴 수 있습니다.

VCF 최적화된 Ubuntu OS는 고객에게 추가 비용 없이 VCF 라이센스에 포함되어 있습니다.고객은 Canonical이 설정한 출시일로부터 5년 동안 Broadcom으로부터 VCF 최적화된 Ubuntu OS 이미지에대한 기업 등급 지원을 받습니다. 활성 VCF 라이센스가 있는 고객과 VCF 9.0을 실행 중인 고객은 솔루션카탈로그에서 Ubuntu OS LTS 릴리스 22.04부터 최적화된 Ubuntu OS 이미지에 접근할 수 있습니다:https://vcf.broadcom.com/vsc/services.

이 모듈에서는 Canonical 이미지 라이브러리를 VKS 서비스에 추가하는 과정을 안내합니다. 이를 통해 플랫폼엔지니어와 개발자는 VM 및 Pods에 대해 Ubuntu Linux 이미지를 활용할 수 있습니다.

이미지 카탈로그를 배포했습니다. 이 모듈에서는 이 실습에 이미지 카탈로그를 추가하기 위해 우리가수행한 단계를 안내합니다. 귀하의 환경에서의 단계는 유사할 것입니다.

# Firefox를 엽니다.

![](images/b8fd1017ea608263f94c3f2cce68ad240823f0bec33410ed0b9294fad8b98516.jpg)

Firefox 브라우저 창이 열려 있지 않은 경우:

1. 작업 표시줄에서 Firefox 아이콘을 클릭합니다.

HOL-2702-01-VCF-L

페이지 69

# VCF 자동화 공급자 포털

![](images/5cc8fcac6f4b4bacbe5ee2f827b10df71aa96b55c004d9b8855a6ce107b517d6.jpg)

Ubuntu 이미지를 VCF 자동화를 통해 사용자에게 제공하기 전에, VCF 자동화 관리자가 콘텐츠 라이브러리를추가하고 이를 사용할 수 있도록 해야 합니다. 이는 VCF에서 수행됩니다.

자동화 공급자 인터페이스에서.

1. Region A 브라우저 탭을 클릭합니다.
2. 클릭 VCF 자동화 - 공급자

HOL-2702-01-VCF-L

페이지 70

# 로그인

![](images/cd26b829e4e2466a0e3917fa53765966d14db6290def0b7354a56673f09facec.jpg)

1. 사용자 이름으로 admin 을 입력합니다.
2. 비밀번호로 VMware123!VMware123! 을 입력합니다.
3. 클릭 로그인.

HOL-2702-01-VCF-L

페이지 71

# 조직 선택

![](images/3f5e25b22949ef48617ee41ec5bec5f91add857f7aa0b08b5d8d7caef5e799e6.jpg)

# 1. 클릭 조직.

# Acme 선택

![](images/533104583f3c5a270132b140d4e3813003923dac8f0c6809f95fff12247def5a.jpg)

# 1. 클릭 Acme.

HOL-2702-01-VCF-L

페이지 72

# Canonical 구독 추가 - 1단계

![](images/38f51a517849086e5ad8d7a0c80bdc4af4204b1c602762139ce050d0eacfd52a.jpg)

1. 설정 을 클릭합니다.

HOL-2702-01-VCF-L

페이지 73

# Canonical 구독 추가 - 2단계

<table><tr><td>Overview</td><td colspan="2">Settings</td></tr><tr><td>Region Quota</td><td>EDIT</td><td>1</td></tr><tr><td>Networking</td><td colspan="2">✓ Subscription to content libraries</td></tr><tr><td>Load Balancing</td><td rowspan="2">Allow this organization to subscribe to external content libraries</td><td rowspan="2">Enabled</td></tr><tr><td>Metadata</td></tr><tr><td>First User</td><td>Allow this organization to subscribe to Canonical content libraries</td><td>Enabled</td></tr><tr><td>Settings</td><td colspan="2">✓ Antivirus</td></tr><tr><td></td><td>Allow blocking the upload of content library items</td><td>Disabled</td></tr></table>

1. 편집 을 클릭합니다.

HOL-2702-01-VCF-L

페이지 74

# Canonical 구독 추가 - 2단계

# Organization Settings

Subscription to content libraries

![](images/f6a8130c91641f7523d522214bd7052f688848e3583f1c0f7c3a2fa58f425be2.jpg)

![](images/a1205b035bdca104eab845d7a3891083372a3f118963d15f99b586fe425bfa5b.jpg)

![](images/c322ac94a795bf81d57fd5427f371f6ba0da1755c8472041803a61a5560d52ce.jpg)

![](images/b6cb0be74646c7c4c7f236d06e0e357d0439a363106d6c9bff8b786e5f13482c.jpg)

Antivirus

![](images/4ac9c1da799c196bb297a06cb85136915d4e57c2925e67dc51dfb5fb94c93fc4.jpg)

Allow blocking the upload of content library items

![](images/756dceaf8dce5c657684e007e8d58d8e4c29ea54a21337bafc3dadfbed807e0d.jpg)

1. 이 조직이 외부 콘텐츠 라이브러리에 구독할 수 있도록 허용 이 선택되어 있는지 확인합니다.
2. 이 조직이 Canonical 콘텐츠 라이브러리에 구독할 수 있도록 허용 이 선택되어 있는지 확인합니다.
3. 저장 을 클릭합니다.

# VCF 자동화 공급자 인터페이스에서 로그아웃

![](images/b2374a451d6e7b604a6b81eb20ec8fa40b5b6b34ab0fd3111b1c56ccd274e2ec.jpg)

HOL-2702-01-VCF-L

75페이지

VCF 자동화 소비자 인터페이스를 계속 진행하기 전에 VCF

자동화 공급자 인터페이스에서 로그아웃해야 합니다.

1. "admin" 옆의 down 화살표를 클릭합니다. (오른쪽 상단 모서리)
2. VCF 자동화 공급자 세션을 종료하려면 로그아웃 을 클릭합니다.

# VCF 자동화 조직 포털로 전환

![](images/7678778c6bb79e19bd9c4369bb56ec47a7d79a7d25c266f1a0663e6bd078e70b.jpg)

1. VCF 자동화 를 클릭합니다.

HOL-2702-01-VCF-L

76페이지

# VCF 자동화에 로그인

vmware

VMware Cloud Foundation

# Automation

Organization name

![](images/a8f17d6a6d542c0132247f29623e5d9bc8d39edbf86517e45dcd08522a991f47.jpg)

![](images/6721bcc7bec3227cff41d2fa1beec3d1f54ec3d3d78d9d964de21501b2e84e23.jpg)

CONTINUE

1. 조직 이름에 acme 를 입력합니다.
2. 계속하려면 CONTINUE 를 클릭하세요.

HOL-2702-01-VCF-L

77페이지

# 자격 증명 입력

![](images/35c12c87ece96f9728955d6d1a6457f32341bb1abc98d0ecf3d82d3dc705bf7f.jpg)

1. 사용자 이름으로 acme-admin 을 입력합니다.
2. 비밀번호로 VMware123!VMware123! 을 입력합니다.
3. 클릭 로그인.

# 콘텐츠 라이브러리 추가 - 1단계

![](images/084623f5f4001a77d8d6876d17f1466f6154af61ab90c80e0629e4ba049d31f5.jpg)

1. 빌드 및 배포 를 클릭합니다.

HOL-2702-01-VCF-L

78페이지

# 콘텐츠 라이브러리

![](images/1f277ee633bf1d5d0bf61c68e1546f72f796555adc10ec3a0169ee2c7faf74c8.jpg)

1. 콘텐츠 라이브러리 를 클릭합니다.

# 콘텐츠 라이브러리 추가 - 1단계

![](images/e0272d2eb35662788a7185daefe4c1e3539b8ae59117d637ec1a77f092ecd05a.jpg)

1. 새 콘텐츠 라이브러리를 생성하는 프로세스를 시작하려면 NEW 를 클릭합니다.

HOL-2702-01-VCF-L

79페이지

여기 이미 라이브러리가 생성되어 있는 것을 볼 수 있습니다. 이것은 우리가 당신을 위해 만든 것입니다. 이연습에서는 Canonical 라이브러리를 생성하기 위해 수행할 단계들을 안내합니다.실제로 생성하지는 않을 것입니다.

# 콘텐츠 라이브러리 생성

# Create a Content Library

1 holitest

Name *

Description

。

Type

① Use if you need the following capabilities

· Create content libraries specific to one or more projects
· Capture VM imagesas reusable blueprints
· Support OVA and OVF images

2

Subscribe to a library

1.  이 예제에서는 라이브러리 이름으로 holtest 를 사용했습니다.
2.  추가할 라이브러리에 구독하기 위해 슬라이더를 오른쪽으로 이동합니다.
3.  NEXT 를 클릭합니다(표시되지 않음).

HOL-2702-01-VCF-L

페이지 80

# 콘텐츠 라이브러리 추가 - 단계 2

![](images/a4ef993db54dc594841f03ff0d2d7dcf8a51e17e33a0f9a3b0d476784dac44d9.jpg)

1. Canonical 에 대한 라디오 버튼을 클릭합니다.
2. NEXT 를 클릭합니다.

![](images/be7074c12329b3de013ed564b6136625b5b07b0a8190e9a54d884eb20a398c0d.jpg)

1. 모든 현재 및 미래 프로젝트에 대한 읽기 권한을 상자에서 클릭하십시오.
2. NEXT 를 클릭합니다.

HOL-2702-01-VCF-L

페이지 81

# 콘텐츠 라이브러리 추가 - 단계 3

Create a Content Library

![](images/6d1ba4d9a9bdd1231fff8fa6553842790489edde2b0ed6c5c4a6245183373419.jpg)

1. 지역 dropdown 을 클릭합니다.
2. 여기서는 us-west 를 사용하고 있습니다.
3. 스토리지 정책 을 선택합니다.
4. NEXT 를 클릭합니다.

HOL-2702-01-VCF-L

페이지 82

# 콘텐츠 라이브러리 추가 - 단계 4

# Create a Content Library

![](images/82805c1ee2b388c78e170d296d166ce3c317d3d06bf7e531e2ab9f4cfe922bb8.jpg)

General

<table><tr><td>Name</td><td>holtest</td></tr><tr><td>Description</td><td>-</td></tr><tr><td>Auto Attach Namespaces</td><td>√ Yes</td></tr><tr><td>Canonical Library</td><td>√ Yes</td></tr></table>

us-west

<table><tr><td>Storage Class</td><td>vSAN Default Storage Policy</td></tr><tr><td>CONFIRM</td><td>CANCEL1</td></tr></table>

1. CANCEL 을 클릭합니다. 여기서는 콘텐츠 라이브러리를 생성하지 않으며 이미 생성되어 있습니다.

![](images/05140977df907910ef3c33931ee9ad31654fd9ab2cb248f871179e235851d348.jpg)

라이브러리 생성 프로세스는 최대 30분이 걸릴 수 있으며

이 랩의 리소스 제약으로 인해 실패할 수 있으므로 확인을 클릭하지 마십시오.

이로써 이 수업이 종료됩니다.

HOL-2702-01-VCF-L

83페이지

# VM 빠른 배포 v9.1

# Fast Deploy로 VM 배포 가속화

다음 몇 페이지에서는 VM Fast Deploy v9.1을 사용하는 과정을 안내합니다. VM Fast Deploy는데이터스토어별 이미지 캐싱 및 델타 디스크 기술을 활용하여 배포 지연 시간을 최소화함으로써 작업 부하전달을 가속화합니다.

# Firefox를 엽니다.

![](images/0f392a3fb0b094c0355761b79ea1ecc0b62c4c4d73c5bd8c9433d6a9ad843466.jpg)

Linux 작업 표시줄에서 Firefox 브라우저를 엽니다.

1. 브라우저를 열기 위해 Firefox 아이콘을 클릭합니다.

HOL-2702-01-VCF-L

84페이지

# VCF 자동화 콘솔 열기

![](images/0eff6e02e648e5c5166645aaa895172002f9f72686d76fde5fa3293bdefe849a.jpg)

VCF 자동화 포털로 이동합니다.

1. 지역 A 북마크 폴더 를 클릭합니다.
2. VCF 자동화 를 클릭합니다.

HOL-2702-01-VCF-L

85페이지

# VCF 자동화 콘솔에 로그인

VMware Cloud Foundation

Automation

Organization name

acme

CONTINUE

조직 이름은 이미 브라우저 창에 캐시되어 있어야 합니다.

VCF 자동화 조직 이름 프롬프트에서 다음 조직 정보를 선택합니다:

1.  조직 이름 드롭다운에서 acme 를 선택합니다.
2.  계속하려면 클릭하세요.

HOL-2702-01-VCF-L

페이지 86

# 로그인

VMware Cloud Foundation

Automation

ACME

![](images/91680e7516cf14b4b65ef4819f63c3e7a18d70f14ebb672589862e85ab83d10a.jpg)

 관리자 자격 증명은 이미 브라우저 창에 캐시되어 있어야 합니다.

VCF 자동화 로그인 프롬프트에서 다음 사용자 및 비밀번호 정보를 입력하십시오:

1.  로그인 방법 드롭다운에서 로컬 계정 을 선택하십시오.
2.  사용자 이름 필드에 acme-admin 을 입력하십시오.
3.  비밀번호 필드에 VMware123!VMware123! 을 입력하십시오.
4.  클릭 로그인.

HOL-2702-01-VCF-L

페이지 87

# 링크드 클론 배포

![](images/e0e06469d635f5f0decf7fb690f32b53fa784942256328224848ce3bcea32c7f.jpg)

1. 빌드 및 배포 클릭.
2. 클릭 가상 머신.
3. 클릭 + VM 생성.

HOL-2702-01-VCF-L

페이지 88

# Canonical 라이브러리에서 1 VM 배포

![](images/3a245d0b709ee51f35a5af6323fe99221decb9dbbb5d07e3da74fa2b39d234c3.jpg)

1. 클릭 OVF에서 배포.
2. 클릭 다음.

HOL-2702-01-VCF-L

페이지 89

# VM 클래스 및 VM 이미지

![](images/7996f41c223b13ff1b9f409c2ddd9ccea0759fe2890d23253bf8d03239ba17ae.jpg)

 1. VM 배포의 나머지 과정을 진행하면서 오른쪽의 YAML 파일 업데이트를 검토하십시오.

1.  VM 이름 입력 vm-1
2.  영역을 선택하십시오 z-Wld-a.
3.  이미지 선택 우분투 24.04 LTS - 노블 - 24.04.20251215.

HOL-2702-01-VCF-L

페이지 90

# VM 클래스 선택

# VMClass

![](images/de68921ff34fa2d6ae074c5ce7399b5cf1b4fe4ab560f7164754c53dde0472e8.jpg)

<table><tr><td></td><td>Name</td><td>CPUs</td><td>↑</td><td>CPU request/limit</td><td>Memory</td><td>Memory request/limit</td></tr><tr><td>○</td><td>best-effort-xsmall</td><td>2 vCPUs</td><td></td><td>No Reservation</td><td>2 GiB</td><td>No Reservation</td></tr><tr><td>●</td><td>best-effort-small</td><td>2 vCPUs</td><td></td><td>No Reservation</td><td>4 GiB</td><td>No Reservation</td></tr><tr><td>○</td><td>best-effort-medium</td><td>2 vCPUs</td><td></td><td>No Reservation</td><td>8 GiB</td><td>No Reservation</td></tr><tr><td>○</td><td>best-effort-large</td><td>4 vCPUs</td><td></td><td>No Reservation</td><td>16 GiB</td><td>No Reservation</td></tr><tr><td>○</td><td>best-effort-xlarge</td><td>4 vCPUs</td><td></td><td>No Reservation</td><td>32 GiB</td><td>No Reservation</td></tr><tr><td colspan="7"></td></tr><tr><td colspan="7"></td></tr></table>

![](images/afb05d900b6ae8376b7266b3f8fe3a8268dc8c516757f693a91a14baa7d4989e.jpg)

![](images/c3e47564cfaa6f97ce0f7e89c711c9ba5af8e6544fc15e9fc9de2b0386d3bad7.jpg)

![](images/d1d874f18071364ce7f6ac287190b1975a7710f7bbe806fb350ec15dc69fcf5d.jpg)

![](images/f66d470b97937c035118ee8449f074a622b9cf6534e240a86d1307348979482a.jpg)

Storage Class

Power State

![](images/78097f01250dd30f0243a5e95eded8483085afacec9982be0d39751fb1b8c696.jpg)

![](images/62172de83c0ee9687613afa0ecc378a3147a743450d36e1ba78832ad57b4137d.jpg)

REVIEW AND CONFIRM

 Canonical 우분투 마켓플레이스 이미지는 VCF 9.1에 내장된 이미지 템플릿입니다.

1.  VM 클래스 선택 최선의 노력-소형.
2.  선택 다음

# 로드 밸런서 추가

# Load Balancer

![](images/15ccff2efb325d6c762348e7cf1a49f736f17a2a1312af8a0a3f147790ba6b5c.jpg)

Selector

1.  선택 추가 드롭다운
2.  선택 새로 만들기 HOL-2702-01-VCF-L

페이지 91

# 로드 밸런서 구성

![](images/3db99e5d922c557f1af1d7e5a203472e050fa26a60b35c100fc240b038efa247.jpg)

1. 로드 밸런서 이름: vm-lb-1 설정
2. 포트 이름: ssh 설정
3. 포트: 22 설정
4. 대상: 22
5. 추가 클릭

# 로드 밸런서 검토

![](images/b10649151895820604a7eae58055f409528b33fbdc780b252716b5315811e74a.jpg)

HOL-2702-01-VCF-L

페이지 92

포트가 테이블에 추가되었음을 확인하십시오.

# 1.  저장 클릭

# 로드 밸런서 구성 보기

Load Balancer

![](images/81dbc6100b1eb73bbd1760175262f8950798c3088ced6bd6cda76e7e685ac631.jpg)

selector

vm-lb-1: vm-lb-selector

로드 밸런서가 구성되어 있음을 알립니다.

HOL-2702-01-VCF-L

93페이지

# 게스트 사용자 정의

# Guest Customization

configure additional users,run any custom scripts at boot time and much more.

![](images/0e6dffb8a8d0b2d530afc73651fe369ee17e1e1f7e7e3d7b2b532b65f1735294.jpg)

![](images/cb61c487cbb564878da54bad19e57137be7d4d90d745521fc1053d0ba084c151.jpg)

![](images/75a650942ed8b225974afaea534e53d0d38f29951396dd52f2235abf91baf4f1.jpg)

![](images/3434d30548e52a4a020049e65fb5673aa88becf59e616236ca070e2246751c4c.jpg)

1. CLOUD-INIT 을 선택하십시오.
2. 원시 구성 전환.
3. 아래 코드 블록을 붙여넣기
4. 다음 누르기

#cloud-config

ssh_pwauth: true

groups:

- 관리 그룹: [root,sys] nusers:
- 이름 : 데브옵스

gecos: Dev S. Ops

lock_passwd: 거짓

passwd: $6$6TAiq24JAIMWDhCz$3Q6RSoBHu1w17nVPy3tjaS.C5/

C1DCwD96r3vGgrOowdRlwU3jNP2QdhEUabkTbtVSx8u3GZKCAKNYvqNwZxH/

# 비밀번호가 Devops123!Devops123!로 설정되었습니다.

sudo: ALL=(ALL) NOPASSWD:ALL

ngroups: sudo, 사용자, 관리자

HOL-2702-01-VCF-L

페이지 94

쉘: /bin/bash

# 전역 네트워크 설정을 입력하십시오.

![](images/ff2488ae87dc600b4bd6b96f719c9a36025fc28ae91e75fee0ee943dbc851fee.jpg)

1. 호스트 이름: vm-1
2. 도메인 이름 설정: vcf.lab
3. 네임서버: 192.0.2.1
4. 검색 도메인: my.domain.local
5. 다음 클릭

HOL-2702-01-VCF-L

95페이지

# VM 배포

5.Review and Confirm

![](images/6bd27ad196144e1d0a304b5b429310fd34f41af5a17e175e5ba93850bcd19e17.jpg)

DEPLOY VM

# 1. 배포 VM 클릭

# VM 배포 보기

# Virtual Machine Service

![](images/4f74a1033701d10a874533777e3bab9e0e06c6156ded036980082e84dd6813b9.jpg)

+CREATEVM

<table><tr><td></td><td>Name</td><td>Status</td><td>Power State</td><td>Zone</td><td>Address</td><td>VM Group</td><td>VM Image</td><td>VM Class</td><td>Age</td></tr><tr><td> $\vdots$ </td><td>»</td><td>vm-1</td><td>Ready</td><td>Powered On</td><td>z-wld-a</td><td>--</td><td>Ubuntu 24.04 LTS - Noble - 24.04.20251215</td><td>best-effort-small</td><td>&lt; 1 min</td></tr></table>

 VM이 얼마나 빠르게 전원이 켜지고 사용 준비가 되는지 주목하세요.

# 빠른 배포 요약을 통한 VM 배포

이 섹션에서는 빠른 배포를 통한 VM 배포의 속도를 시연했습니다.

• VKS의 기초: VM 수준의 "빠른 배포" 최적화는 더 빠른

VKS 클러스터 프로비저닝의 주요 원동력입니다.

• 연결 모드(암호화되지 않음): 거의 즉각적인 전원 켜기를 위한 델타 디스크를 생성한 후백그라운드 디스크 승격이 이루어집니다.

•  직접 모드(암호화됨): 델타 디스크를 사용하지 않고 속도를 보장하는 암호화된 작업 부하를 위한용 경로입니다.

•  효율성: 로컬 데이터스토어 캐싱은 프로비저닝 중에 네트워크를 통해 대용량 이미지 파일을 이동하는 지연간을 제거합니다.

HOL-2702-01-VCF-L

페이지 96

# 대량 작업을 위한 VM 그룹화

# 집단 작업을 위해 VM을 함께 그룹화합니다.

다음 몇 페이지에서는 VM 서비스 그룹의 구성을 안내합니다. VM 서비스 그룹은 가상 머신 집합에 대한집단 작업 및 순차적 전원 켜기 로직을 가능하게 하여 관리를 간소화합니다.

# Firefox를 엽니다.

![](images/32956c7720a3d978834b08478648f0978ab1f7a300b19980188de30b70b04d35.jpg)

Linux 작업 표시줄에서 Firefox 브라우저를 엽니다.

1. 브라우저를 열기 위해 Firefox 아이콘을 클릭합니다.

HOL-2702-01-VCF-L

페이지 97

# VCF 자동화 콘솔 열기

![](images/22531da76a0e790d3723151bb98a7b060cdc435ec96dd651b1f406362b866553.jpg)

VCF 자동화 포털로 이동합니다.

1. 지역 A 북마크 폴더 를 클릭합니다.
2. VCF 자동화 를 클릭합니다.

HOL-2702-01-VCF-L

페이지 98

# VCF 자동화 콘솔에 로그인

VMware Cloud Foundation

Automation

Organization name

acme

CONTINUE

조직 이름은 이미 브라우저 창에 캐시되어 있어야 합니다.

VCF 자동화 조직 이름 프롬프트에서 다음 조직 정보를 선택합니다:

1.  조직 이름 드롭다운에서 acme 를 선택합니다.
2.  계속하려면 클릭하세요.

HOL-2702-01-VCF-L

페이지 99

# 로그인

VMware Cloud Foundation

Automation

ACME

![](images/4bb090b1ff7e3f38ac05f1c87a80888866c25af947c0f987fb79432b8f6d4d9e.jpg)

 관리자 자격 증명은 이미 브라우저 창에 캐시되어 있어야 합니다.

VCF 자동화 로그인 프롬프트에서 다음 사용자 및 비밀번호 정보를 입력하십시오:

1.  로그인 방법 드롭다운에서 로컬 계정 을 선택하십시오.
2.  사용자 이름 필드에 acme-admin 을 입력하십시오.
3.  비밀번호 필드에 VMware123!VMware123! 을 입력하십시오.
4.  클릭 로그인.

HOL-2702-01-VCF-L

페이지 100

# 그룹화를 위한 2번째 연결 클론 VM 배포

![](images/696a60706ba9d489ed48676868bc9ca4004e004a9abbbd00a13d129b9570e3c0.jpg)

1. 빌드 및 배포 클릭.
2. 클릭 가상 머신.
3. 클릭 + VM 생성.

HOL-2702-01-VCF-L

페이지 101

# OVF에서 배포

![](images/91d1cae0f3d1064e83400a330e8b0638858d6625d432a18e0771088226ae659a.jpg)

1. 클릭 OVF에서 배포.
2. 클릭 다음.

HOL-2702-01-VCF-L

페이지 102

# VM 클래스 및 VM 이미지

![](images/db94fc52c1be1ba4b719b74dc1262329a8e31b81b435a60b8a250a39c6cdb9df.jpg)

1. VM 이름 입력 vm-2
2. 영역을 선택하십시오 z-Wld-a.
3. 이미지 선택 우분투 24.04 LTS - 노블 - 24.04.20251215.

HOL-2702-01-VCF-L

페이지 103

# VM 클래스 선택

# VMClass

![](images/38ae9d3c368a3a4ced88aad840c584c34a0b64e26b1a41e72330fbdf11ec81b4.jpg)

<table><tr><td></td><td>Name</td><td>CPUs</td><td>↑</td><td>CPU request/limit</td><td>Memory</td><td>Memory request/limit</td></tr><tr><td>○</td><td>best-effort-xsmall</td><td>2 vCPUs</td><td></td><td>No Reservation</td><td>2 GiB</td><td>No Reservation</td></tr><tr><td>●</td><td>best-effort-small 1</td><td>2 vCPUs</td><td></td><td>No Reservation</td><td>4 GiB</td><td>No Reservation</td></tr><tr><td>○</td><td>best-effort-medium</td><td>2 vCPUs</td><td></td><td>No Reservation</td><td>8 GiB</td><td>No Reservation</td></tr><tr><td>○</td><td>best-effort-large</td><td>4 vCPUs</td><td></td><td>No Reservation</td><td>16 GiB</td><td>No Reservation</td></tr><tr><td>○</td><td>best-effort-xlarge</td><td>4 vCPUs</td><td></td><td>No Reservation</td><td>32 GiB</td><td>No Reservation</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td colspan="2">VM Classes per page 5 1-5 of 8 VM Classes |&lt; &lt; 1 / 2 &gt; |</td></tr></table>

Storage Class

Power State

![](images/8c6f861444e3cc67fa70394e5d2a6c5ed541f881e1ae9c937e95c4ca492e235f.jpg)

![](images/a3f885e454bbe433619e2acf71eb2801d55aadaaf79d8d5ef34ea848eb5bde8c.jpg)

REVIEW AND CONFIRM

1. VM 클래스 선택 최선의 노력-소형.
2. 선택 다음

# 기존 로드 밸런서 추가

Load Balancer

A VM can be exposed as a load-balanced service.

![](images/561271cad2ae4c1ee483a0fa334a17caf79d672f8336c0c4e5b617aeac051584.jpg)

1. 선택 추가
2. 선택 기존

HOL-2702-01-VCF-L

페이지 104

# 로드 밸런서 선택

![](images/ab52d9c8c45fcff961add6bb159813f20bb3a866d01068854141c568d9c30364.jpg)

1. 선택 vm-lb-1
2. 로드 밸런서를 추가를 선택하십시오.

HOL-2702-01-VCF-L

페이지 105

# 확인하고 다음을 클릭하십시오.

# Load Balancer

A VM can be exposed as a load-balanced service. The load balancer willroute traffic from

![](images/06acfe90975d48bb18faf832c357b75691454597d943e092ae45c2125f441ee1.jpg)

![](images/84b7a25a01ef4388d595267e329e774bce48e5ce891c97ff17a9f055cdf5a333.jpg)

# Guest Customization

You can specify any data, configuration or scripts in the bootstrap format that wil be used

<table><tr><td>NONE</td><td>CLOUD-INIT</td><td>SYSPREP</td><td>LINUXPREP</td><td>VAPPCONFIG</td></tr></table>

No guest customization is currently selected. Configuration options willappear here when

![](images/8e82b9a783ca7637b60df0b6e3f19ee36b9869772fb9626a2840c5420456a361.jpg)

1. 로드 밸런서를 확인하십시오.
2. 다음 클릭

HOL-2702-01-VCF-L

페이지 106

# 전역 네트워크 설정을 입력하십시오.

![](images/f68788056d5f8aa5a3a45a037e12e300e77b5db02ef2891e3f0988f16ee723cf.jpg)

![](images/ed9dd144c7f48ef03c1abf9cf88043f314eab7b1e2ddecf5c82ea8f757abb883.jpg)

# Network Interface

![](images/0f4afe9d9be00984bd79cb97b32ff211096eab85b41b11289f2f7187330a6bfe.jpg)

![](images/fff9683e1b3944305230303bdb9cd2042b3a5c663b45841fa1105b04e31b7142.jpg)

#

![](images/7db13d73b183d572a4d8ee9831791fa58ff7c7985114f8628e27a0ec3ced723a.jpg)

![](images/d6661c3cae1b087449289587151a4971c39b959f4a4c097420120cd0086b65f8.jpg)

Nameservers

Search Domains

![](images/b1512e2c761bd6dedd76b421cb53fab76fea99c949b4a98763690f4e9544c203.jpg)

![](images/4dcb5a9e08a49c7d4d4fdceeb4077f95f608b96b9b55a05a18d4df17f1ddb03d.jpg)

# Network Interface

![](images/03ba631a4789714777706062e7125ebf6717cf287a8fb941fe843f45e9f9abe0.jpg)

<table><tr><td></td><td>Name</td><td>Network</td><td>IP Address</td></tr><tr><td>:</td><td>eth0</td><td>vm-default</td><td></td></tr><tr><td></td><td></td><td></td><td>1 - 1 of 1 Network Interface</td></tr></table>

# Global Network Settings

Host Information

![](images/691fd3c451a769f1be7ed2e592f366f829ca77e4dec2230c18ea794964c0fe81.jpg)

Host Name

Domain Name ③

DNS Settings

![](images/c4425907de8d5a6bcbd3fd4a45543db993aa768fd6af6925be74a5da0fc9ed85.jpg)

Nameservers ①

Search Domains ①

![](images/38ddf3ce29dcb9f830c98c7a0c0e39fa41524df07c53a3e0c1b5c8cf9f50efa5.jpg)

![](images/41c562a30b5d4be24d18dc9b5382dfc6eba1093d906f8cdca4ad8b544c3546e8.jpg)

HOL-2702-01-VCF-L

페이지 107

1. 호스트 이름: vm-2
2. 도메인 이름 설정: vcf.lab
3. 네임서버: 192.0.2.2
4. 검색 도메인: my.domain.local
5. 다음 클릭

# VM 배포

![](images/3881fbb5e4cf8a9ee3969a3c8c097d787156dba7b9baf77cd7f9d954c5d4d00d.jpg)

1. VM 배포를 클릭하십시오.

HOL-2702-01-VCF-L

108페이지

# VM 그룹 만들기

![](images/f3d7cbad87200a65276a0bf9673b7c024aab69dc3acea83b5eac5bd3d0d5c655.jpg)

1. 가상 머신 서비스에서 VM 그룹 을 선택합니다.
2. 새 VM 그룹 을 선택합니다.

# 그룹 이름

![](images/c11580eb8d313a01a51d0e2cb354628929b55c58bdf849a3ff06f7c9434f6472.jpg)

HOL-2702-01-VCF-L

페이지 109

1. 그룹 이름을 설정합니다: vmg-1.
2. 클릭 다음.

# VM 선택

![](images/4c2187a4069bb7dfd2f66cc99deb95030d5cc92a31760a5ec721d1addef935b9.jpg)

1. 두 VM 을 선택합니다.
2. 클릭 다음.

# 시작 순서 설정

![](images/be1b8b5ecdca62549b48ce3b1cd0a415673b18b623dd85f6a7dcb9eb17c3dadd.jpg)

1. 웨이브 추가 를 클릭합니다.
2. 2차 웨이브 옆의 ⋮ n을 클릭하세요.
3. 웨이브로 VM 이동을 선택하세요.

HOL-2702-01-VCF-L

페이지 110

# 웨이브에 추가

![](images/2befb8289291cd9bf5d94e4045c2254b7474d63c4e4fb904f4cc64cc7aa3dc4e.jpg)

1. vm-2를 선택하세요.
2. 이동 을 클릭하세요.

# 지연 설정

![](images/0fdbf6e5218a232fb87d2a0e9d3088f2e1fb52bbbe9d9167dcffb48d6a642529.jpg)

1. 웨이브 2에 대한 지연 설정: 10
2. 오른쪽 창에서 이 섹션의 YAML 파일 업데이트를 확인하세요.
3. 다음 클릭

HOL-2702-01-VCF-L

페이지 111

# 검토

![](images/9859f8d438c43ff4e6858e5ff04a7f233498c5567f5c7c4b2341a1bd2bac591d.jpg)

# 1. 검토하고 완료 클릭

# VM 그룹 정책 테스트

![](images/02920b19a08f8d328084699f38bae5760357dbe8b3438cb6d8d25999a0860707.jpg)

1. vmg-1 옆의 ⋮ 클릭
2. 전원 끄기 선택 HOL-2702-01-VCF-L

112페이지

# VM 그룹 전원 끄기

![](images/d649428f8435ab3f25a5da174e09640067c4a3efe45080ca3a055f85d847c9ab.jpg)

# 1. 확인 클릭

# 작업 부하 도메인 vCenter에 대한 새 탭 열기.

![](images/53b9e0288d890fb7113ba0e6542d48734d2b1cee7a5a3efb1b5355be5a1589e0.jpg)

1. 새 Firefox 탭 열기.
2. 지역 A 북마크 선택.
3. 선택 vc-wld01-a 클라이언트.

HOL-2702-01-VCF-L

페이지 113

# vCenter에 로그인

![](images/4a5d5b48a3e358aa462ebdeb441f190facbb9741857d8a4ca740c8f6ffd2b5a7.jpg)

1. 사용자 계정을 입력하세요. administrator@wld.sso
2. 비밀번호를 입력하세요. VMware123!VMware123!
3. 로그인 클릭

HOL-2702-01-VCF-L

페이지 114

# 인벤토리 선택

![](images/ef8aa761362c1f208ecd47c51ddface92804f6c0f3e72bfa978b08cc4519a5fe.jpg)

1. 메뉴를 선택하세요.
2. 인벤토리 를 선택하세요.

HOL-2702-01-VCF-L

115페이지

# 최근 작업 보기

![](images/1994bf41d2c45ec4892a18edad95f45abf58508083ccfa3014eaeb6be79ccfea.jpg)

1. 전원 켜기를 선택할 때 이 위치에서 VM 그룹 작업을 볼 수 있도록 최근 작업 창이 표시되어 있는지인하십시오.

HOL-2702-01-VCF-L

페이지 116

# VCF 자동화 로드

![](images/ea5361117f7ddfd8af07eb2dd72b030579d306293c5bfb87d586c454c974d924.jpg)

1. 자동화 탭 로 돌아갑니다.
2. vmg-1 옆의 ⋮ 를 클릭합니다.
3. 전원 켜기 를 선택합니다.

# VM 그룹 전원 켜기

![](images/cd91cd9282781d94b65ac59bae85c29f4fd81784106a1b90f668515ad7a0d184.jpg)

# 1. 확인 클릭

HOL-2702-01-VCF-L

페이지 117

# vCenter로 전환

![](images/61e2371936e950595328e3c870fa2a6d0298447685d64aa517e32b64b2611f15.jpg)

1. vSphere 클라이언트로 돌아가서 최근 작업을 확인하세요.

vm-2의 배포 지연을 주목하세요.

# VM 그룹 요약

이 섹션에서는 VM 그룹을 만들고 그룹의 기본 관리를 단계별로 진행했습니다.추가 메모는 아래에 나열되어 있습니다.

집합 작업: 여러 VM에서 전원 관리(켜기/끄기/재시작)를동시에 수행합니다.
부팅 순서 지정: "웨이브"를 정의하여 종속성을 설정하고 서비스가올바른 순서로 시작되도록 합니다.
유연성: VM은 생성 시 그룹에 할당되거나 나중에 기존그룹에 추가될 수 있습니다.
•  청사진 준비 완료: 네임스페이스를 응집력 있고 반복 가능한

애플리케이션 스택으로 취급하는 과정을 단순화합니다.

HOL-2702-01-VCF-L

페이지 118

# UI를 사용하여 VM의 스냅샷을 생성합니다.

# 소비자 인터페이스에서 직접 스냅샷 작업 수행

VCF 9.1은 소비자에게 셀프 서비스 스냅샷 관리를 제공하여 소비자가 소비자 인터페이스에서 직접워크로드를 보호하고 복원할 수 있도록 합니다.

# Firefox를 엽니다.

![](images/fe92933da27ed08f0e62bccc04d92dfe719570f0d217e2a2f90766e2e8b38b84.jpg)

Linux 작업 표시줄에서 Firefox 브라우저를 엽니다.

1. 브라우저를 열기 위해 Firefox 아이콘을 클릭합니다.

HOL-2702-01-VCF-L

페이지 119

# 워크로드 클라이언트 콘솔 열기

![](images/310fd98d27c1abc58d17a2ad1cc2d095b7984387ffb0aa9b74063de41813fe36.jpg)

VCF 워크로드 클라이언트로 이동합니다.

1. 지역 A 북마크 폴더를 클릭합니다.
2. vw-wld01-a 클라이언트를 클릭합니다.

HOL-2702-01-VCF-L

페이지 120

# vCenter에 로그인

![](images/53c854497ff5620a9996c38cb1431e6be6ebe2a924ee64abed8a3349fdeb16ff.jpg)

워크로드 vCenter 로그인 프롬프트에서 다음 사용자 및 비밀번호 정보를 입력합니다:

1. 사용자 이름 필드에 administrator@wld.sso를 입력합니다.
2. 비밀번호 필드에 VMware123!VMware123! 을 입력하십시오.
3. 클릭 로그인.

HOL-2702-01-VCF-L

페이지 121

# VCF 자동화 콘솔 열기

![](images/6a100497ab5e5e8dba8dbfec4591148c5b6282e596ad8551394b7b55f32eeb28.jpg)

1. 같은 Firefox 브라우저에서 새 탭 열기.
2. 지역 A 북마크 폴더를 클릭합니다.
3. VCF 자동화 를 클릭합니다.

HOL-2702-01-VCF-L

페이지 122

# VCF 자동화에 로그인

VMware Cloud Foundation

Automation

ACME

![](images/12e2775066af499fcc2683587a204e946588f9e5afc3fe3b371011ef3db6ab78.jpg)

 관리자 자격 증명은 이미 브라우저 창에 캐시되어 있어야 합니다.

VCF 자동화 로그인 프롬프트에서 다음 사용자 및 비밀번호 정보를 입력하십시오:

1.  로그인 방법 드롭다운에서 로컬 계정 을 선택하십시오.
2.  사용자 이름 필드에 acme-admin 을 입력하십시오.
3.  비밀번호 필드에 VMware123!VMware123! 을 입력하십시오.
4.  클릭 로그인.

HOL-2702-01-VCF-L

페이지 123

# 조직 이름 선택

![](images/9f6a15328ec5597fdcf8da6f62f522438a54daa8a77db3ba2de2d1a2439f7c08.jpg)

조직 이름은 이미 브라우저 창에 캐시되어 있어야 합니다.

VCF 자동화 조직 이름 프롬프트에서 다음 조직 정보를 선택합니다:

1.  조직 이름 드롭다운에서 acme 입력.
2.  계속하기 클릭.

HOL-2702-01-VCF-L

페이지 124

# 빌드 및 배포

![](images/a285816c634b1f47e12df77c046b61b9b10caf3ba6ef20c8fdde628ac9c61ccf.jpg)

1. 자동화 콘솔에서 빌드 및 배포 선택
2. 가상 머신 선택
3. vm-1 링크 선택.

HOL-2702-01-VCF-L

125페이지

# 네트워크 서비스

![](images/9997321b21d49b3a0a3b7be9ac36df45bde613fbd1ad507aea54e5790abfe073.jpg)

1. 네트워크 서비스 선택: vm-lb-1 링크.

# 외부 IP 주의

![](images/da7342a73d9f5915b3fb9aa6f2c4809c77b9672ca7cac67195c67718ce31576e.jpg)

1. 외부 IP 주의: 10.1.9.7 HOL-2702-01-VCF-L

126페이지

# 터미널 열기

![](images/650939b863a3bd3c3ff778ca9cd2a050bf2bc16fd1a83223b9d63322f9f634a4.jpg)

1. 터미널을 엽니다.

# 파일 터치

![](images/cc2d33d38cdabe99b2623eb62155ecb05768af076996a0f3493f91c320b5b314.jpg)

1. devops 사용자와 외부 포트를 사용하여 vm-1에 SSH 접속: ssh devops@10.1.9.7
2. 비밀번호 입력: Devops123!Devops123!
3. 파일 보기: ls 파일이 없음을 확인하세요
4. 파일 생성: touch test
5. 파일 test 보기: ls

HOL-2702-01-VCF-L

페이지 127

# VM 선택

![](images/3c2844ee4860a96ed03dfa2714d0975b9b151ade87f1dccb898a57b41deffc63.jpg)

1. 자동화 콘솔에서 빌드 및 배포 선택
2. 가상 머신 선택
3. vm-1 링크 선택.

# 스냅샷 찍기

![](images/8f0a8d76d71436e23267f2705988643902b641892bace94bfafdb1f8f9cd5ae0.jpg)

# 1. 스냅샷 선택 HOL-2702-01-VCF-L

페이지 128

# 2. 선택 스냅샷 찍기 링크

# 스냅샷 만들기

![](images/bacae6c9a4476e6663a347247384a70f903da87e5cc7830ebddb4037208d9e2a.jpg)

# 1. 선택 생성

HOL-2702-01-VCF-L

페이지 129

# 스냅샷 검토

![](images/18ab19036948a7f5539cfab659407e3f9260708a42e72a77769b210d458d6384.jpg)

vm-1

![](images/99ab3ff46a08d5529d5ebaf4bee55b78a69718cbc4094677a200441b6839b4c6.jpg)

![](images/2f05838146aa577dcafe25aa8f9d2ffda9f3961d03de8510c3ab7b0dabdb7d74.jpg)

![](images/ef3c93614faafee3bab632fe2ecf2c159979c8a173d3dafd7204caee8b1f5f92.jpg)

Snapshot size

0.27 MiB

0.27 MiB

스냅샷 정보를 검토합니다.

# 테스트 파일 제거

![](images/6ecc564c669efc78ed8003e0d994686bc04d78ff0877b4ceb603a58e389f5126.jpg)

1.  터미널에 입력 rm -rf test 하여 test 파일을 제거합니다.
2.  입력 ls 하여 파일이 제거되었는지 확인합니다.

HOL-2702-01-VCF-L

페이지 130

# 스냅샷 되돌리기

![](images/f8934bf8f36a6f1807d8aedb90759203eaf58f25a44821a4d8f321b46023cea7.jpg)

![](images/bb6c2c52ec747fe0d6f605c0e41dbebd479ff24cbb4866c02ffa45767c4a32ef.jpg)

1. 자동화 콘솔에서 되돌리기 를 선택합니다.
2. 작업을 확인하려면 되돌리기 를 선택합니다.

HOL-2702-01-VCF-L

페이지 131

# vCenter로 전환

![](images/8b7ef28dce03d5552d3ac49da2b13cc21bf7f0c43d9fc0e1de2d12e9255df6d2.jpg)

Firefox에서 vSphere 탭으로 전환하고 VM 상태 및 최근 작업을 검토합니다.

1. Firefox에서 vSphere 탭 을 선택합니다.
2. vm-1 로 이동합니다.
3. 되돌려진 vm-1이 전원이 꺼져 있습니다.
4. 최근 작업 으로 이동합니다.
5. vm-1 에 대한 스냅샷 활동을 보려면 스크롤합니다.

HOL-2702-01-VCF-L

132페이지

# 자동화 콘솔로 돌아가기

![](images/6eb9f54d035815c33d7c5f98ab6cb001d1b30854053b64dd06758933d845389d.jpg)

1. 자동화 탭을 선택합니다.
2. VM 세부정보를 선택합니다.
3. 스위치를 전환하여 VM의 전원을 켭니다.

# 전원 켜기 확인

![](images/1316538e085be2ffdbf37ecb07ab9b52dfedbd6a8e4e9f4e076b8de4a81479fd.jpg)

1. 확인을 클릭합니다. HOL-2702-01-VCF-L

페이지 133

# 부팅 관찰

![](images/0f93d99c56491c07767c416fa8284b3631a221303b11b907ef2bd28909bccae5.jpg)

![](images/7198f130feef99870a8575923f60d1912fdac6939f746ec822174a33e176705b.jpg)

1. 부팅 프로세스를 보려면 웹 콘솔 열기를 클릭합니다.

HOL-2702-01-VCF-L

페이지 134

테스트 파일이 복원되었는지 확인하십시오.

![](images/f326208f712e92344390b806424902a6d2ef073d28b258bbbd7a6c0bd502c02f.jpg)

1. devops 사용자와 외부 포트를 사용하여 vm-1에 대한 SSh 세션을 재설정하십시오:

ssh

세대 EVO PS@10.1.9.7

2. 비밀번호 입력: Devops123!Devops123!
3. 파일을 보려면 다음을 입력하십시오: ls
4. test 파일이 돌아왔습니다.

# 소비 인터페이스 스냅샷 요약.

이 섹션에서는 소비 인터페이스에서 스냅샷 및 복구를 수행하는 프로세스가 시연되었습니다.

# 노트:

• 셀프 서비스: 스냅샷 수명 주기 관리를 관리자에서 최종 사용자(소비자)로 이동합니다.
• 마찰 감소: 일상적인 데이터 보호 작업에 대한 관리 개입의 필요성을 없앱니다.
• 직접 작업: UI에서 스냅샷 찍기, 편집, 되돌리기 및 삭제를 지원합니다.

HOL-2702-01-VCF-L

135페이지

• 가시성: 소비자는 스냅샷 크기, 생성 시간 및

메모리/정지 포함 여부와 같은 주요 세부정보를 볼 수 있습니다.

HOL-2702-01-VCF-L

136페이지

# 네트워크 가변성

# VM 서비스 2일차 네트워크 가변성

이전에는 네트워크 구성은 일반적으로 프로비저닝 시점에 정의되었습니다. 이제, 기존 VM의 소비인터페이스를 통해 네트워크 인터페이스를 직접 추가, 제거 또는 편집할 수 있게 되었습니다. 이는전체 작업 부하를 재배포하지 않고도 연결성을 쉽게 조정하거나 다중 홈 애플리케이션을 확장할 수 있음을의미합니다. 이러한 변경 사항은 게스트 내에서 적용되기 위해 간단한 전원 사이클이 필요하지만, 가상머신의 장기 수명 주기를 관리하는 데 훨씬 더 간소화된 경로를 제공합니다.

# Firefox를 엽니다.

![](images/aff24fedff1f79ca1511743018eb7c2cdddcb07e001a34f4e8cbd3663b3312f7.jpg)

Linux 작업 표시줄에서 Firefox 브라우저를 엽니다.

1. 브라우저를 열기 위해 Firefox 아이콘을 클릭합니다.

HOL-2702-01-VCF-L

137페이지

# Firefox 탭에서 VCF 자동화 콘솔을 엽니다.

![](images/11ad1feb6eadd6a95f16eda58349cd08ad86e794ada4bed756a37d7249e16166.jpg)

1. 같은 Firefox 브라우저에서 두 번째 탭을 엽니다.
2. 지역 A 북마크 폴더를 클릭합니다.
3. VCF 자동화 를 클릭합니다.

HOL-2702-01-VCF-L

페이지 138

# 조직 선택

![](images/aa4ca747b8f7e5ada39cac2f6ccf36fddddcf5a5e1ac72774f640ea878eb8709.jpg)

조직 이름은 이미 브라우저 창에 캐시되어 있어야 합니다.

VCF 자동화 조직 이름 프롬프트에서 다음 조직 정보를 선택합니다:

1.  조직 이름 드롭다운에서 acme 입력.
2.  계속하기 클릭.

HOL-2702-01-VCF-L

페이지 139

# 로그인

VMware Cloud Foundation

# Automation

ACME

Change Organization

![](images/c6f5e8403e4f1a05c82ccf1f9ba391000df2f8e228eb404e43e27684eba299d3.jpg)

 관리자 자격 증명은 이미 브라우저 창에 캐시되어 있어야 합니다.

VCF 자동화 로그인 프롬프트에서 다음 사용자 및 비밀번호 정보를 입력하십시오:

1.  로그인 방법 드롭다운에서 로컬 계정 을 선택합니다. (표시되지 않음)
2.  사용자 이름 필드에 acme-admin 을 입력하십시오.
3.  비밀번호 필드에 VMware123!VMware123! 을 입력하십시오.
4.  클릭 로그인.

HOL-2702-01-VCF-L

페이지 140

# VM 선택

![](images/a1df0e849af3a46178f35d1d3224467257bf23d887d0045f12fbd0a5f4bc6458.jpg)

1. 자동화 콘솔에서 빌드 및 배포 를 선택합니다.
2. 가상 머신 을 선택합니다.
3. vn-1 을 선택합니다.

# 네트워크 인터페이스 추가

![](images/542c6fc3d5bbb960779922217f3ff98cbd6c0890eaf891d54fa253ff73da87df.jpg)

HOL-2702-01-VCF-L

페이지 141

![](images/dbc389423b6de5352235b99f9270061bce3bc58b3a0e1978222b7dc569b5b2ce.jpg)

1. VM 세부정보 탭에서 아래로 스크롤합니다.
2. 네트워크 인터페이스 섹션을 찾습니다.
3. 네트워크 인터페이스 추가 를 클릭합니다.

인터페이스의 이름을 지정하고 네트워크를 선택합니다.

![](images/6d6b6a4dc3f504b759e8d44cefe08aae494410829fef408a7216690534a20be8.jpg)

1. 이름: eth1 입력
2. rc-testnet 네트워크를 선택합니다.

HOL-2702-01-VCF-L

페이지 142

3. 추가 를 클릭합니다.

# 알림 검토

![](images/4bf9a7abf33b39f0a2300dfc079d366d58cbca9782793d197751e999789e1dc4.jpg)

1. 정보 상자를 검토하십시오.

# VM 전원 끄기

![](images/c721bc7a6a3894d77efb69e88f53880f5a4d334b58030059d2165dfa67b9357d.jpg)

1. 위로 스크롤하고 VM의 전원을 끄십시오.

HOL-2702-01-VCF-L

143페이지

# 전원 끄기 확인

![](images/419b644acd0cf5b363ef092bb8242484a662e92cf5955db5acec0908af30c5d6.jpg)

1. 확인을 클릭합니다.

# VM 전원 켜기

![](images/6af4286eff9c3d972eef0302ba2c1e054a8fe75b875febdae019ee9c267ec956.jpg)

1. VM의 전원을 켜십시오.

HOL-2702-01-VCF-L

144페이지

# 전원 켜기 확인

![](images/e6153ad99f4d81f51d3f748e5e705f79bfd1a6164aea28163ca1848e3f9f9255.jpg)

1. 확인 을 클릭하십시오.

# 네트워크 유효성 검사

![](images/26fca93113b3a05e6e8e576b4a806672ee822cbcb14e2f9626332950b5427cb3.jpg)

1. 네트워크 설정으로 스크롤 다운하세요.
2. 유효성 검사 eth1 가 보이고 rc-testnet에 연결되어 있습니다.

# VM 서비스 2일차 네트워크 변경 가능성 요약

이 섹션에서는 기존 VM 배포에 대한 네트워크 변경을 시연했습니다.

HOL-2702-01-VCF-L

145페이지

• 향상된 유연성: 배포 후 네트워크 수정(추가/제거/편집)을

기존 VM에서 가능하게 합니다.

• 라이프사이클 관리: 전체

작업 재배포 없이 진화하는 애플리케이션 요구 사항을 지원합니다.

• 운영 단계: VM 하드웨어 구성 내에서 네트워크 변경을 완료하기 위해 전원 사이클이 필요합니다.

• 사용자 경험: UI에서 간단하고 직관적인 "네트워크 인터페이스 추가" 워크플로를 통해 관리됩니다.

HOL-2702-01-VCF-L

146페이지

# 모듈 결론

모듈 3이 종료됩니다.

여기에서 다음을 수행할 수 있습니다:

• 다음 랩 모듈로 계속 진행하십시오.
이

랩의 모든 모듈이나 수업으로 이동하려면 [vlp:table-of-contents|목차 표시]를 클릭하세요.

• 랩을 종료하고 나중에 돌아오십시오.

HOL-2702-01-VCF-L

페이지 147

# 모듈 4 - 새로운 컨테이너서비스 (15분)중급

HOL-2702-01-VCF-L

페이지 148

# 모듈 소개

이 모듈은 참가자들에게 vSphere Pods를 소개합니다. 이는 VMware Cloud Foundation 9.1의새로운 기능으로, 전체 Kubernetes 클러스터를 구성하는 오버헤드 없이 격리된 컨테이너를 배포할 수있게 해줍니다. 참가자들은 VCF 자동화 포털에서 리소스 예약 및 네임스페이스 구성을 제공자 측에서설정한 후, vSphere Pod를 처음부터 끝까지 배포하고 VCF 자동화 및 vSphere 클라이언트를 통해 생성과정을 모니터링합니다. 단 15분 만에 참가자들은 VCF 9.1에서 전체 클러스터 배포의 실용적인대안으로 경량 컨테이너 서비스를 언제 어떻게 사용할 수 있는지에 대한 명확한 이해를 얻게 됩니다.

HOL-2702-01-VCF-L

페이지 149

# 컨테이너 서비스 소개

여기에 서비스가 무엇인지 추가하십시오.

# Firefox를 엽니다.

![](images/1724b1f9bff27f13f40f877260db2313f9fa129ae00bcfdf1b2709fb2fb5d81f.jpg)

이전 단계에서 Firefox가 열려 있지 않은 경우, Linux 작업 표시줄에서 Firefox 브라우저를 엽니다.

1. 브라우저를 열기 위해 Firefox 아이콘을 클릭합니다.

# VCF 자동화 열기

![](images/35084678f26e904e96776be889d6cb086b9f29eee02345abca7680c1ec88eb49.jpg)

1. 새 Firefox 브라우저 tab 을 엽니다.
2. VCF 자동화 를 클릭합니다.

HOL-2702-01-VCF-L

페이지 150

# 조직 입력

![](images/aded2b5279ebced42bbf80411042fd5ab33655652d069d36161fad8a25d23220.jpg)

1. 조직 이름으로 acme 를 입력합니다.
2. 계속 을 클릭합니다.

HOL-2702-01-VCF-L

페이지 151

# VCF 자동화에 로그인

VMware Cloud Foundation

# Automation

ACME

![](images/565dbfb8261948af1d363d39925e00a9369d8fcdc21f5885f26eeb97fc43d96c.jpg)

1. 로그인 이름으로 acme-admin 를 입력합니다.
2. 비밀번호로 VMware123!VMware123! 를 입력합니다.
3. 로그인 을 클릭합니다.

HOL-2702-01-VCF-L

페이지 152

# 사용 가능한 서비스 검토

![](images/73b085c1cc3bad6c52a5e2518f469bf9c5a1a957278ef0880774a3bd3160743d.jpg)

사용 가능한 서비스를 검토합니다. 이 랩에서는 vSphere Pod를 배포할 것입니다. 그러나 kubernetes 클러스터,가상 머신 및 기타 서비스도 배포할 수 있습니다.

VCF 자동화의 "빌드 및 배포" 탭에서 사용 가능한 서비스를 검토할 수도 있습니다.

HOL-2702-01-VCF-L

페이지 153

# 빌드 및 배포 옵션 검토

![](images/25b2593efd0bc1811bb9a9adf7de5fd0a93373a23685cbcaa4f1808069f39ce8.jpg)

1. 빌드 및 배포 를 클릭합니다.

HOL-2702-01-VCF-L

페이지 154

# 서비스

![](images/eeeff78477d34250b337689ffde8ea1ee122e28680f238968ce1970393c6e6fd.jpg)

1. 사용 가능한 서비스를 표시하려면 > 를 확장하십시오.

HOL-2702-01-VCF-L

페이지 155

# 사용 가능한 서비스 검토

![](images/5fa100e0a278d369816671ee2f1e9de0eb5b6381586924b3536c559e0b196dd1.jpg)

여기에서 vSphere Kubernetes 서비스(VKS)에 추가할 수 있는 서비스 목록을 볼 수 있습니다. 다음모듈에서는 VMware vSphere Kubernetes 서비스(VKS) 컨테이너 서비스를 생성하는 과정을 안내합니다.

HOL-2702-01-VCF-L

페이지 156

# VCF 자동화에서 로그아웃

![](images/798a63514ed12e8f1544e1eb45739acfee684c2fbcb60af9ae729dfc1e0f36de.jpg)

1. VCF 자동화 창의 오른쪽 상단 모서리에 있는 acme-admin 옆의 아래 화살표를 클릭하십시오.
2. 로그아웃 을 클릭하십시오.

VCF 자동화 사용자 인터페이스에서 로그아웃해야 VCF 자동화 공급자 인터페이스에 다시 로그인할있습니다.

# VMware vSphere 쿠버네티스 서비스 컨테이너 서비스 소개

VCF 9.1 릴리스의 새로운 기능은 컨테이너 서비스로, VKS 클러스터의 일부가 아니거나 쿠버네티스에 의해관리되지 않는 격리된 컨테이너를 배포할 수 있는 기능입니다. 때때로 배포는 전체 클러스터를 생성하는 오버헤드없이 단지 파드(pod)만 필요하며, 이를 vSphere 파드라고 합니다.

vSphere 파드는 ESXI 노드에서 직접 실행되며 일반 컨테이너처럼 취급됩니다. 예를 들어, vSphere 파드에영구 볼륨을 연결할 수 있습니다.

HOL-2702-01-VCF-L

페이지 157

vSphere 파드는 기본적으로 안전하고 격리된 컨테이너입니다. 리눅스 커널을 공유하는 표준 컨테이너와 달리,vSphere 파드는 경량 VM 경계(CRX) 내에서 실행됩니다. 이는 민감한 작업 부하에 대해 하드웨어 수준의격리를 즉시 제공하여 "시끄러운 이웃" 및 공유 커널의 보안 위험을 제거합니다.

vSphere Pods는 클러스터 관리의 복잡성 없이 쿠버네티스 기능을 제공합니다. 이는 컨테이너화된 레거시앱을 보유한 앱 현대화 여정에 있는 고객을 대상으로 하며(하지만 아직 완전히 12-팩터는 아닙니다), 이를통해 전용 K8s 클러스터나 제어 평면을 관리하는 오버헤드를 제거하고 Kubernetes API를 통해 직접Supervisor에 배포할 수 있습니다.

vSphere Pods는 ESX(슈퍼바이저)에서 직접 실행되며, 게스트 OS 계층을 완전히 우회합니다. 이를 통해하이퍼바이저가 워크로드를 직접 스케줄링할 수 있어 지연 시간을 줄이고 성능이 중요한 앱의 처리량을극대화합니다.

이 기능을 사용하기 전에 CPU 및 메모리 예약을 설정해야 합니다. 이 랩에서는 예약 설정 방법을 안내할것입니다.

# Firefox를 엽니다.

![](images/a4f59645012f2b1b1b43dccdbf270e8d4ab37be89114e0905f69f474642d5f0a.jpg)

이전 단계에서 Firefox가 열려 있지 않은 경우, Linux 작업 표시줄에서 Firefox 브라우저를 엽니다.

1. 브라우저를 열기 위해 Firefox 아이콘을 클릭합니다.

HOL-2702-01-VCF-L

페이지 158

# VCF 자동화 열기

![](images/e24686d575b65e8a959b2125d37195c5eb5b82e1d656e084eb22519655c9a59d.jpg)

vSphere Pods 기능을 사용하기 전에 VCF 자동화 관리자가 귀하의 조직 및 네임스페이스에 대한 예약을VCF 자동화 공급자 포털에서 설정해야 합니다. 이 섹션에서는 그 방법을 안내할 것입니다. 이 섹션에서는 VCF자동화의 공급자 포털로 전환하고 있습니다.

1. 새 Firefox 브라우저 탭을 엽니다.
2. VCF 자동화 - 공급자 를 클릭합니다. 이는 VCF 자동화 포털과는 다른 포털입니다.

HOL-2702-01-VCF-L

페이지 159

# VCF 자동화 공급자 포털에 로그인

![](images/fa4e3de254d7cd043d3a01773725e9c02d211e9950021a1bf86121163c7c31a3.jpg)

1. 로그인으로 admin 을 입력합니다.
2. 비밀번호로 VMware123!VMware123! 를 입력합니다.
3. 클릭 로그인.

HOL-2702-01-VCF-L

페이지 160

# ACME 조직으로 진행

![](images/a95afda0dbf1e23e1bfdc1c712864fa1221dfdc0684f41eb57bbd41e42d4fbbd.jpg)

이것은 공급자 인터페이스를 위한 VCF 자동화의 랜딩 페이지입니다.

# 1. 클릭 조직.

1개의 조직을 보여주는 상자에서 "조직"을 클릭할 수도 있습니다.

HOL-2702-01-VCF-L

페이지 161

# 조직 선택

![](images/18bdebed47827148c0a5ebf3849649f2569902e3a08c5d176625c06971066d53.jpg)

# 1. 클릭 Acme.

# 지역 할당량 설정

![](images/f823f84657452177864c1a393212b78847be37e597bbf42771a256a19549ac34.jpg)

# 1. 클릭 지역 할당량.

HOL-2702-01-VCF-L

페이지 162

# 지역 확장

![](images/69f64d9c43962769c46edc1e914ff0a732f7e3308ba7fb5f5b01fd5bd5597fd1.jpg)

# 1. 클릭 >>.

# CPU 예약 주의

![](images/a9253a982b7f21be881c2398768b4242652a47d690486bba4a2e0453733341ba.jpg)

현재 설정된 CPU 예약이 없습니다. CPU 예약이 설정되지 않았기 때문에 이 조직에서 생성된네임스페이스는 CPU 예약이 설정되지 않으며, 조직 수준에서 설정되지 않았기 때문에설정할 수 있는 능력도 없습니다.

HOL-2702-01-VCF-L

페이지 163

# 지역 할당량 설정 계속

![](images/9aeb7eb5165a07aa57005b55195de1539e389b187ee5d5c84cfcdf0caf53295e.jpg)

용량이 보일 때까지 아래로 스크롤합니다.

1. 클릭 용량 추가 . 아래로 스크롤해야 할 수도 있습니다.

# 제한 설정

![](images/4932defbeb1bc57cfd08d89990e9576f8c60f1d42ef24f0670417f6656b65342.jpg)

1. 모든 영역 추가 체크박스를 클릭하십시오 (이는 실제 배포에 적용될 수도 있고 적용되지 않을 수도 있습니다).
2. CPU 한도를 40 으로 설정하십시오.
3. 메모리 한도를 160 으로 설정하십시오.
4. CPU 한도가 GHz로 설정되었고 메모리 한도가 GB로 설정되었는지 확인하십시오.

HOL-2702-01-VCF-L

페이지 164

# 지역 할당량 설정 계속

![](images/b49f4b84242de847f210191ed241bac8fc7012cf5952fef0e6bd30c8db81de2c.jpg)

1. CPU 예약을 일부 값으로 설정하십시오. 여기서는 30 을 사용했습니다.
2. 메모리 예약을 일부 값으로 설정하십시오. 여기서는 100 을 사용했습니다.
3. 저장 을 클릭합니다.
4. CPU와 메모리 예약이 모두 GHz로 설정되었는지 확인하십시오.

# 값 확인

# Region Quota

NEW

<table><tr><td></td><td></td><td>Region</td><td>Status</td><td>Supervisors</td><td>Zones</td><td>CPU Limit</td><td>CPU Reservation</td><td>Memory Limit</td><td>Memory Reservation</td></tr><tr><td> $\gg$ </td><td> $\vdots$ </td><td>us-west</td><td> $\checkmark$  Ready</td><td>supervisor-wld...</td><td>1</td><td>40 GHz</td><td>30 GHz</td><td>160 GB</td><td>100 GB</td></tr></table>

HOL-2702-01-VCF-L

페이지 165

CPU 및 메모리 예약이 새 값으로 설정되었음을 유의하십시오. 이제 VCF 사용자 자동화 콘솔로 이동하여 새네임스페이스를 만들고 vSphere 포드를 생성할 수 있습니다.

# VCF 자동화 공급자 콘솔에서 로그아웃

![](images/894ddef702c623b478b9bef020e025e981f5b4ecd6315965a7ce9921b45ae074.jpg)

이제 VCF 자동화 공급자 콘솔에서 더 이상 변경할 필요가 없으므로 VCF 자동화에서 사용자 보기 창을 열 수있도록 로그아웃해야 합니다.

1. 관리자 오른쪽의 down 화살표 를 클릭하십시오.
2. 로그아웃 을 클릭하십시오.

# VCF 자동화 콘솔 열기

![](images/4a071f05a26e29286a7e34ce6f3a46374c5055c5513bd37c0d0db56692383cf0.jpg)

Firefox가 로드되면:

1. 지역 A 북마크 폴더 를 클릭합니다.

HOL-2702-01-VCF-L

페이지 166

# 2. VCF 자동화 를 클릭하십시오.

# 조직 입력

![](images/c447d559dc565085294c76e122a1762a52312c2a240c233d20363c9a4300a281.jpg)

1. 조직 이름으로 acme 를 입력하십시오.

HOL-2702-01-VCF-L

페이지 167

# 로그인

![](images/03bd29fcc9c2470dae91b3d10613fcc5e1723d03546b3239f8d689b43bb78bf1.jpg)

1. 로그인 이름으로 acme-admin 를 입력합니다.
2. 비밀번호로 VMware123!VMware123! 를 입력합니다.
3. 클릭 로그인.

# 관리 및 거버넌스

![](images/05b148ba7f849068e2130f08361146bdb67407284f59ae5c593c38f99e634b0f.jpg)

HOL-2702-01-VCF-L

168페이지

vSphere 포드를 생성하기 위해 새로운 네임스페이스를 만들기 전에, 우리가 생성할 네임스페이스의네임스페이스 클래스에 메모리 및 CPU 예약이 설정되어 있는지 확인해야 합니다. 네임스페이스 클래스는네임스페이스에 할당된 리소스에 대한 티셔츠와 같은 크기를 가지고 있습니다. 기본적으로 CPU와 메모리는예약되지 않습니다. 이 예제에서는 "최선의 노력 중간" 네임스페이스 클래스를 사용할 것이므로 해당네임스페이스 클래스에 대한 CPU 및 메모리 예약을 설정할 것입니다. "최선의 노력 중간" 네임스페이스를사용하여 생성된 모든 네임스페이스는 이전에 조직을 위해 설정한 예약에서 상속된 이러한 예약을 상속받습니다.

# 1. 관리 및 거버넌스 클릭.

# 네임스페이스 클래스 선택

![](images/cb4baec5628db3da6695ac895068de848e489dac7f26535d8a8a5e17b5f095db.jpg)

1. 네임스페이스 클래스 클릭.
2. 중간 하이퍼링크를 클릭합니다.

HOL-2702-01-VCF-L

페이지 169

# 제한

![](images/0f00ee0163fac5a56b5c0c5408c7e5958579f01fac7e65e7dd9bf9d8b425967c.jpg)

# 1. 제한 클릭.

# 제한 검토

![](images/51113eda3515754190e723a7cfbae3bc6d9541c59adce288c5a43c6c0124e67b.jpg)

CPU 제한은 그대로 두십시오,

1. CPU 제한을 20 GHz로 유지하십시오.
2. 메모리 제한에 80 을 입력하십시오.
3. 기본 MB를 GB 로 변경하십시오.

HOL-2702-01-VCF-L

페이지 170

4. CPU 예약에 20 을 입력하고, CPU 예약이 GHz 로 표시되는지 확인하십시오.
5. 메모리 예약에 40 을 입력하고, 메모리 예약이 GB 로 표시되는지 확인하십시오.
6. 저장 을 클릭합니다.

작업이 완료될 때까지 기다린 후 진행하십시오.

# VCF 자동화 새 네임스페이스 구축 및 배포 - 1단계

![](images/f111d902d9efbff2a2572a67b27a0d776cafbedc81a8ee02c8e2aa9f029cdb36.jpg)

새로운 Pod를 배포하기 전에 VCF 자동화에서 네임스페이스가 어떻게 생성되는지 살펴보겠습니다.

1. 네임스페이스 를 클릭합니다.
2. 새 네임스페이스 를 클릭합니다.

HOL-2702-01-VCF-L

페이지 171

# VCF 자동화 새 네임스페이스 구축 및 배포 - 2단계

![](images/1e81f59ac0545029aaf27c73a680425213fe803d9f3ef50a7175550b85ec3880.jpg)

1. 이름에 hol-test 를 입력합니다.
2. 프로젝트에 default-project 를 입력하기 시작하면 프로젝트 상자에 default-project가 자동으로 채워집니다.
3. 네임스페이스 클래스에서 medium 을 선택합니다.
4. 지역에서 us-west 를 입력하기 시작하면 상자가 us-west로 채워집니다.
5. 영역에서 z-wld-a 를 입력하고 z-wld-a를 선택합니다.
6. 공유 VPC 를 선택합니다.
7. VPC에서 default-us-west 를 입력하면 default-us-west가 자동으로 채워집니다.
8. 생성 을 클릭합니다.

생성한 네임스페이스는 이전에 설정한 CPU 및 메모리 예약을 상속받았음을 주의하세요.

HOL-2702-01-VCF-L

페이지 172

# 네임스페이스 진행 상황 검토

![](images/be4416e3b33333d5ce7179408f21e8bed2051cfc0eec5942d309b880cdcb5384.jpg)

1. 새로운 네임스페이스가 in progress 상태로 표시됩니다.
2. hol-test-ntbng 의 하이퍼링크를 클릭합니다.

HOL-2702-01-VCF-L

페이지 173

# VCF 자동화 빌드 및 새 네임스페이스 배포 - 3단계

![](images/574a55c4f18cdd4f0e8d8f8ad838122f09e03792d43e7f016044b8af1c77fc88.jpg)

1. 상태가 활성 으로 표시될 때까지 기다리십시오.
2. 상태 업데이트를 보려면 브라우저 창을 새로 고쳐야 할 수 있습니다. 또는 뒤로 링크를 클릭하여 이전이지로 돌아가서 하이퍼링크를 클릭하는 이전 단계를 반복할 수 있습니다.

# VCF 자동화 빌드 및 VCF 포드 배포 - 네임스페이스보기에서.

# Services

![](images/888649c53723efce5511558dd8fc9e312d1a682a2f8088829990ad7e9d79d3ea.jpg)

HOL-2702-01-VCF-L

페이지 174

방금 생성한 네임스페이스에서 직접 또는 개요 페이지로 돌아가서 vSphere 포드를 배포하는 여러 가지 방법이있습니다.

방금 생성한 네임스페이스에서 아래로 스크롤하여 서비스로 이동할 수 있습니다.

1. 거기에서 컨테이너 를 클릭할 수 있습니다.

# VCF 자동화 빌드 및 VCF 포드 배포 - 개요보기에서.

![](images/644aaafd4b767c809ab28fb803f08adec81768f1edf156f125cf5beeb8b30da6.jpg)

VCF 자동화 개요 페이지에서.

1. 개요 를 클릭하여 개요 페이지로 돌아갑니다.
2. 클릭 컨테이너.
3. 클릭 빌드 및 배포 . (표시되지 않음)

서비스 아래에서 "컨테이너"를 클릭할 수도 있음을 유의하십시오.

HOL-2702-01-VCF-L

페이지 175

# VCF 자동화 빌드 및 VCF 포드 배포 - 빌드 및 배포에서.

![](images/bc6bdfed428467d17806cd6af6c1c5bf0838b9dcbce23adf27d35e1340b358e1.jpg)

1. 빌드 및 배포 를 클릭합니다.
2. 클릭 컨테이너.

HOL-2702-01-VCF-L

페이지 176

# VCF 자동화 빌드 및 VCF 포드 배포

![](images/e43ce69e9cf8f5044751bb11d900d62b0479357f7494f77697d6ab9274eff241.jpg)

1. 클릭 새 인스턴스 생성.

HOL-2702-01-VCF-L

페이지 177

# 새 VKS 포드 생성 - 네임스페이스 확인.

![](images/01b33ee2efb64abf60a0dffd80c012d9e2a2e2b9f9bd8747b34d23e419609ddc.jpg)

생성한 새로운 hol-test 네임스페이스에 있는지 확인하십시오.

1. hol-test가 표시되지 않으면 down 화살표를 클릭하여 네임스페이스를 hol-test로 변경하십시오.

hol-test 네임스페이스를 선택하지 않으면 기본 네임스페이스에 예약이 설정되어 있지 않기 때문에 vSpherepod를 생성하려고 할 때 오류가 발생합니다.

HOL-2702-01-VCF-L

페이지 178

# VCF 자동화 빌드 및 VCF 포드 배포

![](images/bd33f82aa88e1b4a59352107fdade0e5407a8a3bfb5216d8148bc445debdc452.jpg)

1. 이름을 제공하십시오. 우리는 hol-test here를 사용했습니다.
2. z-wld-a를 선택하십시오.

# 주 컨테이너 이미지 정의

# Primary Container Image

registry requires authentication. If you have an air-gapped environment, you need to host the col  local registry that can be reached from this namespace.

![](images/ca052b65aabada791ef02f0ca2f0e2ed3b4135db9a1b802ebdf3f092539493d7.jpg)

Registry Authentication

Authentication Required

![](images/dd526c80491bd625924dbbbffde5ab7a232fb1091614f76e2f6c6b973708abac.jpg)

ghcr.io/tmm-demo-apps/nginx:latest

Primary Container Image

1. 주 이미지 이름으로 ghcr.io/tmm-demo-apps/ngnix:latest

를 입력하십시오.

다른 값을 검토하고 NEXT(표시되지 않음)를 클릭하십시오.

Persistent Volume, ConfigMap, Secret, Runtime Configuration, Load

Balancer 및 Additional Container에 대한 기본값을 수락하고 NEXT를 클릭하십시오.

HOL-2702-01-VCF-L

페이지 179

# 새 컨테이너 인스턴스 만들기

![](images/69ba031d5e47a4ef425fc6d9d35cc61180ca80ad4cfe91b639636a846db0c437.jpg)

This container instance requires a baseline reservation of 256MB Memory,plus anyadditional CPU and Memory resources requested for your primary and additional containers. The container deployment willfailif this namespace doesn't have sufficient resource reservation. Please contact  your admin to adjust the namespace CPU and Memory reservation.

VIEW EXAMPLE

![](images/c7222696597d5b774d8bb86ace8c97db6c2580351c562d1fa3043d7f2c776c64.jpg)

CREATECONTAINER INSTANCE

1. 컨테이너 인스턴스 만들기 를 클릭하세요.

# VCF 자동화에서 포드 생성 모니터링

![](images/acfd7ca027783fbcad05f1a0baa3582104ec9da31697ffe870d7337985b50280.jpg)

1. hol-test 를 클릭하세요. HOL-2702-01-VCF-L

페이지 180

# 상태 보기

![](images/611978a307ea92aabe9e1a11b47b9c9843acb813cc75c087fd17ab8fd4cf06aa.jpg)

1. hol-test 를 볼 때까지 아래로 스크롤하고, hol-text vpod의 긴 이름을 기록하세요.

VKS 포드를 생성하는 중이므로 "대기 중" 상태가 표시됩니다.

전체 자격 이름 위에 마우스를 올리고, 몇 단계 후 vSphere에서 사용할 vPod의 전체 자격 이름을 복사하세요.

하이퍼링크를 클릭하면 추가 세부정보가 포함된 새로운 VCF 자동화 탭이나 창이 열립니다.

HOL-2702-01-VCF-L

페이지 181

# vCenter로 전환

![](images/54275a5b85a4f370596ba2d043f11a93af982f3b303659ab78800ba80de4194d.jpg)

1. 새로운 Firefox 브라우저 탭을 열고 vc-wld01-a-client를 선택합니다.

HOL-2702-01-VCF-L

페이지 182

# vCenter에 로그인

![](images/69d384d02ef0140d92352585ba3020d36c180f6605f233c34d0e7b80041c05b6.jpg)

사용자 이름과 비밀번호는 이미 입력되어 있어야 합니다. 그렇지 않은 경우

1. 사용자 이름으로 administrator@wld.sso 를 입력합니다.
2. 비밀번호로 VMware123!VMware123! 를 입력합니다.
3. 클릭 로그인.

# Pod 찾기

![](images/01fdea50c52506e85181845e6b07f9e74ee166f0d0d77a6c6d2e8e677d874378.jpg)

HOL-2702-01-VCF-L

페이지 183

1. 이전 단계에서 VCF-Automation에서 복사한 이름을 vSphere 클라이언트의 검색창에 붙여넣습니다.
2. 결과 필드에서 하이퍼링크를 클릭합니다.

# 상태 보기

![](images/fa9af0069ec5a379ea3c326438aa35ffa97946dc271bd752b3388bc7a44657f3.jpg)

대안으로 vCenter 인벤토리를 확장하고, vSphere 포드가 생성된 네임스페이스를 찾아 위와 같이 포드를찾을 수 있습니다.

최근 작업 표시줄에서 포드 생성 상태를 모니터링할 수도 있습니다.

포드 생성이 완료될 때까지 기다릴 필요는 없습니다.

이 모듈은 여기서 종료됩니다.

HOL-2702-01-VCF-L

페이지 184

# 모듈 결론

이 모듈 4는 여기서 종료됩니다.

여기에서 다음을 수행할 수 있습니다:

• 다음 랩 모듈로 계속 진행하십시오.
이

랩의 모든 모듈이나 수업으로 이동하려면 [vlp:table-of-contents|목차 표시]를 클릭하세요.

• 랩을 종료하고 나중에 돌아오십시오.

HOL-2702-01-VCF-L

페이지 185
