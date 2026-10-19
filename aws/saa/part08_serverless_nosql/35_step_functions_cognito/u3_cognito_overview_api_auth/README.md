# u3. Cognito Overview / API Gateway Authentication

강의에서 Cognito는 **외부 사용자 identity**를 serverless architecture에 연결하는 서비스로 사용한다.

## 대표 구조

```text
Mobile / Web User
      ↓ login
   Cognito
      ↓
API Gateway
      ↓
Lambda
      ↓
DynamoDB
```

API Gateway Security 파트에서도 Cognito를 다음처럼 구분한다.

```text
IAM
→ internal AWS applications

Cognito
→ external users / mobile users

Custom Authorizer
→ custom authorization logic
```

## Serverless Architecture에서 역할

강의의 mobile todo app 예시:

```text
Mobile Client
   ↓ authenticate
Cognito
   ↓
API Gateway
   ↓
Lambda
   ↓
DynamoDB
```

즉 애플리케이션 서버가 직접 사용자 인증 시스템을 처음부터 만들지 않고 Cognito를 사용한다.

## 이 단원에서의 범위

현재 강의 자료에서 명확히 강조되는 것은:

```text
external user authentication
API Gateway와 연동
Identity Pools를 통한 temporary credentials
```

이다.

세부적인 UI/가입 정책 구현보다 **어떤 architecture 문제를 해결하는지**를 우선 이해한다.

## 기억할 문장

> Cognito는 web/mobile 같은 외부 사용자를 serverless API와 AWS resource access에 연결하는 managed identity 서비스다.
