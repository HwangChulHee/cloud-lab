# 09부 — Databases, Data & Analytics

SAA의 **Databases in AWS / Data & Analytics** 영역을 정리한다.

이 파트의 핵심은 서비스 이름을 따로 외우는 것이 아니라 **어떤 data model과 분석 요구에 어떤 서비스를 선택하는지** 구분하는 것이다.

## Chapters

- [ ] [36. AWS Database 선택 지도](./36_database_selection/README.md)
- [ ] [37. Athena](./37_athena/README.md)
- [ ] [38. Redshift](./38_redshift/README.md)
- [ ] [39. EMR](./39_emr/README.md)
- [ ] [40. Glue](./40_glue/README.md)
- [ ] [41. OpenSearch](./41_opensearch/README.md)
- [ ] [42. Lake Formation / QuickSight / MSK 등](./42_lakeformation_quicksight_msk/README.md)

## Database 선택 전체 지도

```text
OLTP / SQL / Join
→ RDS / Aurora

NoSQL
→ DynamoDB
→ DocumentDB
→ Keyspaces
→ Neptune

Cache
→ ElastiCache

Object / Archive
→ S3 / Glacier

OLAP / Data Warehouse
→ Redshift

S3 Serverless SQL
→ Athena

Big Data Processing
→ EMR

Search
→ OpenSearch

Graph
→ Neptune

Time Series
→ Timestream
```

## Analytics 전체 지도

```text
Data Sources
   ↓
Glue / Lake Formation
   ↓
S3 Data Lake
   ├→ Athena
   ├→ Redshift Spectrum
   ├→ EMR
   └→ QuickSight
```

Streaming 쪽은:

```text
Producer
   ↓
Kinesis Data Streams / Amazon MSK
   ↓
Managed Service for Apache Flink
   ↓
Real-Time Processing
```

## 먼저 구분할 것

```text
Athena
→ S3 위 serverless SQL

Redshift
→ OLAP data warehouse

EMR
→ Hadoop / Spark cluster

Glue
→ serverless ETL + Data Catalog

OpenSearch
→ full-text / partial search

Lake Formation
→ Data Lake 구축 / 중앙 권한 관리

QuickSight
→ BI / Dashboard

MSK
→ managed Apache Kafka

Managed Service for Apache Flink
→ stream processing
```

## 학습 순서

```text
36 Database 선택 지도
      ↓
37 Athena
S3 SQL
      ↓
38 Redshift
OLAP / Warehouse
      ↓
39 EMR
Big Data Cluster
      ↓
40 Glue
ETL / Catalog
      ↓
41 OpenSearch
Search
      ↓
42 Lake Formation / QuickSight / MSK / Flink
Data Lake / BI / Streaming
```

## 시험에서 특히 중요한 비교

```text
RDS/Aurora
vs
DynamoDB

Athena
vs
Redshift

Athena
vs
EMR

Glue
vs
EMR

OpenSearch
vs
Database Query

Kinesis Data Streams
vs
Amazon MSK

Amazon Data Firehose
vs
Managed Service for Apache Flink
```

## 학습 깊이

이 파트는 현재 **Coverage 중심**이다.

즉 모든 서비스를 직접 구축하는 것보다:

```text
무슨 문제를 해결하는가?
어떤 keyword가 나오면 선택하는가?
어떤 서비스와 헷갈리는가?
```

에 먼저 답할 수 있어야 한다.

현재 `examples/01~16`의 필수 선행조건은 아니며, 이후 portfolio나 analytics 관련 실습이 필요할 때 특정 서비스를 더 깊게 확장한다.
