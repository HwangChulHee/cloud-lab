# cordon·drain·Eviction API·PDB

> 분류: **CKA 필수** · 선수 학습: [독립 학습](../../README.md)의 05-resources-scheduling 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

cordon은 새 Pod 스케줄링을 막지만 기존 Pod를 내리지 않는다. 이 단원에서는 실제 컴포넌트의 동작 순서를 학습하고 관찰 증거와 연결한다.

**학습 결과:** cordon·drain·Eviction API·PDB의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 핵심 질문에서 내부 원리까지

**Node를 보수할 때 서비스 가용성을 어떻게 유지할까?**

### 실행 흐름을 따라가기

cordon은 신규 배치 제한, drain은 Pod eviction 요청, PDB는 계획된 중단의 가용성을 제한한다. Node 강제 장애는 drain과 다르다.

### 예상 상태 해석 예시

SchedulingDisabled는 Node NotReady와 다르다. PDB allowedDisruptions가 0이면 drain이 차단될 수 있다.

> 이 예시는 학습용이며 실제 클러스터 실행 결과가 아니다. 환경·CNI·버전에 따라 출력이 다를 수 있다.

### 개념을 이해했는지 확인하기

- PDB를 무시하는 강제 drain은 어떤 위험이 있는가?
- 이 과정에서 **API 객체 상태를 만드는 주체**와 **실제 Node에서 실행하는 주체**는 각각 누구인가?
- 비슷한 증상을 유발할 수 있는 다른 원인 하나를 들고 확인할 첫 증거를 설명할 수 있는가?

## 선수 개념과 내부 동작

cordon은 새 Pod 스케줄링을 막지만 기존 Pod를 내리지 않는다. drain은 Eviction API를 이용해 Node의 workload를 안전하게 비우려 시도하며 PDB에 의해 지연·차단될 수 있다. DaemonSet Pod는 drain이 일반적으로 삭제하지 않는다. uncordon은 다시 스케줄 가능 상태로 만든다. 강제 노드 장애와 계획된 drain은 PDB 적용 관점에서 다르다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../README.md)의 05-resources-scheduling 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

## 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl get nodes -o wide
kubectl get pdb -A
kubectl get pods -A -o wide
```

## 따라 하기 — 순서와 예상 결과

먼저 기존 07-cka-preview/CONCEPT_BRIDGE.md의 PDB/Eviction 예제를 실행한다. 별도 테스트 Deployment를 replicas=2 이상으로 만들고 두 Worker에 분산한 뒤 테스트 Node를 선택한다. 사전 기록 후 kubectl cordon NODE → kubectl drain NODE --ignore-daemonsets (필요한 emptyDir/PDB 조건은 환경에 맞게 판단) → Pod 재배치 검증 → kubectl uncordon NODE 순서로 진행한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

## 고장 가설과 복구

PDB minAvailable가 너무 높다면 drain이 멈춘다. --force나 --disable-eviction으로 바로 우회하지 말고 PDB와 Ready replicas의 차이를 확인한다. 실습 후 uncordon 및 Node Ready 상태 확인은 필수다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

## 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

## 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[10-cluster-admin 목차](../README.md) · [전체 독립 학습](../../README.md)


## 실제 작업형 Lab — cordon, drain, PDB, uncordon

**실행 환경:** ADM-01에서 구성한 **별도 폐기 가능한 Worker 2대 + Control Plane**. 원래 Kubernetes 1.27 학습 VM에서 Node drain을 수행하지 않는다. 지금 VM에 남아 있는 다른 학습 workload, DaemonSet, local storage, PDB를 먼저 확인하고, 데이터 손실 가능성이 있다면 실행을 중단한다.

```bash
kubectl get nodes -o wide
kubectl get pods -A -o wide
kubectl get pdb -A
kubectl apply -f k8s/10-cluster-admin/06-node-maintenance/pdb-drain.yaml
kubectl -n lab-node-maintenance rollout status deploy/web --timeout=180s
kubectl -n lab-node-maintenance get pods,pdb -o wide
```

**예상:** Worker마다 web Pod 하나씩 Ready, PDB `minAvailable=2`이므로 허용 가능한 자발적 중단(`ALLOWED DISRUPTIONS`)이 0.

### PDB가 drain을 차단하는 이유

테스트 Pod가 배치된 Worker 중 하나를 `DRAIN_NODE`에 지정한다. 다른 사용자 워크로드가 있는 Node는 사용하지 않는다.

```bash
DRAIN_NODE=worker1
kubectl cordon "$DRAIN_NODE"
kubectl -n lab-node-maintenance get pods -o wide
kubectl drain "$DRAIN_NODE" --ignore-daemonsets --timeout=30s
kubectl -n lab-node-maintenance get pdb,pods -o wide
```

**예상:** `minAvailable=2` 상태에서 해당 Pod의 eviction이 차단될 수 있어 drain 명령이 timeout으로 끝난다. **실패는 의도된 테스트 결과**이며, `cordon`/drain이 설정한 `SchedulingDisabled`는 자동으로 복구되지 않는다. 이 상태에서 `--disable-eviction` 또는 `--force` 같은 강제 삭제 우회책으로 PDB를 무시하지 않는다.

### 정책을 변경해 안전하게 drain 완료

```bash
kubectl uncordon "$DRAIN_NODE"
kubectl -n lab-node-maintenance patch pdb web -p '{"spec":{"minAvailable":1}}'
kubectl -n lab-node-maintenance get pdb web
kubectl drain "$DRAIN_NODE" --ignore-daemonsets --timeout=120s
kubectl get node "$DRAIN_NODE"
kubectl -n lab-node-maintenance get pods -o wide
kubectl uncordon "$DRAIN_NODE"
kubectl -n lab-node-maintenance rollout status deploy/web --timeout=180s
```

**예상:** 이제 1개 Pod eviction이 허용된다. 다른 Worker에 이미 Pod가 있고 `required` anti-affinity를 사용하므로 새 Pod는 drain 중 Pending일 수 있지만, uncordon 뒤 원래 Worker에 배치돼 2/2 Ready로 돌아온다. `drain`과 `cordon`은 서로 다르며 drain은 Eviction API/PDB를 고려한다.

### Cleanup / 완료 검증

```bash
kubectl uncordon "$DRAIN_NODE"
kubectl delete namespace lab-node-maintenance
kubectl get nodes -o wide
```

Node가 Ready와 Scheduling 가능 상태로 복귀했는지 확인한다. `kubectl get nodes`의 STATUS가 Ready이면 언제나 scheduling 가능하다고 가정하지 않는다.

**인출:** drain이 PDB로 막힌 이유, PDB `minAvailable`과 Deployment `replicas`의 관계, `NoExecute`/Eviction/Pod 재생성의 차이. 완료는 실제 VM에서 PDB 차단과 정책 변경 뒤 drain/uncordon을 관찰하고 원복했을 때만 기록한다.
