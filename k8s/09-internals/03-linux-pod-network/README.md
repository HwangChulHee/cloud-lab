# Network Namespace·veth·Node 간 Pod 라우팅

> 분류: **운영 심화** · 선수 학습: [독립 학습](../../08-independent/README.md)의 04-networking 시작 전 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

Linux 네트워크 네임스페이스는 인터페이스, 주소, 라우팅 테이블 등을 격리한다. 이 단원에서는 실제 컴포넌트의 동작 순서를 학습하고 관찰 증거와 연결한다.

**학습 결과:** Network Namespace·veth·Node 간 Pod 라우팅의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 핵심 질문에서 내부 원리까지

**Pod IP는 실제 어느 네트워크에 설정되는가?**

### 실행 흐름을 따라가기

Pod마다 네트워크 namespace가 있고 CNI가 IPAM/라우팅/연결을 구성한다. 구현에 따라 veth/bridge/overlay/BGP/eBPF 방식이 다르다.

### 예상 상태 해석 예시

Pod IP 직접 요청이 실패해도 Service DNS 장애라고 단정할 수 없다. Pod Ready, Node 간 route 및 CNI를 살펴본다.

> 이 예시는 학습용이며 실제 클러스터 실행 결과가 아니다. 환경·CNI·버전에 따라 출력이 다를 수 있다.

### 개념을 이해했는지 확인하기

- 같은 Pod의 localhost와 다른 Pod의 localhost는 왜 다른가?
- 이 과정에서 **API 객체 상태를 만드는 주체**와 **실제 Node에서 실행하는 주체**는 각각 누구인가?
- 비슷한 증상을 유발할 수 있는 다른 원인 하나를 들고 확인할 첫 증거를 설명할 수 있는가?

## 선수 개념과 내부 동작

Linux 네트워크 네임스페이스는 인터페이스, 주소, 라우팅 테이블 등을 격리한다. Pod 내 컨테이너는 기본적으로 같은 네트워크 네임스페이스를 공유해 localhost로 통신한다. veth pair는 서로 연결된 가상 이더넷 인터페이스다. Pod IP를 할당하고 호스트 네트워크와 연결하는 실제 방식은 CNI 플러그인마다 다르며 모든 구현이 bridge/overlay를 쓰지는 않는다. 서로 다른 Node 간에는 Node 라우팅, 캡슐화 또는 BGP/underlay 경로 등이 관여할 수 있다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../08-independent/README.md)의 04-networking 시작 전 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

## 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl get nodes -o wide
kubectl -n lab-self-network get pods -o wide
ip -br link
ip -br addr
ip route
kubectl -n kube-system get ds
```

## 따라 하기 — 순서와 예상 결과

04-networking의 setup.yaml만 먼저 생성하고 client와 web Pod의 IP/Node를 표로 기록한다. 같은 Node와 다른 Node를 구별하고 각 Node에서 ip route로 실제 Pod CIDR 경로가 있는지 살핀다. CNI daemonset을 식별하여 그 구현의 IPAM·encapsulation/route 방식을 공식 문서와 대조한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

## 고장 가설과 복구

Pod IP 직접 연결이 안 된다면 먼저 backend Pod Ready/listen, 그다음 Node 간 route/CNI, 마지막 정책을 확인한다. Service DNS나 kube-proxy를 거치지 않는 Pod IP 직접 접근부터 확인해 문제 범위를 축소한다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

## 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

## 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
