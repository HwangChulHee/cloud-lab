# Lab 20 — Blue/Green with Service Selector

> 학습 단계: **중간 가이드**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../02-controllers/08-controller-troubleshooting/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

## 목표

두 버전을 동시에 띄우고 Service selector로 트래픽을 전환한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. v1/v2 ReplicaSet 또는 Deployment를 동시에 만든다.
2. Service를 v1에 연결한다.
3. selector를 v2로 바꿔 즉시 전환한다.
4. v1로 되돌려 rollback을 확인한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. selector 오타로 Endpoint 0 상태를 만든 뒤 복구한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 실습 완료 기록 (2026-11-03)

- ✅ Blue/Green Deployment 각 2개 Pod Ready, Service의 Blue 응답 및 EndpointSlice 검증.
- ✅ Service selector를 blue → green으로 변경하여 HTTP green 및 Green Endpoint 확인.
- ✅ selector를 green → blue로 되돌려 기존 Pod를 재생성하지 않고 트래픽 복구.
- ✅ 잘못된 selector bluue로 EndpointSlice 대상 0개 및 Connection refused 재현. Pod 4개는 Ready 유지.
- ✅ selector 복구 후 HTTP blue, Blue Endpoint 2개 Ready 확인.
- ✅ lab-bluegreen Namespace 삭제 후 NotFound 확인.
- ✅ 복습 2/2 완료: Service selector 변경에 따른 API Server → EndpointSlice Controller → kube-proxy 흐름, Pod 레이블 불일치 시 Endpoint 장애 및 진단 절차 설명.

## 완료 검증

1. RollingUpdate와 Blue/Green의 차이를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.
