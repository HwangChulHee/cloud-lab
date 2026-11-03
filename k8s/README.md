# Kubernetes Guided Labs

로컬 3노드 클러스터에서 Kubernetes를 **개념 이해 → 직접 구축 → 정상 관찰 → 장애 재현 → 원인 분석 → 복구** 순서로 학습하는 저장소입니다. 이론과 실습은 **서로 독립적으로** 진행률을 기록합니다.

## 학습 현황

> 마지막 실습 갱신: **2026-11-03**

| 구분 | 완료 / 전체 | 진행률 | 최근 완료 | 다음 모듈 |
|---|---:|---:|---|---|
| **이론** | **32 / 73** | **43.8%** | Pod Deep Dive 08 — Scheduling Troubleshooting | [Storage & Security 01 — Longhorn & StorageClass](./04-storage-security/01-longhorn-storageclass/README.md) |
| **실습** | **20 / 73** | **27.4%** | [Lab 20 — Blue/Green](./02-controllers/04-deployment-bluegreen/README.md) | **[Lab 21 — DaemonSet](./02-controllers/05-daemonset/README.md)** |

| 실습 트랙 | 완료 / 전체 | 진행률 |
|---|---:|---:|
| 기초 (00–06) | 20 / 42 | 47.6% |
| CKA 확장 (07) | 0 / 16 | 0% |
| 내부 원리 심화 (09) | 0 / 8 | 0% |
| 클러스터 관리 (10) | 0 / 7 | 0% |
| **전체** | **20 / 73** | **27.4%** |

- 현재 실습 위치: **02 Controllers — 4/8 완료 (50%)**. Foundation **2/2**, Core Objects **14/14** 완료.
- 최근 실습 기록: Blue/Green의 selector 전환·복구, 빈 EndpointSlice 장애 재현, Namespace 정리 및 **복습 2/2 완료**.
- 이론 최근 완료: **Pod Deep Dive 08** (세부 학습 4/4, 종합 복습 2/2). 아래 기초 목차는 **이론 32개 / 실습 20개** 체크 상태를 보존합니다.
- 8단계 독립 학습 경로는 기존 73개와 내용을 연결하는 **별도 안내 경로**이며, 완료 개수에 중복 산입하지 않습니다.

## 어디서 시작할까?

| 목적 | 시작점 |
|---|---|
| **현재 진행 중인 VM 실습 이어가기** | [Lab 21 — DaemonSet](./02-controllers/05-daemonset/README.md) |
| 개념부터 강의 없이 순서대로 실습하기 | [08 — 독립 학습 8단계](./08-independent/README.md) · [시작 준비](./08-independent/START.md) |
| 주제별 이론·실습 체크 확인하기 | [42개 기초 커리큘럼](#기초-커리큘럼-42개) |
| CKA 확장 문제 실습하기 | [07 — CKA 확장 16개](./07-cka-preview/README.md) |
| Linux / Kubernetes 내부 동작 탐구하기 | [09 — 내부 원리 심화 8개](./09-internals/README.md) |
| 클러스터 설치·운영·복구 학습하기 | [10 — 클러스터 관리 7개](./10-cluster-admin/README.md) |
| 강의자료와 학습 내용의 대응 관계 확인하기 | [내용 검토 및 연결 기록](./CONTENT_REVIEW.md) |

### 학습 방식과 완료 기준

**Recall → Build → Observe → Break → Diagnose → Recover → Cleanup → Explain**

각 Lab에서는 정상 실행을 확인하고, 의도적으로 실패를 재현하며, 상태와 Events에 근거해 원인을 진단한 뒤 복구합니다. 리소스 정리 및 핵심 내용을 자신의 말로 설명하는 단계까지 마쳐야 실습 완료로 기록합니다.

- **이론 완료(✅)**: 설명과 단원별 복습 완료. 실제 VM 수행과 구분합니다.
- **실습 완료(✅)**: 정상·장애·복구·Cleanup을 실제 클러스터에서 검증한 상태입니다.
- **미완료(⬜)**: 미진행 또는 아직 검증되지 않은 상태입니다.
- 각 실습의 자세한 절차·증거·복습 결과는 **개별 Lab README**에 기록합니다. 확장/관리 실습은 별도 체크합니다.

## 학습 범위

| 구분 | 경로 | 모듈 수 | 주요 내용 |
|---|---|---:|---|
| Foundation | [00-foundation](./00-foundation/) | 2 | 클러스터 검증, kubectl 관찰 |
| Core Objects | [01-core-objects](./01-core-objects/) | 14 | Pod, Service, Volume, PV/PVC, ConfigMap, Namespace |
| Controllers | [02-controllers](./02-controllers/) | 8 | ReplicaSet, Deployment, DaemonSet, Job, CronJob |
| Pod Deep Dive | [03-pod-deep-dive](./03-pod-deep-dive/) | 8 | Lifecycle, Probe, QoS, Affinity, Scheduling |
| Storage & Security | [04-storage-security](./04-storage-security/) | 5 | StorageClass/CSI, 인증, RBAC |
| Advanced | [05-advanced](./05-advanced/) | 4 | StatefulSet, Ingress, HPA |
| Architecture | [06-architecture](./06-architecture/) | 1 | 아키텍처·관측성 종합 |
| CKA 확장 | [07-cka-preview](./07-cka-preview/README.md) | 16 | 시험 관련 확장 실습 |
| 내부 심화 | [09-internals](./09-internals/README.md) | 8 | 컨트롤러·네트워크·스케줄러 내부 |
| 클러스터 관리 | [10-cluster-admin](./10-cluster-admin/README.md) | 7 | 설치, 운영, 장애 대응 |
| **합계** | | **73** | |

## 기초 커리큘럼 (42개)

이 표 하나에서 기초 42개 모듈의 **이론과 실습 상태**를 함께 관리합니다. 각 이름을 누르면 해당 Lab 가이드로 이동합니다.

### Foundation

| # | Lab | 이론 | 실습 |
|---:|---|:---:|:---:|
| 01 | [Cluster Verification](./00-foundation/01-cluster-verification/README.md) | ✅ | ✅ |
| 02 | [kubectl Observation Basics](./00-foundation/02-kubectl-observation-basics/README.md) | ✅ | ✅ |

### Core Objects

| # | Lab | 이론 | 실습 |
|---:|---|:---:|:---:|
| 03 | [Pod Multi-Container](./01-core-objects/01-pod-multicontainer/README.md) | ✅ | ✅ |
| 04 | [Labels & Selectors](./01-core-objects/02-label-selector/README.md) | ✅ | ✅ |
| 05 | [Basic Scheduling & Resources](./01-core-objects/03-node-scheduling-resources/README.md) | ✅ | ✅ |
| 06 | [Service ClusterIP](./01-core-objects/04-service-clusterip/README.md) | ✅ | ✅ |
| 07 | [Service NodePort](./01-core-objects/05-service-nodeport/README.md) | ✅ | ✅ |
| 08 | [Service DNS](./01-core-objects/06-service-dns/README.md) | ✅ | ✅ |
| 09 | [Headless, Endpoint, ExternalName](./01-core-objects/07-headless-endpoint-externalname/README.md) | ✅ | ✅ |
| 10 | [Volume emptyDir](./01-core-objects/08-volume-emptydir/README.md) | ✅ | ✅ |
| 11 | [Volume hostPath](./01-core-objects/09-volume-hostpath/README.md) | ✅ | ✅ |
| 12 | [Static PV/PVC](./01-core-objects/10-pv-pvc-static/README.md) | ✅ | ✅ |
| 13 | [ConfigMap & Secret Env](./01-core-objects/11-configmap-secret-env/README.md) | ✅ | ✅ |
| 14 | [ConfigMap & Secret Mount](./01-core-objects/12-configmap-secret-mount/README.md) | ✅ | ✅ |
| 15 | [Namespace Isolation](./01-core-objects/13-namespace/README.md) | ✅ | ✅ |
| 16 | [ResourceQuota & LimitRange](./01-core-objects/14-resourcequota-limitrange/README.md) | ✅ | ✅ |

### Controllers

| # | Lab | 이론 | 실습 |
|---:|---|:---:|:---:|
| 17 | [ReplicaSet](./02-controllers/01-replicaset/README.md) | ✅ | ✅ |
| 18 | [Deployment Recreate](./02-controllers/02-deployment-recreate/README.md) | ✅ | ✅ |
| 19 | [RollingUpdate & Rollback](./02-controllers/03-deployment-rollingupdate-rollback/README.md) | ✅ | ✅ |
| 20 | [Blue/Green with Service Selector](./02-controllers/04-deployment-bluegreen/README.md) | ✅ | ✅ |
| 21 | [DaemonSet](./02-controllers/05-daemonset/README.md) | ✅ | ⬜ |
| 22 | [Job](./02-controllers/06-job/README.md) | ✅ | ⬜ |
| 23 | [CronJob](./02-controllers/07-cronjob/README.md) | ✅ | ⬜ |
| 24 | [Controller Troubleshooting](./02-controllers/08-controller-troubleshooting/README.md) | ✅ | ⬜ |

### Pod Deep Dive

| # | Lab | 이론 | 실습 |
|---:|---|:---:|:---:|
| 25 | [Pod Lifecycle & Status](./03-pod-deep-dive/01-pod-lifecycle-status/README.md) | ✅ | ⬜ |
| 26 | [Readiness Probe](./03-pod-deep-dive/02-readiness-probe/README.md) | ✅ | ⬜ |
| 27 | [Liveness Probe](./03-pod-deep-dive/03-liveness-probe/README.md) | ✅ | ⬜ |
| 28 | [Pod QoS](./03-pod-deep-dive/04-qos/README.md) | ✅ | ⬜ |
| 29 | [Node Affinity](./03-pod-deep-dive/05-node-affinity/README.md) | ✅ | ⬜ |
| 30 | [Pod Affinity / Anti-Affinity](./03-pod-deep-dive/06-pod-affinity-antiaffinity/README.md) | ✅ | ⬜ |
| 31 | [Taints & Tolerations](./03-pod-deep-dive/07-taints-tolerations/README.md) | ✅ | ⬜ |
| 32 | [Scheduling Troubleshooting](./03-pod-deep-dive/08-scheduling-troubleshooting/README.md) | ✅ | ⬜ |

### Storage & Security

| # | Lab | 이론 | 실습 |
|---:|---|:---:|:---:|
| 33 | [Longhorn & StorageClass](./04-storage-security/01-longhorn-storageclass/README.md) | ⬜ | ⬜ |
| 34 | [Dynamic Provisioning & PV Lifecycle](./04-storage-security/02-dynamic-provisioning-pv-lifecycle/README.md) | ⬜ | ⬜ |
| 35 | [X509, kubeconfig & API](./04-storage-security/03-x509-kubeconfig-api/README.md) | ⬜ | ⬜ |
| 36 | [ServiceAccount & RBAC](./04-storage-security/04-serviceaccount-rbac/README.md) | ⬜ | ⬜ |
| 37 | [Dashboard Auth & kubeconfig Contexts](./04-storage-security/05-dashboard-auth-contexts/README.md) | ⬜ | ⬜ |

### Advanced Workloads

| # | Lab | 이론 | 실습 |
|---:|---|:---:|:---:|
| 38 | [StatefulSet](./05-advanced/01-statefulset/README.md) | ⬜ | ⬜ |
| 39 | [Ingress Routing](./05-advanced/02-ingress-routing/README.md) | ⬜ | ⬜ |
| 40 | [Ingress Canary & TLS](./05-advanced/03-ingress-canary-tls/README.md) | ⬜ | ⬜ |
| 41 | [Horizontal Pod Autoscaler](./05-advanced/04-hpa/README.md) | ⬜ | ⬜ |

### Architecture & Capstone

| # | Lab | 이론 | 실습 |
|---:|---|:---:|:---:|
| 42 | [Architecture & Observability Capstone](./06-architecture/01-architecture-observability-capstone/README.md) | ⬜ | ⬜ |

## 실습 환경 및 실행

```text
Windows (Vagrant + VirtualBox)
├── k8s-master   192.168.56.30
├── k8s-worker1  192.168.56.31
└── k8s-worker2  192.168.56.32

Kubernetes 1.27.2 · containerd · Calico
```

호스트 PowerShell에서 `vagrant ssh master-node`로 접속합니다. Master VM에서 `kubectl`이 인증되지 않으면 관리자 kubeconfig를 설정해야 합니다. 자세한 명령과 주의 사항은 [독립 실습 시작 준비](./08-independent/START.md), [확장 실습 환경](./07-cka-preview/ENVIRONMENT.md)을 참고합니다.

```bash
# Master VM에서 클러스터 상태 점검
kubectl get nodes -o wide
kubectl get pods -A
```

**주의:** `/etc/kubernetes/admin.conf`는 관리자 자격 증명을 포함하므로 GitHub에 커밋하지 않습니다. 시스템에 따라 `sudo KUBECONFIG=/etc/kubernetes/admin.conf kubectl ...`가 필요합니다.

## 실습 중 장애 확인 순서

```text
객체가 존재하는가?
→ spec / status는 무엇인가?
→ Label / Selector / Endpoint가 연결되는가?
→ Events와 컨테이너 로그는?
→ Node / Network / Storage / Permission의 문제인가?
```

```bash
kubectl get pods -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>
kubectl get events -n <namespace> --sort-by=.lastTimestamp
kubectl logs <pod-name> -n <namespace>
```

설정 변경이나 삭제는 **해당 Lab의 안내와 현재 클러스터 상태를 확인한 뒤** 수행합니다. 실습 Namespace를 명시하고, 변경한 Node label/taint는 원복하며, 데이터 삭제 전 PVC/PV의 회수 정책을 확인합니다. `kubectl get all`은 모든 리소스를 보여주지 않으므로 Secret·PVC·EndpointSlice 등은 별도로 조회합니다.

## 학습 자료 및 확장 경로

- [독립 학습 단계별 체크포인트](./08-independent/CHECKPOINTS.md) · [복습 해설](./08-independent/REVIEW_ANSWERS.md)
- [실습용 애드온](./08-independent/ADDONS.md) · [별도 VM/플랫폼 실습](./08-independent/PLATFORM.md)
- [CKA 내용 연결 지도](./07-cka-preview/CONCEPT_BRIDGE.md) · [검증 기록](./07-cka-preview/VALIDATION.md)

> **범위 안내:** 이 저장소의 이론/실습 완료 수치는 사용자 VM에서 실제 검증한 기록을 기준으로 합니다. 선택적 제품 설치나 일부 플랫폼 운영 실습은 별도 범위이며, 모듈 완료만으로 최신 CKA 시험 전체 대비를 보장하지 않습니다.
