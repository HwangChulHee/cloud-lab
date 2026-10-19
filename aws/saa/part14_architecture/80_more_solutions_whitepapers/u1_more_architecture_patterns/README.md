# u1. More Solutions Architecture Patterns

강의의 More Solutions Architecture에서는 이미 배운 서비스를 새로운 조합으로 다시 연결한다.

## Fan-Out

```text
Producer
  ↓
 SNS
 ├→ SQS A
 ├→ SQS B
 └→ SQS C
```

하나의 event를 여러 독립 consumer에 전달한다.

## S3 Event Processing

```text
S3 Event
 ├→ Lambda
 ├→ SQS
 └→ SNS
```

EventBridge를 연결하면 더 다양한 destination과 filtering/archive/replay를 사용할 수 있다.

## API Gateway → AWS Service

강의 예:

```text
Client
 ↓
API Gateway
 ↓
Kinesis Data Streams
 ↓
Amazon Data Firehose
 ↓
S3
```

Lambda를 반드시 거쳐야 하는 것은 아니다.

## 기억할 문장

> Architecture 문제에서는 AWS 서비스 하나가 아니라 event source, integration, buffering, destination을 한 흐름으로 본다.
