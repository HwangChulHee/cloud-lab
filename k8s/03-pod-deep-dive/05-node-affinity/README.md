# Lab 29 — Node Affinity

> 학습 단계: **중간 가이드**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../03-pod-deep-dive/08-scheduling-troubleshooting/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

## 목표

required/preferred와 matchExpressions로 Node 선택을 제어한다.

## 핵심 개념과 오해 방지

required는 후보 노드를 걸러내고 preferred는 후보의 점수에 영향을 준다. preferred weight 하나만으로 특정 노드 배치를 보장하지 않는다. nodeSelectorTerms 사이에는 OR, 한 term의 matchExpressions 사이에는 AND가 적용된다. IgnoredDuringExecution은 배치 후 노드 라벨이 바뀌어도 이 조건만으로 기존 Pod가 자동 이동하지 않는다는 뜻이다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

Worker1/2의 실제 이름을 먼저 확인한다. 아래는 기본 Vagrant 환경의 Worker 이름을 가정한다.

```bash
kubectl get nodes -L cloud-lab/affinity-zone
kubectl label node k8s-worker1 cloud-lab/affinity-zone=west
kubectl label node k8s-worker2 cloud-lab/affinity-zone=east
kubectl apply -f k8s/03-pod-deep-dive/05-node-affinity/affinity.yaml
kubectl -n lab-node-affinity get pods -o wide
kubectl -n lab-node-affinity describe pod impossible
```

**예상:** required는 worker1에만, impossible은 Pending + FailedScheduling, preferred는 선호 조건을 만족하는 Node가 없어도 가능한 worker에 배치된다. Preferred는 강제 제약이 아니다. 실제 Scheduler의 다른 Score 요소 때문에 preferred Pod의 정확한 Node는 고정하지 않는다.

## Break & Diagnose

`required` Pod가 놓인 뒤 worker1의 `cloud-lab/affinity-zone` label을 변경하면 **IgnoredDuringExecution**으로 인해 기존 Pod를 즉시 퇴거시키지 않는다는 점을 관찰한다.

```bash
kubectl label node k8s-worker1 cloud-lab/affinity-zone=other --overwrite
kubectl -n lab-node-affinity get pods -o wide
kubectl -n lab-node-affinity describe pod impossible
```

## Recover / Cleanup

```bash
kubectl label node k8s-worker1 cloud-lab/affinity-zone=west --overwrite
kubectl delete namespace lab-node-affinity
kubectl label node k8s-worker1 cloud-lab/affinity-zone-
kubectl label node k8s-worker2 cloud-lab/affinity-zone-
```

기존에 같은 key가 있었다면 **원래 값으로 복원**한다. 인출: required Filter와 preferred Score의 차이, nodeSelectorTerms 사이 OR / matchExpressions 사이 AND, IgnoredDuringExecution의 의미.
