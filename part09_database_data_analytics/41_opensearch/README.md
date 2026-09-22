# 41. Amazon OpenSearch Service

Amazon OpenSearch Service는 **검색과 분석**을 위한 managed service다.

강의에서는 DynamoDB 같은 database의 보완재로 자주 사용하며, primary key/index 기반 조회를 넘어 **임의 field, partial match, free-text search**가 필요할 때 선택한다.

## Units

- [ ] [u1. Search / Full-Text Use Case](./u1_search_fulltext_use_case/README.md)
- [ ] [u2. DynamoDB + OpenSearch Pattern](./u2_dynamodb_pattern/README.md)
- [ ] [u3. Logs / Kinesis Ingestion Patterns](./u3_logs_kinesis_ingestion/README.md)
- [ ] [u4. Security / Dashboards / SAA Selection](./u4_security_dashboards_selection/README.md)

## 핵심

```text
DynamoDB
→ primary key / index 중심 조회

OpenSearch
→ any field search
→ partial match
→ full-text / unstructured search
```

## Modes

강의에서는 두 mode를 설명한다.

```text
Managed Cluster
Serverless Cluster
```

## Ingestion

```text
Kinesis Data Firehose
AWS IoT
CloudWatch Logs
DynamoDB Streams + Lambda
```

## Visualization

```text
OpenSearch Dashboards
```

를 이용해 data를 시각화할 수 있다.
