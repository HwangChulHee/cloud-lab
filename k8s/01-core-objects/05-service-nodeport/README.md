# Lab 07 — Service NodePort

> 학습 단계: **상세 가이드**

## 목표

Windows Host에서 NodePort를 통해 클러스터 내부 Pod에 접근한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. worker1/2에 Pod를 배치하고 NodePort Service를 만든다.
2. Windows에서 `192.168.56.31:<nodePort>`와 `.32`로 호출한다.
3. 반복 호출로 Pod 응답 분산을 확인한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod <pod>
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. Pod 하나를 삭제하고 요청 결과 변화를 관찰한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. NodePort → Service → Pod 경로를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 CKA 강의 전 예습

- [Service와 NodePort 연결 추적](../../07-cka-preview/05-service-nodeport/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
