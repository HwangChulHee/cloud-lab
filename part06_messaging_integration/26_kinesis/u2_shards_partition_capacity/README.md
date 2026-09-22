# u2. Shard / Partition / Ordering / Capacity

## 1. Shard

Provisioned mode에서 Stream의 처리 용량은 Shard 단위로 생각한다.

```text
Kinesis Stream
├─ Shard 1
├─ Shard 2
└─ Shard 3
```

강의에서는 각 Shard의 입력/출력 처리량 한도를 기준으로 필요한 shard 수를 계산하는 문제를 다룬다.

## 2. Partition Key

Producer가 Record를 넣을 때 Partition Key를 사용한다.

같은 Partition Key의 데이터는 같은 순서 흐름을 유지하도록 설계할 수 있다.

예:

```text
partition key = user-42

event 1
event 2
event 3
→ 같은 사용자 이벤트 순서 보장
```

강의는 같은 Partition ID의 데이터에 ordering guarantee가 있다고 설명한다.

## 3. Hot Partition 감각

특정 Partition Key에 데이터가 지나치게 몰리면 일부 shard에 부하가 집중될 수 있다.

```text
나쁜 key
partitionKey = "all-users"

좋은 방향
여러 key로 분산
```

시험에서는 보통 **Partition Key가 shard 분배와 ordering에 영향을 준다**는 점이 중요하다.

## 4. Capacity Mode

### Provisioned

```text
Shard 수 직접 선택
→ 처리량 직접 관리
→ 필요하면 resharding
```

강의 기준으로 shard당:

```text
입력 1 MB/s 또는 1000 records/s
출력 2 MB/s
```

### On-Demand

```text
Shard 수를 직접 관리하지 않음
자동 scaling
사용량 기반으로 capacity 대응
```

## SAA 판단

```text
예측 가능한 throughput + 직접 capacity 관리
→ Provisioned

traffic 변화가 크고 shard 관리 최소화
→ On-Demand
```
