# 기초 + CKA 강의 전 예습

기존 42개 기초 실습에 CKA 자료의 16개 주제를 연결한 혼합 학습 경로다. 강의를 듣기 전에 개념을 직접 만져보고, 강의에서 설명과 자신의 관찰을 비교한다. 자료의 문제 문구·호스트 이름·시험 환경을 그대로 재현하는 대신 같은 개념과 작업 범위를 연습한다.

[입문·CKA 내용 대조 기록](../CONTENT_REVIEW.md): 개념 설명 보강과 남은 실습 범위를 확인한다.

## 어떻게 진행할까?

1. 표의 **기초 연결**을 읽고 핵심 개념을 떠올린다. 처음 보는 개념이면 그 기초 실습을 먼저 한다.
2. 예습 폴더의 YAML과 명령으로 직접 구축한다. 결과를 예상한 뒤 상태·요청·로그를 본다.
3. 변경/장애 과제를 스스로 시도한다. 막힐 때만 접힌 힌트와 풀이를 펼친다.
4. 검증하고 정리한다. 아래 기록에 예상과 실제 차이를 남긴 뒤 강의를 듣는다.
5. 강의 후 같은 실습을 힌트 없이 한 번 더 한다. 속도보다 원인 설명을 먼저 익힌다.

권장 순서: 설정·확장(01–02) → 저장소(03–04) → Service/Ingress(05–06) → NetworkPolicy(08) → 로그·자원·우선순위(10–12) → CRD(16) → 별도 환경의 Gateway/Helm(07/13) → 제어 평면/CNI/CRI(09/14/15).

42개를 모두 끝낸 후에만 예습할 필요는 없다. **기초 하나와 관련 예습 하나를 짝지어** 진행한다. 전체 실습 번호와 예습 번호는 별도이며 기존 완료 상태는 바꾸지 않는다.

## 시작 환경

[개념 슬라이드와 기초 연결](./CONCEPT_BRIDGE.md)에서 Block/File/Object, Pod 실행 흐름, Affinity/Taint, QoS/PDB, CNI/CRI/CSI까지 함께 확인한다. PDB는 별도의 작은 관찰 예제도 제공한다.

[환경·실행 위치·선행 조건](./ENVIRONMENT.md)을 먼저 읽는다. 현재 1.27.2 환경에서 할 수 있는 주제부터 시작하며 기존 클러스터를 일괄 업그레이드하지 않는다. Gateway/설치 과제는 별도 환경에서 수행한다. Metrics/CNI/Controller/provisioner가 없으면 해당 선행 조건을 준비한 뒤 실행한다.

## 혼합 경로와 자료 범위

| 예습 | 실습 | 연결할 기초 | 필요한 환경 | 상태 |
|---:|---|---|---|:---:|
| 01 | [ConfigMap으로 TLS 설정 바꾸기](./01-configmap-tls/README.md) | [ConfigMap 파일 마운트](../01-core-objects/12-configmap-secret-mount/README.md) / [롤링 업데이트](../02-controllers/03-deployment-rollingupdate-rollback/README.md) | 기존 1.27 클러스터 + openssl/curl | ⬜ |
| 02 | [HPA와 축소 안정화 시간](./02-hpa-behavior/README.md) | [HPA](../05-advanced/04-hpa/README.md) / [기초 자원 설정](../01-core-objects/03-node-scheduling-resources/README.md) | 기존 클러스터 + 정상 Metrics Server | ⬜ |
| 03 | [Retain PV로 데이터 복구하기](./03-pv-data-recovery/README.md) | [정적 PV/PVC](../01-core-objects/10-pv-pvc-static/README.md) / [PV 수명주기](../04-storage-security/02-dynamic-provisioning-pv-lifecycle/README.md) | 기존 클러스터 + worker SSH | ⬜ |
| 04 | [StorageClass와 지연 바인딩](./04-storageclass-binding/README.md) | [StorageClass](../04-storage-security/01-longhorn-storageclass/README.md) / [동적 프로비저닝](../04-storage-security/02-dynamic-provisioning-pv-lifecycle/README.md) | 기존 클러스터 + 동적 provisioner | ⬜ |
| 05 | [Service와 NodePort 연결 추적](./05-service-nodeport/README.md) | [NodePort](../01-core-objects/05-service-nodeport/README.md) / [Labels/Selectors](../01-core-objects/02-label-selector/README.md) | 기존 클러스터 | ⬜ |
| 06 | [Ingress의 host와 path 라우팅](./06-ingress-routing/README.md) | [Ingress Routing](../05-advanced/02-ingress-routing/README.md) / [Service DNS](../01-core-objects/06-service-dns/README.md) | 기존 클러스터 + 설치된 Ingress Controller | ⬜ |
| 07 | [Ingress에서 Gateway API로 전환](./07-gateway-migration/README.md) | [Ingress TLS](../05-advanced/03-ingress-canary-tls/README.md) / [Ingress Routing](../05-advanced/02-ingress-routing/README.md) | 별도 1.34 예습 클러스터 + Ingress/Gateway Controller | ⬜ |
| 08 | [최소 권한 NetworkPolicy](./08-networkpolicy/README.md) | [Namespace](../01-core-objects/13-namespace/README.md) / [Labels/Selectors](../01-core-objects/02-label-selector/README.md) | NetworkPolicy를 실제 집행하는 CNI | ⬜ |
| 09 | [제어 평면 장애를 호스트에서 복구하기](./09-control-plane-recovery/README.md) | [클러스터 기준선](../00-foundation/01-cluster-verification/README.md) / [아키텍처 관찰](../06-architecture/01-architecture-observability-capstone/README.md) | 읽기 관찰은 기존 클러스터 / 장애 주입은 폐기 가능한 kubeadm VM | ⬜ |
| 10 | [파일 로그를 Sidecar로 stdout에 보내기](./10-sidecar-logging/README.md) | [멀티 컨테이너 Pod](../01-core-objects/01-pod-multicontainer/README.md) / [emptyDir](../01-core-objects/08-volume-emptydir/README.md) | 기존 클러스터 | ⬜ |
| 11 | [자원 예산을 계산해 3개 Pod 복구하기](./11-resource-budget/README.md) | [Requests/Limits](../01-core-objects/03-node-scheduling-resources/README.md) / [Quota/LimitRange](../01-core-objects/14-resourcequota-limitrange/README.md) / [Scheduling 진단](../03-pod-deep-dive/08-scheduling-troubleshooting/README.md) | 기존 클러스터 | ⬜ |
| 12 | [PriorityClass와 스케줄링 우선순위](./12-priorityclass/README.md) | [Scheduling](../03-pod-deep-dive/08-scheduling-troubleshooting/README.md) / [QoS](../03-pod-deep-dive/04-qos/README.md) | 기존 클러스터 / 선점 관찰은 전용 노드 | ⬜ |
| 13 | [Helm으로 Argo CD 설치와 템플릿 비교](./13-helm-argocd/README.md) | [Controller](../02-controllers/01-replicaset/README.md) / [RBAC](../04-storage-security/04-serviceaccount-rbac/README.md) | 별도 1.34 예습 클러스터 + Helm 3 + Python/PyYAML | ⬜ |
| 14 | [CNI 설치와 NetworkPolicy 집행 확인](./14-cni-install/README.md) | [클러스터 관찰](../00-foundation/01-cluster-verification/README.md) / [NetworkPolicy 예습](../07-cka-preview/08-networkpolicy/README.md) | CNI 없는 별도 1.34 kubeadm 클러스터 | ⬜ |
| 15 | [CRI와 Linux 네트워크 매개변수 준비](./15-cri-linux-preparation/README.md) | [클러스터 runtime 확인](../00-foundation/01-cluster-verification/README.md) | 별도 Ubuntu 22.04 VM + Docker + 로컬 cri-dockerd 패키지 | ⬜ |
| 16 | [CRD 조회와 kubectl explain 문서 추출](./16-crd-discovery/README.md) | [API/kubeconfig](../04-storage-security/03-x509-kubeconfig-api/README.md) / [kubectl 관찰](../00-foundation/02-kubectl-observation-basics/README.md) | 기존 클러스터 | ⬜ |

## 강의 전후 기록

```text
실습:
시작 상태/환경:
예상한 결과:
실제로 본 상태·이벤트·응답:
원인과 복구에 쓴 변경:
강의에서 확인할 질문:
강의 후 수정한 이해:
정리/원복 확인:
```

완료는 직접 실행·검증·정리하고 원인을 설명할 수 있을 때 체크한다. 강의 자료는 사용자 제공 ZIP의 5개 개념 강의, 16개 과제, 18개 카페 보충자료를 분석해 주제만 연결했다. 원본 PDF·카페 글·댓글은 저장소에 업로드하지 않는다.

## 범위 해석

- ConfigMap immutable, HPA scaleDown behavior 등 보충자료의 개념도 포함한다.
- PriorityClass는 기존 사용자 클래스 값 기준으로 통일한다. 풀이의 고정 상한값과 섞지 않는다.
- PVC는 파일을 이용해 데이터 보존을 확인하고 자원 계산은 작은 quota 예산으로 연습한다.
- CRD는 작은 학습용 API로 먼저 익히고 실제 cert-manager 조회는 설치된 환경에서 이어간다.
- 제어 평면·CNI·CRI 설치는 기존 클러스터 관찰과 전용 VM의 변경 작업을 구분한다.
- 이 경로는 제공 자료 범위의 예습이며 CKA 전체 시험 범위의 완주 판정표는 아니다. 기존 RBAC/스케줄링/롤백 기초는 계속 활용한다.

[기존 Kubernetes 과정](../README.md)

[자료 검증 기록](./VALIDATION.md)
