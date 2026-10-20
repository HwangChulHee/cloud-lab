# Pod 생성 요청에서 프로세스 실행까지

> 분류: **필수 개념** · 선수 학습: [독립 학습](../../08-independent/README.md)의 01-pods 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

Pod 생성은 단일 호출이 아니다. 이 단원은 단순한 명령어 암기가 아니라 Kubernetes API 객체의 변화와 실제 Node/Runtime에서 일어나는 현상을 연결하는 학습이다.

**학습 결과:** Pod 생성 요청에서 프로세스 실행까지의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 선수 개념과 내부 동작

Pod 생성은 단일 호출이 아니다. kubectl은 API Server에 객체를 제출한다. API Server는 인증·인가·Admission 이후 etcd에 원하는 상태를 저장한다. 독립 Pod라면 Deployment/ReplicaSet 컨트롤러를 거치지 않는다. scheduler는 nodeName이 없는 Pod를 watch하고 Filter/Score 후 Binding한다. 해당 Node의 kubelet이 Pod spec을 수신해 CRI의 RunPodSandbox/CreateContainer/StartContainer 등을 통해 실행한다. CNI는 보통 Sandbox 네트워크 구성에 관여하며 kubelet이 status를 갱신한다. Running과 Ready는 다르다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../08-independent/README.md)의 01-pods 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

## 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl get nodes -o wide
kubectl -n lab-self-pods get pod pair -o wide
kubectl -n lab-self-pods get pod pair -o jsonpath='{.metadata.uid}{"\n"}{.spec.nodeName}{"\n"}{.status.phase}{"\n"}'
kubectl -n lab-self-pods describe pod pair
kubectl -n lab-self-pods get events --sort-by=.lastTimestamp
```

## 따라 하기 — 순서와 예상 결과

기존 01-pods를 먼저 apply하고 Ready까지 확인한다. Node 이름을 기록한 후 해당 Node의 호스트 셸에서 sudo crictl pods와 sudo crictl ps로 Pod Sandbox와 컨테이너를 확인한다. kubelet 로그는 sudo journalctl -u kubelet -n 100 --no-pager로 조사한다. crictl의 Pod ID와 Kubernetes Pod UID는 같은 값이 아닐 수 있다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

## 고장 가설과 복구

이미지가 존재하지 않을 때 Pod는 스케줄되었어도 시작에 실패한다. describe의 Failed/Pulling/BackOff와 containerStatuses[*].state.waiting.reason을 찾아 image pull 문제와 scheduling 문제를 구분한다. 잘못된 이미지는 기존 03 Controller 실습의 실패 사례를 재사용한다.

복구 완료 기준은 **동일한 조회나 요청으로 정상 결과를 다시 얻는 것**이다. 관찰할 수 없는 구현(예: CSI driver 미설치, kube-proxy 대체 데이터 평면)은 미검증으로 기록한다.

## 스스로 설명할 문제

1. **Pod 생성 요청에서 프로세스 실행까지**이 필요한 이유를 사용자가 겪을 수 있는 실제 문제로 설명할 수 있는가?
2. 이 현상을 만든 API 객체와 실제 실행한 컴포넌트는 각각 무엇인가?
3. 위 예시의 실패 원인과 동일한 외부 증상을 보이는 다른 원인은 무엇이며 첫 번째로 어떤 증거를 확인할 것인가?
4. Pod/Node 또는 Controller를 재시작하지 않고도 진단 가능한 정보는 무엇인가?

## 환경 및 정리

원래 실습 namespace와 공용 애드온은 연결된 기본 단계의 정리 지침을 따른다. Node taint/route/CNI/etcd 및 Kubernetes 패키지 변경은 별도 안전 조건이 명시된 경우에만 수행한다. 실제 VM 실행 여부는 [CHECKPOINTS](../../08-independent/CHECKPOINTS.md)에 별도로 기록한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
