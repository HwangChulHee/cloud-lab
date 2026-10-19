# u1. Global Serverless Website

강의의 hosted website 예시는 static frontend와 serverless REST API를 분리한다.

```text
Users
  ↓
CloudFront
  ├→ S3 + OAC
  │   static content
  │
  └→ API Gateway
        ↓
      Lambda
        ↓
     DynamoDB
```

## 역할

```text
CloudFront
→ global distribution

S3
→ static content

OAC
→ CloudFront만 S3 origin 접근 허용

API Gateway
→ public REST HTTPS endpoint

Lambda
→ serverless compute

DynamoDB
→ serverless data store
```

강의에서는 global data가 필요하면 DynamoDB Global Tables를 사용할 수 있고 Aurora Global Database도 대안으로 언급한다.
