# u4. Global Data / Caching Selection

Global architecture에서는 **compute 위치뿐 아니라 data와 cache 위치**를 같이 본다.

## Global Data

```text
DynamoDB Global Tables
→ multi-region active-active data

Aurora Global Database
→ primary Region + secondary Regions
```

## Cache Layers

강의의 caching strategy 예시:

```text
CloudFront
→ edge HTTP/content cache

API Gateway Cache
→ API response cache

ElastiCache Redis/Memcached
→ application data / session cache

DAX
→ DynamoDB cache
```

## 판단

```text
전 세계 static/content delivery
→ CloudFront

DynamoDB read microsecond cache
→ DAX

RDS query/session cache
→ ElastiCache

반복 API response
→ API Gateway Cache
```

## 기억할 문장

> Global architecture에서 latency를 줄이려면 사용자와 가까운 delivery/cache 계층과 data replication 전략을 함께 설계한다.
