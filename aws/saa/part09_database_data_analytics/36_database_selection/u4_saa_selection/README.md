# u4. Database SAA 선택 기준

```text
SQL / OLTP / Join
→ RDS / Aurora

serverless key-value / document-like NoSQL
→ DynamoDB

in-memory cache
→ ElastiCache

MongoDB-compatible managed DB
→ DocumentDB

Graph relationships
→ Neptune

Cassandra-compatible
→ Keyspaces

Time-series
→ Timestream

Object / archive
→ S3 / Glacier

Data warehouse / OLAP
→ Redshift

S3 data를 serverless SQL로 분석
→ Athena

Hadoop / Spark / big-data processing cluster
→ EMR

Free-text / partial-match search
→ OpenSearch
```

## 기억할 문장

> Database 선택은 product 이름 암기가 아니라 data model, query pattern, latency, scale, consistency, analytics 요구를 먼저 분류하는 문제다.
