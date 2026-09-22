# u2. Amazon QuickSight

Amazon QuickSight는 **serverless BI / dashboard 서비스**다.

강의에서는 ML-powered business intelligence service로 설명한다.

## 대표 사용

```text
Business Analytics
Visualization
Ad-hoc Analysis
Dashboard
Business Insights
```

## Data Sources

강의에서 다음과 연동된다.

```text
RDS
Aurora
Athena
Redshift
S3
OpenSearch
Timestream
On-Premises JDBC
SaaS
```

## SPICE

QuickSight로 데이터를 import하면 **SPICE in-memory engine**을 사용할 수 있다.

```text
Data Source
   ↓ import
SPICE
   ↓
Fast Dashboard Query
```

## Analysis vs Dashboard

강의 구분:

```text
Analysis
→ visualization / filter / parameter 등을 편집하는 작업 영역

Dashboard
→ Analysis를 publish한 read-only snapshot
→ 공유 대상
```

Dashboard를 공유하려면 먼저 publish해야 한다.

## Users / Groups

강의에서는 QuickSight의 Users/Groups가 IAM 사용자/그룹과 같은 것이 아니라고 강조한다.

## Security

Enterprise Edition에서 Column-Level Security를 설정할 수 있다고 설명한다.

## SAA 판단

```text
BI dashboard / visualization
→ QuickSight

Athena query result 시각화
→ Athena + QuickSight

Redshift warehouse dashboard
→ Redshift + QuickSight
```
