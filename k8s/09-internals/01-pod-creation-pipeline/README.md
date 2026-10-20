# Pod 생성 요청에서 프로세스 실행까지

> 분류: **필수 개념** · 선수 학습: [독립 학습](../../08-independent/README.md)의 01-pods 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

Pod 생성은 단일 호출이 아니다. 이 단원에서는 실제 컴포넌트의 동작 순서를 학습하고 관찰 증거와 연결한다.

**학습 결과:** Pod 생성 요청에서 프로세스 실행까지의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 핵심 질문에서 내부 원리까지

**Pod가 API에 저장되면 이미 실행된 것일까?**

### 실행 흐름을 따라가기

kubectl→API Server 저장→Scheduler Binding→kubelet 관찰→CRI Sandbox/Container 실행→상태 보고. 독립 Pod는 ReplicaSet을 거치지 않는다.

### 예상 상태 해석 예시

nodeName이 비어 있고 PodScheduled=false라면 스케줄 이전 문제다. nodeName은 있지만 ImagePullBackOff면 이미지 준비 문제가 의심된다.

> 이 예시는 학습용이며 실제 클러스터 실행 결과가 아니다. 환경·CNI·버전에 따라 출력이 다를 수 있다.

### 개념을 이해했는지 확인하기

- Pod UID와 container ID의 차이는?
- 이 과정에서 **API 객체 상태를 만드는 주체**와 **실제 Node에서 실행하는 주체**는 각각 누구인가?
- 비슷한 증상을 유발할 수 있는 다른 원인 하나를 들고 확인할 첫 증거를 설명할 수 있는가?

## 선수 개념과 내부 동작

Pod 생성은 단일 호출이 아니다. kubectl은 API Server에 객체를 제출한다. API Server는 인증·인가·Admission 이후 etcd에 원하는 상태를 저장한다. 독립 Pod라면 Deployment/ReplicaSet 컨트롤러를 거치지 않는다. scheduler는 nodeName이 없는 Pod를 watch하고 Filter/Score 후 Binding한다. 해당 Node의 kubelet이 Pod spec을 수신해 CRI의 RunPodSandbox/CreateContainer/StartContainer 등을 통해 실행한다. CNI는 보통 Sandbox 네트워크 구성에 관여하며 kubelet이 status를 갱신한다. Running과 Ready는 다르다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../08-independent/README.md)의 01-pods 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

### 예시: Pod 생성은 왜 여러 컴포넌트를 거칠까?

가상의 `frontend` Pod를 생성한다고 하자. 처음에는 Pod가 API에 저장되지만 `spec.nodeName`이 없다. **API Server**는 요청 인증·인가·Admission과 저장을 처리하고 컨테이너를 직접 만들지 않는다. **Scheduler**가 조건에 맞는 `worker1`을 선택하여 Binding하면 `spec.nodeName=worker1`이 된다. **worker1의 kubelet**은 API에서 할당된 Pod를 관찰하고 CRI를 통해 Pod Sandbox와 컨테이너 실행을 요청한다. 런타임 및 CNI 설정 후 `status.phase=Running`이 될 수 있지만 readiness가 실패하면 `Ready=False`다.

| 관찰값(예시) | 어디까지 진행됐는가? | 다음 확인 |
|---|---|---|
| `nodeName: <empty>`, `PodScheduled=False` | 아직 배치 전 | Events/스케줄링 조건 |
| `nodeName: worker1`, `ImagePullBackOff` | 배치 완료, 실행 준비 실패 | kubelet/Image Pull Events |
| `Running`, `Ready=False` | 실행 중이지만 요청 받을 준비 미완료 | readiness/컨테이너 로그 |

같은 증상인 `Ready=False`라도 실제 병목 단계는 다를 수 있다.

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

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

## 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

## 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
