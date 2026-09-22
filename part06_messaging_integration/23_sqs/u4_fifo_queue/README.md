# u4. SQS FIFO Queue

FIFO는 **First In First Out**이다.

순서와 중복 제어가 중요한 작업에 사용한다.

## 핵심 그림

```text
Producer
1 → 2 → 3 → 4

FIFO Queue

Consumer
1 → 2 → 3 → 4
```

## 1. Ordering

FIFO Queue는 Message Group 안에서 메시지 순서를 유지한다.

`MessageGroupId`는 같은 순서 흐름에 속하는 메시지를 묶는 기준이다.

예:

```text
MessageGroupId = customer-42

order-created
→ payment-requested
→ shipment-started
```

같은 Group 안에서는 순서를 유지해야 하는 이벤트를 처리할 수 있다.

## 2. Deduplication

FIFO Queue는 Deduplication ID를 통해 중복 전송을 제거하는 기능을 제공한다.

```text
같은 Deduplication ID
→ duplicate send 제거
```

이는 Standard Queue의 at-least-once 특성과 구분해서 기억한다.

## 3. Trade-off

강의는 FIFO Queue가 Standard Queue보다 처리량 제약이 있다는 점을 강조한다.

따라서 무조건 FIFO를 쓰는 것이 아니라:

```text
순서/중복 제어가 핵심인가?
→ FIFO

최대 처리량과 단순 확장이 더 중요한가?
→ Standard
```

로 선택한다.

## SAA 판단

```text
금융 거래 순서를 보존
→ FIFO

같은 Message Group의 이벤트 순서 보장
→ FIFO

순서 필요 없음, 대규모 worker 처리
→ Standard
```
