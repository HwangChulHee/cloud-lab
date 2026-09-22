# 06부 — Messaging & Integration

SAA 강의의 비동기 메시징과 이벤트 통합 영역을 정리한다.

이 파트에서는 서비스 이름을 따로 외우기보다 **Queue / Pub-Sub / Event Bus / Streaming**을 먼저 구분하는 것이 중요하다.

## 전체 지도

```text
작업을 Queue에 쌓고 Worker가 가져간다
→ SQS

하나의 메시지를 여러 Subscriber에 배포한다
→ SNS

AWS 서비스/애플리케이션 이벤트를 rule로 routing한다
→ EventBridge

계속 들어오는 실시간 데이터를 stream으로 저장/처리한다
→ Kinesis

기존 메시지 브로커 호환이 중요하다
→ Amazon MQ
```

## Chapters

- [x] [23. SQS](./23_sqs/README.md)
- [x] [24. SNS](./24_sns/README.md)
- [x] 25. EventBridge
- [x] [26. Kinesis](./26_kinesis/README.md)
- [x] [27. Amazon MQ / Integration 선택 기준](./27_amazon_mq_integration_selection/README.md)

## SQS / SNS / Kinesis 먼저 구분

```text
SQS
Producer → Queue ← Consumer
Consumer가 poll
작업 처리 후 message 삭제
decoupling / buffer / worker queue

SNS
Publisher → Topic → Subscribers
Topic이 여러 subscriber에 push
fan-out / notification / pub-sub

Kinesis Data Streams
Producer → Stream → Consumers
실시간 데이터
retention / replay
streaming analytics
```

대표 상황으로 보면:

```text
주문 처리 Worker가 밀린다
→ SQS

주문 생성 이벤트를 결제/배송/분석 세 곳에 모두 전달
→ SNS + 필요하면 각 SQS Queue

클릭 로그가 초당 계속 들어오고 실시간 분석 + 과거 재처리가 필요
→ Kinesis Data Streams
```

## 학습 순서

```text
23 SQS
Queue와 비동기 처리 이해
   ↓
24 SNS
Pub/Sub와 Fan-Out 이해
   ↓
25 EventBridge
Event Routing 이해
   ↓
26 Kinesis
Streaming과 Replay 이해
   ↓
27 Amazon MQ / Integration 선택 기준
서비스 전체 비교
```

시험 전에는 서비스별 역할과 선택 기준을 중심으로 학습한다. 이후 포트폴리오에서는 SQS를 중심으로 비동기 작업 처리까지 확장한다.

## 포트폴리오 연결

```text
Cloud Shop

Order API
   ↓
SQS
   ↓
Worker
   ↓
RDS / 외부 작업
```

SQS는 실제 백엔드/클라우드 포트폴리오에 직접 연결할 가치가 높다. SNS와 Kinesis는 우선 SAA 수준의 선택 기준과 구조를 충분히 이해한 뒤 필요에 따라 확장한다.
