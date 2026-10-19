# u3. AWS Schema Conversion Tool

AWS SCT(Schema Conversion Tool)는 **database schema를 한 engine에서 다른 engine 형식으로 변환**한다.

## 예시

강의에서 다음을 예로 든다.

```text
OLTP
SQL Server / Oracle
→ MySQL / PostgreSQL / Aurora

OLAP
Teradata / Oracle
→ Amazon Redshift
```

## 언제 필요한가?

```text
Source Engine ≠ Target Engine
→ SCT 고려
```

예:

```text
Oracle → Aurora PostgreSQL
→ schema conversion 필요
```

## 언제 필요하지 않은가?

강의 예:

```text
On-Premises PostgreSQL
→ RDS PostgreSQL
```

DB engine 자체가 PostgreSQL로 동일하기 때문에 SCT가 필요하지 않는다.

## DMS와 역할 분리

```text
SCT
→ Schema Conversion

DMS
→ Data Migration / Replication
```

## 기억할 문장

> SCT는 데이터를 옮기는 서비스가 아니라 database engine이 달라질 때 schema를 변환하는 도구다.
