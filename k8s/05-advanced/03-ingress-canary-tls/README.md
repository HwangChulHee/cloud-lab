# Lab 40 — Ingress Canary & TLS

> 학습 단계: **가이드 축소**

## 목표

가중치/헤더 기반 Canary와 HTTPS 종료를 실험한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. v1/v2 backend를 준비한다.
2. canary-weight로 일부 요청만 v2에 전달한다.
3. header 기반 Canary를 확인한다.
4. TLS Secret을 만들고 HTTPS Ingress를 구성한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod <pod>
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 잘못된 TLS Secret 또는 host를 설정해 실패 후 복구한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Blue/Green과 Canary의 트래픽 전환 차이를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 CKA 강의 전 예습

- [Ingress에서 Gateway API로 전환](../../07-cka-preview/07-gateway-migration/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
