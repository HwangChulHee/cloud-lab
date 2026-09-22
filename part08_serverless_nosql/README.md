# 08부 — Serverless & NoSQL

SAA 강의의 **Serverless Overview / Serverless Architectures** 영역을 정리한다.

이 파트에서는 개별 서비스를 따로 외우기보다 먼저 아래 조합을 이해한다.

```text
Client
  ↓
API Gateway
  ↓
Lambda
  ↓
DynamoDB
```

여기에 사용자 인증과 workflow를 붙이면:

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

복잡한 작업 흐름
→ Step Functions
```

## Chapters

- [ ] [32. Lambda](./32_lambda/README.md)
- [ ] [33. API Gateway](./33_api_gateway/README.md)
- [ ] [34. DynamoDB](./34_dynamodb/README.md)
- [ ] [35. Step Functions / Cognito 등 Serverless 연계 서비스](./35_step_functions_cognito/README.md)

## Serverless 전체 지도

강의에서는 Serverless를 "서버가 없다"가 아니라 **개발자가 서버를 직접 관리 / provision / 보지 않는 구조**로 설명한다.

대표 서비스:

```text
Lambda
DynamoDB
Cognito
API Gateway
S3
SNS / SQS
Amazon Data Firehose
Aurora Serverless
Step Functions
Fargate
```

## 먼저 구분할 것

```text
Lambda
→ serverless function compute

API Gateway
→ REST / WebSocket API entry point

DynamoDB
→ serverless NoSQL database

Step Functions
→ workflow orchestration

Cognito
→ external user authentication / identity
```

## 대표 architecture 1 — Serverless REST API

```text
Client
  ↓ HTTPS
API Gateway
  ↓ invoke
Lambda
  ↓ CRUD
DynamoDB
```

## 대표 architecture 2 — Authenticated Mobile App

```text
Mobile User
    ↓
Cognito
    ↓
API Gateway
    ↓
Lambda
    ↓
DynamoDB
```

사용자가 private S3 같은 AWS resource에 직접 접근해야 하면 Cognito Identity Pool에서 temporary AWS credentials를 받아 접근하는 패턴을 강의에서 다룬다.

## 대표 architecture 3 — Event Driven

```text
S3 Object Upload
      ↓
Lambda
      ↓
Thumbnail 생성
      ↓
S3 / DynamoDB
```

또는:

```text
DynamoDB Item Change
      ↓
DynamoDB Streams
      ↓
Lambda
      ↓
SES / SNS / Other Processing
```

## 시험에서 특히 중요한 비교

```text
Lambda
vs
EC2 / ECS / Fargate

API Gateway Edge-Optimized
vs Regional
vs Private

DynamoDB Provisioned
vs On-Demand

DynamoDB Query
vs Scan

GSI
vs LSI

DAX
vs ElastiCache

DynamoDB Streams
vs Kinesis Data Streams

Cognito
vs IAM authentication

Step Functions
vs Lambda끼리 직접 chaining
```

## 학습 순서

```text
32 Lambda
serverless compute
    ↓
33 API Gateway
API entry / auth / throttling / cache
    ↓
34 DynamoDB
NoSQL / key / capacity / indexes / streams
    ↓
35 Step Functions + Cognito
workflow / identity
    ↓
전체 serverless architecture 조합
```

## 현재 examples와의 관계

8부는 현재 `examples/01~16`의 필수 선행조건은 아니다.

시험 전에는 **서비스 선택 기준과 serverless architecture 조합**을 정확히 이해하는 데 집중한다. 이후 실제 프로젝트에서는 API Gateway + Lambda + DynamoDB나 Cognito 기반 별도 serverless 기능을 추가할 수 있다.
