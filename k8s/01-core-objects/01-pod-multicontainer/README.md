# Lab 03 — Pod Multi-Container

> 학습 단계: **상세 가이드**

## 목표

한 Pod 안의 여러 Container가 네트워크를 공유하는 방식을 확인한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. 포트 8000/8080 컨테이너를 가진 Pod를 만든다.
2. Pod IP로 각 포트를 호출한다.
3. 컨테이너 내부에서 `localhost`로 다른 컨테이너를 호출한다.
4. Pod 재생성 후 IP 변화를 확인한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod <pod>
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 같은 포트를 사용하는 컨테이너 구성으로 충돌을 재현한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Pod IP, Container port, localhost 관계를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 CKA 강의 전 예습

- [파일 로그를 Sidecar로 stdout에 보내기](../../07-cka-preview/10-sidecar-logging/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
