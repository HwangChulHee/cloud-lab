# Lab 29 — Node Affinity

> 학습 단계: **중간 가이드**

## 목표

required/preferred와 matchExpressions로 Node 선택을 제어한다.

## 핵심 개념과 오해 방지

required는 후보 노드를 걸러내고 preferred는 후보의 점수에 영향을 준다. preferred weight 하나만으로 특정 노드 배치를 보장하지 않는다. nodeSelectorTerms 사이에는 OR, 한 term의 matchExpressions 사이에는 AND가 적용된다. IgnoredDuringExecution은 배치 후 노드 라벨이 바뀌어도 이 조건만으로 기존 Pod가 자동 이동하지 않는다는 뜻이다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. worker1/2에 서로 다른 label을 붙인다.
2. required affinity로 특정 Node에 배치한다.
3. 존재하지 않는 label required로 Pending을 만든다.
4. 같은 조건을 preferred로 바꿔 fallback 배치를 확인한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. preferred weight를 다르게 설정해 선호도를 비교한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. required와 preferred 차이를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.
