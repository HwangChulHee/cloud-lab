# Lab 28 — Pod QoS

> 학습 단계: **중간 가이드**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/05-resources-scheduling/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

requests/limits 조합에 따른 QoS Class를 비교한다.

## 핵심 개념과 오해 방지

기본 컨테이너 자원 설정에서 Guaranteed는 모든 일반/init 컨테이너의 CPU와 memory에 request/limit이 모두 있고 각각 같은 경우다. BestEffort는 CPU/memory request/limit이 없으며 나머지는 Burstable이다. 하나의 컨테이너만 Guaranteed 조건을 만족한다고 Pod 전체가 Guaranteed가 되지는 않는다.

노드 압박 시 삭제 순서를 QoS 세 단계만으로 확정하지 않는다. kubelet은 압박 자원의 request 초과 사용 여부, Priority, request 대비 사용량 등을 고려한다. CPU는 보통 제한 초과 시 throttling하고 memory 제한 초과 시 컨테이너 OOMKilled가 발생할 수 있다. CPU를 많이 썼다는 이유로 memory 압박 퇴거와 동일하게 취급하지 않는다. 공용 클러스터에 실제 메모리 압박을 주입하지 않고 상태와 규칙을 비교한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. Guaranteed/Burstable/BestEffort Pod를 각각 만든다.
2. `status.qosClass`와 resources를 비교한다.
3. 노드 자원 압박 개념과 어떤 Pod가 더 보호되는지 정리한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. requests/limits 조합을 바꾼 새 Pod를 별도 이름으로 만들어 QoS를 비교한다. 기본 1.27 환경에서는 실행 중인 Pod의 resources를 직접 수정하지 않는다. 최신 resize 기능도 QoS 변경을 허용한다고 가정하지 않는다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. 세 QoS Class 조건을 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [PriorityClass와 스케줄링 우선순위](../../07-cka-preview/12-priorityclass/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
