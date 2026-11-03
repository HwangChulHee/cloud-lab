# Lab 25 — Pod Lifecycle & Status

> 학습 단계: **중간 가이드**

## 실습 안내

이 README가 해당 주제의 공식 학습 자료다. **실습 전 상태 확인 → 리소스 구축 → 정상 증거 수집 → 제한된 장애 재현 → 복구 → 정리 → 인출 질문** 순서로 진행한다. 기존 독립 코스는 별도 진도로 계산하지 않는다.

## 목표

Pod phase와 Container 상태/재시작을 관찰한다.

## 핵심 개념과 오해 방지

`status.phase`의 Pending/Running/Succeeded/Failed/Unknown과 kubectl 표의 STATUS는 같지 않다. CrashLoopBackOff는 컨테이너 재시작 대기 사유이고 Completed는 표시용 상태/종료 사유이며 별도의 Pod phase가 아니다. restartPolicy=Always인 짧은 명령은 exit 0이어도 반복 재시작할 수 있으므로 완료 Pod 비교에는 Never를 사용한다. 컨테이너 재시작은 같은 Pod 안에서, Controller 재생성은 새 Pod UID에서 발생한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

```bash
kubectl apply -f k8s/03-pod-deep-dive/01-pod-lifecycle-status/lifecycle.yaml
kubectl -n lab-pod-lifecycle get pods -o wide
kubectl -n lab-pod-lifecycle get pods -o custom-columns=NAME:.metadata.name,PHASE:.status.phase
kubectl -n lab-pod-lifecycle describe pod crash
kubectl -n lab-pod-lifecycle describe pod bad-image
kubectl -n lab-pod-lifecycle get pod crash -o jsonpath='{.status.containerStatuses[0].restartCount}{"\n"}'
```

**예상:** running은 Running; completed는 Succeeded/표시 Completed; crash는 Pod phase Running일 수 있지만 컨테이너가 Waiting/CrashLoopBackOff, `restartCount` 증가; bad-image는 이미지 조회 오류로 Waiting/ImagePullBackOff 또는 ErrImagePull. 이미지를 가져오지 못한 Pod가 Phase Pending을 보일 수도 있다.

## Break & Diagnose

```bash
kubectl -n lab-pod-lifecycle get pod crash -o jsonpath='{.metadata.uid}{"\n"}'
kubectl -n lab-pod-lifecycle get pod crash -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}{"\n"}'
kubectl -n lab-pod-lifecycle logs crash --previous
kubectl -n lab-pod-lifecycle get events --sort-by=.lastTimestamp
```

**판별:** 같은 Pod UID와 증가하는 restartCount라면 컨테이너 재시작이다. 삭제 후 새 UID가 생기는 Controller 재생성과 구별한다. `--previous` 로그는 이전 컨테이너가 없을 때 오류를 반환할 수 있다.

## Recover

독립 Pod의 컨테이너 command는 수정할 수 없으므로 **새 Pod 이름**으로 정상이 되는 예를 확인한다.

```bash
kubectl -n lab-pod-lifecycle run recovered --image=busybox:1.37 --restart=Never -- sh -c 'echo recovered'
kubectl -n lab-pod-lifecycle wait --for=jsonpath='{.status.phase}'=Succeeded pod/recovered --timeout=120s
kubectl -n lab-pod-lifecycle logs recovered
```

## 완료 검증 / Cleanup / Explain

각 Pod의 **Pod phase / kubectl STATUS / Container state / restartCount / Events**를 한 표로 기록한다.

```bash
kubectl delete namespace lab-pod-lifecycle
```

인출 질문: CrashLoopBackOff가 Pod phase가 아닌 이유? `OOMKilled`와 `Evicted`는 어느 계층의 상태를 확인해야 하는가? 독립 Pod를 지워도 자동 재생성되지 않는 이유?
