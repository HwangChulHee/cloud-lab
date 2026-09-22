# u6. DynamoDB Streams / Global Tables / TTL

## 1. DynamoDB Streams

Table Item의 변경을 ordered stream으로 기록한다.

```text
INSERT
UPDATE
DELETE
   ↓
DynamoDB Streams
   ↓
Lambda / Processing
```

강의 use case:

```text
welcome email
real-time analytics
derivative table
cross-region replication
Lambda trigger
```

강의에서는 DynamoDB Streams retention을 24시간으로 설명한다.

## 2. DynamoDB Streams vs Kinesis Data Streams

```text
DynamoDB Streams
→ 24h retention
→ limited consumers

Kinesis Data Streams for DynamoDB
→ 더 긴 retention
→ 더 많은 consumers
→ Kinesis ecosystem 연동
```

## 3. Global Tables

```text
Region A Table
   ↕ replication
Region B Table
```

특징:

```text
multi-region
active-active
각 Region에서 read/write
low latency global access
DynamoDB Streams 필요
```

## 4. TTL

Time To Live.

Item의 expiry timestamp를 기준으로 만료된 Item을 자동 삭제한다.

대표 사용:

```text
session data
temporary records
오래된 data 자동 정리
```

## SAA 판단

```text
item 변경 이벤트 처리
→ DynamoDB Streams

multi-region active-active
→ Global Tables

자동 데이터 만료
→ TTL
```
