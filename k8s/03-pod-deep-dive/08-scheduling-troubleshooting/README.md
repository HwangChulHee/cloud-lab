# Lab 32 — Scheduling Troubleshooting

> 학습 단계: **중간 가이드**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../03-pod-deep-dive/08-scheduling-troubleshooting/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

## 목표

Pending 원인을 requests, affinity, taint 관점에서 구분한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. 서로 다른 원인의 Pending Pod 3개를 준비한다.
2. Events만 보고 resource 부족/affinity 불일치/taint 미허용을 구분한다.
3. 각 문제를 최소 변경으로 복구한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 원인 정보를 보지 않고 증상만 보고 순서대로 진단한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. 스케줄링 장애 점검 순서를 자신의 말로 정리한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [자원 예산을 계산해 3개 Pod 복구하기](../../07-cka-preview/11-resource-budget/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.

- [PriorityClass와 스케줄링 우선순위](../../07-cka-preview/12-priorityclass/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.


## 종합 진단: 같은 Ready 실패, 서로 다른 책임 계층

Lab 25–31에서 이미 수행한 QoS/Probe/Affinity/Taint 실습을 처음부터 반복하는 대신, **여러 실패가 섞인 상태에서 먼저 증거를 보고 원인 계층을 구분**한다. 핵심은 Scheduler Filter/Score, kubelet Probe/Restart, Container 종료 상태의 차이를 설명하는 것이다.

### 1. 관찰 환경 구축

`extended-setup.yaml`은 Namespace와 QoS 비교 Pod를, `extended-health.yaml`은 Readiness/Liveness를, `extended-status.yaml`은 완료/Crash 사례를, `extended-placement.yaml`은 Affinity 배치를 제공한다. 관련 자산은 본 Lab에만 보존한다.

```bash
kubectl get nodes -L kubernetes.io/hostname
PLACEMENT_WORKER=k8s-worker1
kubectl apply -f k8s/03-pod-deep-dive/08-scheduling-troubleshooting/extended-setup.yaml
kubectl apply -f k8s/03-pod-deep-dive/08-scheduling-troubleshooting/extended-health.yaml
sed "s/REPLACE_WORKER_HOSTNAME/$PLACEMENT_WORKER/" k8s/03-pod-deep-dive/08-scheduling-troubleshooting/extended-placement.yaml > /tmp/lab-self-placement.yaml
kubectl apply -f /tmp/lab-self-placement.yaml
kubectl apply -f k8s/03-pod-deep-dive/08-scheduling-troubleshooting/extended-status.yaml
kubectl -n lab-self-placement get deploy,pods -o wide
```

실제 `kubernetes.io/hostname` label이 `k8s-worker1`이 아니라면 `PLACEMENT_WORKER`에 조회한 label 값을 넣는다. `place`는 지정 Node에, `near`는 `place`와 같은 Node에, `spread`는 서로 다른 Node에 배치될 것으로 예측한다.

### 2. 증상만 보고 장애 위치 분류

| 실험 | 대상 | 예상 증거 | 확인할 컴포넌트 |
|---|---|---|---|
| A | `crash` Pod | 재시작·종료 코드·CrashLoopBackOff | kubelet/runtime |
| B | `health` Readiness 실패 | Running but Ready=False, EndpointSlice ready=false | kubelet/EndpointSlice |
| C | `place` 신규 Pod 배치 실패 | Pending + FailedScheduling | Scheduler Filter |

**A: 컨테이너 종료 분석**

```bash
kubectl -n lab-self-placement get pod crash -o jsonpath='{.status.phase}{" / "}{.status.containerStatuses[0].restartCount}{"\n"}'
kubectl -n lab-self-placement describe pod crash
kubectl -n lab-self-placement logs crash --previous
```

**B: Probe 실패 분석**

```bash
HEALTH_POD=$(kubectl -n lab-self-placement get pod -l app=health -o jsonpath='{.items[0].metadata.name}')
kubectl -n lab-self-placement exec "$HEALTH_POD" -- rm /tmp/ready
kubectl -n lab-self-placement get pod "$HEALTH_POD" -o wide
kubectl -n lab-self-placement get endpointslices -l kubernetes.io/service-name=health -o yaml
```

**C: 새 Pod의 배치 실패 분석**

```bash
kubectl -n lab-self-placement patch deploy place --type=merge -p '{"spec":{"template":{"spec":{"nodeSelector":{"cloud-lab/impossible":"true"}}}}}'
kubectl -n lab-self-placement get pods -l app=place -o wide
kubectl -n lab-self-placement get events --sort-by=.lastTimestamp
```

기존 RollingUpdate Pod가 남아 **서비스가 살아 있는 동안에도 신규 Pod만 Pending일 수 있다.** 이것은 Deployment controller가 충분한 가용성을 유지하려고 기존 Pod를 즉시 삭제하지 않기 때문이다.

### 3. 최소 복구 및 동일 조건 재검증

```bash
kubectl -n lab-self-placement exec "$HEALTH_POD" -- touch /tmp/ready
kubectl -n lab-self-placement patch deploy place --type=merge -p '{"spec":{"template":{"spec":{"nodeSelector":null}}}}'
kubectl -n lab-self-placement rollout status deploy/health --timeout=120s
kubectl -n lab-self-placement rollout status deploy/place --timeout=120s
kubectl -n lab-self-placement get pods -o wide
```

`crash`는 독립 Pod이므로 잘못된 command를 제자리 수정하지 않고 별도의 정상 Pod로 교체하거나 테스트 종료 시 Namespace와 함께 삭제한다. 이를 Controller의 복제본 복구와 구분한다.

### 4. Runbook / Cleanup / 인출

```bash
kubectl delete namespace lab-self-placement
rm -f /tmp/lab-self-placement.yaml
```

실패 상태만 보여주고 어떤 실험인지 감춘 상태에서 아래를 수행할 수 있으면 완료다.

1. **처음 확인할 세 명령**을 선택한다. 모든 경우에 무작정 `kubectl logs`부터 보지는 않는다.
2. `Pending + FailedScheduling`, `Running + Ready=False`, `CrashLoopBackOff`의 책임 계층을 분류한다.
3. 두 개 이상의 가설을 세우고 가장 판별력 있는 증거로 반증한다.
4. 최소 수정으로 복구하고 변경 전후 Pod/Events/Service 상태를 비교한다.

**선택 확장:** LimitRange 기본값과 Admission 거절은 `extended-limits.yaml`, `extended-over.yaml`을 사용해 Lab 16의 내용을 복습한다. 이 선택 확장은 Lab 32 완료를 위한 별도 필수 단계가 아니다.
