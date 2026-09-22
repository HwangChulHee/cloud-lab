# u2. Amazon MQ Broker / Queue / Topic

Amazon MQ는 **message broker**를 관리형으로 제공하는 형태로 이해한다.

## 1. Broker

Broker는 Producer와 Consumer 사이에서 메시지를 받아 전달하는 서버 역할을 한다.

```text
Producer
   │
   ▼
Message Broker
   │
   ▼
Consumer
```

SQS처럼 추상적인 Queue API만 사용하는 느낌보다 **브로커가 실제로 존재한다**는 점이 중요하다.

## 2. Queue 기능

강의에서는 Amazon MQ가 SQS와 비슷한 Queue 기능을 제공한다고 설명한다.

```text
Producer
   ↓
Queue
   ↓
Consumer
```

작업을 한 Consumer가 처리하는 형태의 messaging에 사용할 수 있다.

## 3. Topic 기능

SNS와 비슷한 Topic/Pub-Sub 형태도 지원한다.

```text
Publisher
   ↓
Topic
   ├→ Subscriber A
   └→ Subscriber B
```

즉 Amazon MQ 하나가 기존 브로커 세계의 Queue와 Topic 기능을 모두 제공할 수 있다는 점을 기억한다.

## 4. SQS/SNS와 구조 차이

```text
SQS
→ AWS managed queue service

SNS
→ AWS managed pub/sub service

Amazon MQ
→ managed message broker
→ Queue + Topic
→ 기존 protocol/application compatibility
```

## 핵심

Amazon MQ를 고르는 이유는 단순히 "Queue도 되고 Topic도 된다"가 아니다.

**기존 broker protocol과 application compatibility를 유지해야 한다는 요구사항**이 핵심 선택 기준이다.
