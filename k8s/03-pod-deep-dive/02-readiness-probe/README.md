# Lab 26 — Readiness Probe

> 학습 단계: **중간 가이드**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/05-resources-scheduling/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

Running과 Ready의 차이 및 Service Endpoint 편입 조건을 확인한다.

## 핵심 개념과 오해 방지

Readiness 실패는 일반 Service의 트래픽 대상에서 빠지게 하며 컨테이너를 재시작하지 않는다. liveness와 함께 써야 할 역할이 서로 다르다. HTTP probe의 성공 범위는 200 이상 400 미만이므로 400은 실패다. failureThreshold/successThreshold는 연속 실패·성공 횟수이며, 파일 한 번 생성 후 즉시 Ready라고 단정하지 않는다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. readiness exec probe Pod와 Service를 만든다.
2. Ready=false일 때 EndpointSlice에 주소가 남아 있어도 conditions.ready=false라 일반 Service 트래픽 대상에서 제외되는지 확인한다. legacy Endpoints에서는 notReadyAddresses도 비교한다. publishNotReadyAddresses는 기본 false로 둔다.
3. ready.txt를 생성해 probe 성공 후 Endpoint 편입을 관찰한다.
4. Events와 Conditions를 함께 본다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. ready.txt를 다시 제거해 트래픽 대상에서 빠지는지 확인한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Readiness 실패 시 Pod가 재시작되는지 여부를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.
