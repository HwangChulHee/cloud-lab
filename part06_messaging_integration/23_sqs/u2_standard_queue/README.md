# u2. SQS Standard Queue

Standard Queue는 일반적인 SQS 기본 Queue 유형이다.

## 핵심 특징

강의 기준으로 다음 성질을 기억한다.

```text
높은 처리량
메시지 보관
At-Least-Once Delivery
Best-Effort Ordering
```

## 1. At-Least-Once Delivery

Standard Queue에서는 같은 메시지가 드물게 두 번 전달될 수 있다.

따라서 Consumer는 가능하면 **같은 작업을 다시 실행해도 문제가 없도록** 설계하는 것이 안전하다.

예:

```text
나쁜 예
message 재전달
→ 결제를 다시 실행
→ 중복 결제

개선
orderId를 기준으로 이미 처리한 주문인지 확인
→ 중복 처리 방지
```

이런 성질을 **Idempotency(멱등성)**와 연결해서 이해하면 좋다.

## 2. Best-Effort Ordering

Standard Queue는 전송 순서를 항상 그대로 보장하지 않는다.

```text
Producer
1 → 2 → 3

Consumer가 보는 순서
1 → 3 → 2 가능
```

절대적인 순서가 필요한 요구사항이라면 FIFO Queue를 고려한다.

## 3. Message Retention

메시지는 일정 기간 Queue에 저장될 수 있다. 강의에서는 기본 4일, 최대 14일까지 설정할 수 있다고 설명한다.

Consumer가 잠시 중단돼도 retention 기간 안이라면 이후 다시 처리할 수 있다.

## 4. Multiple Consumers

여러 Consumer가 같은 Queue를 병렬로 poll할 수 있다.

```text
Message A → Worker 1
Message B → Worker 2
Message C → Worker 3
```

이는 SNS처럼 **같은 메시지를 모든 Consumer에게 복제**하는 구조와 다르다.

SQS에서는 일반적으로 Queue의 하나의 메시지를 한 작업 단위로 경쟁 소비한다.

## SAA 판단

```text
순서 엄격히 필요 없음 + 높은 처리량
→ Standard SQS

중복 가능성을 애플리케이션에서 처리 가능
→ Standard SQS

같은 이벤트를 여러 독립 시스템에 각각 전달
→ SQS 하나보다 SNS + 여러 SQS Queue fan-out 고려
```
