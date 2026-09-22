# 36. AWS Database 선택 지도

AWS에는 데이터 모델과 접근 방식이 다른 여러 관리형 데이터 서비스가 있다.

강의에서는 특정 서비스 이름부터 외우기보다 먼저 다음 질문으로 요구사항을 분류한다.

## Units

- [ ] [u1. Database 선택 질문](./u1_selection_questions/README.md)
- [ ] [u2. Database Type 전체 지도](./u2_database_types_map/README.md)
- [ ] [u3. Specialized Databases](./u3_specialized_databases/README.md)
- [ ] [u4. SAA 선택 기준](./u4_saa_selection/README.md)

## 먼저 물어볼 것

```text
Read-heavy / Write-heavy / Balanced?
Throughput은 얼마나 필요한가?
Traffic이 변동하는가?

얼마나 많은 데이터를 얼마나 오래 저장하는가?
Latency 요구는?
동시 사용자는?

Data model은?
Joins가 필요한가?
Structured / Semi-structured / Unstructured?

Reporting / Search / OLTP / OLAP?
Strong schema가 필요한가?
```

## 전체 지도

```text
Relational / OLTP
→ RDS / Aurora

NoSQL
→ DynamoDB
→ DocumentDB
→ Keyspaces
→ Neptune

Cache
→ ElastiCache

Object Store
→ S3 / Glacier

Data Warehouse / Analytics
→ Redshift
→ Athena
→ EMR

Search
→ OpenSearch

Graph
→ Neptune

Ledger
→ QLDB

Time Series
→ Timestream
```

## 가장 중요한 습관

```text
"어떤 DB가 제일 좋은가?"
X

"이 workload의 data model / query / latency / scale 요구에
어떤 DB가 맞는가?"
O
```
