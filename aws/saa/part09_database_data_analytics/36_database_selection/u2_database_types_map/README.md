# u2. Database Type 전체 지도

강의의 Database Types 분류를 그대로 정리한다.

## RDBMS / OLTP

```text
RDS
Aurora
```

특징:

```text
SQL
transactions
joins
structured relational data
```

## NoSQL

```text
DynamoDB
ElastiCache
Neptune
DocumentDB
Keyspaces
```

강의는 이들을 RDBMS와 다른 NoSQL 계열 선택지로 묶는다.

## Object Store

```text
S3
Glacier
```

큰 object와 archive/backup에 사용한다.

## Data Warehouse / Analytics

```text
Redshift
Athena
EMR
```

OLTP가 아니라 분석/BI/대규모 처리 문제에 초점을 둔다.

## Search

```text
OpenSearch
```

free-text / unstructured search를 위해 사용한다.

## Graph

```text
Neptune
```

관계 중심 데이터에 사용한다.

## Ledger

```text
Amazon QLDB
```

강의의 Database Types에서는 Ledger database로 분류한다.

## Time Series

```text
Amazon Timestream
```

시간 흐름에 따라 계속 쌓이는 event/metric 데이터에 사용한다.
