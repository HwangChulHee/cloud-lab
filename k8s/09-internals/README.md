# Kubernetes 내부 동작 — Lab 연결 및 선택 심화

이 폴더의 8개 내용은 보존하되 **두 번째 필수 기초 커리큘럼이 아니다.** 기초 Lab에 이미 통합한 개념은 반복 구축하지 않고, Linux/커널/CNI 심화처럼 관찰 범위가 다른 경우에만 선택적으로 진행한다. 기존 73개 총계와 완료 기록은 임의로 변경하지 않는다.

| ID | 주제 | 공식 기본 위치 | 09의 역할 |
|---|---|---|---|
| INT-01 | Pod 생성 Pipeline | [Pod 기본](../01-core-objects/01-pod-multicontainer/README.md) | 선택: CRI/Pod Sandbox 관찰 |
| INT-02 | Watch/Reconciliation | [Controller Troubleshooting](../02-controllers/08-controller-troubleshooting/README.md) | 참조: 중복 재실습 불필요 |
| INT-03 | Linux Pod 네트워크 | [Service 기본](../01-core-objects/04-service-clusterip/README.md) | **독립 심화 유지:** namespace/veth/라우팅 |
| INT-04 | kube-proxy·NAT·conntrack | [ClusterIP](../01-core-objects/04-service-clusterip/README.md) | 선택: 노드 데이터 평면 추적 |
| INT-05 | Scheduler/Eviction | [Scheduling Troubleshooting](../03-pod-deep-dive/08-scheduling-troubleshooting/README.md) | 참조: 중복 재실습 불필요 |
| INT-06 | CSI 볼륨 수명 | [Dynamic Provisioning](../04-storage-security/02-dynamic-provisioning-pv-lifecycle/README.md) | 선택: CSI 드라이버 구성요소 관찰 |
| INT-07 | Admission/PSA | [ServiceAccount & RBAC](../04-storage-security/04-serviceaccount-rbac/README.md) | **독립 심화 유지:** PSA 정책 재현 |
| INT-08 | 계층별 장애 추론 | [Lab 42 Capstone](../06-architecture/01-architecture-observability-capstone/README.md) | 참조: 최종 과제 시나리오 |

## 실행 원칙

1. 먼저 해당 00–06 Lab을 수행한다. 09는 중복 학습의 필수 조건이 아니다.
2. 노드 관찰이 필요하면 현재 Lab의 Namespace/객체를 우선 재사용한다. 아래 상세 문서에 있는 `lab-self-*`는 **예전 08 리소스 이름**이므로 그대로 있다고 가정하지 않는다.
3. CNI 구현별로 veth/overlay/BGP/eBPF의 경로가 다르다. 결과는 Calico 및 실제 kube-proxy 모드에 맞춰 해석한다.
4. 클러스터 파괴 위험이 있는 작업은 운영 중인 학습 VM이 아니라 별도 VM에서 실시한다.

## 원본 상세 자료

| ID | 모듈 | 연결 시점 | 학습 분류 |
|---|---|---|---|
| INT-01 | [INT-01 Pod 생성부터 실행까지](./01-pod-creation-pipeline/README.md) | 01 | 필수 개념 |
| INT-02 | [INT-02 Watch와 Reconciliation](./02-reconciliation-watch/README.md) | 03 | 필수 개념 |
| INT-03 | [INT-03 Linux 네트워크와 CNI](./03-linux-pod-network/README.md) | 04 setup 이후, Service 확인 전 | 운영 심화 |
| INT-04 | [INT-04 Service와 kube-proxy 데이터 경로](./04-service-dataplane/README.md) | 04 완료 후 | 운영 심화 |
| INT-05 | [INT-05 Scheduling과 Eviction](./05-scheduler-eviction/README.md) | 05 | 필수 개념 |
| INT-06 | [INT-06 CSI와 볼륨 수명](./06-csi-volume-lifecycle/README.md) | 06 | 운영 심화 |
| INT-07 | [INT-07 Admission과 Pod Security](./07-admission-pod-security/README.md) | 07 완료 후 | 필수 개념 |
| INT-08 | [INT-08 계층별 장애 추론](./08-system-failure-analysis/README.md) | 08 완료 후 | 운영 심화 |

이전 문서의 `08-independent` 선수조건은 레거시 연결이다. 현재 공식 선수 학습은 위 표의 00–06 Lab으로 해석한다.
