# 32. AWS Lambda

AWS Lambda는 서버를 직접 프로비저닝하거나 관리하지 않고 **함수 단위로 코드를 실행**하는 serverless compute 서비스다.

강의의 핵심 비교는 EC2와 Lambda다.

```text
EC2
→ 계속 실행되는 virtual server
→ RAM/CPU 기반
→ scaling 시 instance 추가/제거 고려

Lambda
→ virtual function
→ on-demand 실행
→ 짧은 실행에 적합
→ scaling 자동화
```

## Units

- [x] [u1. Serverless / Lambda 기본 구조](./u1_serverless_lambda_basics/README.md)
- [x] [u2. Event Sources / Integrations](./u2_event_sources_integrations/README.md)
- [x] [u3. Limits / Memory / Timeout / Storage](./u3_limits_memory_timeout_storage/README.md)
- [x] [u4. Concurrency / Throttling / Cold Start](./u4_concurrency_cold_start/README.md)
- [x] [u5. VPC / IAM / Logging](./u5_vpc_iam_logging/README.md)
- [x] [u6. SAA 선택 기준](./u6_saa_selection/README.md)

## 대표 구조

```text
API Gateway
    ↓
Lambda
    ↓
DynamoDB
```

또는:

```text
S3 Object Created
      ↓
    Lambda
      ↓
Thumbnail 생성
      ↓
S3 / DynamoDB
```

## 강의 핵심

```text
pay per request / duration
CloudWatch monitoring
여러 AWS 서비스와 통합
memory 증가 시 CPU/network도 함께 증가
최대 실행 시간 15분
reserved concurrency
provisioned concurrency
```

## SAA 선택 기준

```text
짧은 on-demand code 실행
→ Lambda

서버 운영 없이 event-driven processing
→ Lambda

15분보다 긴 작업 / arbitrary container runtime
→ Lambda보다 ECS/Fargate 또는 Batch 쪽 고려
```
