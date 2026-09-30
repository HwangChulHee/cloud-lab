# 강의 없이 진행하는 Kubernetes 독립 학습

이 경로가 Kubernetes 과정의 기본 시작점이다. 영상이나 강의 ZIP 없이 **설명 읽기 → 실행 → 예상과 비교 → 실패·복구 → 정리 → 풀이 없는 재실행**으로 진행한다. 기존 42개 기초는 주제별 복습에, 16개 CKA 자료 기반 실습은 단계별 확장에 사용한다. 번호 순서대로 42개를 먼저 끝낼 필요는 없다.

## 시작 방법

1. [시작 준비](./START.md)에서 현재 클러스터·Linux 셸·kubeconfig·레포 경로를 확인한다.
2. 아래 01–08을 순서대로 실행한다. 각 문서의 명령은 **저장소 루트** 기준이다. 연결된 확장 문서는 해당 문서의 폴더 이동 안내를 따른다.
3. 첫 회에는 제공 YAML과 풀이를 참고한다. 예상 출력이 안 나오면 Events/로그로 원인을 해결하고 정상 검증을 다시 한다.
4. [완료 기준](./CHECKPOINTS.md)의 설명·실행·복구·정리를 확인한 뒤 넘어간다. 실패 명령을 건너뛴 것으로 완료 처리하지 않는다.

| 단계 | 핵심 질문 | 실행할 내용 | 연결된 확장 |
|---:|---|---|---|
| 01 [Pod와 관찰](./01-pods/README.md) | 같은 Pod에서 공유되는 것은? | Namespace/label, init, localhost, emptyDir, UID | 10 Sidecar는 03 설명 후 실행 |
| 02 [설정 주입](./02-configuration/README.md) | 설정을 바꿨는데 왜 값이 다른가? | ConfigMap/Secret, env/mount/subPath, immutable | 01 TLS 설정은 03의 rollout 후 실행 |
| 03 [Controller](./03-controllers/README.md) | 누가 개수를 복구하고 업데이트하는가? | ReplicaSet/Deployment, rolling/rollback/Recreate, Blue/Green, DaemonSet/Job/CronJob | 01 ConfigMap TLS, 10 Sidecar |
| 04 [Service와 DNS](./04-networking/README.md) | 이름은 되는데 왜 응답이 없는가? | ClusterIP/Headless/ExternalName, 수동 EndpointSlice, NodePort Cluster/Local/LB 관찰 | 05 Service 연결 추적 |
| 05 [자원·Probe·배치](./05-resources-scheduling/README.md) | 생성 거부·Pending·NotReady를 어떻게 나누는가? | phase/reason, init와 Probe, QoS/LimitRange, affinity/anti-affinity, taint | 11 Quota 예산, 12 Priority |
| 06 [영속 저장소](./06-storage/README.md) | Pod/PVC 삭제 뒤 무엇이 남는가? | 정적 PV/Retain, 동적 StorageClass, StatefulSet의 두 PVC | 03 PV 복구, 04 지연 바인딩 |
| 07 [인증과 권한](./07-security/README.md) | 누구로 어디까지 요청할 수 있는가? | x509/Token API 호출, RBAC, 격리된 kubeconfig context | 16 CRD 탐색 |
| 08 [노출·확장·통합 진단](./08-operations/README.md) | 앱은 정상인데 사용자는 왜 실패하는가? | Ingress/TLS, HPA, NetworkPolicy, 여러 실패 위치의 비교 | 02 HPA, 06 Ingress, 08 NetworkPolicy |

03을 끝낸 뒤 01 ConfigMap TLS와 10 Sidecar 확장을 실행하고 정리한다. 04를 끝낸 뒤 05 Service 확장을 실행한다. 나머지 확장은 각 단계 문서 안의 위치에서 수행한다. 표에 이름이 나온 것은 각각 별도 namespace를 쓰므로 앞 단계 앱을 계속 유지할 필요는 없다.

## 강의가 없어도 따라갈 수 있게 바꾼 점

- 과제 문장만 있는 기초에 8단계 실행 가이드를 연결하고 Pod/Controller/Service/설정/배치/저장소/RBAC/TLS YAML을 제공한다.
- 정상 출력뿐 아니라 **의도한 실패와 실제 준비 실패**를 구분한다. 첫 회는 풀이를 보고, 두 번째는 요구사항을 보고 진행한다.
- 기본 과정은 현재 클러스터를 사용한다. 동적 스토리지·Ingress·metrics는 필요한 단계에서 [애드온 설치](./ADDONS.md)를 진행한다.
- 설치·제어 평면 장애·Gateway/Helm은 [플랫폼 경로](./PLATFORM.md)로 분리한다. CNI 없는 새 클러스터에서는 CNI 설치 후 NetworkPolicy 집행을 검증한다.
- Dashboard UI와 Longhorn 제품 설치는 선택 확장이다. 토큰/context/RBAC와 동적 PVC의 핵심 개념은 UI나 특정 제품 없이 기본 과정에서 직접 실행한다.

## 막혔을 때 진행 순서

| 증상 | 먼저 확인 |
|---|---|
| Ready/rollout 대기 timeout | 해당 namespace Pod describe와 Events; 이미지/배치/init/Probe 구분 |
| API가 Forbidden | 현재 context/주체, can-i, 응답의 Quota/Admission 원인 |
| Pod가 없는데 Deployment 존재 | ReplicaSet FailedCreate |
| Pod Pending | Scheduled condition, 요청 자원·배치·PVC |
| DNS 성공 + HTTP 실패 | Service selector, endpoint의 주소/Ready, 실제 앱 port |
| PV Bound인데 실행 실패 | Pod의 mount Events와 실제 노드 경로/driver |
| HPA unknown | metrics APIService와 Pod metrics, requests |
| TLS 실패 | 접속 호스트/SNI, Secret, 실제 인증서, Controller 로그 |

외부 LB가 없거나 CNI가 정책을 집행하지 않는 것은 구현/환경 제약으로 따로 기록한다. LB 라우팅·정책 집행을 확인한 것처럼 체크하지 않는다. 필수 환경은 ADDONS/PLATFORM 안내로 준비하고 해당 검증을 다시 한다.

## 어디까지 완료하면 되는가?

기본 완료는 01–08의 정상·실패·복구·정리를 실행하고 [단계별 기준](./CHECKPOINTS.md)을 설명할 수 있는 상태다. 연결된 확장도 실제 실행 여부를 별도로 기록한다. 고정 날짜나 하루 분량을 정하지 않고 하나의 단계가 길면 구축/장애/재실행으로 나눠 진행한다.

플랫폼 완료는 새 클러스터의 CNI/정책, 제어 평면 복구, Helm, Gateway/Canary, 선택 CRI adapter까지 별도로 확인한다. HA 구성·kubeadm upgrade·etcd snapshot restore·실제 중앙 로그/시계열 시스템 운영은 이 경로에 완성된 과정이 없다. 강의 없이 실행 가능한 이 과정의 범위와 CKA 전체 대비 완료는 구분한다.

## 기존 목차와 연결

[42개 기초 목차](../README.md#커리큘럼) · [16개 확장 목차](../07-cka-preview/README.md) · [개념 지도](../07-cka-preview/CONCEPT_BRIDGE.md). 각 기초 문서 상단의 독립 가이드 링크와 curriculum.json에 모든 연결을 기록했다. 기존 완료 체크는 변경하지 않았다.

이 자료는 정적 링크/명령 문법/API 스키마 검증을 수행하지만, 사용자 VM에서 모두 실행한 기록은 아니다. 실제 완료 증거는 본인이 실행해 CHECKPOINTS 기록에 남긴다. [검증 기록](../07-cka-preview/VALIDATION.md).
