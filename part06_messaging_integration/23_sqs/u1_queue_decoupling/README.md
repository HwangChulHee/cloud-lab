# u1. SQS Queue / Decoupling / Producer & Consumer

## 1. Queue란?

Queue는 처리할 작업을 **중간에 쌓아두는 버퍼**라고 생각하면 된다.

```text
Producer 1 ─┐
Producer 2 ─┼→ SQS Queue → Consumer 1
Producer 3 ─┘             → Consumer 2
```

Producer는 Consumer가 지금 처리 가능한지 직접 알 필요 없이 메시지를 Queue에 넣는다.

## 2. Producer

Producer는 `SendMessage` API 등을 사용해 메시지를 SQS에 넣는다.

예:

```json
{
  "orderId": 1036,
  "customerId": 42,
  "action": "CREATE_ORDER"
}
```

메시지는 Consumer가 성공적으로 처리한 뒤 삭제할 때까지 Queue에 유지된다.

## 3. Consumer

Consumer는 EC2, 서버 애플리케이션, Lambda 등이 될 수 있다.

기본 흐름:

```text
ReceiveMessage
→ 메시지 처리
→ 성공
→ DeleteMessage
```

Consumer가 메시지를 받았다는 것만으로 메시지가 즉시 삭제되는 것은 아니다.

## 4. 왜 Decoupling인가?

직접 호출:

```text
Web App → Worker
```

Worker가 느려지면 Web App도 영향을 받는다.

SQS 사용:

```text
Web App → SQS → Worker
```

Worker가 잠시 느려져도 Producer는 Queue에 작업을 넣고 자신의 흐름을 계속할 수 있다.

## 5. Horizontal Scaling

여러 Consumer가 같은 Queue에서 메시지를 가져가 병렬 처리할 수 있다.

```text
             ┌→ Worker A
SQS Queue ───┼→ Worker B
             └→ Worker C
```

작업량이 많아지면 Worker 수를 늘려 처리량을 높일 수 있다.

## 기억할 문장

> SQS는 Producer와 Consumer 사이에 Queue를 두어 두 계층의 처리 속도와 장애를 분리한다.
