# Lab 31 — Taints & Tolerations

> 학습 단계: **중간 가이드**

## 실습 안내

이 README가 해당 주제의 공식 학습 자료다. **실습 전 상태 확인 → 리소스 구축 → 정상 증거 수집 → 제한된 장애 재현 → 복구 → 정리 → 인출 질문** 순서로 진행한다. 기존 독립 코스는 별도 진도로 계산하지 않는다.

## 목표

Node가 Pod를 거부하는 조건과 예외 허용 방식을 확인한다.

## Recall

nodeSelector/Node Affinity처럼 "어디로 갈지 정하는 기능"과 Taint/Toleration처럼 "들어올 수 있는지 제한하는 기능"을 구분한다.

## Build & Observe

실습 대상은 본인 Vagrant Worker1이며 **NoSchedule만 사용**한다. 노드에 원래 존재하는 Taint와 label을 먼저 기록한다. 다른 사용자의 workload가 없는지 확인한다.

```bash
kubectl get nodes -o wide
kubectl describe node k8s-worker1
kubectl get nodes -L cloud-lab/taint-demo
kubectl label node k8s-worker1 cloud-lab/taint-demo=target
kubectl taint node k8s-worker1 cloud-lab/lab31=true:NoSchedule
kubectl apply -f k8s/03-pod-deep-dive/07-taints-tolerations/taints.yaml
kubectl -n lab-taints get pods -o wide
kubectl -n lab-taints describe pod blocked
kubectl -n lab-taints describe pod allowed
```

**예상:** blocked는 NodeSelector로 worker1만 선택하지만 NoSchedule taint를 감당하지 못해 Pending, allowed는 Toleration이 있으므로 worker1에서 Running이다. 다른 Worker로 우회하지 못하도록 **둘 다 nodeSelector를 사용했다**.

## Break & Diagnose

`kubectl describe pod blocked`의 `FailedScheduling` Event에서 untolerated taint를 확인한다. `PodScheduled=False`와 `Ready=False`를 구분한다. Toleration은 Node를 선택하는 수단이 아니라 **배치 허용 조건**이다. NoExecute는 기존 Pod까지 퇴거시킬 수 있으므로 기본 실습에서 사용하지 않는다.

## Recover / Cleanup

```bash
kubectl taint node k8s-worker1 cloud-lab/lab31:NoSchedule-
kubectl -n lab-taints get pods -o wide
kubectl -n lab-taints wait --for=condition=Ready pod/blocked --timeout=120s
kubectl delete namespace lab-taints
kubectl label node k8s-worker1 cloud-lab/taint-demo-
kubectl describe node k8s-worker1
```

기존 동일 key가 있었다면 무작정 덮어쓰지 말고 원래 값으로 되돌린다. 인출: NoSchedule/PreferNoSchedule/NoExecute 차이, Taint와 Affinity 차이, tolerationSeconds의 의미.
