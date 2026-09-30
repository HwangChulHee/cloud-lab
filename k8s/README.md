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

> kubeconfig가 기본 사용자에 설정되지 않은 경우 master에서 `KUBECONFIG=/etc/kubernetes/admin.conf`를 사용한다.

## 공통 흐름

```text
Recall → Build → Observe → Break → Diagnose → Recover → Cleanup → Explain
```

기본 진단 도구:

```bash
kubectl get <resource> -o wide
kubectl describe <resource> <name>
kubectl get events --sort-by=.lastTimestamp
kubectl logs <pod>
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
