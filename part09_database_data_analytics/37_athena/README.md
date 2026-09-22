# 37. Amazon Athena

Amazon Athena는 **Amazon S3에 저장된 데이터를 SQL로 분석하는 serverless query service**다.

강의의 시험 팁은 매우 직접적이다.

> S3의 데이터를 serverless SQL로 분석해야 한다면 Athena를 떠올린다.

## Units

- [ ] [u1. Serverless SQL on S3](./u1_serverless_sql_s3/README.md)
- [ ] [u2. Performance / Cost Optimization](./u2_performance_cost/README.md)
- [ ] [u3. Federated Query](./u3_federated_query/README.md)
- [ ] [u4. SAA Selection](./u4_saa_selection/README.md)

## 기본 구조

```text
S3
 ↓
Athena
 ↓ SQL
Query Result
 ↓
S3
```

QuickSight와 결합하면:

```text
S3 → Athena → QuickSight
            → Dashboard
```

## 지원 형식

강의에서는 다음을 언급한다.

```text
CSV
JSON
ORC
Avro
Parquet
```

## 비용 감각

강의에서는 **scan한 데이터 양 기준**으로 과금되는 구조를 설명한다.

따라서 데이터 형식/압축/partition이 성능뿐 아니라 비용에도 직접 연결된다.
