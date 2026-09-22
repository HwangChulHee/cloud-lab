# u3. Read Scaling / Caching

Read-heavy workload는 source database만 계속 키우는 대신 여러 계층에서 read를 줄일 수 있다.

```text
Client
 ↓
CloudFront Cache
 ↓
Application
 ↓
ElastiCache
 ↓
RDS Read Replica / Primary
```

## 계층별 역할

```text
CloudFront
→ edge에서 static/cacheable HTTP response

ElastiCache
→ application/database query cache

RDS Read Replica
→ relational DB read scaling

DAX
→ DynamoDB read acceleration
```

Cache는 stale data와 invalidation 전략을 반드시 함께 고려한다.
