# Lab 40 — Ingress Canary & TLS

> 학습 단계: **가이드 축소**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/08-operations/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

가중치/헤더 기반 Canary와 HTTPS 종료를 실험한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. v1/v2 backend를 준비한다.
2. 기존 격리된 ingress-nginx 학습 환경에서만 nginx.ingress.kubernetes.io/canary와 canary-weight로 일부 요청을 v2에 전달한다. 이 annotation은 Ingress 표준이 아니므로 다른 Controller에 그대로 적용하지 않는다. 신규 환경에서는 해당 구현의 트래픽 분할 기능 또는 Gateway API HTTPRoute의 backendRefs.weight로 대체한다.
3. header 기반 Canary를 확인한다.
4. TLS Secret을 만들고 HTTPS Ingress를 구성한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 잘못된 TLS Secret 또는 host를 설정하고 실제 인증서/SNI/응답을 비교한 뒤 복구한다. Controller에 따라 기본 인증서로 HTTPS 연결이 계속될 수 있으므로 curl -k의 성공만으로 정상 TLS 설정이라고 판단하지 않는다. 자체 서명 인증서는 --cacert와 --resolve로 검증한다.

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

## 연결된 확장 실습

- [Ingress에서 Gateway API로 전환](../../07-cka-preview/07-gateway-migration/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
