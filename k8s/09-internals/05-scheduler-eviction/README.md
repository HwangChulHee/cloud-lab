# Filtering·Scoring·OOMKilled·Node Eviction

> 분류: **필수 개념** · 선수 학습: [독립 학습](../../08-independent/README.md)의 05-resources-scheduling 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

스케줄러는 nodeSelector/affinity/taint, PVC 토폴로지와 requests를 토대로 후보 Node를 Filter한 다음 Score한다. 이 단원에서는 실제 컴포넌트의 동작 순서를 학습하고 관찰 증거와 연결한다.

**학습 결과:** Filtering·Scoring·OOMKilled·Node Eviction의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 핵심 질문에서 내부 원리까지

**Pod Pending과 OOMKilled를 왜 구별해야 할까?**

### 실행 흐름을 따라가기

Scheduler는 request와 배치 조건으로 Filter/Score한다. OOMKilled는 실행된 컨테이너의 메모리 종료, NodePressure Eviction은 kubelet이 Node 압박에 대응하는 별개 상황이다.

### 예상 상태 해석 예시

FailedScheduling은 PodScheduled 조건에서, OOMKilled는 lastState.terminated.reason에서 관찰하는 것이 출발점이다.

> 이 예시는 학습용이며 실제 클러스터 실행 결과가 아니다. 환경·CNI·버전에 따라 출력이 다를 수 있다.

### 개념을 이해했는지 확인하기

- CPU throttling과 OOMKilled의 차이는?
- 이 과정에서 **API 객체 상태를 만드는 주체**와 **실제 Node에서 실행하는 주체**는 각각 누구인가?
- 비슷한 증상을 유발할 수 있는 다른 원인 하나를 들고 확인할 첫 증거를 설명할 수 있는가?

## 선수 개념과 내부 동작

스케줄러는 nodeSelector/affinity/taint, PVC 토폴로지와 requests를 토대로 후보 Node를 Filter한 다음 Score한다. kubectl top의 현재 CPU가 최소인 Node를 단순 선택하지 않는다. CPU limit 초과는 통상 throttling으로 이어지고, 메모리 limit 위반은 OOMKilled로 이어질 수 있다. Node Pressure Eviction은 kubelet이 메모리/디스크/PID 압박 상황에서 Pod를 종료하는 별도 메커니즘이다. QoS 외에 request 초과 사용·Priority도 영향을 미친다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../08-independent/README.md)의 05-resources-scheduling 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

### 예시: 세 종류의 실패를 다른 단계에서 찾기

- **Pending/FailedScheduling:** Pod가 `cpu: 2`를 요청하지만 조건에 맞는 Node에는 할당 가능한 자원이 없다. Scheduler 이벤트에 `Insufficient cpu`가 나타날 수 있다.
- **OOMKilled:** Pod가 배치돼 실행되었으나 컨테이너가 메모리 제한을 넘겨 종료된다. `lastState.terminated.reason=OOMKilled`를 확인한다.
- **Evicted:** Node의 메모리·디스크 압박에 kubelet이 대응하여 Pod를 축출한다. Pod의 `status.reason`과 Node Conditions를 함께 확인한다.

즉 Scheduler가 보고 판단하는 **requests**와 실행 시 적용되는 **limits**, NodePressure는 서로 다른 계층이다. CPU 제한은 일반적으로 즉시 종료보다 throttling으로 나타날 수 있다.

## 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl get nodes -o wide
kubectl describe nodes
kubectl -n lab-self-placement get pods -o wide
kubectl -n lab-self-placement get events --sort-by=.lastTimestamp
```

## 따라 하기 — 순서와 예상 결과

기존 05단계에서 nodeSelector를 불가능한 값으로 변경하고 FailedScheduling 이벤트를 관찰한다. LimitRange/ResourceQuota에서 API 단계 거부와 이미 생성된 Pending을 비교한다. QoS 세 클래스를 조회해 계산 규칙을 설명한다. OOM/Node Pressure는 개념과 로그 사례 분석을 먼저 진행한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

## 고장 가설과 복구

Pending에는 Pod spec.nodeName과 PodScheduled 조건을, OOMKilled에는 lastState.terminated.reason과 restartCount를, Evicted에는 Pod status.reason과 Node Conditions를 제시한다. Node를 실제 고갈시키는 장애 주입은 하지 않는다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

## 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

## 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
