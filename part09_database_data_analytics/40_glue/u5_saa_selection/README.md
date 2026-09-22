# u5. Glue SAA Selection

```text
serverless ETL
→ Glue

schema 자동 발견
→ Glue Crawler

metadata catalog
→ Glue Data Catalog

CSV → Parquet
→ Glue ETL

Athena / Redshift Spectrum table metadata
→ Glue Data Catalog

이전 처리 data 재처리 방지
→ Job Bookmark

Kinesis/Kafka stream transformation
→ Glue Streaming ETL
```

## Glue vs EMR

```text
Glue
→ managed/serverless ETL 중심

EMR
→ Spark/Hadoop 등 big-data framework cluster
```

## 면접용 설명

> Glue는 serverless ETL과 metadata catalog를 함께 제공하고, Crawler로 schema를 발견해 Data Catalog에 저장하며 Athena나 Redshift Spectrum 같은 analytics 서비스가 그 metadata를 사용할 수 있습니다.
