# Lab 26 — Readiness Probe

> 학습 단계: **중간 가이드**

## 실습 안내

이 README가 해당 주제의 공식 학습 자료다. **실습 전 상태 확인 → 리소스 구축 → 정상 증거 수집 → 제한된 장애 재현 → 복구 → 정리 → 인출 질문** 순서로 진행한다. 기존 독립 코스는 별도 진도로 계산하지 않는다.

## 목표

Running과 Ready의 차이 및 Service Endpoint 편입 조건을 확인한다.

## 핵심 개념과 오해 방지

Readiness 실패는 일반 Service의 트래픽 대상에서 빠지게 하며 컨테이너를 재시작하지 않는다. liveness와 함께 써야 할 역할이 서로 다르다. HTTP probe의 성공 범위는 200 이상 400 미만이므로 400은 실패다. failureThreshold/successThreshold는 연속 실패·성공 횟수이며, 파일 한 번 생성 후 즉시 Ready라고 단정하지 않는다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

```bash
kubectl apply -f k8s/03-pod-deep-dive/02-readiness-probe/readiness.yaml
kubectl -n lab-readiness rollout status deploy/web --timeout=120s
kubectl -n lab-readiness wait --for=condition=Ready pod/client --timeout=120s
kubectl -n lab-readiness get pods -o wide
kubectl -n lab-readiness get endpointslices -l kubernetes.io/service-name=web -o yaml
kubectl -n lab-readiness exec client -- wget -qO- http://web
```

**예상:** web Ready=True, EndpointSlice ready=True, HTTP 200. Probe는 kubelet이 Pod 내의 파일 존재를 테스트하고, Ready 상태를 API에 보고하면 EndpointSlice Controller가 전달 대상을 갱신한다.

## Break & Diagnose

```bash
kubectl -n lab-readiness exec deploy/web -- rm /tmp/ready
kubectl -n lab-readiness get pods -o wide
kubectl -n lab-readiness get endpointslices -l kubernetes.io/service-name=web -o yaml
kubectl -n lab-readiness describe pod -l app=web
kubectl -n lab-readiness exec client -- wget -T 3 -qO- http://web
```

**예상:** Probe 주기 뒤 Ready=False, EndpointSlice `conditions.ready=false`, HTTP 실패. Pod는 여전히 Running이고 restartCount는 증가하지 않는다. kube-proxy 규칙/요청 전파 지연은 관찰을 통해 구분한다.

## Recover

```bash
kubectl -n lab-readiness exec deploy/web -- touch /tmp/ready
kubectl -n lab-readiness rollout status deploy/web --timeout=120s
kubectl -n lab-readiness get endpointslices -l kubernetes.io/service-name=web
kubectl -n lab-readiness exec client -- wget -qO- http://web
```

## 완료 검증 / Cleanup / Explain

Running과 Ready의 차이, Service DNS가 성공해도 HTTP가 실패할 수 있는 이유, Liveness 실패와 Readiness 실패의 복구 결과 차이를 설명한다.

```bash
kubectl delete namespace lab-readiness
```
