# u1. Redshift OLAP / Cluster Architecture

## 1. OLAP

Redshift는 OLTP가 아니라 **Online Analytical Processing**에 사용한다.

```text
OLTP
→ 주문 생성 / 계좌 변경 / transaction
→ RDS / Aurora

OLAP
→ 대량 데이터 집계 / 분석 / BI
→ Redshift
```

## 2. Columnar Storage

row 단위보다 column 단위 분석에 유리한 columnar storage를 사용한다.

대량 aggregation에서 효율적이다.

## 3. Parallel Query Engine

여러 Compute Node가 query를 병렬 처리한다.

## 4. Leader Node

```text
Query
 ↓
Leader Node
→ query planning
→ 결과 aggregation
 ↓
Compute Nodes
→ 실제 query 처리
```

## 5. Modes

강의에서는 두 가지 mode를 구분한다.

```text
Provisioned Cluster
→ instance type 직접 선택
→ reserved instance로 비용 절감 가능

Redshift Serverless
→ cluster capacity 관리 부담 감소
```

## 기억할 문장

> Redshift는 대량 분석과 BI를 위한 columnar OLAP warehouse이고, transaction processing database가 아니다.
