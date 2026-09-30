# 입문·CKA 자료 내용 대조 기록

2026-09-30. 제공된 입문 ZIP 24개 파일(개념 PDF 5개, 아키텍처 PPTX 1개, 보충 PDF 18개)과 CKA ZIP 39개 파일(개념 PDF 5개, 과제 PDF 16개, 보충 PDF 18개)의 텍스트를 추출해 현재 과정과 대조했다. 주요 개념·과제와 보충 설명을 검토했고, 판정에 필요한 Probe·HPA·Storage 도표는 렌더링해 확인했다. 모든 페이지의 시각적 교정이나 실제 클러스터 실습 완료를 뜻하지 않는다. 원본 자료는 저장소에 복제하지 않았다.

## 내용 중심으로 보강한 부분

| 자료 주제 | 기존 과정에서 약했던 부분 | 반영한 학습 내용 |
|---|---|---|
| 입문 기본 오브젝트·Service | NodePort 호출 위주, 외부 정책과 LB 비교 부족 | [NodePort](./01-core-objects/05-service-nodeport/README.md)에 Cluster/Local/LB 비교 YAML과 외부 호출 결과표 추가 |
| 입문 컨트롤러·중급 컨트롤러 | 생성 명령보다 보장 범위 설명 부족 | ReplicaSet의 소유권, RollingUpdate 가용 조건, DaemonSet 대상 조건, Job 재시도, CronJob 중복 실행, StatefulSet의 책임 경계 |
| 입문 Pod·스케줄링 | 상태·재시작·퇴거·선호 배치가 섞일 여지 | phase/reason, 컨테이너 재시작과 Pod 교체, Probe 성공 범위, QoS와 퇴거, required/preferred·topology 조건 |
| 입문 중급 오브젝트·저장소·보안 | 이름/범위/인코딩/재사용의 단순화 | Headless DNS 조건, ExternalName CNAME, Secret 인코딩과 암호화, Quota Admission, PV Retain 회수, RBAC scope |
| 입문 HPA·CKA Workloads | 계산 예시는 있지만 단위와 확장 계층 설명 부족 | [HPA](./05-advanced/04-hpa/README.md)에 CPU 단위·추천식·실제 동작 조건, HPA/VPA/노드 확장 비교 |
| 입문 아키텍처 PPTX·CKA Architecture | 요소별 목록에서 생성/트래픽/로그 흐름으로 연결 부족 | [개념 연결 지도](./07-cka-preview/CONCEPT_BRIDGE.md)에 인증→권한→Admission, 3개 네트워크, 로그와 metrics 경계 |
| CKA Troubleshooting | API/etcd 복구와 quota 계산에 초점 | [제어 평면](./07-cka-preview/09-control-plane-recovery/README.md)에 scheduler 진단, [자원 예산](./07-cka-preview/11-resource-budget/README.md)에 실제 노드별 계산 연결 |

## 원본을 읽을 때 구분할 표현

아래는 자료의 특정 설명을 현재 학습에 적용할 때 주의할 지점이다. 그림의 단순화, 오타, 특정 과제 조건을 구분한다.

| 위치 | 확인한 표현/생략 | 학습할 정확한 기준 |
|---|---|---|
| 입문 Probe 보충자료 p.6 | HTTP 성공 범위를 400까지 포함하는 표현 | 200 이상, 400 미만; readiness는 전달 대상, liveness는 컨테이너 재시작과 연결 |
| CKA Workloads & Scheduling p.5 | CPU quantities에 ms 표기 | CPU m은 millicpu; 1000m=1 CPU. 사용률은 request 대비 값 |
| 입문 중급 오브젝트 p.9 | Retain 이후 재사용 불가로 읽힐 수 있는 도표 | 자동 재사용되지 않는 상태와 관리자의 데이터 확인·수동 회수/재연결을 구분 |
| CKA Core Components 보충자료 p.2 | scheduler 자원을 worker의 10%로 설정 | 해당 과제 조건으로 취급; 일반 권장값으로 고정하지 않고 manifest/로그/노드 근거로 진단 |
| 입문 QoS·Quota·Scheduling 설명 | 클래스 순서, 총량, 여유 노드 선택을 단순화 | 퇴거는 초과 사용·Priority 등도 고려; Quota는 Admission, 배치는 requests와 조건·scoring |
| 입문 StatefulSet·롤링 업데이트 | DB 안정성/무중단을 컨트롤러 기능으로 확대 해석할 여지 | StatefulSet은 DB 복제·선출·백업을 구현하지 않음; 롤링 가용성에는 앱/Probe/종료/자원 조건 필요 |

판정 근거: [Probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/), [CPU 자원](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/), [HPA](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/), [PV Retain](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#retain), [노드 압박 퇴거](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/), [Quota](https://kubernetes.io/docs/concepts/policy/resource-quotas/), [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/).

## 두 자료를 함께 읽는 순서

1. 입문 기본 오브젝트 → Pod/Label/Service/Volume → CKA 01·03·05.
2. 입문 컨트롤러·Probe·자원 → Deployment/Job/QoS → CKA 02·10·11·12.
3. 입문 중급 오브젝트·보안 → StorageClass/RBAC/Ingress → CKA 04·06·07·08.
4. 아키텍처와 개념 연결 지도 → CKA 09·13·14·15·16.

전체 연결은 [혼합 예습 경로](./07-cka-preview/README.md)를 따른다. 하나의 주제마다 먼저 숫자·상태·요청 결과를 예측하고 실제 Events/로그/응답으로 비교한다. 예를 들어 Service 종류만 암기하지 말고 `Cluster/Local`에서 어느 노드 호출이 성공할지 설명한다.

## 첫 내용 검토 시점의 개선 범위

첫 내용 검토 시점에는 기초 42개 중 상당수가 과제 개요였다. 실행용 YAML과 예상 출력, 힌트를 모두 갖춘 자료로 만들려면 각 Lab별 추가 작업이 필요하다. 이번에는 외부 트래픽 정책 비교를 실행 가능하게 추가했으며 42개 전체를 완성형 실습으로 바꾸지는 않았다.

CKA 16개 예습은 제공된 과제를 연결한 경로다. kubeadm 설치·업그레이드·HA 구성, etcd 백업/복원, Kustomize 등의 별도 실행 과정을 갖추지 않았으므로 CKA 전체 대비 완료로 보지 않는다. VPA와 노드 자동 확장도 이번에는 개념 비교 범위다.

1.27 기본 환경과 1.34 과제 환경을 섞지 않는다. 특히 native sidecar, CRI/CNI 설치, Gateway 구현은 [환경 안내](./07-cka-preview/ENVIRONMENT.md)의 조건을 확인한다. 실제 검증 범위는 [검증 기록](./07-cka-preview/VALIDATION.md)에 남긴다.

## 독립 학습 요청 후의 커리큘럼 보강

[8단계 독립 과정](./08-independent/README.md)에 실행 가이드와 YAML을 추가하고 기존 42개 기초·16개 확장 전부를 연결했다. 강의 수강을 선행 조건에서 제거했다. 정상/실패 예상, 풀이를 보는 첫 회와 풀이 없는 재실행, 애드온 설치, 플랫폼 분리, 단계별 완료 기준을 제공한다. UI·Longhorn 제품 설치는 선택으로 구분하고 기존 애플리케이션/저장소 개념은 실행 경로에 포함했다. 이 보강도 실제 클러스터 실행 검증을 뜻하지 않으며 HA/업그레이드/etcd snapshot restore 전체 과정은 여전히 별도 범위다.
