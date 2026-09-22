# u3. Microservices Communication

강의의 Microservices architecture에서는 각 서비스가 서로 다른 AWS 구성을 가질 수 있다고 설명한다.

예:

```text
service1
→ API Gateway + Lambda + ElastiCache

service2
→ ELB + EC2 Auto Scaling + RDS

service3
→ ELB + ECS + DynamoDB
```

Route 53에서 각 service endpoint를 연결할 수 있다.

## Synchronous

```text
API Gateway
Load Balancer
REST API
```

응답을 즉시 기다리는 통신이다.

## Asynchronous

강의에서 다음을 언급한다.

```text
SQS
Kinesis
SNS
Lambda triggers / S3 events
```

Spike와 component coupling을 줄이는 데 사용할 수 있다.

## 기억할 문장

> Microservice마다 같은 runtime/database를 강제하기보다 요구사항에 맞는 구조를 선택하고, 동기/비동기 통신 방식을 의도적으로 구분한다.
