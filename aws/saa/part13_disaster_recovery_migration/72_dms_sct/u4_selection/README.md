# u4. DMS + SCT 선택 기준

## 같은 Engine

```text
PostgreSQL → RDS PostgreSQL
Oracle → Oracle

Data Migration
→ DMS

Schema Conversion
→ 보통 SCT 불필요
```

## 다른 Engine

```text
Oracle → MySQL
SQL Server → Aurora
Teradata → Redshift

Schema
→ SCT

Data
→ DMS
```

## Migration 중 downtime 최소화

```text
source DB 계속 사용
+ 변경사항 계속 복제
→ DMS CDC
```

## DMS Multi-AZ

```text
migration replication instance의 HA 필요
→ DMS Multi-AZ
```

## 기억할 문장

> 같은 engine이면 DMS 중심, 다른 engine이면 SCT로 schema를 바꾸고 DMS로 data를 옮긴다.
