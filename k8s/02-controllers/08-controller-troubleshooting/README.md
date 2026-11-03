# Lab 24 — Controller Troubleshooting

> 학습 단계: **중간 가이드**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../08-independent/03-controllers/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

## 목표

여러 Controller의 이상 상태를 증상만 보고 진단한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. ReplicaSet replicas 불일치, Deployment rollout 정지, DaemonSet node mismatch, Job 실패를 순서대로 진단한다.
2. 각 케이스에서 `get`, `describe`, Events 중 어떤 정보가 결정적이었는지 기록한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 정답 가이드 없이 4개 장애를 복구한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Controller별 원하는 상태와 실제 상태 차이를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.


## 내부 동작 심화: Watch와 Reconciliation

Deployment → ReplicaSet → Pod의 소유 관계를 `ownerReferences`로 확인한다. Deployment Controller는 ReplicaSet의 원하는 상태를, ReplicaSet Controller는 Pod 개수를 맞추며, **kubelet이 Deployment 전체 복제본 수를 관리하는 것은 아니다**.

```bash
kubectl get deployments,replicasets,pods -n <namespace>
kubectl get deployment <name> -n <namespace> -o jsonpath='{.metadata.generation}{" / "}{.status.observedGeneration}{"\n"}'
kubectl get pods -n <namespace> -o custom-columns=NAME:.metadata.name,OWNER:.metadata.ownerReferences[0].name,UID:.metadata.uid
```

`spec.replicas`와 `status.readyReplicas`는 서로 다른 값일 수 있다. Watch가 변경을 효율적으로 전달하더라도 재연결·재조회·재조정이 필요할 수 있다. Pod 삭제 후 새 Pod가 생성되는 동안 API 객체 상태와 실제 실행 상태를 따로 기록한다. 심화 참고: [Reconciliation 관찰 절차](../../09-internals/02-reconciliation-watch/README.md).


## 내부 동작 심화 통합 — 02-reconciliation-watch

기존 INT 모듈의 개념·관찰·원인 분석 내용을 이 Lab에 병합했다. 코드 블록에 등장하는 `lab-self-*`는 이전 독립 예제의 실습용 Namespace이며, 현재 Lab의 리소스를 우선 사용하거나 해당 확장 YAML을 적용한 뒤 관찰한다. 별도 INT 진도는 만들지 않는다.

#### 선수 개념과 내부 동작

API 객체의 spec은 원하는 상태, status는 관찰된 상태다. Deployment Controller는 ReplicaSet의 revision/복제 수를 조절하고 ReplicaSet Controller는 Pod 개수를 맞춘다. Scheduler와 kubelet은 별도의 루프에서 동작한다. watch는 변경 이벤트를 효율적으로 받는 수단이지만 끊김·재연결·재동기화가 존재한다. observedGeneration이 generation보다 뒤처졌다면 Controller가 새 spec을 아직 반영하지 않았을 수 있다.

#### 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../README.md)의 03-controllers 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

#### 예시: replicas=2인 Deployment에서 Pod 하나를 삭제하면?

`Deployment/web → ReplicaSet/web-abc → Pod/web-abc-1, web-abc-2`인 상황을 가정한다. `web-abc-1`을 삭제해도 Deployment의 `spec.replicas=2`는 그대로다. ReplicaSet Controller는 현재 수와 원하는 수의 차이를 보고 새 `web-abc-3`을 만든다. Scheduler와 kubelet은 새 Pod의 배치와 실행을 각각 진행한다. Deployment Controller가 매번 컨테이너를 직접 재시작하는 것은 아니다.

관찰할 것은 **소유권(ownerReferences), 새로운 Pod UID, replicas/readyReplicas의 변화**다. 복구가 완료됐어도 원래 Pod UID가 돌아오는 것은 아니다.

#### 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl -n lab-self-control get deploy,rs,pods -o wide
kubectl -n lab-self-control get deploy web -o jsonpath='{.metadata.generation}{" / "}{.status.observedGeneration}{"\n"}'
kubectl -n lab-self-control get rs -o wide
kubectl -n lab-self-control get pods -o custom-columns=NAME:.metadata.name,OWNER:.metadata.ownerReferences[0].name,UID:.metadata.uid
```

#### 따라 하기 — 순서와 예상 결과

03-controllers 실습 리소스를 유지한 상태에서 웹 Pod 이름과 UID를 기록한다. Pod 하나를 삭제하고 watch로 새 Pod가 나타나는지 확인한다. 그 다음 ReplicaSet의 ownerReference를 조회하여 새 Pod의 직접 관리자가 Deployment가 아닌 ReplicaSet임을 확인한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

#### 고장 가설과 복구

Pod를 지우고도 새 Pod가 안 나타나면 ReplicaSet의 desired/current/ready와 Events를 확인한다. Pod가 생겼지만 Ready가 아니면 Scheduler·ImagePull·Probe로 진단 계층을 이동한다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

#### 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

#### 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

#### 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/concepts/architecture/controller/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../README.md)
