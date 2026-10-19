# u3. SNS Message Filtering / FIFO

## 1. Subscription Filter Policy

SNS Topic의 모든 Subscriber가 모든 메시지를 받아야 하는 것은 아니다.

Subscription에 JSON Filter Policy를 설정하면 조건에 맞는 메시지만 받을 수 있다.

예:

```text
Order Event
{
  state: "PLACED"
}
        │
        ▼
      SNS
       │
       ├→ Placed Queue    filter: PLACED
       ├→ Cancelled Queue filter: CANCELLED
       └→ All Queue       filter 없음
```

Filter Policy가 없는 Subscription은 모든 메시지를 받는다.

## 왜 좋은가?

Subscriber 안에서:

```text
메시지 받음
→ if state == ...
→ 아니면 버림
```

을 반복하는 대신 SNS 단계에서 필요한 이벤트만 전달할 수 있다.

## 2. FIFO

강의에서는 SNS에도 FIFO capability가 있고 SQS FIFO와 함께 순서가 필요한 Pub/Sub 패턴을 만들 수 있다는 점을 다룬다.

개념적으로:

```text
Publisher
   ↓
SNS FIFO Topic
   ↓
SQS FIFO Queue
   ↓
Consumer
```

순서 요구가 없는 일반 알림/분배라면 Standard SNS/SQS 구성이 더 단순할 수 있다.

## SAA 판단

```text
구독자별 이벤트 조건 분리
→ SNS Filter Policy

같은 Topic에서 모든 구독자가 전부 받음
→ Filter 없음

Fan-Out + ordering 요구
→ SNS FIFO + SQS FIFO 고려
```
