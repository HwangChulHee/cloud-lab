# kubeadm·CRI·CNI 설치 순서

> 분류: **CKA 필수** · 선수 학습: [플랫폼 준비](../../08-independent/PLATFORM.md) · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

kubeadm은 API Server/etcd 등 Control Plane을 부트스트랩하는 도구이고 kubelet과 container runtime은 노드에서 지속 실행된다. 이 단원에서는 실제 컴포넌트의 동작 순서를 학습하고 관찰 증거와 연결한다.

**학습 결과:** kubeadm·CRI·CNI 설치 순서의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 핵심 질문에서 내부 원리까지

**kubeadm init 성공 후에도 Node가 NotReady인 이유는?**

### 실행 흐름을 따라가기

kubeadm 부트스트랩과 kubelet/CRI/CNI의 실제 Node 실행은 책임이 다르다. CNI 설치 전후 Node Conditions와 CoreDNS 상태를 비교한다.

### 예상 상태 해석 예시

API 요청은 성공해도 CNI 미설치로 Node가 NotReady일 수 있다.

> 이 예시는 학습용이며 실제 클러스터 실행 결과가 아니다. 환경·CNI·버전에 따라 출력이 다를 수 있다.

### 개념을 이해했는지 확인하기

- kubeadm과 kubelet의 책임은?
- 이 과정에서 **API 객체 상태를 만드는 주체**와 **실제 Node에서 실행하는 주체**는 각각 누구인가?
- 비슷한 증상을 유발할 수 있는 다른 원인 하나를 들고 확인할 첫 증거를 설명할 수 있는가?

## 선수 개념과 내부 동작

kubeadm은 API Server/etcd 등 Control Plane을 부트스트랩하는 도구이고 kubelet과 container runtime은 노드에서 지속 실행된다. kubeadm init 후 CNI가 없으면 Node NotReady나 CoreDNS Pending을 관찰할 수 있다. init과 join, CNI 설치, kubelet 설정은 서로 다른 책임이다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [플랫폼 준비](../../08-independent/PLATFORM.md)를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

## 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl get nodes -o wide
kubectl -n kube-system get pods -o wide
sudo systemctl status kubelet --no-pager
sudo crictl info
```

## 따라 하기 — 순서와 예상 결과

기존 08-independent/PLATFORM.md의 Ubuntu 전용 VM 준비→kubeadm init/join→CNI 설치 순서를 따른다. init 직후/ CNI 설치 후 Ready 변화와 kube-system Pod를 비교한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

## 고장 가설과 복구

Node NotReady면 kubelet journal, CRI socket 및 CNI Pod/설정 순서로 확인한다. 기존 Rocky 1.27 VM에서 kubeadm reset/init을 실행하지 않는다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

## 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

## 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[10-cluster-admin 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
