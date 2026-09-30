# Lab 22 — Job

> 학습 단계: **중간 가이드**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/03-controllers/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

완료형 workload의 재시도·병렬성·완료 횟수를 확인한다.

## 핵심 개념과 오해 방지

completions는 성공적으로 완료해야 할 작업 수이고, 실패 재시도 때문에 실제 생성된 Pod 수는 더 많을 수 있다. parallelism은 동시에 실행할 작업 수의 상한이며 항상 그 개수가 Running인 것은 아니다. restartPolicy=OnFailure는 같은 Pod 안의 컨테이너 재시작을, Never는 실패 Pod 이후 새 Pod 재시도를 관찰하기 좋다. backoffLimit와 activeDeadlineSeconds도 함께 본다. 완료한 Pod는 TTL 등 별도 정리 정책이 없으면 남아 있을 수 있다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. 단일 Job을 실행한다.
2. 서로 다른 completions/parallelism 값을 가진 새 Job을 별도 이름으로 만들어 Pod 실행 패턴을 비교한다.
3. activeDeadlineSeconds를 적용한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 실패 command가 들어 있는 새 Job을 만들어 retry/Failed 상태를 관찰한다. 기존 Job의 Pod template command는 immutable이므로 직접 수정하지 않는다. 복구도 정상 command의 새 Job으로 실행한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Job의 성공 조건을 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.
