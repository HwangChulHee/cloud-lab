# 04. Service·DNS·EndpointSlice로 연결 추적하기

## 먼저 이해할 것

Service selector는 Pod label을 고르고 EndpointSlice에 주소가 기록된다. ClusterIP는 그 backend에 접근하는 가상 주소다. Headless는 backend 주소를 DNS로 제공한다. ExternalName은 DNS 별칭이며 프록시가 아니다. Service가 있어도 endpoint가 없으면 앱에 전달할 수 없다.

## 따라 하기

```bash
kubectl apply -f k8s/08-independent/04-networking/setup.yaml
kubectl -n lab-self-network rollout status deploy/web --timeout=120s
kubectl -n lab-self-network wait --for=condition=Ready pod/client pod/named --timeout=120s
kubectl -n lab-self-network exec client -- nslookup web
kubectl -n lab-self-network exec client -- nslookup web.lab-self-network.svc.cluster.local
kubectl -n lab-self-network exec client -- wget -qO- http://web
kubectl -n lab-self-network get svc web
kubectl -n lab-self-network get endpointslices -l kubernetes.io/service-name=web -o wide
kubectl -n lab-self-network exec client -- nslookup named.headless.lab-self-network.svc.cluster.local
kubectl -n lab-self-network exec client -- nslookup outside
```

web DNS 응답은 Service IP이고 named의 DNS 응답은 Pod IP다. cluster domain을 변경한 환경이면 cluster.local을 실제 값으로 바꾼다. outside 조회는 클러스터 외부 DNS가 가능한 환경에서 CNAME/외부 주소를 보여준다. 외부 DNS가 막혀도 web의 내부 DNS와는 별개 문제다.

## 변경 → 실패 → 복구

```bash
kubectl -n lab-self-network patch svc web --type=merge -p '{"spec":{"selector":{"app":"missing"}}}'
kubectl -n lab-self-network get endpointslices -l kubernetes.io/service-name=web -o yaml
kubectl -n lab-self-network exec client -- wget -T 3 -qO- http://web
kubectl -n lab-self-network patch svc web --type=merge -p '{"spec":{"selector":{"app":"web"}}}'
kubectl -n lab-self-network exec client -- wget -T 3 -qO- http://web
```

DNS는 성공해도 HTTP는 실패할 수 있다. selector 복구 후 nginx HTML이 돌아와야 한다. EndpointSlice controller와 데이터 평면 반영에는 지연이 있을 수 있다.

## selector 없는 Service를 수동으로 연결하기

```bash
BACKEND_IP=$(kubectl -n lab-self-network get pod -l app=web -o jsonpath='{.items[0].status.podIP}')
sed "s/REPLACE_BACKEND_IP/$BACKEND_IP/" k8s/08-independent/04-networking/manual-endpoint.yaml > /tmp/lab-self-endpoint.yaml
kubectl apply -f /tmp/lab-self-endpoint.yaml
kubectl -n lab-self-network exec client -- wget -T 3 -qO- http://manual
```

nginx HTML을 예상한다. web Pod가 교체되면 수동 EndpointSlice의 주소는 자동 갱신되지 않는다. 주소 갱신의 주체를 selector 기반 Service와 비교한다.

## NodePort와 LoadBalancer로 확장

[외부 트래픽 정책 실습](../../01-core-objects/05-service-nodeport/README.md#트래픽-정책과-loadbalancer-비교-실습)을 실행한다. 별도 lab-service-path namespace를 만들고, Windows에서 두 worker를 호출해 Cluster/Local 결과표를 채운 뒤 그 namespace를 정리한다. 외부 LB 구현 없이 Pending인 상태는 LB 동작 완료와 구분해 기록한다.

## 완료와 정리

`이름 → Service → EndpointSlice → Pod` 중 어디가 잘못되면 DNS만 성공하는지 설명한다.

```bash
kubectl delete namespace lab-self-network
rm -f /tmp/lab-self-endpoint.yaml
```

다음: [05 자원·Probe·배치](../05-resources-scheduling/README.md).

[독립 학습 순서](../README.md)
