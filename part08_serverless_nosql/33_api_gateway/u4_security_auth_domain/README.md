# u4. API Gateway Security / Authentication / Custom Domain

강의에서는 API Gateway 인증 방식을 세 가지로 정리한다.

## 1. IAM

```text
IAM Roles
→ internal AWS applications
```

AWS identity 기반 internal API에 적합하다.

## 2. Cognito

```text
Cognito
→ external users
→ mobile/web users
```

외부 사용자의 인증을 관리하는 serverless pattern에 연결된다.

## 3. Custom Authorizer

직접 작성한 authorization logic을 적용할 수 있다.

```text
Client
  ↓ token/request
API Gateway
  ↓
Custom Authorizer
  ↓ allow/deny
Backend
```

## 4. Custom Domain + ACM

API Gateway custom domain에 HTTPS certificate를 연결할 수 있다.

강의 구분:

```text
Edge-Optimized
→ ACM certificate: us-east-1

Regional
→ ACM certificate: API Gateway와 같은 Region
```

DNS는 Route 53 CNAME 또는 A Alias와 연결한다.

## SAA 판단

```text
internal IAM identity
→ IAM Auth

external/mobile user identity
→ Cognito

custom auth logic
→ Custom Authorizer
```
