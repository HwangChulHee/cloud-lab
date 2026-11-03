# Lab 06 — Service ClusterIP

> 학습 단계: **기초 개념·실습 과제**  
> **실습 상태: ✅ 완료 (2026-10-22)**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../08-independent/04-networking/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

## 목표

휘발성 Pod IP 대신 Service의 고정 진입점을 사용하는 이유를 확인한다.

## 핵심 개념과 오해 방지

ClusterIP는 Service 객체가 유지되는 동안 안정적인 가상 IP다. Service를 삭제하고 다시 만들면 IP가 달라질 수 있다. API Server나 Service 객체가 HTTP 요청을 직접 중계하는 것은 아니며, kube-proxy 또는 대체 데이터 평면이 EndpointSlice의 backend로 전달한다. 요청마다 정확한 균등 분산을 보장하지 않고, 연결 재사용과 sessionAffinity도 결과에 영향을 준다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. Pod와 ClusterIP Service를 만든다.
2. Service IP:port로 호출한다.
3. Pod를 교체한 뒤 Service IP가 유지되는지 확인한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. selector를 깨뜨려 Service는 존재하지만 요청이 실패하는 상태를 만든다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. `kubectl get svc,endpoints`로 정상 연결을 검증한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 실습 완료 기록 (2026-10-22)

- [x] `lab-clusterip` namespace 및 `web-1`, `web-2` Nginx Pod 생성. 두 Pod가 서로 다른 worker에서 Ready.
- [x] `web-svc` ClusterIP `10.97.180.115:80` 및 두 backend EndpointSlice 확인.
- [x] `kube-proxy` 설정 `mode: ""` 확인, 해당 v1.27 환경의 iptables NAT 규칙(`KUBE-SVC`, `KUBE-SEP`, DNAT) 관찰.
- [x] 임시 BusyBox HTTP client로 ClusterIP 요청, Nginx HTML 수신.
- [x] `web-1` 삭제 시 Service IP 유지 및 Endpoint 감소 확인. 재생성 후 Pod IP `20.100.194.76` → `20.100.194.78`, EndpointSlice 갱신 확인.
- [x] Service selector를 `app=nonexistent`로 변경해 Endpoint가 비는 현상과 `Connection refused` 확인.
- [x] selector를 `app=web`으로 복구해 두 Endpoint 및 HTTP 응답 재확인.
- [x] namespace 삭제 후 `NotFound` 확인; 실습 리소스 정리 완료.

> 기록된 IP와 출력은 당시 실습 환경의 관측값이며 이후 재실행 시 달라질 수 있다. 본 기록은 이 기초 Lab 완료 증거이며 별도의 `08-independent` 통합 단계나 `09-internals`/`10-cluster-admin` 수행 완료를 의미하지 않는다.


## 내부 동작 심화 통합 — 04-service-dataplane

기존 INT 모듈의 개념·관찰·원인 분석 내용을 이 Lab에 병합했다. 코드 블록에 등장하는 `lab-self-*`는 이전 독립 예제의 실습용 Namespace이며, 현재 Lab의 리소스를 우선 사용하거나 해당 확장 YAML을 적용한 뒤 관찰한다. 별도 INT 진도는 만들지 않는다.

#### 선수 개념과 내부 동작

EndpointSlice는 Service 백엔드의 주소·포트·준비 상태를 표현하는 API 객체이지 패킷 전달 장치가 아니다. 일반적인 kube-proxy는 Service/EndpointSlice 변경을 watch해 Node의 전달 규칙을 갱신하고, 실제 요청 패킷의 목적지 변환(DNAT)은 Linux 커널이 처리한다. conntrack은 연결의 원래/변환된 튜플을 추적해 응답 경로의 역변환을 가능하게 한다. SNAT/MASQUERADE는 소스 IP 보존·외부 트래픽 정책·라우팅 조건에 따라 발생하며 모든 ClusterIP 요청에서 무조건 필요한 것은 아니다. iptables·nftables·IPVS는 같은 API 의미를 구현하는 서로 다른 데이터 평면이다. 일부 CNI는 eBPF 등으로 kube-proxy를 대체한다.

#### 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [기본 학습](../../README.md), [내부 심화 목차](../../09-internals/README.md)를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

#### 예시: ClusterIP 요청의 주소 변화

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

#### 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl -n lab-self-network get svc web -o wide
kubectl -n lab-self-network get endpointslices -l kubernetes.io/service-name=web -o wide
kubectl -n kube-system get ds kube-proxy
kubectl -n kube-system get cm kube-proxy -o yaml
kubectl -n lab-self-network exec client -- nslookup web
kubectl -n lab-self-network exec client -- wget -qO- http://web
```

#### 따라 하기 — 순서와 예상 결과

04-networking 실습의 Cleanup **이전**에 진행한다. 1) client Pod IP·web ClusterIP·backend Pod IP를 기록한다. 2) web DNS가 ClusterIP로 해석되는지 확인한다. 3) client에서 backend Pod IP 직접 요청과 ClusterIP 요청을 비교한다. 4) kube-proxy mode를 확인한 후 Node 호스트에서 iptables-save -t nat 또는 해당 구현의 규칙을 관찰한다. 5) conntrack 명령이 있으면 연결 전후 엔트리를 비교한다. Node 호스트에서 `sudo iptables-save -t nat | grep KUBE-SVC`와 `sudo conntrack -L`를 실행할 때는 iptables 모드임을 먼저 확인하고, 명령 도구가 없다면 관찰 불가로 기록한다. nftables/IPVS/eBPF 기반에서는 해당 구현의 규칙 조회 도구를 사용한다. 6) selector를 missing으로 바꿔 EndpointSlice 변경과 신규 연결 실패를 확인한 다음 복구한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

#### 고장 가설과 복구

DNS 성공 + HTTP 실패면 DNS가 아닌 selector/EndpointSlice/앱 listen/전달 규칙을 조사한다. EndpointSlice는 정상인데 Service만 실패하면 데이터 평면·정책·포트가 후보가 된다. 이미 성립한 연결은 conntrack 때문에 규칙 변경 직후에도 지속될 수 있어 새 연결로 비교한다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

#### 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

#### 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

#### 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/reference/networking/virtual-ips/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../README.md)
