# Lab 16 — ResourceQuota & LimitRange

> 학습 단계: **기초 개념·실습 과제**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/05-resources-scheduling/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

Namespace 단위 자원 정책이 Pod 생성에 미치는 영향을 확인한다.

## 핵심 개념과 오해 방지

ResourceQuota는 namespace 전체의 총 요청량·제한량·객체 수를 관리하고, LimitRange는 개별 Container/Pod/PVC의 기본값과 허용 범위를 관리한다. 둘 다 노드의 실제 사용량을 기준으로 자동 확장하는 기능은 아니다.

`defaultRequest`와 `default`의 차이, `min`/`max`, `maxLimitRequestRatio`를 비교한다. LimitRange로 기본값이 먼저 채워지면 자원값 없는 Pod도 quota 조건을 만족할 수 있다. 정책 추가가 기존 Pod의 설정을 자동 수정하거나 기존 Pod를 즉시 퇴거시키지는 않는다. API 거절로 Pod가 생성되지 않은 경우와 생성 후 Pending인 경우를 구분한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. memory requests/limits ResourceQuota를 만든다.
2. 자원값 없는 Pod 생성 실패를 확인한다.
3. 누적 quota 초과와 pod 개수 quota 초과를 확인한다.
4. LimitRange의 default/min/max를 적용해 자동 주입과 거부를 관찰한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 정책을 만족하지 않는 Pod YAML을 단계별로 수정해 성공시킨다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. 거부 메시지에서 어떤 정책이 원인인지 식별한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [자원 예산을 계산해 3개 Pod 복구하기](../../07-cka-preview/11-resource-budget/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.

## 실습 기록 (2026-10-29)

- `lab-resource-policy` Namespace에 ResourceQuota `lab-quota` 생성: `requests.memory=512Mi`, `limits.memory=1Gi`, `pods=3`.
- requests/limits 없이 `no-resources-pod` 생성 시 `Forbidden: failed quota ... must specify limits.memory; requests.memory` 확인. Pod 객체는 생성되지 않았고 Quota Used는 0.
- 요청/제한을 128Mi/256Mi로 지정한 뒤 Pod가 `k8s-worker1`에서 Running, quota Used=128Mi/256Mi 및 pods=1 확인.
- 두 번째 Pod에 request 400Mi를 주어 `requested: requests.memory=400Mi, used: 128Mi, limited: 512Mi` 거부 확인. 256Mi/512Mi로 수정 후 k8s-worker2에서 Running, Used=requests 384Mi, limits 768Mi, pods 2.
- 세 번째 Pod(32Mi/64Mi)는 정상 생성, 네 번째 Pod는 `requested: pods=1, used: pods=3, limited: pods=3`로 거부. Used=requests 416Mi, limits 832Mi, pods 3.
- 세 번째 Pod를 삭제해 예산 확보 후 LimitRange `lab-limits` 생성: 컨테이너 메모리 `defaultRequest=64Mi`, `default=128Mi`, `min=32Mi`, `max=512Mi`.
- 자원 설정을 생략한 `default-resource-pod` 생성 성공. API 저장된 Pod spec에 `requests.memory=64Mi` 및 `limits.memory=128Mi` 자동 주입 검증. Used=requests 448Mi, limits 896Mi, pods 3.
- `default-resource-pod`를 삭제한 후 `exceed-limit-pod`의 limit 768Mi는 `maximum memory usage per Container is 512Mi, but limit is 768Mi`로 거부됨. request/limit을 64Mi/128Mi로 수정하여 Pod 생성 성공, 최종 Used=requests 448Mi, limits 896Mi, pods 3.
- YAML 수정 과정에 tab 문자 들여쓰기 오류 발생 후 공백 들여쓰기로 수정하여 재적용 성공.
- **Cleanup:** `kubectl delete namespace lab-resource-policy` 후 namespace 조회 `NotFound` 확인. 실습 전용 Pod/Quota/LimitRange 정리 완료.
- **복습:** 2문제 진행 예정.
