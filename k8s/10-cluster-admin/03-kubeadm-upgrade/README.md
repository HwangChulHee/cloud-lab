# kubeadm 업그레이드 순서와 버전 스큐

> 분류: **CKA 필수** · 선수 학습: [독립 학습](../../08-independent/README.md)의 ADM-01 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

Kubernetes는 kubeadm, API Server, kubelet, kubectl 사이의 버전 스큐 규칙을 갖는다. 이 단원에서는 실제 컴포넌트의 동작 순서를 학습하고 관찰 증거와 연결한다.

**학습 결과:** kubeadm 업그레이드 순서와 버전 스큐의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 핵심 질문에서 내부 원리까지

**왜 모든 Node 패키지를 한번에 올리지 않는가?**

### 실행 흐름을 따라가기

kubeadm·API Server·kubelet·kubectl 버전 스큐와 지원되는 minor 업그레이드 경로를 지키고 Control Plane 이후 Worker를 한 대씩 갱신한다.

### 예상 상태 해석 예시

API Server와 kubelet 버전 차이가 있어도 지원 범위일 수 있다. Node NotReady는 CRI/CNI 문제일 수도 있다.

> 이 예시는 학습용이며 실제 클러스터 실행 결과가 아니다. 환경·CNI·버전에 따라 출력이 다를 수 있다.

### 개념을 이해했는지 확인하기

- drain과 uncordon을 업그레이드 전후에 쓰는 이유는?
- 이 과정에서 **API 객체 상태를 만드는 주체**와 **실제 Node에서 실행하는 주체**는 각각 누구인가?
- 비슷한 증상을 유발할 수 있는 다른 원인 하나를 들고 확인할 첫 증거를 설명할 수 있는가?

## 선수 개념과 내부 동작

Kubernetes는 kubeadm, API Server, kubelet, kubectl 사이의 버전 스큐 규칙을 갖는다. 설치된 패키지 고정값과 실제 minor를 확인한 후 공식 지원 경로로 한 minor씩 업그레이드한다. Control Plane에서 kubeadm을 먼저 갱신하고 upgrade plan/apply를 진행하며 kubelet을 갱신·재시작한다. Worker는 drain, kubeadm upgrade node, kubelet 재시작, uncordon 흐름을 따른다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../08-independent/README.md)의 [ADM-01](../01-kubeadm-bootstrap/README.md) 과정을 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

## 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl version
kubectl get nodes -o wide
kubeadm version
apt-cache madison kubeadm
sudo apt-mark showhold
```

## 따라 하기 — 순서와 예상 결과

별도 PLATFORM VM에서 시작 버전, 목표 버전 및 apt repository minor 경로를 명시해 표를 만든다. VM 스냅샷과 etcd snapshot을 먼저 확보한다. 대상 minor의 kubeadm 패키지를 설치한 뒤 kubeadm upgrade plan으로 제약을 확인하고 공식 upgrade apply 과정을 진행한다. Control Plane kubelet 업데이트·재시작 후 Worker를 한 대씩 cordon/drain → kubeadm upgrade node → kubelet 패키지 업데이트·재시작 → uncordon한다. 각 노드의 버전과 Ready를 기록한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

## 고장 가설과 복구

API 접근 실패면 static Pod/kubelet 로그를, Worker NotReady면 kubelet/CRI/CNI를 확인한다. 전체 버전을 한번에 변경하거나 1.27에서 최신 minor로 건너뛰지 않는다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

## 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

## 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[10-cluster-admin 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
