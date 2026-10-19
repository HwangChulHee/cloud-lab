# u5. DynamoDB Accelerator (DAX)

DAX는 DynamoDB 전용 **fully managed in-memory cache**다.

## 구조

```text
Application
    ↓
DAX Cluster
    ↓
DynamoDB
```

## 강의 핵심

```text
highly available
in-memory cache
microseconds latency
DynamoDB API compatible
application logic 변경 최소화
default cache TTL 5 minutes
```

## 언제 필요한가?

```text
DynamoDB read congestion
→ DAX

같은 item / query 반복 read
→ DAX
```

## DAX vs ElastiCache

강의 비교:

```text
DAX
→ DynamoDB individual object
→ Query / Scan cache

ElastiCache
→ aggregation result 등 application-level cache
```

즉 DynamoDB 자체 read path를 가속하는 목적이면 DAX가 자연스럽다.

## SAA 판단

```text
DynamoDB read latency를 microseconds 수준으로 낮춤
→ DAX

복잡한 aggregation 결과 cache
→ ElastiCache 고려
```
