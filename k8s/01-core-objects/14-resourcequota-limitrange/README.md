# Lab 16 — ResourceQuota & LimitRange

> 학습 단계: **상세 가이드**

## 목표

Namespace 단위 자원 정책이 Pod 생성에 미치는 영향을 확인한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. memory requests/limits ResourceQuota를 만든다.
2. 자원값 없는 Pod 생성 실패를 확인한다.
3. 누적 quota 초과와 pod 개수 quota 초과를 확인한다.
4. LimitRange의 default/min/max를 적용해 자동 주입과 거부를 관찰한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod <pod>
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 정책을 만족하지 않는 Pod YAML을 단계별로 수정해 성공시킨다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. 거부 메시지에서 어떤 정책이 원인인지 식별한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.
