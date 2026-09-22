# u3. DynamoDB Capacity Modes / Consistency

## 1. Provisioned Mode

강의에서는 기본 capacity mode로 설명한다.

사용자가 미리 처리량을 지정한다.

```text
RCU = Read Capacity Units
WCU = Write Capacity Units
```

특징:

```text
예측 가능한 traffic
capacity planning 필요
Auto Scaling 가능
provisioned RCU/WCU에 비용
```

## 2. On-Demand Mode

```text
read/write 자동 scale
capacity planning 불필요
사용량 기반 비용
traffic 급변에 적합
```

강의에서는 Provisioned보다 단가가 더 비쌀 수 있지만 unpredictable workload에 적합하다고 설명한다.

## 3. Consistency

DynamoDB read에서는 consistency 선택을 구분한다.

```text
Eventually Consistent Read
→ 최신 write가 즉시 보이지 않을 수 있음
→ 일반적으로 더 효율적

Strongly Consistent Read
→ 최신 값을 보장하는 방향
→ 비용/제약 차이 고려
```

## 4. Write

write는 WCU와 연결된다.

시험에서는 Item size와 read/write 유형에 따라 capacity 계산 문제로 연결될 수 있다.

## SAA 판단

```text
traffic이 안정적 / 예측 가능
→ Provisioned

traffic이 갑자기 크게 바뀜
→ On-Demand

최신 값 즉시 필요
→ Strongly Consistent Read 고려
```
