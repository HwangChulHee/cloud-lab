# Lab 27 — Liveness Probe

> 학습 단계: **중간 가이드**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../03-pod-deep-dive/08-scheduling-troubleshooting/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

## 목표

애플리케이션 비정상 상태를 kubelet이 재시작으로 복구하는 과정을 확인한다.

## 핵심 개념과 오해 방지

Liveness 실패는 kubelet이 해당 컨테이너를 종료하고 restartPolicy에 따라 재시작하는 계기다. Pod 전체를 새 객체로 만드는 것과 구분한다. HTTP probe는 200 이상 400 미만이 성공이며 400/500은 실패다. liveness와 startup의 successThreshold는 1이어야 한다.

느린 기동을 장애로 오인하지 않으려면 startupProbe를 고려한다. startupProbe가 성공하기 전에는 liveness/readiness를 실행하지 않는다. HTTP probe는 기본적으로 kubelet이 Pod IP로 요청하므로 host를 localhost로 고정하면 다른 의미가 될 수 있다. 앱의 외부 의존성 장애를 liveness로 연결하면 불필요한 재시작이 반복될 수 있다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

```bash
kubectl apply -f k8s/03-pod-deep-dive/03-liveness-probe/liveness.yaml
kubectl -n lab-liveness rollout status deploy/web --timeout=120s
kubectl -n lab-liveness get pods -l app=web -o wide
kubectl -n lab-liveness get pods -l app=web -o custom-columns=NAME:.metadata.name,UID:.metadata.uid,RESTARTS:.status.containerStatuses[0].restartCount
```

**예상:** Ready=True, restartCount=0. 이 liveness는 kubelet의 exec Probe로 `/tmp/live` 파일을 검사한다. 파일은 매번 컨테이너가 기동할 때 생성된다.

## Break & Diagnose

```bash
kubectl -n lab-liveness exec deploy/web -- rm /tmp/live
kubectl -n lab-liveness get pods -w
# 두 번 이상의 probe 실패를 관찰하고 Ctrl+C
kubectl -n lab-liveness describe pod -l app=web
kubectl -n lab-liveness get pods -l app=web -o custom-columns=NAME:.metadata.name,UID:.metadata.uid,RESTARTS:.status.containerStatuses[0].restartCount
```

**예상:** `Liveness probe failed` Event 뒤 kubelet이 컨테이너를 재시작한다. Deployment나 ReplicaSet이 반드시 새 Pod를 만든다는 뜻은 아니다. **같은 UID와 restartCount 증가**를 확인한다. 재시작 후 `/tmp/live` 파일이 다시 생성돼 정상으로 돌아오는지 본다.

## Recover

```bash
kubectl -n lab-liveness rollout status deploy/web --timeout=120s
kubectl -n lab-liveness exec deploy/web -- test -f /tmp/live
kubectl -n lab-liveness get pods -l app=web -o wide
```

앱 오류를 liveness가 고칠 수 없는 경우에는 단순 재시작만 반복돼 CrashLoopBackOff로 이어질 수 있다. 느린 초기 기동에는 Startup Probe를 사용하고, 외부 DB 장애를 무조건 Liveness에 연결하지 않는다.

## 완료 검증 / Cleanup / Explain

Pod UID 유지 여부, restartCount 증가, Event 내용, 복구 후 Ready 상태를 기록하고 Startup/Readiness/Liveness의 역할 차이를 설명한다.

```bash
kubectl delete namespace lab-liveness
```
