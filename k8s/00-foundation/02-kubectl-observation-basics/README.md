# Lab 02 — kubectl Observation Basics

> 학습 단계: **기초 개념·실습 과제**

## 목표

이후 모든 실습에서 반복할 조회·상세·이벤트·로그 흐름을 익힌다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. `get`, `describe`, `logs`, `exec`, `get events --sort-by=.lastTimestamp`를 각각 사용한다.
2. `-o wide`, `-o yaml`, `-w` 출력 차이를 확인한다.
3. namespace 지정과 `-A` 차이를 확인한다.

독립 관찰용 Pod를 만들어 이름과 namespace를 확실히 고정한다. Linux kubectl 셸에서 실행한다.

```bash
kubectl create namespace lab-observation
kubectl -n lab-observation run observer --image=busybox:1.37 --restart=Never -- sh -c 'while true; do date; sleep 5; done'
kubectl -n lab-observation wait --for=condition=Ready pod/observer --timeout=120s
kubectl -n lab-observation get pods -o wide
kubectl -n lab-observation get pod observer -o yaml
kubectl -n lab-observation describe pod observer
kubectl -n lab-observation logs observer --tail=5
kubectl -n lab-observation exec observer -- hostname
kubectl -n lab-observation get events --sort-by=.lastTimestamp
kubectl -n lab-observation get pods -w
```

watch는 Ctrl+C로 종료한다. `get all`에 ConfigMap/Secret/PVC가 빠지는 점과 `get pods -A`의 namespace 열을 비교한다. ImagePullBackOff라면 wait를 반복하기 전에 Events에서 registry 연결과 이미지 태그를 확인한다.

## Break & Diagnose

```bash
kubectl -n lab-observation get pod missing
kubectl -n default get pod observer
```

두 명령은 NotFound가 예상된다. 같은 이름이라도 namespace가 다르면 다른 객체다. `kubectl -n lab-observation get pod observer`로 원래 객체가 남아 있는지 확인한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. 명령 결과만 보고 리소스 종류, namespace, 상태를 설명한다.

## Cleanup

```bash
kubectl delete namespace lab-observation
```

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 CKA 강의 전 예습

- [CRD 조회와 kubectl explain 문서 추출](../../07-cka-preview/16-crd-discovery/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
