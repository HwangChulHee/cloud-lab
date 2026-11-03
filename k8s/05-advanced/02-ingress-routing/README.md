# Lab 39 — Ingress: Host / Path 라우팅

> **필수** · 기존 1.27 Vagrant 클러스터 · 공용 Traefik 필요 · `lab-self-edge` Namespace

## 1. Overview / Recall

Ingress는 HTTP(S) 요청의 host/path 규칙을 선언하는 API 객체이고, 실제 트래픽을 전달하는 주체는 **Ingress Controller**다. IngressClass가 존재해도 Controller/Backend가 없다면 요청은 성공하지 않는다.

시작 전에 Service → EndpointSlice → Pod 전달 과정과 IngressClass의 역할을 설명한다.

## 2. 준비와 정상 구축

[애드온 설치 가이드](../../guides/ADDONS.md#traefik-ingress)의 Traefik을 확인하고 **없을 때만** 설치한다. 공용 Controller를 이 Lab에서 삭제하지 않는다.

```bash
kubectl get ingressclass
kubectl -n lab-self-ingress get deploy,svc traefik
kubectl apply -f k8s/05-advanced/02-ingress-routing/routing-lab.yaml
kubectl -n lab-self-edge rollout status deploy/shopping --timeout=120s
kubectl -n lab-self-edge rollout status deploy/customer --timeout=120s
kubectl -n lab-self-edge get ingress,svc,pods -o wide
kubectl -n lab-self-edge get endpointslices
```

**예상:** shopping/customer Pod 각각 Ready, 두 Service의 EndpointSlice에 준비된 주소가 존재한다.

## 3. Host / Path와 직접 연결을 구분

첫 셸에서 아래 명령을 실행하고 그대로 유지한다.

```bash
kubectl -n lab-self-ingress port-forward svc/traefik 8080:80
```

같은 머신의 **두 번째 셸**에서 실행한다.

```bash
curl -fsS -H 'Host: shop.study.local' http://127.0.0.1:8080/shopping
curl -fsS -H 'Host: shop.study.local' http://127.0.0.1:8080/customer
curl -fsS -H 'Host: customer.study.local' http://127.0.0.1:8080/
curl -i -H 'Host: wrong.study.local' http://127.0.0.1:8080/shopping
```

**예상:** 순서대로 `shopping`, `customer`, `customer`가 나오고, 마지막 요청은 이 Ingress의 규칙과 매칭되지 않아 404 계열 응답이 나온다. Host와 Path는 함께 평가된다.

## 4. Break — 존재하지 않는 Backend

```bash
kubectl -n lab-self-edge patch ingress shop-routes --type=json \
  -p='[{"op":"replace","path":"/spec/rules/0/http/paths/0/backend/service/name","value":"missing-shopping"}]'
kubectl -n lab-self-edge describe ingress shop-routes
kubectl -n lab-self-edge get svc,endpointslices
curl -i -H 'Host: shop.study.local' http://127.0.0.1:8080/shopping
curl -fsS -H 'Host: shop.study.local' http://127.0.0.1:8080/customer
kubectl -n lab-self-ingress logs deploy/traefik --tail=50
```

**예상:** shopping만 실패하고 customer는 계속 성공한다. `kubectl get pods`가 Running이라고 해서 Ingress 라우팅이 정상이라는 증거는 아니다. 오류 응답 상태는 Controller 구현에 따라 다르므로 특정 숫자 하나를 강제하지 않는다.

## 5. Recover

```bash
kubectl -n lab-self-edge patch ingress shop-routes --type=json \
  -p='[{"op":"replace","path":"/spec/rules/0/http/paths/0/backend/service/name","value":"shopping"}]'
curl -fsS -H 'Host: shop.study.local' http://127.0.0.1:8080/shopping
kubectl -n lab-self-edge get ingress shop-routes -o yaml
```

**예상:** `shopping` 응답이 다시 나온다. 단순 재시작이 아니라 **잘못 변경한 Service 참조만 원복**했는지 확인한다.

## 6. Cleanup / Explain

port-forward 셸은 Ctrl+C로 종료한다. 다른 Lab의 자산이 없다면 아래처럼 앱 오브젝트만 제거한다.

```bash
kubectl -n lab-self-edge delete ingress/shop-routes deployment/shopping deployment/customer service/shopping service/customer --ignore-not-found
```

이 YAML에는 공용 Traefik이 감시하는 `lab-self-edge` Namespace도 포함되어 있다. 위 명령은 **앱 리소스만 삭제하며 Namespace와 Traefik RBAC를 보존**한다. 모든 Ingress 실습을 끝낸 뒤 [애드온 정리](../../guides/ADDONS.md#애드온-정리)를 따른다.

**인출 질문:** (1) Ingress와 Controller의 책임 구분 (2) Service와 EndpointSlice가 정상인데 외부 HTTP만 실패하는 세 가지 원인 (3) Host 불일치와 backend Service 불일치를 구별할 증거는?

완료 기준: host/path 조합 3개 성공 → 한 backend만 실패 → Controller/Ingress/Service 증거 기록 → 최소 수정 복구 → 공유 리소스를 보존한 정리.

다음: [Lab 40 Ingress TLS/Canary](../03-ingress-canary-tls/README.md). [Gateway API 전환 연습](../../07-cka-preview/07-gateway-migration/README.md)은 별도 CKA 문제로 유지한다.
