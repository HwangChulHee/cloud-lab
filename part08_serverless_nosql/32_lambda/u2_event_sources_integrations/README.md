# u2. Lambda Event Sources / Integrations

Lambda는 AWS의 여러 서비스와 연결된다.

강의에서 주요 integration으로 다음을 제시한다.

```text
API Gateway
Kinesis
DynamoDB
S3
CloudFront
CloudWatch Logs
SNS
SQS
Cognito
EventBridge
```

## 1. API 요청

```text
Client
  ↓
API Gateway
  ↓
Lambda
  ↓
DynamoDB
```

Serverless REST API의 대표 구조다.

## 2. S3 Event

```text
S3 Object Created
      ↓
Lambda
      ↓
Thumbnail 생성
      ↓
S3
```

Image metadata를 DynamoDB에 저장하는 패턴도 강의에서 함께 소개한다.

## 3. Scheduled Job

```text
EventBridge
Every 1 hour
     ↓
Lambda
     ↓
Task 수행
```

기존 cron server 없이 주기 작업을 실행할 수 있다.

## 4. Stream / Queue

```text
SQS → Lambda
Kinesis → Lambda
DynamoDB Stream → Lambda
```

이 경우 Lambda가 메시지/record 처리 계층으로 동작한다.

## 핵심

Lambda 자체보다 **어떤 이벤트가 Lambda를 호출하고, Lambda가 어느 서비스로 결과를 보낼지**를 architecture 관점에서 생각한다.
