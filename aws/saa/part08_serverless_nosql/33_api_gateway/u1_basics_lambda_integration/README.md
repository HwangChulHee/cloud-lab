# u1. API Gateway 기본 역할 / Lambda Integration

## 1. API Gateway란?

Client가 backend에 접근하는 API entry point 역할을 한다.

```text
Client
  ↓
API Gateway
  ↓
Backend
```

Backend는 Lambda일 수도 있고 HTTP endpoint나 AWS Service일 수도 있다.

## 2. Lambda Integration

강의에서 대표 serverless API:

```text
Client
  ↓ REST HTTPS
API Gateway
  ↓ invoke
Lambda
  ↓ CRUD
DynamoDB
```

서버를 직접 운영하지 않고 API와 compute/database를 조합할 수 있다.

## 3. WebSocket

API Gateway는 WebSocket protocol도 지원한다.

REST request-response가 아니라 양방향 통신이 필요한 경우 연결할 수 있다.

## 4. API Lifecycle 기능

강의에서 다음 기능을 언급한다.

```text
API Versioning
Stages: dev / test / prod
Request Validation
Request / Response Transformation
OpenAPI import
SDK generation
```

## 기억할 문장

> API Gateway는 API 진입점에서 backend 호출, 인증, throttling, cache, stage 같은 공통 기능을 관리한다.
