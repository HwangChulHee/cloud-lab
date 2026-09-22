# 23. Amazon SQS

SAA 강의의 **Amazon SQS(Simple Queue Service)** 내용을 정리한다.

SQS는 애플리케이션 계층 사이에 메시지를 보관하는 **Queue 기반 비동기 메시징 서비스**다. Producer와 Consumer를 직접 붙이지 않고 Queue를 사이에 두어 서로 독립적으로 확장할 수 있게 한다.

```text
Producer
   │ SendMessage
   ▼
SQS Queue
   │ poll / ReceiveMessage
   ▼
Consumer
   │
   └─ 처리 성공 후 DeleteMessage
```

## Units

- [ ] [u1. Queue / Decoupling / Producer & Consumer](./u1_queue_decoupling/README.md)
- [ ] [u2. Standard Queue / At-Least-Once / Ordering](./u2_standard_queue/README.md)
- [ ] [u3. Visibility Timeout / Long Polling](./u3_visibility_long_polling/README.md)
- [ ] [u4. FIFO Queue](./u4_fifo_queue/README.md)
- [ ] [u5. DLQ / Scaling / Buffer Pattern](./u5_dlq_scaling_buffer/README.md)
- [ ] [u6. Security & SAA Selection](./u6_security_saa_selection/README.md)

## 전체 그림

```text
동기 결합
Frontend ─────────→ Backend
            느리거나 장애
                ↓
          Frontend도 영향

SQS로 분리
Frontend → SQS Queue → Worker
             │
             └─ 일시적으로 메시지 축적 가능
```

핵심은 **처리 요청을 바로 처리할 서버에 강하게 결합하지 않는 것**이다.

## SAA 핵심 선택 기준

```text
작업을 비동기로 넘기고 싶다
→ SQS

Consumer가 자기 속도로 가져가게 하고 싶다
→ SQS

순서가 중요하지 않고 높은 처리량이 필요하다
→ Standard Queue

순서 보장 + 중복 제거가 중요하다
→ FIFO Queue

실패 메시지를 별도로 격리하고 싶다
→ DLQ

Queue backlog에 따라 worker를 늘리고 싶다
→ SQS + CloudWatch + Auto Scaling
```

## SNS / Kinesis와 먼저 구분

```text
SQS
= Queue
= Consumer가 pull
= 처리 후 message 삭제

SNS
= Pub/Sub
= 하나의 publish를 여러 subscriber에 push

Kinesis Data Streams
= 실시간 streaming
= 일정 기간 데이터를 보관하며 replay 가능
```
