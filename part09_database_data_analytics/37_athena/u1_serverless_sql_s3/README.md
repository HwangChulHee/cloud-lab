# u1. Athena — Serverless SQL on S3

Athena는 S3 파일에 대해 SQL query를 실행한다.

```text
CloudTrail Logs
ALB Logs
VPC Flow Logs
Application Data
      ↓
      S3
      ↓
    Athena
      ↓ SQL
Analysis / Reporting
```

서버나 cluster를 직접 만들 필요가 없다.

## 대표 사용 사례

```text
Business Intelligence
Analytics
Reporting
VPC Flow Logs 분석
ELB Logs 분석
CloudTrail Trail 분석
```

## SQL

표준 SQL 방식으로 파일을 조회한다.

중요한 점은 Athena가 일반 OLTP database가 아니라 **S3 data analytics** 용도라는 것이다.

## Athena vs RDS

```text
RDS
→ application transaction / OLTP

Athena
→ S3에 이미 있는 파일 분석
```

## 기억할 문장

> Athena는 S3에 저장된 데이터를 별도 DB/cluster로 적재하지 않고 serverless SQL로 분석할 때 사용하는 서비스다.
