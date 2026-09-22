# u5. Serverless Architecture Selection

8부 전체를 실제 architecture로 연결한다.

## 1. Serverless REST API

```text
Client
  ↓ HTTPS
API Gateway
  ↓
Lambda
  ↓
DynamoDB
```

## 2. Authentication 추가

```text
User
  ↓
Cognito
  ↓
API Gateway
  ↓
Lambda
  ↓
DynamoDB
```

## 3. User가 S3에 직접 접근

```text
User
  ↓ authenticate
Cognito Identity Pool
  ↓ temporary AWS credentials
S3
```

Backend가 모든 file transfer를 대신 처리하지 않아도 된다.

## 4. Read Cache

```text
API Gateway Cache
→ REST response cache

DAX
→ DynamoDB read cache
```

두 cache 계층을 구분한다.

## 5. Change Event

```text
DynamoDB
   ↓ Stream
Lambda
   ↓
SES / SNS / 다른 처리
```

강의의 welcome email architecture가 대표 예다.

## 6. Workflow Orchestration

```text
API Gateway
   ↓
Step Functions
   ├→ Lambda
   ├→ SQS
   └→ ECS
```

## 최종 선택 지도

```text
function compute
→ Lambda

REST/WebSocket API entry
→ API Gateway

serverless NoSQL
→ DynamoDB

workflow orchestration
→ Step Functions

external user authentication
→ Cognito

temporary AWS credentials for app users
→ Cognito Identity Pools
```

## 기억할 문장

> Serverless architecture는 Lambda 하나가 아니라 API Gateway, Cognito, DynamoDB, Step Functions, S3/SQS 같은 관리형 서비스를 조합해 서버 운영 부담을 줄이는 구조다.
