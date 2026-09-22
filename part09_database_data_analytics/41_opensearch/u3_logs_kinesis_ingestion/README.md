# u3. OpenSearch Logs / Kinesis Ingestion Patterns

강의는 OpenSearch ingestion을 여러 source와 연결한다.

## CloudWatch Logs — Real-Time Pattern

```text
CloudWatch Logs
      ↓ Subscription Filter
Lambda Function
      ↓
OpenSearch
```

강의에서는 real-time 패턴으로 보여준다.

## CloudWatch Logs — Near Real-Time Pattern

```text
CloudWatch Logs
      ↓ Subscription Filter
Kinesis Data Firehose
      ↓
OpenSearch
```

Firehose buffering 때문에 near real-time으로 이해한다.

## Kinesis Data Streams

```text
Kinesis Data Streams
      ↓
Lambda
      ↓
OpenSearch
```

또는:

```text
Kinesis Data Streams
      ↓
Amazon Data Firehose
      ↓
OpenSearch
```

## Transformation

Firehose 또는 Lambda path에서 data transformation을 추가할 수 있다.

## 핵심

```text
실시간 custom processing
→ Kinesis / Lambda → OpenSearch

관리형 delivery
→ Firehose → OpenSearch
```
