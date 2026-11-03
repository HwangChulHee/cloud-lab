# Lab 32 — Scheduling Troubleshooting

> 학습 단계: **중간 가이드**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/05-resources-scheduling/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

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

Scheduler는 `kubectl top`의 실시간 CPU가 가장 낮은 노드를 단순 선택하지 않는다. CPU limit 초과 시 throttling과 메모리 초과 시 OOMKilled, NodePressure Eviction을 구별한다. QoS 외에도 requests 초과 사용과 Priority가 eviction 판단에 영향을 미칠 수 있다. 독립 추가 실습을 새로 만들기보다는 Lab 25–32에서 얻은 결과를 이곳에 종합한다. [내부 참고](../../09-internals/05-scheduler-eviction/README.md).
