# u6. SQS Security & SAA Selection

## 1. Encryption

강의에서 다루는 SQS 보안 계층:

```text
In-flight
→ HTTPS API

At-rest
→ KMS key

필요 시
→ Client-side encryption
```

## 2. IAM Policy

IAM Policy는 어떤 User/Role이 SQS API를 호출할 수 있는지 제어한다.

예:

```text
Producer Role
→ sqs:SendMessage

Consumer Role
→ sqs:ReceiveMessage
→ sqs:DeleteMessage
```

최소 권한으로 역할을 나누는 것이 핵심이다.

## 3. SQS Access Policy

Queue 자체에도 Resource Policy 성격의 Access Policy를 둘 수 있다.

대표 사용:

```text
다른 AWS Account에서 Queue 접근
SNS Topic이 Queue에 메시지 전송
S3 Event가 Queue에 메시지 전송
```

IAM Policy와 Queue Policy를 별개의 접근 제어 계층으로 본다.

## 4. SAA 최종 선택 지도

```text
Producer와 Worker를 느슨하게 결합
→ SQS

Consumer pull model
→ SQS

순서가 필요
→ FIFO

중복을 애플리케이션에서 허용/제어 가능
→ Standard

빈 polling 비용/호출 감소
→ Long Polling

작업이 Visibility Timeout보다 길다
→ Timeout 조정 / ChangeMessageVisibility

반복 실패 메시지 격리
→ DLQ

Queue backlog에 따라 worker 확장
→ SQS + CloudWatch + Auto Scaling
```

## 면접용 설명

> SQS는 Producer와 Consumer 사이에 durable queue를 두어 처리 속도와 장애를 분리하는 서비스입니다. Consumer는 메시지를 poll하고 성공 후 삭제하며, Standard Queue에서는 중복과 순서 변경 가능성을 고려해 멱등성을 설계합니다. 순서가 필요하면 FIFO, 반복 실패는 DLQ, 긴 처리에는 Visibility Timeout을 함께 봅니다.
