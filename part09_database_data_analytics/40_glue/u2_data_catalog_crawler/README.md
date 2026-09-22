# u2. Glue Data Catalog / Crawler

## Data Catalog

Data Catalog는 dataset의 **metadata catalog**다.

```text
S3
RDS
DynamoDB
JDBC Sources
   ↓
Glue Data Catalog
   ├─ Database Metadata
   └─ Table Metadata
```

실제 데이터를 저장하는 곳이 아니라 **데이터가 어디에 있고 어떤 schema인지 설명하는 metadata**를 관리한다.

## Crawler

Glue Crawler가 source를 탐색해 schema를 발견하고 Catalog에 metadata를 기록한다.

```text
Data Source
   ↓
Glue Crawler
   ↓
Data Discovery
   ↓
Glue Data Catalog
```

## Catalog를 사용하는 서비스

강의에서 다음을 연결한다.

```text
Athena
Redshift Spectrum
EMR
Glue Jobs
```

## 핵심

```text
Crawler
→ schema discovery

Data Catalog
→ metadata repository

Athena / Redshift Spectrum
→ Catalog metadata 활용
```
