# Lab 23 — CronJob

> 학습 단계: **중간 가이드**

## 실습 안내

이 README가 해당 주제의 공식 학습 자료다. **실습 전 상태 확인 → 리소스 구축 → 정상 증거 수집 → 제한된 장애 재현 → 복구 → 정리 → 인출 질문** 순서로 진행한다. 기존 독립 코스는 별도 진도로 계산하지 않는다.

## 목표

주기 실행과 동시 실행 정책을 비교한다.

## 핵심 개념과 오해 방지

concurrencyPolicy는 같은 CronJob이 만든 Job들 사이의 실행 정책이다. Allow는 중첩을 허용하고 Forbid는 이전 작업이 끝나지 않았을 때 새 스케줄 실행을 건너뛰며 Replace는 실행 중인 이전 Job을 새 Job으로 교체한다. 다른 CronJob이나 독립 수동 Job까지 전역적으로 직렬화하지 않는다.

suspend=true는 앞으로의 예약 실행을 멈추며 이미 실행 중인 Job은 그대로 계속된다. timeZone, startingDeadlineSeconds, 성공/실패 history limit도 구분한다. 스케줄러는 정확히 한 번 실행을 보장하지 않으므로 작업은 중복 실행에도 안전하게 설계해야 한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

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
