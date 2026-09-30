# 12. PriorityClass와 스케줄링 우선순위

> 강의 전 예습 · 참고 주제: task-priorityclass · 환경: 기존 클러스터 / 선점 관찰은 전용 노드

기초 연결: [Scheduling](../../03-pod-deep-dive/08-scheduling-troubleshooting/README.md) · [QoS](../../03-pod-deep-dive/04-qos/README.md)

## 먼저 이해할 것

Priority는 스케줄링 우선순위이며 QoS와 다른 축이다. 높은 priority는 자원 부족 시 낮은 priority Pod를 선점할 수 있다. 항상 다른 Pod를 내쫓는 것은 아니다. 자료의 고정 999999999 대신 이 실습에서 만든 reference 클래스의 실제 값보다 1 작은 값을 계산한다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/12-priorityclass`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

```bash
kubectl apply -f setup.yaml
kubectl get priorityclass
kubectl -n preview-priority rollout status deploy/logger --timeout=120s
```

reference=900100, low=1000을 확인한다. 시스템 클래스의 값을 계산 기준에 넣지 않는다.

## 2. 직접 바꿔보기

1. preview-reference보다 1 작은 preview-high를 만든다.
2. logger Deployment의 Pod template에 priorityClassName을 반영한다.
3. rollout 후 Pod priority를 확인한다.

추가 관찰은 아래 힌트의 **전용 노드 선점 실험**으로 진행한다. 기본 실습에는 자원 부족이 없으므로 다른 Pod가 쫓겨나지 않는 것이 정상이다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

```bash
kubectl get pc preview-high -o yaml
kubectl -n preview-priority get pods -o custom-columns=NAME:.metadata.name,CLASS:.spec.priorityClassName,PRIORITY:.spec.priority
kubectl -n preview-priority rollout status deploy/logger --timeout=120s
```

value=900099, logger Pod의 class=preview-high, rollout 성공을 확인한다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

```bash
kubectl apply -f solution.yaml
kubectl -n preview-priority patch deploy logger --type=merge \
  -p '{"spec":{"template":{"spec":{"priorityClassName":"preview-high"}}}}'
```

### 선택: 전용 노드에서 선점 확인

다른 학습 워크로드가 없는 disposable worker에서만 한다. `kubectl describe node 노드명`으로 Allocatable과 이미 예약된 requests를 확인한다. 전용 hostname을 nodeSelector로 사용하고 낮은 priority filler와 높은 priority logger가 같은 노드만 선택하게 한다.

1. 가용 CPU 예산의 약 70%를 요청하는 `filler` Deployment를 preview-low로 실행한다. replicas=1이다.
2. logger를 replicas=0으로 낮추고 같은 노드에 예산의 약 50%를 요청하도록 수정한다. memory는 충분히 작게 유지한다.
3. logger replicas=1로 돌리고 Events를 관찰한다. 둘이 동시에 들어갈 수 없지만 logger 단독은 들어갈 수 있어야 한다.
4. filler가 선점되고 logger가 실행되는지, filler의 새 Pod가 Pending인지 확인한다.
5. filler를 삭제하고 logger requests를 원래 50m/32Mi로 되돌린다. nodeSelector도 제거한다.

노드 자원 자체를 초과하는 요청은 선점으로 해결되지 않는다. ResourceQuota로만 막은 상태도 이 실험을 대신하지 못한다. 다른 Deployment를 수정해서 공간을 만들지 않는다.

</details>

## 4. 정리 및 재실행

```bash
kubectl delete namespace preview-priority
kubectl delete pc preview-reference preview-low preview-high --ignore-not-found
```

시스템 PriorityClass와 다른 실습의 클래스는 유지한다.

## 강의에서 확인할 질문

- QoS와 Priority는 각각 어떤 판단에 쓰이는가?
- 높은 Priority Pod가 있어도 선점이 발생하지 않는 경우는?

[전체 예습 경로](../README.md)
