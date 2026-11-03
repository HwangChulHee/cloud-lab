# Lab 28 — Pod QoS

> 학습 단계: **중간 가이드**

## 실습 안내

이 README가 해당 주제의 공식 학습 자료다. **실습 전 상태 확인 → 리소스 구축 → 정상 증거 수집 → 제한된 장애 재현 → 복구 → 정리 → 인출 질문** 순서로 진행한다. 기존 독립 코스는 별도 진도로 계산하지 않는다.

## 목표

requests/limits 조합에 따른 QoS Class를 비교한다.

## 핵심 개념과 오해 방지

기본 컨테이너 자원 설정에서 Guaranteed는 모든 일반/init 컨테이너의 CPU와 memory에 request/limit이 모두 있고 각각 같은 경우다. BestEffort는 CPU/memory request/limit이 없으며 나머지는 Burstable이다. 하나의 컨테이너만 Guaranteed 조건을 만족한다고 Pod 전체가 Guaranteed가 되지는 않는다.

노드 압박 시 삭제 순서를 QoS 세 단계만으로 확정하지 않는다. kubelet은 압박 자원의 request 초과 사용 여부, Priority, request 대비 사용량 등을 고려한다. CPU는 보통 제한 초과 시 throttling하고 memory 제한 초과 시 컨테이너 OOMKilled가 발생할 수 있다. CPU를 많이 썼다는 이유로 memory 압박 퇴거와 동일하게 취급하지 않는다. 공용 클러스터에 실제 메모리 압박을 주입하지 않고 상태와 규칙을 비교한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

```bash
kubectl apply -f k8s/03-pod-deep-dive/04-qos/qos.yaml
kubectl -n lab-qos get pod -o wide
kubectl -n lab-qos get pod best burst guaranteed cpu-only -o custom-columns=NAME:.metadata.name,QOS:.status.qosClass
kubectl -n lab-qos describe pod guaranteed
kubectl -n lab-qos get pod cpu-only -o yaml
```

**예상:** best=BestEffort, burst=Burstable, guaranteed=Guaranteed, cpu-only=Burstable. CPU만 request=limit이라도 **메모리 request/limit가 없으므로** Guaranteed가 아니다.

## Break & Diagnose

QoS는 Pod spec의 리소스 정의로 결정되는 분류다. CPU limit에 도달하면 일반적으로 throttling이 발생하고, 메모리 limit을 넘으면 OOMKilled가 발생할 수 있다. Node MemoryPressure에 의한 Eviction과 다르다. 단순 QoS 순위만으로 축출 순서를 확정하지 않는다. 학습 클러스터 전체를 OOM으로 몰아넣지 않는다.

## Recover / Cleanup

잘못된 request/limit가 있을 경우 동일한 기존 Pod의 필드를 강제로 수정하는 대신 새 실험 Pod를 사용해 비교한다.

```bash
kubectl delete namespace lab-qos
```

## 완료 검증 / 설명하기

네 Pod의 resources와 status.qosClass를 근거로 분류를 설명한다. Guaranteed가 CPU만 설정해도 성립하는가? CPU throttling과 OOMKilled와 Evicted의 원인이 무엇인가? Priority가 Eviction에 미치는 영향은?
