# Lab 41 — Horizontal Pod Autoscaler

> 학습 단계: **가이드 축소**

## 강의 없이 시작하기

이 README가 이 주제의 **공식 학습·실습 기록**입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [이전 독립 코스의 추가 실행 자산](../../05-advanced/03-ingress-canary-tls/README.md)은 고유 예제나 YAML이 필요할 때 참고하며 별도로 중복 완료하지 않습니다.

## 목표

Metrics를 기반으로 replicas가 자동 조절되는 과정을 확인한다.

## 계산과 확장 범위를 구분하기

CPU `1000m`은 1 CPU이며 `m`은 밀리초가 아니다. CPU request `100m`인 Pod가 `50m`을 쓰면 사용률은 50%다. HPA의 `averageUtilization`은 request 대비 사용률이고, `averageValue`는 절대 평균 사용량이다.

단순화한 추천식은 `ceil(현재 replicas × 관측값 / 목표값)`이다. Pod 1개, request 100m, 사용량 200m, 목표 50%라면 사용률 200%이므로 추천값은 4개다. 실제 결정에는 tolerance, metrics 누락, readiness, min/max와 behavior가 추가로 반영된다. 추천값이 4라고 4개가 즉시 Ready가 되는 것은 아니다.

| 방식 | 바꾸는 대상 | 이 환경에서의 조건 |
|---|---|---|
| HPA | workload의 replicas | Metrics Server 또는 해당 metrics API, 새 Pod를 배치할 자원 |
| VPA | 컨테이너의 자원 requests 중심 | 별도 애드온, 버전·정책에 따른 Pod 재생성/resize 동작 확인 |
| 노드 자동 확장 | 노드 수/용량 | 인프라와 연동하는 별도 구현; Vagrant VM은 HPA로 자동 증설되지 않음 |

VPA와 HPA를 함께 쓸 때 같은 CPU/memory를 양쪽이 조정하면 사용률의 분모와 replicas가 동시에 바뀔 수 있다. 공존 방식을 별도로 설계한다. HTTP 부하가 CPU를 늘렸다고 memory 사용량도 지속적으로 늘어나는 것은 아니므로 memory HPA 비교에는 메모리 사용 특성이 분명한 앱이 필요하다.

관찰 기록은 `request → 실제 사용량 → HPA target/current → desired replicas → Ready replicas → Pending Events` 순서로 남긴다. `kubectl top`은 최근 사용량이고 scheduler는 배치 판단에서 requests를 사용한다.

참고: [HPA 알고리즘](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/), [워크로드 자동 확장](https://kubernetes.io/docs/concepts/workloads/autoscaling/), [VPA와 HPA 병용 조건](https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/known-limitations.md).

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. Metrics Server와 `kubectl top`을 확인한다.
2. requests가 있는 Deployment+Service를 만든다.
3. CPU HPA를 만들고 부하를 발생시켜 scale-out/in을 관찰한다.
4. Memory 기준 HPA도 비교한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 관찰할 자원(CPU 또는 memory)의 request와 limit을 모두 제거하고 rollout 완료 후 실제 Pod resources를 확인한다. limit만 남기면 request가 limit 값으로 자동 주입될 수 있다. LimitRange의 기본값도 확인한다.
2. HPA의 utilization metric 계산 오류를 Conditions/Events에서 확인한다. 평균 사용량(AverageValue) 방식은 request 기반 사용률과 구분한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. HPA가 어떤 값으로 desired replicas를 바꾸는지 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [HPA와 축소 안정화 시간](../../07-cka-preview/02-hpa-behavior/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.


## 실행형 Lab — Metrics → HPA → Scale-Out/In

기존 Vagrant 클러스터에서 [Metrics Server](../../guides/ADDONS.md#metrics-server)가 정상인지 먼저 확인한다. `kubectl top nodes`가 실패하면 HPA 문제로 결론 내리기 전에 metrics 수집을 점검한다.

```bash
kubectl top nodes
kubectl get apiservice v1beta1.metrics.k8s.io
kubectl apply -f k8s/05-advanced/04-hpa/hpa.yaml
kubectl -n lab-hpa rollout status deploy/php-apache --timeout=180s
kubectl -n lab-hpa get hpa,deploy,pods
kubectl -n lab-hpa describe hpa php-apache
```

**예상:** cpu utilization `current/50%`를 표시하고 minReplicas=1, maxReplicas=5다. Metrics 수집 시점 때문에 초기에 `unknown`이 나올 수 있으니 Conditions/Events와 `kubectl top pods`로 구분한다.

### 부하 주입과 관측

```bash
kubectl apply -f k8s/05-advanced/04-hpa/load.yaml
kubectl -n lab-hpa get pods
kubectl -n lab-hpa get hpa,deploy -w
# 현재 사용률, desired replicas, 실제 Ready 변화를 관찰 후 Ctrl+C
kubectl -n lab-hpa describe hpa php-apache
kubectl -n lab-hpa top pods
```

**예상:** CPU 부하가 충분하면 HPA가 Deployment replicas를 늘리고 ReplicaSet이 Pod를 생성한다. 부하·Metrics 수집 주기·스케줄 자원에 따라 **정확한 replica 수와 시점은 달라진다**. Pod가 Pending이면 HPA가 아니라 Scheduler의 자원/배치 실패일 수 있다. Load Pod는 CPU limit를 갖춰 노드 전체에 과도한 부하를 주지 않게 했다.

### 복구 및 축소

```bash
kubectl -n lab-hpa delete pod load --wait=true
kubectl -n lab-hpa get hpa,deploy
kubectl -n lab-hpa describe hpa php-apache
```

HPA scale-down은 기본 안정화 창 때문에 지연될 수 있다. 스케일 다운 완료까지의 대기와 Metrics 목표치를 기록한다. Scale-out이 관찰되지 않으면 `kubectl top pods`, HPA Conditions, request와 실제 CPU 부하를 확인한 후 판단한다. 정상 동작을 확인하기 위해 사용자가 `kubectl scale deploy`로 수동 replica 수를 강제하지 않는다.

## 장애 분석: CPU request 누락

[CKA 확장 02](../../07-cka-preview/02-hpa-behavior/README.md)는 request 없는 경우의 `ScalingActive` 오류, HPA 안정화 행동을 **별도의 시험형 문제**로 연습한다. 이 Lab에서는 CPU request와 Metrics API가 존재하는 정상 HPA 시나리오에 집중한다.

## Cleanup / 인출

```bash
kubectl delete namespace lab-hpa
```

CPU request 200m와 사용량 100m이면 utilization은 몇 %인가? 1개의 현재 Pod가 사용률 200%, 목표 50%일 때 단순화된 추천 replica 수는? HPA, VPA, 노드 자동 확장은 각각 무엇을 조절하는가?
