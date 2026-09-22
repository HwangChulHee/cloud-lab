# u1. EMR Overview / Use Cases

EMR은 대규모 데이터를 처리하기 위한 cluster를 쉽게 구성한다.

```text
Huge Dataset
   ↓
EMR Cluster
   ↓
Spark / Hadoop / Presto / Flink
   ↓
Processed Result
```

강의는 EMR이 provisioning과 configuration을 대신 관리한다고 설명한다.

## Use Cases

```text
data processing
machine learning
web indexing
big data analytics
```

## Athena와 차이 감각

```text
Athena
→ S3 SQL query
→ serverless
→ ad-hoc 분석

EMR
→ 직접 big-data framework 실행
→ cluster 기반
→ Spark/Hadoop/Flink 등
```

## 기억할 문장

> EMR은 Hadoop/Spark 계열 Big Data framework를 AWS의 managed EC2 cluster에서 실행할 때 사용하는 서비스다.
