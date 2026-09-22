# u1. AWS Lake Formation

AWS Lake Formation은 **Data Lake를 구축하고 관리하는 fully managed service**다.

강의에서는 Data Lake를 analytics를 위한 중앙 데이터 저장소로 설명한다.

## 역할

```text
S3
RDS
On-Premises DB
Relational / NoSQL
      ↓
Lake Formation
      ↓
Data Lake on S3
```

Lake Formation이 지원하는 작업:

```text
discover
cleanse
transform
ingest
catalog
de-duplicate
access control
```

## Glue와 관계

강의에서 Lake Formation은 **AWS Glue 위에 구축된 서비스**로 설명된다.

```text
Glue Crawlers
Glue ETL
Glue Data Catalog
      ↓
Lake Formation
      ↓
Data Lake + Centralized Security
```

## Fine-Grained Access Control

강의 핵심:

```text
row-level security
column-level security
centralized permissions
```

예:

```text
Athena User A
→ 특정 column만

QuickSight User B
→ 허용된 dataset만
```

## 소비 서비스

강의 diagram에서 다음이 연결된다.

```text
Athena
Redshift
EMR
QuickSight
```

## SAA 판단

```text
여러 source의 data lake를 빠르게 구축
→ Lake Formation

S3 data lake의 중앙 권한 관리
→ Lake Formation

ETL 자체
→ Glue
```
