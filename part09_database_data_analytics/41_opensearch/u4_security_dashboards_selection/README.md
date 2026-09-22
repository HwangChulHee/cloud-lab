# u4. OpenSearch Security / Dashboards / SAA Selection

강의에서 OpenSearch security는 다음과 연결된다.

```text
Cognito
IAM
KMS encryption at rest
TLS in transit
```

## OpenSearch Dashboards

검색/분석 결과를 visualization하는 UI다.

```text
OpenSearch Data
      ↓
OpenSearch Dashboards
      ↓
Visualization
```

## SAA 선택 지도

```text
full-text search
→ OpenSearch

partial match
→ OpenSearch

DynamoDB item search 확장
→ DynamoDB Streams + Lambda + OpenSearch

CloudWatch Logs 검색/분석
→ Logs → Lambda/Firehose → OpenSearch

transactional relational DB
→ OpenSearch 아님

S3 serverless SQL
→ Athena
```

## 면접용 설명

> OpenSearch는 free-text와 flexible field search를 위한 검색 서비스이고, DynamoDB나 다른 database의 source of truth를 유지한 채 search index를 별도로 운영하는 패턴이 일반적입니다.
