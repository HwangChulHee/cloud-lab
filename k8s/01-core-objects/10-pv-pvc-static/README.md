# Lab 12 — Static PV/PVC

> 학습 단계: **기초 개념·실습 과제**

## 목표

Pod → PVC → PV → 실제 저장소 연결을 단계별로 확인한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. 서로 다른 capacity/accessMode의 PV를 만든다.
2. PVC가 어떤 PV와 Bound 되는지 확인한다.
3. PVC를 Pod에 마운트해 파일을 생성한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 기존 Bound PVC는 유지하고, 매칭 가능한 PV가 없는 조건의 새 PVC를 별도 이름으로 만들어 Pending을 재현한다. Bound PVC의 accessModes/storageClassName/volumeName을 제자리에서 바꾸는 실험은 하지 않는다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. PV/PVC 매칭 조건과 local PV의 nodeAffinity를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 CKA 강의 전 예습

- [Retain PV로 데이터 복구하기](../../07-cka-preview/03-pv-data-recovery/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
