# Lab 09 — Headless, Endpoint, ExternalName

> 학습 단계: **기초 개념·실습 과제**  
> **실습 상태: ✅ 완료 (2026-10-22)**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/04-networking/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

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
