# 39. Amazon EMR

Amazon EMR(Elastic MapReduce)은 **대규모 Big Data 처리용 managed cluster service**다.

강의에서는 Hadoop cluster를 손쉽게 만들고 Spark, HBase, Presto, Flink 등을 함께 사용할 수 있게 해주는 서비스로 설명한다.

## Units

- [ ] [u1. EMR Overview / Use Cases](./u1_emr_overview_use_cases/README.md)
- [ ] [u2. Node Types](./u2_node_types/README.md)
- [ ] [u3. Purchasing / Long-Running vs Transient](./u3_purchasing_cluster_lifecycle/README.md)
- [ ] [u4. SAA Selection](./u4_saa_selection/README.md)

## 기본 구조

```text
EMR Cluster
├─ Master Node
├─ Core Nodes
└─ Task Nodes (optional)
```

## 포함되는 대표 ecosystem

```text
Apache Hadoop
Apache Spark
HBase
Presto
Flink
```

## 대표 use case

```text
Big Data Processing
Machine Learning
Web Indexing
Large-scale ETL
```

## 핵심

```text
수백 EC2 instance 규모 cluster 가능
provisioning/configuration를 EMR이 관리
Auto Scaling 지원
Spot과 통합
```
