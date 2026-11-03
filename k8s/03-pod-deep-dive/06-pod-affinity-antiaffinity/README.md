# Lab 30 — Pod Affinity / Anti-Affinity

> 학습 단계: **중간 가이드**

## 실습 안내

이 README가 해당 주제의 공식 학습 자료다. **실습 전 상태 확인 → 리소스 구축 → 정상 증거 수집 → 제한된 장애 재현 → 복구 → 정리 → 인출 질문** 순서로 진행한다. 기존 독립 코스는 별도 진도로 계산하지 않는다.

## 목표

다른 Pod의 label을 기준으로 함께/분리 배치한다.

## 핵심 개념과 오해 방지

topologyKey가 kubernetes.io/hostname이면 같은/다른 노드이고, topology.kubernetes.io/zone이면 같은/다른 zone을 의미한다. PodAffinity를 항상 같은 노드 배치라고 일반화하지 않는다. 기본 탐색 namespace 범위와 labelSelector도 확인한다. required Pod anti-affinity는 admission 설정에 따라 hostname topology만 허용할 수 있으므로, 기본 실습은 hostname을 사용한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

기본 Worker1의 기존 `cloud-lab/affinity-anchor` label이 없음을 확인한다. `anchor`를 worker1에 놓고 다른 두 Pod의 affinity/anti-affinity를 비교한다.

```bash
kubectl get nodes -L cloud-lab/affinity-anchor
kubectl label node k8s-worker1 cloud-lab/affinity-anchor=yes
kubectl apply -f k8s/03-pod-deep-dive/06-pod-affinity-antiaffinity/pod-affinity.yaml
kubectl -n lab-pod-affinity get pods -o wide
kubectl -n lab-pod-affinity describe pod near
kubectl -n lab-pod-affinity describe pod away
```

**예상:** anchor/near는 같은 Node, away는 다른 eligible Node. `topologyKey: kubernetes.io/hostname`은 **Node 단위**의 근접·분리를 의미한다. 두 Worker가 준비되지 않은 클러스터에서는 away가 Pending인 것이 제약에 따른 결과일 수 있다.

## Break & Diagnose

anchor가 사라지면 새로운 required PodAffinity가 충족되지 않을 수 있다. 기존 near Pod가 자동으로 옮겨지는 것은 아니다.

```bash
kubectl -n lab-pod-affinity delete pod anchor
kubectl -n lab-pod-affinity get pods -o wide
kubectl -n lab-pod-affinity get events --sort-by=.lastTimestamp
```

새 Pod를 관찰하기 위해 동일 manifest에서 anchor만 다시 생성하고 Scheduling 상태를 확인한다. 삭제된 Pod를 자동 복구하는 Controller가 없음을 설명한다.

## Recover / Cleanup

```bash
kubectl delete namespace lab-pod-affinity
kubectl label node k8s-worker1 cloud-lab/affinity-anchor-
```

Node label을 기존 값으로 복원한다. 인출: Node Affinity와 Pod Affinity의 label 대상 차이, hostname과 zone topology 차이, 필수 anti-affinity에서 Pending이 발생하는 이유.
