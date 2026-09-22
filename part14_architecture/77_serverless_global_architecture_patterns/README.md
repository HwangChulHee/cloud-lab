# 77. Serverless / Global Architecture Patterns

이 단원은 강의의 Serverless Architectures와 More Solutions Architecture에서 여러 managed service를 조합하는 패턴을 다시 정리한다.

## Units

- [ ] [u1. Global Serverless Website](./u1_global_serverless_website/README.md)
- [ ] [u2. Event-Driven Processing](./u2_event_driven_processing/README.md)
- [ ] [u3. Microservices Communication](./u3_microservices_communication/README.md)
- [ ] [u4. Global Data / Caching Selection](./u4_global_data_caching/README.md)

## 대표 구조

```text
Users
 ↓
CloudFront
 ├→ S3 static content
 └→ API Gateway
       ↓
     Lambda
       ↓
    DynamoDB
```

여기에 DynamoDB Streams, Lambda, SES, S3 Event Notification 등을 붙여 event-driven 기능을 확장한다.
