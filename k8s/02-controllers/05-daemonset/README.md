# Lab 21 — DaemonSet: 적합한 Node마다 Pod 하나

> **필수 실습** · 기존 Vagrant 3노드 클러스터 · namespace: `lab-daemonset` · 관련 개념: Label/Selector(Lab 04), Deployment(Lab 17–20)

## 1. Overview / Recall

목표는 **DaemonSet Controller가 적합한 Node마다 하나의 Pod를 유지**하는 과정을 관찰하고, 배치 조건 변화가 기존 Pod에 어떤 영향을 주는지 설명하는 것이다.

먼저 답해 본다.

1. Deployment `replicas: 2`와 DaemonSet이 서로 다른 점은?
2. Control Plane에 `NoSchedule` taint가 있어도 DaemonSet이 항상 그곳에 배치될까?
3. Node label이 바뀌면 기존 Pod는 누가 정리할까?

## 2. Build — 대상 Node를 명시적으로 준비

**변경 범위:** Worker 2대에만 이 Lab 전용 label을 붙인다. Control Plane taint를 제거하지 않는다. 실행 전 같은 label이 사용 중이지 않은지 확인한다.

```bash
kubectl config current-context
kubectl get nodes -o wide --show-labels
kubectl get nodes -L cloud-lab/daemonset
# 기본 Vagrant 클러스터의 실제 Node 이름 확인 후 실행
kubectl label node k8s-worker1 cloud-lab/daemonset=yes
kubectl label node k8s-worker2 cloud-lab/daemonset=yes
kubectl apply -f k8s/02-controllers/05-daemonset/daemonset.yaml
kubectl -n lab-daemonset rollout status ds/node-web --timeout=180s
kubectl -n lab-daemonset get ds,pods -o wide
```

**예상:** DESIRED=2, CURRENT=2, READY=2, 두 Pod의 `spec.nodeName`이 각각 Worker 1/2. 이미지 pull이 늦다면 `describe pod`의 Events로 확인한다.

## 3. Observe — Controller와 실제 HTTP 비교

```bash
kubectl -n lab-daemonset describe ds node-web
kubectl -n lab-daemonset get pods -l app=node-web -o wide --show-labels
kubectl -n lab-daemonset get pods -l app=node-web -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.metadata.ownerReferences[0].kind}{" "}{.spec.nodeName}{" "}{.status.podIP}{"\n"}{end}'
```

각 Worker에서 nginx가 구동 중인지 확인할 때는 해당 Pod IP를 조회해 **실제 접근 가능한 셸**에서 `curl -I http://POD_IP/`를 실행한다. Pod IP가 host 네트워크에서 라우팅 불가능하면 테스트 Pod 또는 `kubectl port-forward`로 접근한다. Ready와 네트워크 도달성은 별도로 검증한다.

## 4. Break & Diagnose — Node 대상 축소

```bash
kubectl label node k8s-worker2 cloud-lab/daemonset-
kubectl -n lab-daemonset get pods -l app=node-web -o wide
kubectl -n lab-daemonset get ds node-web
kubectl -n lab-daemonset describe ds node-web
kubectl -n lab-daemonset get events --sort-by=.lastTimestamp
```

**예상:** Worker2가 더 이상 DaemonSet의 대상이 아니므로 해당 Pod가 정리되고 DESIRED가 1로 감소한다. 이것은 컨테이너 CrashLoopBackOff나 Deployment replica 부족과 **다른 원인**이다. 삭제 전후 변화가 즉시 보이지 않으면 Reconciliation 지연과 Events를 확인한다.

## 5. Recover — Label 복구와 재생성 확인

```bash
kubectl label node k8s-worker2 cloud-lab/daemonset=yes
kubectl -n lab-daemonset rollout status ds/node-web --timeout=180s
kubectl -n lab-daemonset get ds,pods -o wide
```

**예상:** 다시 DESIRED=2, READY=2. Worker2에 새로 생긴 Pod는 **기존과 이름 또는 UID가 달라질 수 있다.** DaemonSet Controller가 API Server에 Pod를 생성하고 Scheduler/kubelet이 Node에서 실행한다는 역할 분담을 설명한다.

## 6. Cleanup — Node Label까지 원상 복구

```bash
kubectl delete namespace lab-daemonset
kubectl label node k8s-worker1 cloud-lab/daemonset-
kubectl label node k8s-worker2 cloud-lab/daemonset-
kubectl get nodes -L cloud-lab/daemonset
```

실습 전 이미 동일 label을 쓰고 있었다면 **기존 값으로 복원**하고 덮어쓰지 않는다. `kubectl get all`은 모든 리소스를 포함하지 않으므로 Namespace 삭제 완료와 Node Label 복원까지 확인한다.

## 실습 기록 (2026-11-05)

- ✅ 시작 전 Node 3대 Ready 및 `cloud-lab/daemonset` Label 부재 확인.
- ✅ Worker 1/2에 `cloud-lab/daemonset=yes` 설정 후 `node-web` DaemonSet 생성.
- ✅ 최종 `DESIRED=2 / CURRENT=2 / READY=2`; Worker 1/2에 각각 1개 Pod Running 확인.
- ✅ 관찰 도중 Worker 1이 잠시 `NotReady` 및 `node.kubernetes.io/unreachable:NoExecute` 상태가 됨. 당시 DaemonSet은 `DESIRED=1 / MISSCHEDULED=1`, Worker 1 Pod는 `ContainerCreating` 및 `Pulling image` 상태였음. 이후 수동 개입 없이 Worker 1과 DaemonSet이 정상화됨. **근본 원인은 확인되지 않았으며 이미지 Pull이 Node 장애를 유발했다는 증거는 없음.**
- ✅ Worker 2 Label 제거 → 대상 Node 1대, `DESIRED=1 / READY=1`; Worker 2 Pod 삭제 확인.
- ✅ Worker 2 Label 복원 → `DESIRED=2 / READY=2`; 기존 Pod `node-web-mcnhx` 대신 신규 `node-web-8crt4` 생성 확인.
- ✅ Namespace `lab-daemonset` 삭제 후 `NotFound`, Worker 1/2 실습 Label 제거 및 3대 모두 Ready 확인.
- ⚪ Pod에 대한 실제 HTTP curl 요청은 수행하지 않았으므로 HTTP 도달성은 검증되지 않음.
- ✅ 복습 3/3 진행: (1) Deployment replicas vs DaemonSet Node당 1개, (2) unreachable:NoExecute에 대한 DaemonSet 자동 toleration, (3) DESIRED 부족의 nodeSelector/taint 원인 구분. 3번의 진단 명령어(`describe ds`, `get nodes --show-labels/-L`, `describe node`)는 해설을 통해 보강했으며 자체 인출은 미완료.

## 7. Explain — 인출 퀴즈 및 완료 기준

- Node가 Ready여도 DaemonSet이 Pod를 만들지 않는 이유 두 가지는?
- `nodeSelector`에 맞지 않게 바뀐 Node의 Pod는 어떻게 되는가?
- DaemonSet Pod가 `Pending`이면 Node label, taint, 요청 자원 중 어떤 증거부터 볼 것인가?

**완료:** 두 Worker에 각각 한 Pod가 Ready → label 변경으로 대상 1대 → 복원 후 다시 2대 Ready → Namespace/Node Label 정리 → 3개 질문을 자신의 말로 설명한다.

참고: [Kubernetes DaemonSet 공식 문서](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/) · [Controller Troubleshooting](../08-controller-troubleshooting/README.md).
