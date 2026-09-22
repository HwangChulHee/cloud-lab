# u3. Athena Federated Query

Athena Federated Query는 S3뿐 아니라 여러 data source를 하나의 SQL query 흐름에 연결할 수 있게 한다.

## 구조

```text
Athena
  ↓
Lambda Data Source Connector
  ├→ RDS
  ├→ DynamoDB
  ├→ DocumentDB
  ├→ Redshift
  ├→ HBase on EMR
  ├→ CloudWatch Logs
  └→ On-Premises DB
```

강의에서는 Data Source Connector가 **AWS Lambda에서 실행**된다고 설명한다.

## 결과 저장

Query 결과는 S3에 저장할 수 있다.

## 언제 쓰나?

```text
S3 + RDS + DynamoDB 등
여러 source를 SQL로 함께 조회
→ Athena Federated Query
```

## 기억할 문장

> Athena Federated Query는 Lambda 기반 connector를 통해 AWS/on-premises의 다양한 source를 SQL query 대상으로 확장한다.
