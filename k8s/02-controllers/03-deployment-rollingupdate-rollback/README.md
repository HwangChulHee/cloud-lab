# Lab 19 — RollingUpdate & Rollback

> 학습 단계: **중간 가이드**

## 목표

중단 없는 업데이트와 revision rollback을 실험한다.

## 핵심 개념과 오해 방지

RollingUpdate가 무중단을 자동 보장하지는 않는다. Ready Pod 수, readinessProbe, maxUnavailable/maxSurge, minReadySeconds, 새 Pod를 위한 노드 자원, 앱의 종료 처리가 함께 맞아야 한다. maxSurge는 일시적으로 추가 Pod를 허용하므로 quota와 노드 여유도 본다.

Deployment rollback은 Pod template revision을 되돌린다. 외부 ConfigMap/Secret 내용이나 DB 스키마까지 자동 복구하지 않는다. `revisionHistoryLimit`에 따라 이전 ReplicaSet이 정리되면 돌아갈 revision도 제한된다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. v1에서 v2로 RollingUpdate한다.
2. 요청을 지속하며 v1/v2 공존 구간을 관찰한다.
3. `rollout status/history`를 확인한다.
4. 이전 revision으로 rollback한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 존재하지 않는 이미지로 rollout을 멈추고 원인을 찾은 뒤 rollback한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Deployment와 ReplicaSet의 관계를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 CKA 강의 전 예습

- [ConfigMap으로 TLS 설정 바꾸기](../../07-cka-preview/01-configmap-tls/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
