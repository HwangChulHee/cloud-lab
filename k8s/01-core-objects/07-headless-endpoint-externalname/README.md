# Lab 09 — Headless, Endpoint, ExternalName

> 학습 단계: **기초 개념·실습 과제**  
> **실습 상태: ✅ 완료 (2026-10-22)**

## 실습 안내

이 README가 해당 주제의 공식 학습 자료다. **실습 전 상태 확인 → 리소스 구축 → 정상 증거 수집 → 제한된 장애 재현 → 복구 → 정리 → 인출 질문** 순서로 진행한다. 기존 독립 코스는 별도 진도로 계산하지 않는다.

## 목표

Service discovery의 세 가지 변형을 비교한다.

## 핵심 개념과 오해 방지

Headless Service(`clusterIP: None`)는 Service 가상 IP 대신 backend 주소를 DNS에 제공한다. 개별 Pod의 안정적인 이름은 hostname/subdomain 또는 StatefulSet의 serviceName 구성과 Ready 조건을 함께 확인한다. 임의 Pod의 metadata.name만으로 모든 Pod별 DNS가 생긴다고 가정하지 않는다.

ExternalName은 외부 이름을 가리키는 DNS CNAME이다. proxy, 포트 변환, HTTP Host 변경, TLS SNI 변경을 수행하지 않는다. DNS 별칭 조회가 성공해도 HTTP 가상 호스트나 인증서 이름 때문에 요청이 실패할 수 있으므로 `nslookup`과 실제 요청을 별도로 검증한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. Headless Service를 만들고 DNS가 Pod IP를 반환하는지 확인한다.
2. selector 기반 Endpoint를 조회한다.
3. selector 없는 Service + 수동 EndpointSlice를 연결한다. discovery.k8s.io/v1, kubernetes.io/service-name 라벨, 고유 endpointslice.kubernetes.io/managed-by 라벨과 실제 backend IP/port를 지정한다. legacy Endpoints는 1.27 비교 관찰에만 사용한다.
4. ExternalName Service로 외부 도메인을 추상화한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 잘못된 Endpoint IP를 넣어 연결 실패를 재현한 뒤 복구한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. ClusterIP/Headless/ExternalName의 결과 차이를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 실습 완료 기록 (2026-10-22)

- [x] `lab-headless` namespace 생성 및 Active 확인.
- [x] `web-1` Pod는 `k8s-worker1` (`20.100.194.84`), `web-2` Pod는 `k8s-worker2` (`20.110.126.10`)에서 Running/Ready 확인.
- [x] `web-headless` Service `clusterIP: None` 및 EndpointSlice에 양쪽 Pod IP 자동 등록 확인.
- [x] BusyBox `dns-client`에서 Headless FQDN 조회 시 실제 Pod IP 두 개 반환 확인.
- [x] 각각의 Pod에 직접 HTTP 접근 성공. Headless DNS 이름으로 10회 HTTP 요청 시 Worker 1: 6회 / Worker 2: 4회 응답. 이는 kube-proxy VIP 로드밸런싱이 아닌 클라이언트 주소 선택 결과임.
- [x] selector 없는 `manual-svc` 생성 시 ClusterIP `10.109.43.79`는 있으나 자동 EndpointSlice가 없는 것 확인.
- [x] 수동 EndpointSlice `manual-svc-1`을 Worker 1의 실제 Pod IP `20.100.194.84`로 지정하고 `wget http://10.109.43.79` HTTP 성공 확인.
- [x] EndpointSlice IP를 `20.100.194.200`으로 변경했을 때 `wget: download timed out` 재현, 원본 IP로 복원 후 HTTP 정상 확인.
- [x] `external-web` ExternalName Service가 `example.com`을 가리키는 CNAME을 반환하고 외부 DNS에서 A/AAAA 레코드가 조회되는 것 확인.
- [x] `lab-headless` namespace 삭제 후 `NotFound` 확인.

> 수동 EndpointSlice의 `ready: true`는 실제 서버의 가용성을 자동 검증하지 않는다. ExternalName은 HTTP 프록시가 아닌 DNS 별칭이다. 복습 문답은 별도로 기록한다.

## 복습 완료 기록 (2026-10-22)

- [x] 문제 1: ClusterIP Service는 Service 가상 IP를, Headless Service는 backend Pod IP들을 DNS로 반환하며 트래픽 대상 선택 주체가 다름을 설명.
- [x] 문제 2: selector 없는 Service는 자동 EndpointSlice가 생성되지 않아 백엔드 연결이 없고, 수동 EndpointSlice로 해결함을 설명.
- [x] 문제 3: 수동 EndpointSlice에 잘못된 IP를 매핑하면 `ready: true`여도 타임아웃하며 실제 IP로 수정해야 함을 설명.
- [x] 문제 4: ExternalName은 `example.com`을 가리키는 CNAME 별칭을 제공하고 HTTP 프록시나 로드밸런싱을 수행하지 않음을 설명. 실제 A/AAAA 조회와 CNAME 응답을 구별하여 보완.
- [x] 문제 5: 한 backend Pod 삭제 시 EndpointSlice와 Headless DNS에서 해당 Pod IP가 제외되고, 일반 ClusterIP Service DNS 응답은 그대로 유지됨을 설명.

**복습 결과: 5/5 정답.** 실습 완료 수치는 별도로 변경하지 않음.


## 독립 심화: selector 없는 Service와 수동 EndpointSlice

기존 Headless/ExternalName 관찰과 별도로, selector가 **없는** ClusterIP Service `manual`을 만들고 이 Service를 가리키는 `EndpointSlice`에 실제 Ready Pod IP/port를 직접 설정한다. 기존 Service의 자동 EndpointSlice와 차이를 관찰한다.

1. `kubectl get pod -o wide`로 백엔드 IP를 확인하고 수동 EndpointSlice의 `addresses`를 채운다.
2. `kubernetes.io/service-name: manual` 레이블을 설정하고, `kubectl get endpointslices -l kubernetes.io/service-name=manual -o yaml`로 확인한다.
3. 테스트 Pod에서 `wget -qO- http://manual`로 응답을 확인한다.
4. 백엔드 Pod를 재생성한 뒤 수동 EndpointSlice가 **자동 갱신되지 않는다**는 점을 관찰하고 올바른 IP로 복구한다.

기존 실행 예제: [수동 EndpointSlice YAML](../../01-core-objects/07-headless-endpoint-externalname/manual-endpoint.yaml), [네트워크 재현 환경](../../01-core-objects/07-headless-endpoint-externalname/extended-setup.yaml). 예제의 placeholder를 실제 주소로 변경해야 하며, 현재 Lab에서 쓰는 namespace와 자동 생성 EndpointSlice를 혼동하지 않는다.


## 통합 확장 실습 — Service·EndpointSlice 종합 연결

이 절은 이전 독립 8단계 과정의 고유 실습·장애 재현을 이 Lab에 합친 것이다. 별도의 8단계 진도를 만들지 않는다. `extended-*.yaml` 자산은 이 Lab에 보존되어 있으며 별도 `lab-self-*` Namespace를 생성하므로 기존 완료 실습을 덮어쓰지 않는다.

#### 따라 하기

```bash
kubectl apply -f k8s/01-core-objects/07-headless-endpoint-externalname/extended-setup.yaml
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

#### 변경 → 실패 → 복구

```bash
kubectl -n lab-self-network patch svc web --type=merge -p '{"spec":{"selector":{"app":"missing"}}}'
kubectl -n lab-self-network get endpointslices -l kubernetes.io/service-name=web -o yaml
kubectl -n lab-self-network exec client -- nslookup web
kubectl -n lab-self-network exec client -- wget -T 3 -qO- http://web
```

전파가 끝나기 전에는 이전 backend로 성공할 수 있다. EndpointSlice와 wget을 다시 조회해 실제 HTTP 실패를 확인한 뒤 아래 복구를 실행한다. API/exec 자체의 오류는 Service 전달 실패의 증거로 쓰지 않는다. 변화가 없다면 selector와 EndpointSlice를 먼저 확인한다.

```bash
kubectl -n lab-self-network patch svc web --type=merge -p '{"spec":{"selector":{"app":"web"}}}'
kubectl -n lab-self-network exec client -- wget -T 3 -qO- http://web
```

DNS는 성공해도 HTTP는 실패할 수 있다. selector 복구 후 nginx HTML이 돌아와야 한다. 즉시 실패하면 같은 wget을 다시 실행해 성공을 확인한다. EndpointSlice controller와 데이터 평면 반영에는 지연이 있을 수 있다.

#### selector 없는 Service를 수동으로 연결하기

```bash
BACKEND_IP=$(kubectl -n lab-self-network get pod -l app=web -o jsonpath='{.items[0].status.podIP}')
sed "s/REPLACE_BACKEND_IP/$BACKEND_IP/" k8s/01-core-objects/07-headless-endpoint-externalname/manual-endpoint.yaml > /tmp/lab-self-endpoint.yaml
kubectl apply -f /tmp/lab-self-endpoint.yaml
kubectl -n lab-self-network exec client -- wget -T 3 -qO- http://manual
```

nginx HTML을 예상한다. web Pod가 교체되면 수동 EndpointSlice의 주소는 자동 갱신되지 않는다. 주소 갱신의 주체를 selector 기반 Service와 비교한다.

#### NodePort와 LoadBalancer로 확장

[외부 트래픽 정책 실습](../05-service-nodeport/README.md#트래픽-정책과-loadbalancer-비교-실습)을 실행한다. 별도 lab-service-path namespace를 만들고, Windows에서 두 worker를 호출해 Cluster/Local 결과표를 채운 뒤 그 namespace를 정리한다. 외부 LB 구현 없이 Pending인 상태는 LB 동작 완료와 구분해 기록한다.

#### 내부 패킷 경로 심화 (정리 전에 진행)

아래 namespace를 삭제하기 전에 [INT-03 Linux Pod 네트워크](../../01-core-objects/04-service-clusterip/README.md)와 [INT-04 Service 데이터 평면](../../01-core-objects/04-service-clusterip/README.md)을 실행한다. 삭제한 후 심화 문서를 진행하려면 이 단계의 setup.yaml을 다시 apply하고 Pod Ready를 확인한다. EndpointSlice·kube-proxy 커널 규칙과 신규 요청을 비교하는 데 실제 Service 리소스가 필요하다.

#### 누적 복습 — 다음 단계 전에

앞 단계의 개념을 현재 증상에 다시 연결한다. 문서를 닫고 세 질문에 답하며, 어려운 질문은 실제 spec/status/Events를 근거로 다시 설명한다.

1. Pod IP와 Service IP 차이는?
2. DNS 성공·HTTP 실패의 가능한 원인 둘은?
3. readiness와 EndpointSlice는 어떤 관계인가?

관련 내부 심화를 할 경우 이 단계의 **namespace를 정리하기 전에** 진행한다. 개념만 읽을 때는 리소스 재생성을 강제하지 않는다.

#### 완료와 정리

`이름 → Service → EndpointSlice → Pod` 중 어디가 잘못되면 DNS만 성공하는지 설명한다.

```bash
kubectl delete namespace lab-self-network
rm -f /tmp/lab-self-endpoint.yaml
```

다음: [05 자원·Probe·배치](../../03-pod-deep-dive/08-scheduling-troubleshooting/README.md).

[독립 학습 순서](../../README.md)
