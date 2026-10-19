# u4. Athena SAA 선택 기준

```text
S3 data를 SQL로 분석
→ Athena

serverless analytics
→ Athena

VPC Flow Logs / ALB Logs / CloudTrail 분석
→ S3 + Athena

scan 비용 절감
→ Parquet/ORC + Compression + Partition

CSV/JSON을 columnar format으로 변환
→ Glue

여러 data source를 Athena SQL로 조회
→ Federated Query
```

## Athena vs Redshift

```text
Athena
→ S3 위 serverless ad-hoc query
→ cluster 없음

Redshift
→ OLAP data warehouse
→ 반복적 join / aggregation / BI workload
```

## 면접용 설명

> Athena는 S3 데이터를 SQL로 바로 분석하는 serverless query service이고, 비용은 scan한 데이터 양에 영향을 받기 때문에 Parquet/ORC, compression, partitioning이 중요합니다.
