# 38. Amazon Redshift

Amazon Redshift는 **OLAP / data warehousing**을 위한 analytics database다.

강의에서는 PostgreSQL 기반 SQL interface를 사용하지만 OLTP용으로 쓰지 않는다고 명확히 구분한다.

## Units

- [ ] [u1. OLAP / Cluster Architecture](./u1_olap_cluster_architecture/README.md)
- [ ] [u2. Loading / Spectrum](./u2_loading_spectrum/README.md)
- [ ] [u3. Snapshots / DR / Multi-AZ](./u3_snapshots_dr_multiaz/README.md)
- [ ] [u4. Athena와 비교 / SAA Selection](./u4_athena_comparison_selection/README.md)

## 핵심 특징

```text
OLAP / Analytics / Data Warehouse
Columnar Storage
Parallel Query Engine
SQL Interface
Provisioned Cluster or Serverless
BI Tools Integration
```

## 기본 구조

```text
Client / BI Tool
      ↓ JDBC/ODBC
Leader Node
      ↓
Compute Nodes
      ↓
Query Processing
```

## SAA 감각

```text
transaction DB
→ RDS/Aurora

large-scale analytics / joins / aggregations
→ Redshift

S3 files를 ad-hoc serverless SQL로 분석
→ Athena
```
