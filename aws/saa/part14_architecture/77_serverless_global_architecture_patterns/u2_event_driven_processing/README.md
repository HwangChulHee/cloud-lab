# u2. Event-Driven Processing

Serverless architecture는 request-response뿐 아니라 **event가 다음 작업을 자동으로 시작하는 흐름**이 중요하다.

## Welcome Email 예시

```text
DynamoDB Item Change
      ↓
DynamoDB Streams
      ↓
Lambda
      ↓ IAM Role
Amazon SES
```

## Thumbnail 예시

```text
Image Upload
   ↓
S3
   ↓ event
Lambda
   ↓
Thumbnail 생성
   ↓
S3
```

강의에서는 S3 event target으로 SQS / SNS / Lambda를 언급한다.

EventBridge를 사용하면 더 다양한 destination과 filtering, archive/replay 기능으로 확장할 수 있다.

## 기억할 문장

> Event-driven architecture에서는 producer가 다음 component를 직접 동기 호출하지 않고 event/stream/queue를 통해 작업을 이어갈 수 있다.
