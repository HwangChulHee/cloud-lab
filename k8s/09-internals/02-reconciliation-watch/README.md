# Watch와 Reconciliation의 실제 책임

> 분류: **필수 개념** · 선수 학습: [독립 학습](../../08-independent/README.md)의 03-controllers 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

API 객체의 spec은 원하는 상태, status는 관찰된 상태다. 이 단원에서는 실제 컴포넌트의 동작 순서를 학습하고 관찰 증거와 연결한다.

**학습 결과:** Watch와 Reconciliation의 실제 책임의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 핵심 질문에서 내부 원리까지

**왜 Pod 삭제 후 새 Pod가 자동 생성되는가?**

### 실행 흐름을 따라가기

Deployment Controller는 ReplicaSet을, ReplicaSet Controller는 Pod 개수를 맞춘다. Watch는 객체 변경을 전파하고 주기적 재동기화가 관찰 상태와 원하는 상태 차이를 줄인다.

### 예상 상태 해석 예시

Deployment replicas=2, Ready=1이면 API에는 두 개가 있어도 준비된 것은 한 개일 수 있다.

> 이 예시는 학습용이며 실제 클러스터 실행 결과가 아니다. 환경·CNI·버전에 따라 출력이 다를 수 있다.

### 개념을 이해했는지 확인하기

- 왜 kubelet이 Deployment 전체 개수를 관리하지 않는가?
- 이 과정에서 **API 객체 상태를 만드는 주체**와 **실제 Node에서 실행하는 주체**는 각각 누구인가?
- 비슷한 증상을 유발할 수 있는 다른 원인 하나를 들고 확인할 첫 증거를 설명할 수 있는가?

## 선수 개념과 내부 동작

API 객체의 spec은 원하는 상태, status는 관찰된 상태다. Deployment Controller는 ReplicaSet의 revision/복제 수를 조절하고 ReplicaSet Controller는 Pod 개수를 맞춘다. Scheduler와 kubelet은 별도의 루프에서 동작한다. watch는 변경 이벤트를 효율적으로 받는 수단이지만 끊김·재연결·재동기화가 존재한다. observedGeneration이 generation보다 뒤처졌다면 Controller가 새 spec을 아직 반영하지 않았을 수 있다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../08-independent/README.md)의 03-controllers 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

## 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl -n lab-self-control get deploy,rs,pods -o wide
kubectl -n lab-self-control get deploy web -o jsonpath='{.metadata.generation}{" / "}{.status.observedGeneration}{"\n"}'
kubectl -n lab-self-control get rs -o wide
kubectl -n lab-self-control get pods -o custom-columns=NAME:.metadata.name,OWNER:.metadata.ownerReferences[0].name,UID:.metadata.uid
```

## 따라 하기 — 순서와 예상 결과

03-controllers 실습 리소스를 유지한 상태에서 웹 Pod 이름과 UID를 기록한다. Pod 하나를 삭제하고 watch로 새 Pod가 나타나는지 확인한다. 그 다음 ReplicaSet의 ownerReference를 조회하여 새 Pod의 직접 관리자가 Deployment가 아닌 ReplicaSet임을 확인한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

## 고장 가설과 복구

Pod를 지우고도 새 Pod가 안 나타나면 ReplicaSet의 desired/current/ready와 Events를 확인한다. Pod가 생겼지만 Ready가 아니면 Scheduler·ImagePull·Probe로 진단 계층을 이동한다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

## 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

## 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/concepts/architecture/controller/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
