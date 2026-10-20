# Service·EndpointSlice·kube-proxy·NAT·conntrack

> 분류: **운영 심화** · 선수 학습: [기본 학습](../../08-independent/README.md), [내부 심화 목차](../../09-internals/README.md) · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

EndpointSlice는 Service 백엔드의 주소·포트·준비 상태를 표현하는 API 객체이지 패킷 전달 장치가 아니다. 이 단원은 단순한 명령어 암기가 아니라 Kubernetes API 객체의 변화와 실제 Node/Runtime에서 일어나는 현상을 연결하는 학습이다.

**학습 결과:** Service·EndpointSlice·kube-proxy·NAT·conntrack의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 선수 개념과 내부 동작

EndpointSlice는 Service 백엔드의 주소·포트·준비 상태를 표현하는 API 객체이지 패킷 전달 장치가 아니다. 일반적인 kube-proxy는 Service/EndpointSlice 변경을 watch해 Node의 전달 규칙을 갱신하고, 실제 요청 패킷의 목적지 변환(DNAT)은 Linux 커널이 처리한다. conntrack은 연결의 원래/변환된 튜플을 추적해 응답 경로의 역변환을 가능하게 한다. SNAT/MASQUERADE는 소스 IP 보존·외부 트래픽 정책·라우팅 조건에 따라 발생하며 모든 ClusterIP 요청에서 무조건 필요한 것은 아니다. iptables·nftables·IPVS는 같은 API 의미를 구현하는 서로 다른 데이터 평면이다. 일부 CNI는 eBPF 등으로 kube-proxy를 대체한다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [기본 학습](../../08-independent/README.md), [내부 심화 목차](../../09-internals/README.md)를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

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

복구 완료 기준은 **동일한 조회나 요청으로 정상 결과를 다시 얻는 것**이다. 관찰할 수 없는 구현(예: CSI driver 미설치, kube-proxy 대체 데이터 평면)은 미검증으로 기록한다.

## 스스로 설명할 문제

1. **Service·EndpointSlice·kube-proxy·NAT·conntrack**이 필요한 이유를 사용자가 겪을 수 있는 실제 문제로 설명할 수 있는가?
2. 이 현상을 만든 API 객체와 실제 실행한 컴포넌트는 각각 무엇인가?
3. 위 예시의 실패 원인과 동일한 외부 증상을 보이는 다른 원인은 무엇이며 첫 번째로 어떤 증거를 확인할 것인가?
4. Pod/Node 또는 Controller를 재시작하지 않고도 진단 가능한 정보는 무엇인가?

## 환경 및 정리

원래 실습 namespace와 공용 애드온은 연결된 기본 단계의 정리 지침을 따른다. Node taint/route/CNI/etcd 및 Kubernetes 패키지 변경은 별도 안전 조건이 명시된 경우에만 수행한다. 실제 VM 실행 여부는 [CHECKPOINTS](../../08-independent/CHECKPOINTS.md)에 별도로 기록한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/reference/networking/virtual-ips/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
