# Kubernetes 내부 동작 심화

기존 8단계 독립 학습에 **단계별로 연결되는 병렬 경로**다. 순서대로 전부 완료해야 다음 단계로 이동하는 추가 필수 단계가 아니다.

| ID | 모듈 | 연결 시점 | 학습 분류 |
|---|---|---|---|
| INT-01 | [INT-01 Pod 생성부터 실행까지](./01-pod-creation-pipeline/README.md) | 01 | 필수 개념 |
| INT-02 | [INT-02 Watch와 Reconciliation](./02-reconciliation-watch/README.md) | 03 | 필수 개념 |
| INT-03 | [INT-03 Linux 네트워크와 CNI](./03-linux-pod-network/README.md) | 04 시작 전 | 운영 심화 |
| INT-04 | [INT-04 Service와 kube-proxy 데이터 경로](./04-service-dataplane/README.md) | 04 완료 후 | 운영 심화 |
| INT-05 | [INT-05 Scheduling과 Eviction](./05-scheduler-eviction/README.md) | 05 | 필수 개념 |
| INT-06 | [INT-06 CSI와 볼륨 수명](./06-csi-volume-lifecycle/README.md) | 06 | 운영 심화 |
| INT-07 | [INT-07 Admission과 Pod Security](./07-admission-pod-security/README.md) | 07 완료 후 | 필수 개념 |
| INT-08 | [INT-08 계층별 장애 추론](./08-system-failure-analysis/README.md) | 08 완료 후 | 운영 심화 |

모듈은 공통적으로 **핵심 질문 → 구성요소 흐름 → 학습용 예상 상태 → 관찰 → 장애 추론 → 주제별 이해 확인** 순서로 학습한다. 단원 내용의 *필수 개념*과 *운영 심화*를 구분하고, 실행 가능한 리소스가 삭제되었다면 선수 실습을 재생성한 뒤 관찰한다.

기존 학습 진입점: [08-independent](../08-independent/README.md). 위험한 클러스터 변경은 [별도 플랫폼](../08-independent/PLATFORM.md) 경로에서만 수행한다. 관찰과 실제 실행 검증은 별도 기록한다.
