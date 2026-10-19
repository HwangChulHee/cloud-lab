# u5. Analytics 서비스 최종 선택 지도

9부 Data & Analytics를 요구사항으로 정리한다.

## 저장 / 처리 / 분석 / 시각화

```text
Data Lake
→ S3 + Lake Formation

ETL / Metadata
→ Glue

S3 SQL
→ Athena

Data Warehouse / OLAP
→ Redshift

Big Data Cluster
→ EMR

Search
→ OpenSearch

BI Dashboard
→ QuickSight

Stream Processing
→ Managed Service for Apache Flink

Managed Kafka
→ Amazon MSK
```

## 대표 architecture

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

Streaming:

```text
Producer
   ↓
Kinesis Data Streams / MSK
   ↓
Managed Service for Apache Flink
   ↓
Processed Stream
```

## 최종 비교

| 요구사항 | 선택 |
|---|---|
| S3 data를 SQL로 ad-hoc 분석 | Athena |
| OLAP warehouse | Redshift |
| Hadoop/Spark cluster | EMR |
| ETL / Data Catalog | Glue |
| full-text / partial search | OpenSearch |
| Data Lake 구축 / 중앙 권한 | Lake Formation |
| BI / Dashboard | QuickSight |
| stream processing | Managed Service for Apache Flink |
| managed Apache Kafka | MSK |

## 기억할 문장

> Athena는 S3 SQL, Redshift는 warehouse, EMR은 big-data cluster, Glue는 ETL/catalog, OpenSearch는 search, Lake Formation은 data lake governance, QuickSight는 BI, MSK/Flink는 streaming 생태계다.
