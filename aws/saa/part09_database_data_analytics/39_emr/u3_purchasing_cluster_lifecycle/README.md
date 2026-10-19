# u3. EMR Purchasing / Cluster Lifecycle

강의는 EMR Node의 구매 옵션을 EC2와 연결해서 설명한다.

## On-Demand

```text
reliable
predictable
중간에 회수되지 않음
```

## Reserved

```text
장기 사용
cost savings
```

강의에서는 EMR이 사용 가능한 Reserved capacity를 자동으로 활용한다고 설명한다.

## Spot

```text
저렴함
중단 가능
Task Node에 특히 적합
```

## Long-Running Cluster

항상 존재하는 cluster.

지속적인 big-data workload에 적합하다.

## Transient Cluster

필요할 때 생성해 작업을 마치고 종료하는 temporary cluster.

```text
Job 시작
→ EMR Cluster 생성
→ Processing
→ 결과 저장
→ Cluster 종료
```

## SAA 판단

```text
중단되어도 되는 추가 compute
→ Spot Task Node

지속적/안정적 node
→ On-Demand 또는 Reserved 고려

일회성 batch
→ Transient Cluster
```
