# Lab 05 — Basic Scheduling & Resources

> 학습 단계: **상세 가이드**

## 목표

nodeSelector와 requests/limits가 배치 가능 여부와 실행 자원 제어에 미치는 영향을 확인한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. Pod를 worker1에 nodeSelector로 고정하고 실제 배치 Node를 확인한다.
2. memory requests/limits가 있는 Pod를 만들고 `kubectl describe pod`에서 Requests/Limits를 확인한다.
3. `kubectl describe node`의 Allocatable과 현재 요청량을 함께 본다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl describe pod <pod>
kubectl describe node k8s-worker1
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 대상 Node가 수용할 수 없는 큰 memory request를 지정해 Pod를 Pending으로 만든다.
2. `FailedScheduling` Event에서 실제 원인이 insufficient memory인지 확인한다.

> 서로 다른 request 값을 줬을 때 "자원이 가장 많은 Node로 간다"는 식의 배치 예측은 하지 않는다. Scheduler는 여러 조건과 점수를 함께 사용하므로, 이 실습은 **배치 가능/불가능과 request의 의미**에 집중한다.

## Recover

request를 수용 가능한 값으로 낮춰 정상 스케줄링되는지 확인한다.

## 완료 검증

1. requests와 limits의 역할 차이를 설명한다.
2. Pending 상태에서 `Events`가 왜 중요한지 설명한다.

## Cleanup

이 Lab에서 만든 Pod를 삭제한다.

## 설명하기

> Scheduler가 Pod를 배치할 수 있는지를 판단할 때 requests는 ______로 사용되고, limits는 ______을 제한한다.

## 연결된 CKA 강의 전 예습

- [HPA와 축소 안정화 시간](../../07-cka-preview/02-hpa-behavior/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.

- [자원 예산을 계산해 3개 Pod 복구하기](../../07-cka-preview/11-resource-budget/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
