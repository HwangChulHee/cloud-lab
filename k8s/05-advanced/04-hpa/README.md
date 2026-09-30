# Lab 41 — Horizontal Pod Autoscaler

> 학습 단계: **가이드 축소**

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

## 연결된 CKA 강의 전 예습

- [HPA와 축소 안정화 시간](../../07-cka-preview/02-hpa-behavior/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
