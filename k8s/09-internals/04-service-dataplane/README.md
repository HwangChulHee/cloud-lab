# Service·EndpointSlice·kube-proxy·NAT·conntrack

> 분류: **운영 심화** · 선수 학습: [기본 학습](../../08-independent/README.md), [내부 심화 목차](../../09-internals/README.md) · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

EndpointSlice는 Service 백엔드의 주소·포트·준비 상태를 표현하는 API 객체이지 패킷 전달 장치가 아니다. 이 단원에서는 실제 컴포넌트의 동작 순서를 학습하고 관찰 증거와 연결한다.

**학습 결과:** Service·EndpointSlice·kube-proxy·NAT·conntrack의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 핵심 질문에서 내부 원리까지

**kube-proxy는 각 패킷을 직접 중계할까?**

### 실행 흐름을 따라가기

EndpointSlice Controller가 Backend 정보를 API로 제공한다. kube-proxy 또는 대체 구현이 전달 규칙을 구성하고, 커널이 DNAT·conntrack 등을 처리한다. DNS는 서비스 IP 해석과 별도다.

### 예상 상태 해석 예시

DNS가 ClusterIP를 반환해도 EndpointSlice가 비면 전달 대상이 없어 HTTP는 실패할 수 있다. 이전 연결과 새 연결은 conntrack 때문에 다를 수 있다.

> 이 예시는 학습용이며 실제 클러스터 실행 결과가 아니다. 환경·CNI·버전에 따라 출력이 다를 수 있다.

### 개념을 이해했는지 확인하기

- EndpointSlice는 네트워크 패킷을 직접 전달하는가?
- 이 과정에서 **API 객체 상태를 만드는 주체**와 **실제 Node에서 실행하는 주체**는 각각 누구인가?
- 비슷한 증상을 유발할 수 있는 다른 원인 하나를 들고 확인할 첫 증거를 설명할 수 있는가?

## 선수 개념과 내부 동작

EndpointSlice는 Service 백엔드의 주소·포트·준비 상태를 표현하는 API 객체이지 패킷 전달 장치가 아니다. 일반적인 kube-proxy는 Service/EndpointSlice 변경을 watch해 Node의 전달 규칙을 갱신하고, 실제 요청 패킷의 목적지 변환(DNAT)은 Linux 커널이 처리한다. conntrack은 연결의 원래/변환된 튜플을 추적해 응답 경로의 역변환을 가능하게 한다. SNAT/MASQUERADE는 소스 IP 보존·외부 트래픽 정책·라우팅 조건에 따라 발생하며 모든 ClusterIP 요청에서 무조건 필요한 것은 아니다. iptables·nftables·IPVS는 같은 API 의미를 구현하는 서로 다른 데이터 평면이다. 일부 CNI는 eBPF 등으로 kube-proxy를 대체한다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [기본 학습](../../08-independent/README.md), [내부 심화 목차](../../09-internals/README.md)를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

### 예시: ClusterIP 요청의 주소 변화

가상의 환경에서 클라이언트 Pod `10.244.1.10:50000`이 `web` DNS를 조회해 Service ClusterIP `10.96.0.50:80`을 얻었다고 하자. EndpointSlice에는 Ready인 백엔드 `10.244.2.20:8080`이 기록돼 있다.

1. **DNS:** CoreDNS가 `web → 10.96.0.50`을 반환한다. DNS는 백엔드 Pod를 골라 HTTP 요청을 직접 전달하지 않는다.
2. **제어 경로:** EndpointSlice Controller는 Pod와 Service 정보를 바탕으로 엔드포인트를 관리하고 kube-proxy(또는 대체 데이터 평면)는 API 변경을 관찰해 전달 규칙을 갱신한다.
3. **요청 데이터 경로:** `10.244.1.10:50000 → 10.96.0.50:80` 요청이 Node의 데이터 평면을 지나며 예컨대 **DNAT**되어 목적지가 `10.244.2.20:8080`이 된다.
4. **응답:** conntrack 등 연결 추적에 의해 응답이 원래 클라이언트의 연결과 일관되도록 역변환된다. 어떤 경로에서 **SNAT**가 추가되는지는 externalTrafficPolicy·라우팅·masquerade 설정에 따라 달라진다.

| 단계 | 목적지 주소(가상 예시) | 관찰할 것 |
|---|---|---|
| DNS 해석 | 10.96.0.50 | `nslookup web` |
| EndpointSlice | 10.244.2.20:8080 | `kubectl get endpointslices -o yaml` |
| Service 전달 | 10.96.0.50:80 → 10.244.2.20:8080 | 현재 proxy mode와 해당 Node의 전달 규칙 |

**반례:** DNS는 성공하지만 EndpointSlice의 Ready 백엔드가 없다면 신규 HTTP 연결이 실패할 수 있다. Pod IP 직접 연결은 정상인데 Service만 실패하면 selector·EndpointSlice·Service port/targetPort·데이터 평면을 분리해 확인한다. kube-proxy가 각 패킷마다 API를 조회하지는 않는다.

## 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl -n lab-self-network get svc web -o wide
kubectl -n lab-self-network get endpointslices -l kubernetes.io/service-name=web -o wide
kubectl -n kube-system get ds kube-proxy
kubectl -n kube-system get cm kube-proxy -o yaml
kubectl -n lab-self-network exec client -- nslookup web
kubectl -n lab-self-network exec client -- wget -qO- http://web
```

## 따라 하기 — 순서와 예상 결과

04-networking 실습의 Cleanup **이전**에 진행한다. 1) client Pod IP·web ClusterIP·backend Pod IP를 기록한다. 2) web DNS가 ClusterIP로 해석되는지 확인한다. 3) client에서 backend Pod IP 직접 요청과 ClusterIP 요청을 비교한다. 4) kube-proxy mode를 확인한 후 Node 호스트에서 iptables-save -t nat 또는 해당 구현의 규칙을 관찰한다. 5) conntrack 명령이 있으면 연결 전후 엔트리를 비교한다. Node 호스트에서 `sudo iptables-save -t nat | grep KUBE-SVC`와 `sudo conntrack -L`를 실행할 때는 iptables 모드임을 먼저 확인하고, 명령 도구가 없다면 관찰 불가로 기록한다. nftables/IPVS/eBPF 기반에서는 해당 구현의 규칙 조회 도구를 사용한다. 6) selector를 missing으로 바꿔 EndpointSlice 변경과 신규 연결 실패를 확인한 다음 복구한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

## 고장 가설과 복구

DNS 성공 + HTTP 실패면 DNS가 아닌 selector/EndpointSlice/앱 listen/전달 규칙을 조사한다. EndpointSlice는 정상인데 Service만 실패하면 데이터 평면·정책·포트가 후보가 된다. 이미 성립한 연결은 conntrack 때문에 규칙 변경 직후에도 지속될 수 있어 새 연결로 비교한다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

## 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

## 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/reference/networking/virtual-ips/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
