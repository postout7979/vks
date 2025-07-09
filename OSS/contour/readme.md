## 사용법 ##

run.sh 파일과 01-crds.txt 파일을 로컬 리눅스 머신에 다운로드 혹은 생성하시기 바랍니다.

01-crds.txt는 영구적으로 삭제를 금합니다.

run.sh 파일을 실행하면, 몇 가지 선택과 질문 사항이 제공됩니다.

기본적으로 contour는 기본 설치 모드와 avi LB를 사용하도록 ako에 대한 loadBalancerClass를 지정과 ingress-class-name을 지정하는 모드로 구분됩니다.
첫 번째 질문에서 숫자 1을 입력 시, ingress-class-name을 사용하는 모드이며, 숫자 2를 입력시에는 기본 모드로 배포됩니다.
두 번째 질문은 contour를 배포하기 위한 namespace name을 입력합니다. namespace 구성 항목에는 pod security에 대한 label을 기본 포함하고 있습니다.

## 숫자 1을 선택하여, ingress-class-name을 사용할 경우 ##
세 번째 질문으로 ingress-class-name에 대한 name을 입력합니다.
이는 03-contour.yaml 파일의 deployment 항목의 container runtime의 servce 영역의 마지막 줄로 --ingress-class-name={your class name} 전달자를 envoy에 전달하여, 사용하도록 합니다.

또한, ako plugin이 해당 cluster에 설치되어 있는 것을 전제로 진행되며, ako 배포 시, nameselector에 대한 label이 사전에 정의되어 있어야 합니다. key, value
ako에 nameselector의 key: Red, value: Prod 일 경우에는 이 스크립트에서 label 입력 시, Red: Prod로 입력을 필요로 합니다.
해당 label은 namespace에 추가되어, contour가 배포된 namespace의 envoy가 external LoadBalancer(여기서는 AKO로 구성된 Avi LB)로부터 IP를 가져오고, 네트워크 서비스를 제공합니다.

입력된 ingress-class-name은 ingressClass.yaml을 생성하여, cluster에 contour controller에 대한 ingressclass를 생성합니다.

ingress class는 ingress 혹은 httpproxy 배포 시, 해당 되는 yaml 값의 spec.ingressClassName={your ingress name}으로 추가되어, service가 어떤 인그레스를 사용할지 선택하도록 제공합니다.
