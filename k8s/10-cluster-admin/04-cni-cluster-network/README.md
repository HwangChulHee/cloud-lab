# CNI 설치·Node 라우팅·NetworkPolicy

> 분류: **CKA 필수** · 선수 학습: [기본 학습](../../README.md), [내부 심화 목차](../../README.md) · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

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
2. [기본 학습](../../README.md), [내부 심화 목차](../../README.md)를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
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

[10-cluster-admin 목차](../README.md) · [전체 독립 학습](../../README.md)


## 작업형 실습 — CNI 설치 전후와 데이터 경로 구분

**대상:** [ADM-01](../01-kubeadm-bootstrap/README.md)의 **별도 VM**. 기존 1.27 Calico CNI를 삭제하거나 교체하지 않는다. 아래 조회 단계는 현재 환경에서도 안전하며, CNI 설치·변경은 폐기 가능한 클러스터에서만 수행한다.

```bash
kubectl get nodes -o wide
kubectl -n kube-system get pods -o wide
kubectl get --raw=/readyz
kubectl get pods -A --field-selector=status.phase=Pending
kubectl get endpointslices -A
kubectl get networkpolicies -A
```

### 단계 A — CNI 설치 전 상태 예측

1. 새 클러스터에서 kubeadm init 성공 뒤 CNI 설치 **전** Node Conditions와 CoreDNS Pending 여부를 기록한다.
2. Pod CIDR, Service CIDR, VM LAN 대역이 서로 겹치지 않는지 확인한다.
3. CRI가 kubelet과 정상 연결돼 있어도 왜 Pod sandbox 네트워크가 준비되지 않을 수 있는지 설명한다.

### 단계 B — CNI 설치·검증

[플랫폼의 Calico 설치 절차](../../guides/PLATFORM.md#5-cni-설치-control-plane)를 따라 **별도 VM에서만** 설치한다. 각 Node Ready, CNI Pod Ready 및 CoreDNS 정상화까지 기다린다. 다음 조회를 수행한다.

```bash
kubectl get nodes -o wide
kubectl -n kube-system get pods -o wide
kubectl get pods -A -o wide
kubectl describe node k8s-worker1
```

실제 별도 클러스터 Node 이름은 위 예제와 다를 수 있으므로 `kubectl get nodes`의 값을 사용한다. CNI DaemonSet이 성공해도 Pod 간 통신을 자동으로 증명한 것은 아니다.

### 단계 C — 같은 Node / 다른 Node 요청

```bash
kubectl create namespace lab-cni
kubectl -n lab-cni create deployment web --image=nginx:1.28-alpine --replicas=2
kubectl -n lab-cni expose deployment web --port=80 --target-port=80
kubectl -n lab-cni rollout status deploy/web --timeout=180s
kubectl -n lab-cni get pods -o wide
kubectl -n lab-cni get endpointslices
kubectl -n lab-cni run client --image=busybox:1.37 --restart=Never -- sleep 3600
kubectl -n lab-cni wait --for=condition=Ready pod/client --timeout=120s
kubectl -n lab-cni exec client -- nslookup web
kubectl -n lab-cni exec client -- wget -qO- http://web
```

Pod가 모두 같은 Node에 놓였으면 **다른 Node 통신이 입증되지 않았다**고 기록한다. NodeSelector/affinity를 이용해 2개 Pod가 서로 다른 Worker에 배치되도록 한 뒤 직접 Pod IP와 Service IP의 요청 결과를 비교한다. Pod CIDR의 VXLAN/IPIP/BGP 전달 여부는 **실제 CNI 모드**에 따라 다르다.

### 진단 / 정리

- DNS 실패: CoreDNS Pod, CoreDNS Service, Node DNS 설정부터 확인.
- Pod IP 직접 통신 실패: Pod Ready, Node CIDR, CNI DaemonSet/노드 라우팅 확인.
- ClusterIP만 실패: Service selector, EndpointSlice, kube-proxy 또는 대체 데이터 평면 확인.
- NetworkPolicy에서만 실패: 정책 selector/ingress/egress 및 해당 CNI의 정책 집행 확인.

```bash
kubectl delete namespace lab-cni
```

**완료:** CNI 전/후 Node Ready 및 CoreDNS, 양쪽 Worker의 Pod 통신, DNS와 Service 분리 검증, Namespace 정리. 이미 설치된 CNI 자체는 이 Lab 종료 시 삭제하지 않는다.
