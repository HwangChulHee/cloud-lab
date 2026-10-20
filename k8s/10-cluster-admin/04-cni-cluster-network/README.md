# CNI 설치·Node 라우팅·NetworkPolicy

> 분류: **CKA 필수** · 선수 학습: [기본 학습](../../08-independent/README.md), [내부 심화 목차](../../09-internals/README.md) · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

CNI는 kubelet/runtime이 Pod 네트워크를 설정할 때 호출하는 인터페이스이며 IPAM, 라우팅·오버레이 등의 실제 동작은 플러그인이 맡는다. 이 단원은 단순한 명령어 암기가 아니라 Kubernetes API 객체의 변화와 실제 Node/Runtime에서 일어나는 현상을 연결하는 학습이다.

**학습 결과:** CNI 설치·Node 라우팅·NetworkPolicy의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

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

복구 완료 기준은 **동일한 조회나 요청으로 정상 결과를 다시 얻는 것**이다. 관찰할 수 없는 구현(예: CSI driver 미설치, kube-proxy 대체 데이터 평면)은 미검증으로 기록한다.

## 스스로 설명할 문제

1. **CNI 설치·Node 라우팅·NetworkPolicy**이 필요한 이유를 사용자가 겪을 수 있는 실제 문제로 설명할 수 있는가?
2. 이 현상을 만든 API 객체와 실제 실행한 컴포넌트는 각각 무엇인가?
3. 위 예시의 실패 원인과 동일한 외부 증상을 보이는 다른 원인은 무엇이며 첫 번째로 어떤 증거를 확인할 것인가?
4. Pod/Node 또는 Controller를 재시작하지 않고도 진단 가능한 정보는 무엇인가?

## 환경 및 정리

원래 실습 namespace와 공용 애드온은 연결된 기본 단계의 정리 지침을 따른다. Node taint/route/CNI/etcd 및 Kubernetes 패키지 변경은 별도 안전 조건이 명시된 경우에만 수행한다. 실제 VM 실행 여부는 [CHECKPOINTS](../../08-independent/CHECKPOINTS.md)에 별도로 기록한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[10-cluster-admin 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
