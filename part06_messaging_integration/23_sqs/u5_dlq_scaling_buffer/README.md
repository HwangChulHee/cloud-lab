# u5. DLQ / Scaling / Buffer Pattern

## 1. SQS as Buffer

SQS는 갑자기 요청이 몰릴 때 Backend 앞에서 작업을 잠시 쌓아두는 Buffer로 사용할 수 있다.

```text
Traffic Spike
     │
     ▼
 Frontend
     │
     ▼
 SQS Queue
     │
     ▼
 Workers
     │
     ▼
 Database
```

Queue가 없다면 Backend나 DB가 순간 부하를 직접 맞는다.

Queue가 있으면 Producer 속도와 Consumer 처리 속도를 분리할 수 있다.

## 2. Queue Length 기반 Auto Scaling

강의에서는 `ApproximateNumberOfMessages` 같은 Queue 길이 지표를 CloudWatch에서 보고 Auto Scaling과 연결하는 패턴을 다룬다.

```text
SQS Queue Length 증가
        ↓
CloudWatch Alarm
        ↓
Auto Scaling Group
        ↓
Worker EC2 증가
```

즉 CPU뿐 아니라 **대기 작업량(backlog)**을 기준으로 Worker를 확장할 수 있다.

## 3. Dead-Letter Queue

정상 Queue에서 반복적으로 처리에 실패하는 메시지를 별도의 Queue로 격리하는 패턴이다.

```text
Main Queue
   │
   ├─ 성공 → DeleteMessage
   │
   └─ 여러 번 실패
          ↓
         DLQ
```

DLQ의 목적은 실패 메시지를 무한히 반복 처리하는 대신 **분리해서 조사할 수 있게 하는 것**이다.

운영에서는 다음을 본다.

```text
어떤 메시지가 실패했나?
왜 계속 실패했나?
코드 문제인가?
데이터 문제인가?
재처리 가능한가?
```

## 4. SQS + Lambda

Lambda도 SQS를 Event Source로 사용해 비동기 Worker처럼 동작할 수 있다.

개념적으로:

```text
Producer → SQS → Lambda
                 │
                 └→ 처리 / retry / failure path
```

## SAA 판단

```text
DB가 순간 트래픽을 버티지 못한다
→ SQS를 buffer로 고려

Queue가 계속 쌓인다
→ Consumer scale-out 고려

특정 메시지가 반복 실패한다
→ DLQ

Frontend와 긴 작업을 분리
→ SQS
```
