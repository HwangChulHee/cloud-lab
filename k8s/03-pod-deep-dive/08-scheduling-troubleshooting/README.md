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


## 운영 심화 연결: Scheduler Filter/Score와 Eviction 판단

기존 스케줄링 장애 실습에 다음 세 가지 **서로 다른 실패 계층**을 분리해 기록한다.

| 증상 | 책임 주체/계층 | 최초 확인 증거 |
|---|---|---|
| `Pending` + `FailedScheduling` | Scheduler의 Filter 조건 (requests, affinity, taint, PVC 토폴로지) | `describe pod`의 Events와 PodScheduled |
| 컨테이너 `OOMKilled` | 실행 중 메모리 제한/커널 OOM | `lastState.terminated.reason`, restartCount |
| Node 압박에 의한 `Evicted` | kubelet eviction | Pod status/message와 Node Conditions/Events |

Scheduler는 `kubectl top`의 실시간 CPU가 가장 낮은 노드를 단순 선택하지 않는다. CPU limit 초과 시 throttling과 메모리 초과 시 OOMKilled, NodePressure Eviction을 구별한다. QoS 외에도 requests 초과 사용과 Priority가 eviction 판단에 영향을 미칠 수 있다. 독립 추가 실습을 새로 만들기보다는 Lab 25–32에서 얻은 결과를 이곳에 종합한다. [내부 참고](../../03-pod-deep-dive/08-scheduling-troubleshooting/README.md).


## 통합 확장 실습 — 자원·배치·Probe 종합

이 절은 이전 독립 8단계 과정의 고유 실습·장애 재현을 이 Lab에 합친 것이다. 별도의 8단계 진도를 만들지 않는다. `extended-*.yaml` 자산은 이 Lab에 보존되어 있으며 별도 `lab-self-*` Namespace를 생성하므로 기존 완료 실습을 덮어쓰지 않는다.

> 주의: 합쳐진 배치 예제는 현재 42개 Lab의 개별 사례를 우선 사용한다. 원본 통합 YAML을 4개 파일로 분리했다. 아래 명령은 확장 QoS·Probe·Affinity·상태 관찰을 위한 입력 파일을 순서대로 설치한다.

#### 따라 하기

worker의 실제 hostname label 값을 고른다. 기본 환경은 worker 두 개이며, spread는 서로 다른 노드에 배치돼야 한다.

```bash
kubectl get nodes -L kubernetes.io/hostname
PLACEMENT_WORKER=REPLACE_WORKER_HOSTNAME
kubectl apply -f k8s/03-pod-deep-dive/08-scheduling-troubleshooting/extended-setup.yaml
kubectl apply -f k8s/03-pod-deep-dive/08-scheduling-troubleshooting/extended-health.yaml
sed "s/REPLACE_WORKER_HOSTNAME/$PLACEMENT_WORKER/" k8s/03-pod-deep-dive/08-scheduling-troubleshooting/extended-placement.yaml > /tmp/lab-self-placement.yaml
kubectl apply -f /tmp/lab-self-placement.yaml
kubectl apply -f k8s/03-pod-deep-dive/08-scheduling-troubleshooting/extended-status.yaml
kubectl -n lab-self-placement rollout status deploy/health --timeout=120s
kubectl -n lab-self-placement rollout status deploy/place --timeout=120s
kubectl -n lab-self-placement rollout status deploy/spread --timeout=120s
kubectl -n lab-self-placement rollout status deploy/near --timeout=120s
kubectl -n lab-self-placement get pods -o wide
kubectl -n lab-self-placement get pod best burst guaranteed -o custom-columns=NAME:.metadata.name,QOS:.status.qosClass
```

BestEffort, Burstable, Guaranteed와 spread의 서로 다른 nodeName을 예상한다. near는 place와 같은 노드에 배치되는 positive affinity를 비교한다. 노드 한 개만 쓸 수 있는 환경에서는 spread 한 개가 Pending인 것이 예상 결과다. 과목 완료를 위해서는 두 worker 환경을 준비하거나 그 환경 제약을 해결한다.

#### phase와 표시 상태를 나눠 보기

```bash
kubectl -n lab-self-placement get pod finished crash
kubectl -n lab-self-placement get pod finished crash -o custom-columns=NAME:.metadata.name,PHASE:.status.phase
kubectl -n lab-self-placement logs finished
kubectl -n lab-self-placement describe pod crash
kubectl -n lab-self-placement delete pod crash --wait=true
kubectl -n lab-self-placement run crash --image=busybox:1.37 --restart=Never -- sleep 3600
kubectl -n lab-self-placement wait --for=condition=Ready pod/crash --timeout=120s
```

finished는 Completed 표시와 Succeeded phase, crash는 반복 실패 뒤 CrashLoopBackOff 표시와 컨테이너 waiting reason을 비교한다. CrashLoopBackOff를 별도 Pod phase로 외우지 않는다. 복구한 crash는 새 UID이며 Running이다.

#### LimitRange 기본값과 거부 확인

QoS 초기 비교를 먼저 끝내고 다음을 실행한다.

```bash
kubectl apply -f k8s/03-pod-deep-dive/08-scheduling-troubleshooting/extended-limits.yaml
kubectl -n lab-self-placement get pod best -o jsonpath='{.status.qosClass}{"\n"}'
kubectl -n lab-self-placement run defaulted --image=busybox:1.37 --restart=Never -- sleep 3600
kubectl -n lab-self-placement get pod defaulted -o yaml
kubectl apply -f k8s/03-pod-deep-dive/08-scheduling-troubleshooting/extended-over.yaml
```

기존 best는 BestEffort로 남고 새 defaulted에는 request/limit 기본값이 채워진다. 마지막 Pod는 CPU max 300m을 넘겨 생성이 거부된다. 실제 Pod가 없으므로 scheduler Pending 장애와 다르다. 나머지 단계의 sleep/nginx Pod는 허용 범위 안의 자원을 사용한다.

#### Probe 실패와 복구

```bash
HEALTH_POD=$(kubectl -n lab-self-placement get pod -l app=health -o jsonpath='{.items[0].metadata.name}')
kubectl -n lab-self-placement exec "$HEALTH_POD" -- rm /tmp/ready
kubectl -n lab-self-placement wait --for=condition=Ready=false pod/"$HEALTH_POD" --timeout=60s
kubectl -n lab-self-placement get pod "$HEALTH_POD"
kubectl -n lab-self-placement get endpointslices -l kubernetes.io/service-name=health -o yaml
kubectl -n lab-self-placement exec "$HEALTH_POD" -- touch /tmp/ready
kubectl -n lab-self-placement wait --for=condition=Ready pod/"$HEALTH_POD" --timeout=120s
kubectl -n lab-self-placement exec "$HEALTH_POD" -- rm /tmp/live
kubectl -n lab-self-placement get pod "$HEALTH_POD" -w
```

readiness 실패가 반영되면 0/1이 되고 endpoint의 ready=false를 볼 수 있다. 이때 restartCount는 늘지 않는다. liveness 실패 뒤에는 같은 Pod의 restartCount가 늘고 시작 command가 파일을 다시 만들면서 Ready로 돌아온다. watch를 Ctrl+C로 종료한다. UID가 유지되는지도 확인한다.

#### 배치 실패와 복구

```bash
kubectl -n lab-self-placement patch deploy place --type=merge -p '{"spec":{"template":{"spec":{"nodeSelector":{"cloud-lab/missing":"true"}}}}}'
kubectl -n lab-self-placement get pods -l app=place
kubectl -n lab-self-placement get events --sort-by=.lastTimestamp
kubectl -n lab-self-placement patch deploy place --type=merge -p '{"spec":{"template":{"spec":{"nodeSelector":null}}}}'
kubectl -n lab-self-placement rollout status deploy/place --timeout=120s
```

일치하는 노드가 없어 새 Pod가 Pending에 남는다. 기존 Pod가 남아 있는 rolling 상태와 독립 Pod Pending을 구분한다. preferred는 우선순위이지 강제 조건이 아니다. [Node Affinity](../05-node-affinity/README.md)와 [Pod Affinity](../06-pod-affinity-antiaffinity/README.md)의 AND/OR·topology 설명을 읽는다.

#### taint/toleration 비교

이번 전용 key가 이미 있는 노드에서는 아래 변경을 하지 않는다. 기존 값이 없음을 먼저 확인하고, 학습 worker에서만 실행한다. NoSchedule은 기존 Pod를 퇴거시키지 않으므로 template annotation을 바꿔 새 Pod를 만든다.

```bash
PLACEMENT_NODE=$(kubectl -n lab-self-placement get pod -l app=place -o jsonpath='{.items[0].spec.nodeName}')
kubectl get node "$PLACEMENT_NODE" -o jsonpath='{.spec.taints}{"\n"}'
kubectl taint node "$PLACEMENT_NODE" cloud-lab/self-study=true:NoSchedule
kubectl -n lab-self-placement patch deploy place --type=merge -p '{"spec":{"template":{"metadata":{"annotations":{"study":"taint"}}}}}'
kubectl -n lab-self-placement get pods -l app=place
kubectl -n lab-self-placement get events --sort-by=.lastTimestamp
kubectl -n lab-self-placement patch deploy place --type=merge -p '{"spec":{"template":{"spec":{"tolerations":[{"key":"cloud-lab/self-study","operator":"Equal","value":"true","effect":"NoSchedule"}]}}}}}'
kubectl -n lab-self-placement rollout status deploy/place --timeout=120s
kubectl taint node "$PLACEMENT_NODE" cloud-lab/self-study:NoSchedule-
```

#### Quota와 Priority로 확장하기

[11 자원 예산](../../07-cka-preview/11-resource-budget/README.md)을 구축→힌트→복구→정리까지 실행한다. ReplicaSet FailedCreate와 이번 Pending을 비교한다. 이어 [12 PriorityClass](../../07-cka-preview/12-priorityclass/README.md)를 진행한다. 이 두 문서의 풀이를 첫 회에는 참고하고 두 번째에는 닫고 실행한다. 선점 실험은 그 문서의 전용 노드 조건을 따른다.

#### 누적 복습 — 다음 단계 전에

앞 단계의 개념을 현재 증상에 다시 연결한다. 문서를 닫고 세 질문에 답하며, 어려운 질문은 실제 spec/status/Events를 근거로 다시 설명한다.

1. FailedScheduling과 OOMKilled의 차이는?
2. request와 limit 중 배치에 직접 사용되는 값은?
3. Pod Ready와 Pod Scheduled가 다른 이유는?

관련 내부 심화를 할 경우 이 단계의 **namespace를 정리하기 전에** 진행한다. 개념만 읽을 때는 리소스 재생성을 강제하지 않는다.

#### 완료와 정리

Ready=false, Pending, OOMKilled, API Forbidden을 같은 문제로 취급하지 않고 첫 확인 대상을 말한다. 실제 OOM/노드 메모리 압박 주입은 이 단계에 필요하지 않다.

```bash
kubectl delete namespace lab-self-placement
rm -f /tmp/lab-self-placement.yaml
```

taint 원복 명령을 먼저 성공시킨다. 다음: [06 영속 저장소](../../05-advanced/01-statefulset/README.md).

[독립 학습 순서](../../README.md)
