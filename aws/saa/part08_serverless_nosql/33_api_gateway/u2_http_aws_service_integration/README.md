# u2. API Gateway HTTP / AWS Service Integration

API Gateway는 Lambda 전용 서비스가 아니다.

## 1. HTTP Integration

기존 HTTP backend를 API Gateway 뒤에 둘 수 있다.

예:

```text
Client
  ↓
API Gateway
  ↓
HTTP Backend
  ├─ On-Premises API
  └─ Application Load Balancer
```

왜 앞에 API Gateway를 두는가?

```text
rate limiting
caching
user authentication
API keys
request control
```

## 2. AWS Service Integration

API Gateway가 Lambda를 거치지 않고 AWS API를 호출하도록 구성할 수도 있다.

강의 예시:

```text
Client
  ↓
API Gateway
  ├→ Start Step Functions
  └→ Send message to SQS
```

또 다른 예:

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

## 핵심 선택

단순히 "API Gateway = Lambda 앞"으로 외우지 않는다.

```text
Lambda Integration
HTTP Integration
AWS Service Integration
```

세 형태를 구분한다.
