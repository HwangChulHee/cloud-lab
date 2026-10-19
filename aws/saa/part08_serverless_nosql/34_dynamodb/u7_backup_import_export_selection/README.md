# u7. DynamoDB Backup / Import / Export / SAA Selection

## 1. PITR

강의에서는 Continuous Backup / Point-in-Time Recovery를 최근 35일 범위로 설명한다.

```text
PITR enabled
→ backup window 내 특정 시점 복구
→ 복구 시 새 Table 생성
```

## 2. On-Demand Backup

```text
full backup
long-term retention
직접 삭제할 때까지 유지
```

Backup 작업은 table performance/latency에 영향을 주지 않는 방향으로 설명한다.

AWS Backup을 통한 관리와 cross-region copy도 연결된다.

## 3. Export to S3

DynamoDB data를 S3로 export할 수 있다.

강의 핵심:

```text
PITR 필요
RCU 소비하지 않음
S3에서 Athena 분석 가능
```

## 4. Import from S3

S3의 CSV / DynamoDB JSON / ION 형식 데이터를 새 DynamoDB Table로 import할 수 있다.

```text
S3
 ↓ import
New DynamoDB Table
```

강의에서는 write capacity를 소비하지 않고 새 table을 만든다고 설명한다.

## 최종 선택 지도

```text
serverless NoSQL
→ DynamoDB

unpredictable traffic
→ On-Demand

predictable traffic
→ Provisioned + Auto Scaling

microseconds cache
→ DAX

item changes
→ Streams

multi-region active-active
→ Global Tables

automatic expiration
→ TTL

point-in-time recovery
→ PITR
```

## 면접용 설명

> DynamoDB는 serverless key-value/document database로 Partition Key 중심으로 데이터를 분산합니다. Capacity Mode, consistency, secondary index를 access pattern에 맞춰 선택하고, read hotspot은 DAX, change processing은 Streams, multi-region active-active는 Global Tables로 확장할 수 있습니다.
