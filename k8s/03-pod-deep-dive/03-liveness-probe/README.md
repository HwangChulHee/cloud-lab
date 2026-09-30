# Lab 27 — Liveness Probe

> 학습 단계: **중간 가이드**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/05-resources-scheduling/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

애플리케이션 비정상 상태를 kubelet이 재시작으로 복구하는 과정을 확인한다.

## 핵심 개념과 오해 방지

Liveness 실패는 kubelet이 해당 컨테이너를 종료하고 restartPolicy에 따라 재시작하는 계기다. Pod 전체를 새 객체로 만드는 것과 구분한다. HTTP probe는 200 이상 400 미만이 성공이며 400/500은 실패다. liveness와 startup의 successThreshold는 1이어야 한다.

느린 기동을 장애로 오인하지 않으려면 startupProbe를 고려한다. startupProbe가 성공하기 전에는 liveness/readiness를 실행하지 않는다. HTTP probe는 기본적으로 kubelet이 Pod IP로 요청하므로 host를 localhost로 고정하면 다른 의미가 될 수 있다. 앱의 외부 의존성 장애를 liveness로 연결하면 불필요한 재시작이 반복될 수 있다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. HTTP `/health` liveness probe를 설정한다.
2. 정상 상태의 restartCount를 기록한다.
3. 애플리케이션을 500 상태로 만들고 failureThreshold 이후 재시작을 관찰한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. probe path를 고의로 틀려 재시작 루프를 만든 뒤 복구한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Readiness와 Liveness의 실패 결과 차이를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.
