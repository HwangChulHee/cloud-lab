# 35. Step Functions / Cognito 등 Serverless 연계 서비스

이 단원은 Serverless 파트에서 Lambda / API Gateway / DynamoDB를 **workflow와 user identity**까지 연결한다.

강의의 핵심 축은 두 가지다.

```text
AWS Step Functions
→ 여러 작업을 순서 / 병렬 / 조건 / 오류 처리로 orchestration

Amazon Cognito
→ 외부 사용자 authentication
→ temporary AWS credentials / AWS resource access
```

## Units

- [ ] [u1. Step Functions Overview](./u1_step_functions_overview/README.md)
- [ ] [u2. Workflow / Error Handling / Integrations](./u2_workflow_error_handling_integrations/README.md)
- [ ] [u3. Cognito Overview / API Gateway Authentication](./u3_cognito_overview_api_auth/README.md)
- [ ] [u4. Cognito Identity Pools / Temporary Credentials](./u4_identity_pools_temporary_credentials/README.md)
- [ ] [u5. Serverless Architecture Selection](./u5_serverless_architecture_selection/README.md)

## 대표 Serverless API

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

## 직접 AWS Resource 접근

강의의 모바일 앱 예시는 다음 구조를 보여준다.

```text
Mobile App
   ↓ authenticate
Cognito
   ↓ temporary AWS credentials
Private S3 Bucket
```

## Workflow

```text
Request
  ↓
Step Functions
  ├→ Lambda A
  ├→ Choice
  ├→ Lambda B / ECS / SQS
  └→ Result
```

## SAA 선택

```text
여러 serverless 작업 orchestration
→ Step Functions

외부 web/mobile user 인증
→ Cognito

사용자에게 제한된 temporary AWS credentials 발급
→ Cognito Identity Pools
```
