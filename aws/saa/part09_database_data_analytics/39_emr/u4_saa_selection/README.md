# u4. EMR SAA Selection

```text
Hadoop/Spark cluster 필요
→ EMR

대규모 distributed data processing
→ EMR

Spark / HBase / Presto / Flink
→ EMR

ad-hoc S3 SQL
→ Athena

OLAP warehouse
→ Redshift
```

## Cost / Scale

```text
Task Node
→ Spot으로 비용 절감 가능

Cluster size
→ Auto Scaling

일회성 batch
→ Transient Cluster
```

## 면접용 설명

> EMR은 Hadoop/Spark 같은 Big Data framework를 AWS에서 managed cluster 형태로 실행하는 서비스이며, Master/Core/Task node를 나눠 운영하고 Spot/Auto Scaling을 이용해 비용과 처리량을 조정할 수 있습니다.
