# Lab 31 — Taints & Tolerations

> 학습 단계: **중간 가이드**

## 목표

Node가 Pod를 거부하는 조건과 예외 허용 방식을 확인한다.

## Recall

nodeSelector/Node Affinity처럼 "어디로 갈지 정하는 기능"과 Taint/Toleration처럼 "들어올 수 있는지 제한하는 기능"을 구분한다.

## Build & Observe

1. worker1에 실습용 `hw=gpu:NoSchedule` taint를 건다.
2. worker1을 nodeSelector로 지정한 Pod를 두 개 만들고, toleration 있는 Pod와 없는 Pod를 비교한다.
3. toleration이 있는 Pod만 스케줄링되는지 Events로 확인한다.
4. Toleration만 넣고 nodeSelector를 빼서 **허용했다고 해서 해당 Node를 선택하는 것은 아님**을 확인한다.

## Optional: NoExecute

`NoExecute`는 해당 Node의 기존 Pod를 퇴거시킬 수 있으므로 **현재 worker에 다른 사용자 workload가 없는 것을 확인한 경우에만** 진행한다.

1. 실습용 Pod 두 개를 같은 worker에 배치한다.
2. 한 Pod에는 `tolerationSeconds`를 짧게 지정하고, 다른 Pod에는 시간 제한 없는 NoExecute toleration을 준다.
3. 실습용 NoExecute taint를 적용하고 두 Pod의 퇴거 차이를 관찰한다.
4. 관찰 직후 taint를 제거한다.

## Recover

NoSchedule/NoExecute 실습용 taint를 모두 제거하고 Node 상태가 정상인지 확인한다.

## 완료 검증

1. NoSchedule / PreferNoSchedule / NoExecute 차이를 설명한다.
2. Toleration은 Node 선택 기능이 아니라 taint에 대한 **허용 조건**임을 설명한다.

## Cleanup

Pod와 실습용 Node label/taint를 모두 삭제한다. `kubectl describe node`로 taint가 남지 않았는지 확인한다.

## 설명하기

> Taint는 Node가 Pod를 ______하기 위한 조건이고, Toleration은 그 조건을 ______하지만 해당 Node를 선택해 주지는 않는다.
