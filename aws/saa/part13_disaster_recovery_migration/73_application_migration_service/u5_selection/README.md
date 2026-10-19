# u5. Migration 서비스 선택 지도

## Planning

```text
on-prem server inventory / utilization / dependency 파악
→ Application Discovery Service

migration 진행 정보 통합 확인
→ Migration Hub
```

## Server Migration

```text
기존 physical/virtual/cloud server를 AWS로 rehost
→ Application Migration Service (MGN)
```

## Disaster Recovery

```text
server를 continuous block-level replication하고
재해 시 AWS로 failover
→ Elastic Disaster Recovery (DRS)
```

## Database

```text
data migration / CDC
→ DMS

different DB engine schema conversion
→ SCT
```

## Data Transfer

```text
대규모 일회성 offline transfer
→ Snowball

대규모 ongoing sync
→ DataSync

ongoing DB replication
→ DMS

stable private network path
→ Direct Connect / VPN
```

## 최종 기억

> Discovery는 조사, MGN은 server rehost, DRS는 server DR, DMS는 DB data, SCT는 DB schema, Snowball/DataSync는 대량 data 이동 문제를 해결한다.
