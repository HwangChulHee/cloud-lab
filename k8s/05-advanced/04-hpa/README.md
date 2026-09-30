# Lab 41 — Horizontal Pod Autoscaler

> 학습 단계: **가이드 축소**

## 목표

Metrics를 기반으로 replicas가 자동 조절되는 과정을 확인한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. Metrics Server와 `kubectl top`을 확인한다.
2. requests가 있는 Deployment+Service를 만든다.
3. CPU HPA를 만들고 부하를 발생시켜 scale-out/in을 관찰한다.
4. Memory 기준 HPA도 비교한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod <pod>
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. requests를 제거해 HPA metric 계산 문제가 생기는지 확인하고 원인을 찾는다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. HPA가 어떤 값으로 desired replicas를 바꾸는지 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 CKA 강의 전 예습

- [HPA와 축소 안정화 시간](../../07-cka-preview/02-hpa-behavior/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
