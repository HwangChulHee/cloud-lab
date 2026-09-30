# Gateway Canary — 가중치와 헤더 조건 비교

별도 1.34 환경의 [07 Gateway](../07-cka-preview/07-gateway-migration/README.md) 1–3단계에서 HTTPS를 정상 확인한 뒤, **07의 정리 전에** 진행한다. 이미 정리했다면 Gateway/TLS/HTTPRoute를 해당 문서대로 다시 구축한다. Gateway 데이터 평면 Service를 9443:443으로 port-forward한 첫 셸을 유지하고 같은 머신의 두 번째 셸에서 실행한다.

## 먼저 이해할 것

Blue/Green은 Service 대상을 한 번에 바꾼다. Canary는 두 버전을 함께 운영하며 일부 트래픽을 새 버전에 준다. weight는 장기적인 분배 비율이지 10번 요청마다 정확히 8/2를 보장하는 설정이 아니다. 헤더 조건은 특정 요청을 새 버전으로 보내는 별도 기준이다.

## 따라 하기

```bash
kubectl apply -f k8s/08-independent/canary.yaml
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

## 변경 → 복구

헤더 없는 기본 경로에서 canary weight를 0으로 바꾸고, 새 요청에서 v1만 받는지 비교한다. 첫 번째 헤더 rule은 여전히 v2로 간다.

```bash
kubectl -n preview-gateway patch httproute web-route --type=json \
  -p='[{"op":"replace","path":"/spec/rules/1/backendRefs/1/weight","value":0}]'
curl --cacert /tmp/preview-gateway.crt --resolve preview.local:9443:127.0.0.1 https://preview.local:9443/
curl --cacert /tmp/preview-gateway.crt --resolve preview.local:9443:127.0.0.1 -H 'X-Canary: always' https://preview.local:9443/
kubectl apply -f k8s/08-independent/canary.yaml
```

## 정리

기본 경로를 원래 web Service로 되돌린다. Deployment/Service만 삭제하고 Gateway나 공유 CRD를 지우지 않는다.

```bash
kubectl -n preview-gateway patch httproute web-route --type=merge \
  -p='{"spec":{"rules":[{"matches":[{"path":{"type":"PathPrefix","value":"/"}}],"backendRefs":[{"name":"web","port":80}]}]}}'
kubectl -n preview-gateway delete deploy stable canary
kubectl -n preview-gateway delete svc stable canary
```

원래 HTTPS 응답을 확인하고 07 문서의 port-forward/namespace/인증서 정리를 완료한다.

[플랫폼 경로](./PLATFORM.md) · [독립 학습 순서](./README.md)
