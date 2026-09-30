# Kubernetes Guided Labs

현재 로컬 3노드 클러스터를 이용해 Kubernetes를 **누적형 + 관찰형 + 장애복구형**으로 익히는 42개 기초 실습과 **16개 CKA 강의 전 예습**을 연결한 과정이다.

> 개념 회상 → 생성 → 정상 검증 → 조건 변경 → 일부러 실패 → Events/상태 추적 → 복구 → 설명


## 기초와 CKA를 함께 진행하기

[기초 + CKA 강의 전 예습 경로](./07-cka-preview/README.md)에서 기존 기초와 자료의 16개 주제를 짝지어 진행한다. 기초 개념을 읽고 → 바로 실행할 YAML로 구축하고 → 설정 변경/장애를 직접 해결하고 → 강의에서 이해를 확인한다. 기존 42개를 모두 마친 뒤 시작할 필요는 없다.

[예습 환경 안내](./07-cka-preview/ENVIRONMENT.md)에서 현재 1.27.2 클러스터와 별도 VM이 필요한 실습을 구분한다. Gateway API, NetworkPolicy, PriorityClass, Helm, CRD, CNI/CRI, 제어 평면 복구까지 자료 범위를 다루며 완료 체크는 실제 실행 후 직접 표시한다.

## 실습 철학

1. **동작을 본다.** YAML 작성으로 끝내지 않고 요청, 상태, Endpoint, Event, Log, Metric 변화를 확인한다.
2. **지식은 누적한다.** 앞에서 배운 Pod/Label/Service/Volume이 뒤의 Deployment, Probe, Ingress, HPA, StatefulSet의 전제가 된다.
3. **각 실습은 독립 복구 가능하게 한다.** 삭제/재실행할 수 있고, Node label/taint 등은 실습 종료 시 원복한다.
4. **성공보다 실패를 중요하게 본다.** selector 오타, Pending, 403, Probe 실패, quota 초과 등을 일부러 만든다.
5. **뒤로 갈수록 가이드를 줄인다.** 초반은 따라 하고 중반은 조건 중심, 후반은 증상/요구사항 중심으로 진행한다.
6. **최종 목표는 상태를 보고 추론하는 것.** 왜 Pending인지, 왜 트래픽이 안 가는지, 왜 403인지 스스로 좁혀간다.

## 현재 환경

```text
Windows Host
└─ VirtualBox + Vagrant
   ├─ k8s-master  192.168.56.30
   ├─ k8s-worker1 192.168.56.31
   └─ k8s-worker2 192.168.56.32

Kubernetes 1.27.2
Container Runtime: containerd
```

> admin.conf는 root만 읽을 수 있으므로 master에서 단일 명령은 `sudo KUBECONFIG=/etc/kubernetes/admin.conf kubectl ...`로 실행한다. Linux 셸 전체를 실습에 사용하려면 아래처럼 본인 kubeconfig를 준비한다. Windows PowerShell에서 bash 문법을 그대로 실행하지 않는다.

```bash
mkdir -p "$HOME/.kube"
# 기존 config가 있으면 덮어쓰지 말고 별도 파일/환경변수로 사용한다.
test ! -e "$HOME/.kube/config" && sudo install -m 600 -o "$(id -u)" -g "$(id -g)" /etc/kubernetes/admin.conf "$HOME/.kube/config"
kubectl config current-context
kubectl get nodes -o wide
```

이 kubeconfig는 관리자 권한을 담고 있으므로 저장소에 넣지 않는다. 버전별 애드온 조건과 실행 위치는 [환경 안내](./07-cka-preview/ENVIRONMENT.md)를 따른다.

## 자료의 사용 방식과 변경 규칙

기초 42개 문서는 실습 목표와 관찰·장애 과제를 중심으로 구성돼 있다. 모든 기초 폴더에 실행용 YAML이 제공되는 것은 아니다. 연결된 CKA 예습에는 구축용 YAML과 풀이가 있으며, 기초의 개념을 읽고 예습으로 실행을 이어갈 수 있다. 이 과정은 강의 전 예습 경로이고 CKA 전체 시험 대비 완료를 뜻하지 않는다.

- 독립 Pod의 command, volume, nodeSelector, affinity, resources 등 변경은 기본 1.27 환경에서 **YAML 수정 → 해당 실습 Pod 삭제 → 재생성**으로 한다. `kubectl edit pod`로 모두 변경할 수 있다고 가정하지 않는다.
- Deployment는 Pod template을 수정하고 rollout을 기다린다. 기존 Pod가 직접 이동하는 것이 아니라 새 Pod가 생성된다.
- PVC의 class/accessModes/volumeName 변경 실험은 새 PVC로 비교한다. 기존 데이터가 있으면 삭제하기 전에 PV의 reclaimPolicy부터 확인한다.
- Job의 command/Pod template 변경은 새 Job으로 실행한다. QoS 비교도 새 Pod로 한다.
- `kubectl get all`은 모든 리소스를 보여주지 않는다. ConfigMap, Secret, PVC, RBAC, Ingress 등은 종류를 직접 지정한다. `get ... -w`는 종류 하나씩 실행한다.
- 앞 실습의 namespace를 암묵적으로 재사용하지 않고 `-n`을 명시한다. 노드 labels/taints는 변경 전 값을 기록하고 직접 바꾼 항목만 원복한다.


## 공통 흐름

```text
Recall → Build → Observe → Break → Diagnose → Recover → Cleanup → Explain
```

기본 진단 도구 (`POD_NAME`, `NODE_NAME`, `RESOURCE_TYPE`, `RESOURCE_NAME`은 조회한 실제 값으로 바꾼다):

```bash
kubectl get RESOURCE_TYPE -o wide
kubectl describe RESOURCE_TYPE RESOURCE_NAME
kubectl get events --sort-by=.lastTimestamp
kubectl logs POD_NAME
kubectl get endpoints
```

## 커리큘럼

### Foundation

| # | Lab | 상태 |
|---:|---|:---:|
| 01 | [Cluster Verification](./00-foundation/01-cluster-verification/README.md) | ⬜ |
| 02 | [kubectl Observation Basics](./00-foundation/02-kubectl-observation-basics/README.md) | ⬜ |

### Core Objects

| # | Lab | 상태 |
|---:|---|:---:|
| 03 | [Pod Multi-Container](./01-core-objects/01-pod-multicontainer/README.md) | ⬜ |
| 04 | [Labels & Selectors](./01-core-objects/02-label-selector/README.md) | ⬜ |
| 05 | [Basic Scheduling & Resources](./01-core-objects/03-node-scheduling-resources/README.md) | ⬜ |
| 06 | [Service ClusterIP](./01-core-objects/04-service-clusterip/README.md) | ⬜ |
| 07 | [Service NodePort](./01-core-objects/05-service-nodeport/README.md) | ⬜ |
| 08 | [Service DNS](./01-core-objects/06-service-dns/README.md) | ⬜ |
| 09 | [Headless, Endpoint, ExternalName](./01-core-objects/07-headless-endpoint-externalname/README.md) | ⬜ |
| 10 | [Volume emptyDir](./01-core-objects/08-volume-emptydir/README.md) | ⬜ |
| 11 | [Volume hostPath](./01-core-objects/09-volume-hostpath/README.md) | ⬜ |
| 12 | [Static PV/PVC](./01-core-objects/10-pv-pvc-static/README.md) | ⬜ |
| 13 | [ConfigMap & Secret Env](./01-core-objects/11-configmap-secret-env/README.md) | ⬜ |
| 14 | [ConfigMap & Secret Mount](./01-core-objects/12-configmap-secret-mount/README.md) | ⬜ |
| 15 | [Namespace Isolation](./01-core-objects/13-namespace/README.md) | ⬜ |
| 16 | [ResourceQuota & LimitRange](./01-core-objects/14-resourcequota-limitrange/README.md) | ⬜ |

### Controllers

| # | Lab | 상태 |
|---:|---|:---:|
| 17 | [ReplicaSet](./02-controllers/01-replicaset/README.md) | ⬜ |
| 18 | [Deployment Recreate](./02-controllers/02-deployment-recreate/README.md) | ⬜ |
| 19 | [RollingUpdate & Rollback](./02-controllers/03-deployment-rollingupdate-rollback/README.md) | ⬜ |
| 20 | [Blue/Green with Service Selector](./02-controllers/04-deployment-bluegreen/README.md) | ⬜ |
| 21 | [DaemonSet](./02-controllers/05-daemonset/README.md) | ⬜ |
| 22 | [Job](./02-controllers/06-job/README.md) | ⬜ |
| 23 | [CronJob](./02-controllers/07-cronjob/README.md) | ⬜ |
| 24 | [Controller Troubleshooting](./02-controllers/08-controller-troubleshooting/README.md) | ⬜ |

### Pod Deep Dive

| # | Lab | 상태 |
|---:|---|:---:|
| 25 | [Pod Lifecycle & Status](./03-pod-deep-dive/01-pod-lifecycle-status/README.md) | ⬜ |
| 26 | [Readiness Probe](./03-pod-deep-dive/02-readiness-probe/README.md) | ⬜ |
| 27 | [Liveness Probe](./03-pod-deep-dive/03-liveness-probe/README.md) | ⬜ |
| 28 | [Pod QoS](./03-pod-deep-dive/04-qos/README.md) | ⬜ |
| 29 | [Node Affinity](./03-pod-deep-dive/05-node-affinity/README.md) | ⬜ |
| 30 | [Pod Affinity / Anti-Affinity](./03-pod-deep-dive/06-pod-affinity-antiaffinity/README.md) | ⬜ |
| 31 | [Taints & Tolerations](./03-pod-deep-dive/07-taints-tolerations/README.md) | ⬜ |
| 32 | [Scheduling Troubleshooting](./03-pod-deep-dive/08-scheduling-troubleshooting/README.md) | ⬜ |

### Storage & Security

| # | Lab | 상태 |
|---:|---|:---:|
| 33 | [Longhorn & StorageClass](./04-storage-security/01-longhorn-storageclass/README.md) | ⬜ |
| 34 | [Dynamic Provisioning & PV Lifecycle](./04-storage-security/02-dynamic-provisioning-pv-lifecycle/README.md) | ⬜ |
| 35 | [X509, kubeconfig & API](./04-storage-security/03-x509-kubeconfig-api/README.md) | ⬜ |
| 36 | [ServiceAccount & RBAC](./04-storage-security/04-serviceaccount-rbac/README.md) | ⬜ |
| 37 | [Dashboard Auth & kubeconfig Contexts](./04-storage-security/05-dashboard-auth-contexts/README.md) | ⬜ |

### Advanced Workloads

| # | Lab | 상태 |
|---:|---|:---:|
| 38 | [StatefulSet](./05-advanced/01-statefulset/README.md) | ⬜ |
| 39 | [Ingress Routing](./05-advanced/02-ingress-routing/README.md) | ⬜ |
| 40 | [Ingress Canary & TLS](./05-advanced/03-ingress-canary-tls/README.md) | ⬜ |
| 41 | [Horizontal Pod Autoscaler](./05-advanced/04-hpa/README.md) | ⬜ |

### Architecture & Capstone

| # | Lab | 상태 |
|---:|---|:---:|
| 42 | [Architecture & Observability Capstone](./06-architecture/01-architecture-observability-capstone/README.md) | ⬜ |

## 완료 기준

- 정상 동작을 실제 요청/상태로 확인했다.
- 의도한 장애를 재현했다.
- `describe / events / logs / endpoints / top` 중 적절한 도구로 원인을 찾았다.
- 최소 변경으로 복구했다.
- 마지막 확인 질문을 자신의 말로 답할 수 있다.
- 실습 리소스와 Node 설정을 정리했다.

## 진단 기본 순서

```text
Object 존재?
→ spec과 status는?
→ label/selector 연결은?
→ Events는?
→ Container 상태/로그는?
→ Node/Network/Storage/Permission 조건은?
```
