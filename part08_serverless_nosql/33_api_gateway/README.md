# 33. Amazon API Gateway

Amazon API Gateway는 HTTP/REST/WebSocket API의 진입점을 관리하는 서비스다.

강의에서는 API Gateway를 Lambda와 결합한 serverless API뿐 아니라 **HTTP backend / AWS Service Integration**까지 연결해서 설명한다.

## Units

- [ ] [u1. API Gateway 기본 역할 / Lambda Integration](./u1_basics_lambda_integration/README.md)
- [ ] [u2. HTTP / AWS Service Integration](./u2_http_aws_service_integration/README.md)
- [ ] [u3. Endpoint Types](./u3_endpoint_types/README.md)
- [ ] [u4. Security / Auth / Custom Domain](./u4_security_auth_domain/README.md)
- [ ] [u5. Throttling / Cache / Stages / SAA Selection](./u5_throttling_cache_stages_selection/README.md)

## 대표 구조

```text
Client
  ↓ HTTPS
API Gateway
  ↓
Lambda
  ↓
DynamoDB
```

## API Gateway가 제공하는 것

강의 기준 핵심:

```text
REST / WebSocket
API versioning
dev / test / prod environments
Authentication / Authorization
API keys
throttling
OpenAPI import
request/response transformation
validation
SDK generation
response caching
```

## Integration 종류

```text
Lambda
HTTP Backend
AWS Service
```

## SAA 선택 기준

```text
Lambda 기반 REST API
→ API Gateway + Lambda

기존 HTTP backend 앞에 auth/cache/rate limit 추가
→ API Gateway + HTTP integration

AWS API를 직접 API로 노출
→ API Gateway + AWS Service integration
```
