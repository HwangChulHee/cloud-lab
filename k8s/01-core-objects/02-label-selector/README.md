# Lab 04 — Labels & Selectors

> 학습 단계: **기초 개념·실습 과제**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/01-pods/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

Label이 리소스 분류와 연결에 어떻게 쓰이는지 실험한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. type/lo 라벨 조합이 다른 Pod 여러 개를 만든다.
2. `kubectl get pods -l`로 집합을 조회한다.
3. selector가 다른 Service 두 개를 만들어 연결 대상 차이를 확인한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. Service selector를 존재하지 않는 값으로 바꾸고 Endpoint가 비는지 확인한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Service selector와 Pod label 매칭 결과를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [Service와 NodePort 연결 추적](../../07-cka-preview/05-service-nodeport/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.

- [최소 권한 NetworkPolicy](../../07-cka-preview/08-networkpolicy/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
