# 11. 자원 예산을 계산해 3개 Pod 복구하기

> 강의 전 예습 · 참고 주제: task-resource · 환경: 기존 클러스터

기초 연결: [Requests/Limits](../../01-core-objects/03-node-scheduling-resources/README.md) · [Quota/LimitRange](../../01-core-objects/14-resourcequota-limitrange/README.md) · [Scheduling 진단](../../03-pod-deep-dive/08-scheduling-troubleshooting/README.md)

## 먼저 이해할 것

requests는 스케줄링과 quota 계산에 쓰이며 실제 사용량(top)과 다르다. 이 실습은 namespace quota를 작은 자원 예산으로 사용해 다른 학습 Pod를 압박하지 않는다. 일반 순차 init container의 요청량은 합산이 아니라 최대 init 요청과 일반 컨테이너 요청 합계 중 큰 값으로 계산한다. 이 Pod는 각각 1개라 같은 요청값을 쓰면 그 값이 유효 요청이다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/11-resource-budget`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

```bash
kubectl apply -f setup.yaml
kubectl -n preview-budget get deploy,rs,pods
kubectl -n preview-budget describe quota budget
kubectl -n preview-budget get events --sort-by=.lastTimestamp
kubectl describe nodes
```

quota 때문에 3개가 모두 생성되지 못한다. 노드 자원 부족의 Pending과 달리 ReplicaSet의 FailedCreate/exceeded quota를 볼 수 있다.

## 2. 직접 바꿔보기

총 CPU 1200m, 메모리 768Mi 예산에서 3개 Pod에 같은 requests를 준다. 예산의 10% 이상을 여유로 남긴다. 일반 container와 init container의 requests는 같게, limits는 유지한다.

변경 중 rollout의 추가 Pod가 예산을 초과하지 않도록 replicas=0으로 잠시 낮추거나 Recreate를 사용한다. 마지막에는 replicas=3이어야 한다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

```bash
kubectl -n preview-budget get deploy app
kubectl -n preview-budget get pods
kubectl -n preview-budget describe quota budget
kubectl -n preview-budget get deploy app -o yaml
```

3개 Ready, 일반/init requests 일치, 기존 limits 유지, quota 10% 이상 여유를 확인한다. 실제 노드 부족이면 quota 외에 Allocatable과 기존 requests도 함께 확인한다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

10% 여유 기준으로 Pod당 CPU 상한은 360m, 메모리는 약 230Mi다. 예시는 350m/224Mi다.

```bash
kubectl -n preview-budget scale deploy app --replicas=0
kubectl -n preview-budget wait --for=delete pod -l app=app --timeout=120s
kubectl apply -f solution.yaml
kubectl -n preview-budget rollout status deploy/app --timeout=120s
```

실제 노드에서는 `Allocatable - 기존 Pod requests - 여유분`을 나눠 계산한다. 강의 풀이의 400m/400Mi를 모든 환경의 정답으로 사용하지 않는다.

</details>

## 4. 정리 및 재실행

```bash
kubectl delete namespace preview-budget
```

## 강의에서 확인할 질문

- quota 초과와 노드 자원 부족은 어느 리소스의 Events에서 차이가 나는가?
- 순차 init 컨테이너 요청을 일반 컨테이너처럼 모두 더하면 왜 부정확한가?

[전체 예습 경로](../README.md)
