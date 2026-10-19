# u2. SNS + SQS Fan-Out

## 왜 SNS와 SQS를 같이 쓰나?

SNS만 사용하면 여러 Subscriber에게 메시지를 보낼 수 있다.

하지만 각 Consumer가 잠시 장애가 나거나 자신의 속도로 처리해야 한다면 Queue가 유용하다.

```text
                 ┌→ SQS Queue A → Worker A
Producer → SNS ──┼→ SQS Queue B → Worker B
                 └→ SQS Queue C → Worker C
```

이 구조를 **Fan-Out Pattern**이라고 한다.

## 장점

같은 이벤트를 여러 독립 파이프라인이 받는다.

예:

```text
OrderCreated
   │
   ▼
 SNS
   ├→ payment-queue
   ├→ shipping-queue
   └→ analytics-queue
```

각 Queue는 독립적으로:

```text
메시지 보관
Consumer scale
Visibility Timeout
DLQ
재처리
```

를 가질 수 있다.

## SNS만 쓸 때와 차이

```text
SNS → Worker 직접
→ Worker가 바로 메시지를 받아야 함

SNS → SQS → Worker
→ Queue가 buffer 역할
→ Worker 장애/속도 차이를 흡수
```

## SAA 판단

```text
같은 메시지를 여러 Queue에 복제
→ SNS Fan-Out

Producer가 Queue마다 여러 번 SendMessage
→ 가능하지만 결합도 증가

Producer → SNS 한 번 publish
→ 여러 SQS Queue subscribe
→ Fan-Out
```

## 핵심

> SNS는 복제/분배, SQS는 보관/비동기 처리 버퍼 역할을 맡는다.
