# u6. Lambda SAA 선택 기준

## 선택 지도

```text
event-driven short code
→ Lambda

S3 object upload 후 처리
→ S3 Event + Lambda

scheduled serverless job
→ EventBridge + Lambda

REST backend
→ API Gateway + Lambda

DynamoDB item change 처리
→ DynamoDB Streams + Lambda

queue worker
→ SQS + Lambda
```

## Lambda를 피해야 할 수 있는 상황

```text
15분보다 긴 실행
→ Lambda 제한과 충돌

arbitrary Docker runtime
→ ECS/Fargate 선호

지속적으로 항상 실행되는 server process
→ EC2/ECS 등 고려
```

## Concurrency 판단

```text
429 throttling
→ concurrency 확인

특정 function이 다른 function capacity를 잠식
→ Reserved Concurrency

cold start latency 최소화
→ Provisioned Concurrency
```

## 면접용 설명

> Lambda는 event-driven serverless compute로 짧은 함수를 on-demand로 실행하고 자동 scaling합니다. 다만 최대 실행 시간이 15분이고 concurrency/cold start 특성을 이해해야 하며, VPC나 RDS와 연결할 때는 networking과 connection scaling을 별도로 설계해야 합니다.
