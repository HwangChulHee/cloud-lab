# Lab 23 — CronJob

> 학습 단계: **중간 가이드**

## 강의 없이 시작하기

이 README가 이 주제의 **공식 학습·실습 기록**입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [이전 독립 코스의 추가 실행 자산](../../02-controllers/08-controller-troubleshooting/README.md)은 고유 예제나 YAML이 필요할 때 참고하며 별도로 중복 완료하지 않습니다.

## 목표

주기 실행과 동시 실행 정책을 비교한다.

## 핵심 개념과 오해 방지

concurrencyPolicy는 같은 CronJob이 만든 Job들 사이의 실행 정책이다. Allow는 중첩을 허용하고 Forbid는 이전 작업이 끝나지 않았을 때 새 스케줄 실행을 건너뛰며 Replace는 실행 중인 이전 Job을 새 Job으로 교체한다. 다른 CronJob이나 독립 수동 Job까지 전역적으로 직렬화하지 않는다.

suspend=true는 앞으로의 예약 실행을 멈추며 이미 실행 중인 Job은 그대로 계속된다. timeZone, startingDeadlineSeconds, 성공/실패 history limit도 구분한다. 스케줄러는 정확히 한 번 실행을 보장하지 않으므로 작업은 중복 실행에도 안전하게 설계해야 한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. 짧은 schedule로 CronJob을 만든다.
2. manual Job trigger를 수행한다.
3. suspend/resume을 확인한다.
4. Allow/Forbid/Replace를 비교한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 실행 시간이 주기보다 긴 Job으로 concurrency 차이를 재현한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. 각 concurrencyPolicy의 동작을 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.


## 따라 하기 — CronJob 예약 실행·수동 실행·중첩 제어

시작 전에 현재 컨텍스트와 시각을 확인한다. `* * * * *`는 **매분** 실행하며 90초 작업이므로 중첩을 관찰할 수 있다.

```bash
kubectl apply -f k8s/02-controllers/07-cronjob/cronjob-lab.yaml
kubectl -n lab-cronjob get cronjob clock
kubectl -n lab-cronjob create job manual --from=cronjob/clock
kubectl -n lab-cronjob get jobs,pods -o wide
kubectl -n lab-cronjob describe cronjob clock
```

**예상:** 직접 만든 `manual` Job은 바로 시작한다. 예약 Job은 다음 분 경계 이후 생성될 수 있다. `Forbid`는 CronJob이 관리하는 예약 Job끼리 겹치지 않게 하므로 **수동 Job까지 절대 직렬화하지 않는다**.

```bash
kubectl -n lab-cronjob patch cronjob clock --type=merge -p '{"spec":{"suspend":true}}'
kubectl -n lab-cronjob get cronjob clock -o yaml
kubectl -n lab-cronjob get jobs,pods
kubectl -n lab-cronjob patch cronjob clock --type=merge -p '{"spec":{"suspend":false}}'
kubectl -n lab-cronjob patch cronjob clock --type=merge -p '{"spec":{"concurrencyPolicy":"Replace"}}'
kubectl -n lab-cronjob describe cronjob clock
```

**예상:** suspend는 미래의 예약 실행을 멈추지만 **진행 중인 Job은 종료하지 않는다**. `Replace`는 이후 예약 시 이전 실행 중 Job을 교체할 수 있다. CronJob의 LastScheduleTime과 Job 생성 시각을 구별한다. 예약 시점을 실제로 관찰하지 못했다면 동시 실행 정책까지 완료 처리하지 않는다.

```bash
kubectl -n lab-cronjob patch cronjob clock --type=merge -p '{"spec":{"suspend":true}}'
kubectl delete namespace lab-cronjob
```

**인출:** Allow/Forbid/Replace, suspend와 이미 실행 중인 Job 관계, idempotent 작업 설계 이유를 설명한다.
