# u1. AWS Database Migration Service

AWS DMS(Database Migration Service)는 database를 AWS로 또는 AWS 환경 사이에서 **빠르고 안전하게 migration / replication**하는 서비스다.

강의 핵심:

```text
resilient
self-healing
source database remains available during migration
homogeneous migration 지원
heterogeneous migration 지원
continuous replication with CDC
```

## Homogeneous Migration

같은 database engine끼리 migration한다.

```text
Oracle → Oracle
PostgreSQL → RDS PostgreSQL
```

이 경우 schema 구조가 동일 계열이므로 SCT가 필요하지 않을 수 있다.

## Heterogeneous Migration

다른 database engine으로 이동한다.

```text
Microsoft SQL Server → Aurora
Oracle → MySQL / PostgreSQL 계열
```

이 경우 data 이동은 DMS, schema 변환은 SCT를 조합한다.

## 기억할 문장

> DMS의 역할은 database data를 옮기거나 지속 복제하는 것이다.
