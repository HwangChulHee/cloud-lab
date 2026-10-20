# CNI 설치·Node 라우팅·NetworkPolicy

> 분류: **CKA 필수** · 선수 학습: [기본 학습](../../08-independent/README.md), [내부 심화 목차](../../09-internals/README.md) · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

CNI는 kubelet/runtime이 Pod 네트워크를 설정할 때 호출하는 인터페이스이며 IPAM, 라우팅·오버레이 등의 실제 동작은 플러그인이 맡는다. 이 단원에서는 실제 컴포넌트의 동작 순서를 학습하고 관찰 증거와 연결한다.

**학습 결과:** CNI 설치·Node 라우팅·NetworkPolicy의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 핵심 질문에서 내부 원리까지

**NetworkPolicy를 생성했는데도 트래픽이 통과하는 이유는?**

### 실행 흐름을 따라가기

NetworkPolicy는 API에 정책 의도를 저장하지만 집행 가능한 CNI가 필요하다. 정책의 실제 효과는 allow/deny 양성·음성 요청으로 확인한다.

### 예상 상태 해석 예시

kubectl get netpol 성공은 패킷 차단 증거가 아니다.

> 이 예시는 학습용이며 실제 클러스터 실행 결과가 아니다. 환경·CNI·버전에 따라 출력이 다를 수 있다.

### 개념을 이해했는지 확인하기

- CNI와 kube-proxy의 책임 경계는?
- 이 과정에서 **API 객체 상태를 만드는 주체**와 **실제 Node에서 실행하는 주체**는 각각 누구인가?
- 비슷한 증상을 유발할 수 있는 다른 원인 하나를 들고 확인할 첫 증거를 설명할 수 있는가?

## 선수 개념과 내부 동작

CNI는 kubelet/runtime이 Pod 네트워크를 설정할 때 호출하는 인터페이스이며 IPAM, 라우팅·오버레이 등의 실제 동작은 플러그인이 맡는다. NetworkPolicy API 생성 자체가 네트워크 차단을 보장하지 않는다. 정책을 집행하는 CNI가 있어야 한다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [기본 학습](../../08-independent/README.md), [내부 심화 목차](../../09-internals/README.md)를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

## 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl get nodes -o wide
kubectl get pods -A -o wide
kubectl get networkpolicy -A
ip route
```

## 따라 하기 — 순서와 예상 결과

새 클러스터에서 기존 07-cka-preview/14-cni-install/README.md를 따라 CNI를 설치하고, 08-networkpolicy의 frontend 허용/other 차단 테스트로 실제 집행을 확인한다. Pod CIDR이 노드/LAN/VPN 주소와 겹치지 않는지 우선 검사한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

## 고장 가설과 복구

CNI 설치 뒤 CoreDNS Pending이면 kube-system Pod 이벤트와 CNI daemonset 로그, Node IP/route를 확인한다. 기존 클러스터의 CNI를 덮어 설치하지 않는다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

## 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

## 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[10-cluster-admin 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
