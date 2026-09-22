# u3. Database / Cache Scaling

Stateful application의 data tier에서는 **Read Scaling, Cache, HA**를 구분한다.

## RDS Read Replica

```text
RDS Primary
  ├→ Write
  └→ Replication → Read Replica
```

Read traffic을 분산한다.

## ElastiCache Lazy Loading

```text
Application
   ↓ read
ElastiCache
   ├─ hit → 응답
   └─ miss
        ↓
       RDS
        ↓
   cache에 저장
```

강의에서는 cache invalidation 전략이 필요하다고 강조한다.

## Multi-AZ

```text
RDS Multi-AZ
→ High Availability / failover

Read Replica
→ Read scaling
```

둘을 목적 기준으로 섞지 않는다.

## 기억할 문장

> Read Replica는 읽기 확장, ElastiCache는 반복 읽기 감소, Multi-AZ는 DB 가용성이다.
