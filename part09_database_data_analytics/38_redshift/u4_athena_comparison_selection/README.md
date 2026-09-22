# u4. Redshift vs Athena / SAA Selection

## Redshift

```text
OLAP warehouse
반복적인 BI workload
복잡한 joins / aggregations
columnar storage
parallel query
```

## Athena

```text
S3 data
serverless
ad-hoc SQL
scan-based cost
cluster 없음
```

강의는 Redshift가 Athena보다 **joins / aggregations 같은 반복 분석에서 더 빠른 선택**이 될 수 있다고 설명한다.

## 선택 지도

```text
PB-scale data warehouse
→ Redshift

BI dashboard의 핵심 warehouse
→ Redshift

S3 파일을 가끔 serverless query
→ Athena

Redshift에서 S3 data 직접 query
→ Spectrum

QuickSight
→ Athena/Redshift 등과 연동 가능
```

## 면접용 설명

> Redshift는 OLAP data warehouse라서 대규모 join, aggregation, 반복 BI workload에 적합하고, Athena는 S3 데이터를 별도 cluster 없이 serverless SQL로 ad-hoc 분석할 때 적합합니다.
