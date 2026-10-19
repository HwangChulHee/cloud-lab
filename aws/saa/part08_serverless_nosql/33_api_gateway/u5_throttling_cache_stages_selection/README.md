# u5. API Gateway Throttling / Cache / Stages / SAA Selection

## 1. Throttling

API Gateway에서 request rate를 제한할 수 있다.

```text
많은 Client Requests
       ↓
API Gateway
   rate limit
       ↓
Backend 보호
```

Backend Lambda나 HTTP system이 감당할 수 있는 수준으로 요청을 제어하는 데 도움이 된다.

## 2. API Keys

API Key를 만들고 client usage를 식별/제어하는 구조를 사용할 수 있다.

시험에서는 API Key와 authentication 자체를 같은 개념으로 섞지 않는다.

## 3. Caching

API 응답을 API Gateway에서 cache할 수 있다.

```text
Client
  ↓
API Gateway Cache
  ├─ hit → 즉시 응답
  └─ miss → backend 호출
```

읽기 요청이 많을 때 backend invocation과 latency를 줄이는 데 사용할 수 있다.

## 4. Stages

```text
dev
test
prod
```

환경별 배포를 분리할 수 있다.

## 최종 선택

```text
serverless REST API
→ API Gateway + Lambda

VPC 내부 전용 API
→ Private API + Interface Endpoint

global client
→ Edge-Optimized

backend 보호
→ throttling

read-heavy repeated response
→ API Gateway cache

external user authentication
→ Cognito
```

## 면접용 설명

> API Gateway는 API 진입점에서 backend integration뿐 아니라 인증, throttling, caching, stage, custom domain 같은 공통 API 기능을 중앙화하는 서비스입니다.
