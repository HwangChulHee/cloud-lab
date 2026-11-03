# 07. Ingress에서 Gateway API로 전환

> 독립 실행 가능한 확장 실습 · 참고 주제: task-gateway · 환경: 별도 1.34 예습 클러스터 + Ingress/Gateway Controller

기초 연결: [Ingress TLS](../../05-advanced/03-ingress-canary-tls/README.md) · [Ingress Routing](../../05-advanced/02-ingress-routing/README.md)

[독립 과정에서의 위치](../../guides/PLATFORM.md). 처음에는 예시 풀이를 참고해 구축하고, 두 번째에는 요구사항만 보고 실행한다. 강의 수강은 선행 조건이 아니다.

## 먼저 이해할 것

GatewayClass는 구현 선택, Gateway는 listener와 TLS, HTTPRoute는 host/path/backend 연결을 담당한다. 리소스 생성만으로 성공을 판단하지 않고 Accepted/Programmed/ResolvedRefs와 실제 HTTPS 요청을 확인한다. 이 과제의 유지 대상은 HTTPS host·인증서·경로·backend이며 HTTP redirect는 추가 과제로 둔다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/07-gateway-migration`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

[환경 준비](../ENVIRONMENT.md)의 Gateway 조건을 충족한 뒤 실행한다.

```bash
kubectl get ingressclass,gatewayclass
kubectl api-resources --api-group=gateway.networking.k8s.io
kubectl apply -f setup.yaml
openssl req -x509 -nodes -newkey rsa:2048 -days 2 \
  -keyout /tmp/preview-gateway.key -out /tmp/preview-gateway.crt \
  -subj '/CN=preview.local' -addext 'subjectAltName=DNS:preview.local'
kubectl -n preview-gateway create secret tls web-tls \
  --key=/tmp/preview-gateway.key --cert=/tmp/preview-gateway.crt
```

`old-ingress.yaml`의 클래스 placeholder를 바꾸고 apply한다. 기존 Controller Service의 443을 로컬 8443으로 port-forward해 `curl --cacert /tmp/preview-gateway.crt --resolve preview.local:8443:127.0.0.1 https://preview.local:8443/`가 성공하는 기준선을 만든다.

## 2. 직접 바꿔보기

1. 기존 Ingress의 TLS와 backend를 조사한다.
2. 같은 host `preview.local`, 인증서 `web-tls`, HTTPS 443 listener로 Gateway를 만든다.
3. 같은 `/` 경로를 `web:80`에 연결하는 HTTPRoute를 만든다.
4. Gateway 경유 HTTPS가 성공한 뒤 Ingress를 삭제한다.
5. HTTPRoute backend 이름을 잘못 바꿔 ResolvedRefs와 실제 요청을 비교하고 복구한다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

```bash
kubectl -n preview-gateway get gateway web-gateway -o yaml
kubectl -n preview-gateway get httproute web-route -o yaml
kubectl -n preview-gateway get svc
```

Gateway 구현이 생성한 데이터 평면 Service의 이름과 HTTPS 포트를 확인해 9443으로 port-forward한다. Controller의 관리용 Service와 혼동하지 않는다.

```bash
curl --cacert /tmp/preview-gateway.crt --resolve preview.local:9443:127.0.0.1 https://preview.local:9443/
kubectl -n preview-gateway get ingress
```

Nginx 응답 성공, Gateway Accepted/Programmed, Route Accepted/ResolvedRefs, Ingress 삭제를 확인한다. HTTPRoute Conditions는 status.parents 아래에 있다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

`solution.yaml`의 GatewayClass를 실제 값으로 바꾼다.

```bash
kubectl apply -f solution.yaml
kubectl -n preview-gateway get gateway,httproute
# HTTPS 검증을 마친 뒤에만 실행
kubectl -n preview-gateway delete ingress web
kubectl -n preview-gateway patch httproute web-route --type=json \
  -p='[{"op":"replace","path":"/spec/rules/0/backendRefs/0/name","value":"missing"}]'
kubectl -n preview-gateway get httproute web-route -o yaml
kubectl apply -f solution.yaml
```

서로 다른 namespace의 Secret/Service를 참조하는 경우 별도의 허용 조건이 필요하다. 이 실습은 모두 같은 namespace에 둔다.

</details>

[Gateway Canary 가중치·헤더 비교](../../07-cka-preview/07-gateway-migration/README.md)를 이어 할 경우 아래 정리를 하기 전에 실행한다.

## 4. 정리 및 재실행

port-forward를 종료한다. 공용 CRD/Controller는 삭제하지 않는다.

```bash
kubectl delete namespace preview-gateway
rm -f /tmp/preview-gateway.key /tmp/preview-gateway.crt
```

## 스스로 설명할 질문

- Gateway와 HTTPRoute를 분리하면 관리 책임을 어떻게 나눌 수 있는가?
- 정상으로 생성됐지만 ResolvedRefs=False이면 어디를 확인할 것인가?

[전체 확장 경로](../README.md)


## Gateway Canary — 이전 확장 실습 병합


별도 1.34 환경의 [07 Gateway](./README.md) 1–3단계에서 HTTPS를 정상 확인한 뒤, **07의 정리 전에** 진행한다. 이미 정리했다면 Gateway/TLS/HTTPRoute를 해당 문서대로 다시 구축한다. Gateway 데이터 평면 Service를 9443:443으로 port-forward한 첫 셸을 유지하고 같은 머신의 두 번째 셸에서 실행한다.

### 먼저 이해할 것

Blue/Green은 Service 대상을 한 번에 바꾼다. Canary는 두 버전을 함께 운영하며 일부 트래픽을 새 버전에 준다. weight는 장기적인 분배 비율이지 10번 요청마다 정확히 8/2를 보장하는 설정이 아니다. 헤더 조건은 특정 요청을 새 버전으로 보내는 별도 기준이다.

### 따라 하기

```bash
kubectl apply -f k8s/07-cka-preview/07-gateway-migration/canary.yaml
kubectl -n preview-gateway rollout status deploy/stable --timeout=120s
kubectl -n preview-gateway rollout status deploy/canary --timeout=120s
kubectl -n preview-gateway get httproute web-route -o yaml
curl --cacert /tmp/preview-gateway.crt --resolve preview.local:9443:127.0.0.1 -H 'X-Canary: always' https://preview.local:9443/
```

Route의 Accepted/ResolvedRefs를 먼저 확인한다. 헤더 요청은 v2다. 헤더 없는 요청은 80/20 가중치로 두 backend를 사용한다.

```bash
for i in $(seq 1 100); do
  curl -fsS --max-time 5 --cacert /tmp/preview-gateway.crt \
    --resolve preview.local:9443:127.0.0.1 https://preview.local:9443/
done | sort | uniq -c
```

v1/v2 횟수를 비교한다. 실패 curl을 응답 비율로 세지 말고 먼저 TLS/Route/endpoint를 복구한다. 고정된 정확한 80/20 횟수는 완료 조건이 아니다.

### 변경 → 복구

헤더 없는 기본 경로에서 canary weight를 0으로 바꾸고, 새 요청에서 v1만 받는지 비교한다. 첫 번째 헤더 rule은 여전히 v2로 간다.

```bash
kubectl -n preview-gateway patch httproute web-route --type=json \
  -p='[{"op":"replace","path":"/spec/rules/1/backendRefs/1/weight","value":0}]'
curl --cacert /tmp/preview-gateway.crt --resolve preview.local:9443:127.0.0.1 https://preview.local:9443/
curl --cacert /tmp/preview-gateway.crt --resolve preview.local:9443:127.0.0.1 -H 'X-Canary: always' https://preview.local:9443/
kubectl apply -f k8s/07-cka-preview/07-gateway-migration/canary.yaml
```

### 정리

기본 경로를 원래 web Service로 되돌린다. Deployment/Service만 삭제하고 Gateway나 공유 CRD를 지우지 않는다.

```bash
kubectl -n preview-gateway patch httproute web-route --type=merge \
  -p='{"spec":{"rules":[{"matches":[{"path":{"type":"PathPrefix","value":"/"}}],"backendRefs":[{"name":"web","port":80}]}]}}'
kubectl -n preview-gateway delete deploy stable canary
kubectl -n preview-gateway delete svc stable canary
```

원래 HTTPS 응답을 확인하고 07 문서의 port-forward/namespace/인증서 정리를 완료한다.

[플랫폼 경로](./PLATFORM.md) · [독립 학습 순서](./README.md)
