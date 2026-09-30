# Lab 06 — Service ClusterIP

> 학습 단계: **기초 개념·실습 과제**

## 목표

휘발성 Pod IP 대신 Service의 고정 진입점을 사용하는 이유를 확인한다.

## 핵심 개념과 오해 방지

ClusterIP는 Service 객체가 유지되는 동안 안정적인 가상 IP다. Service를 삭제하고 다시 만들면 IP가 달라질 수 있다. API Server나 Service 객체가 HTTP 요청을 직접 중계하는 것은 아니며, kube-proxy 또는 대체 데이터 평면이 EndpointSlice의 backend로 전달한다. 요청마다 정확한 균등 분산을 보장하지 않고, 연결 재사용과 sessionAffinity도 결과에 영향을 준다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. Pod와 ClusterIP Service를 만든다.
2. Service IP:port로 호출한다.
3. Pod를 교체한 뒤 Service IP가 유지되는지 확인한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. selector를 깨뜨려 Service는 존재하지만 요청이 실패하는 상태를 만든다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. `kubectl get svc,endpoints`로 정상 연결을 검증한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.
