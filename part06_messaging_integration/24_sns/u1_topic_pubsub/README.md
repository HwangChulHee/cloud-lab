# u1. SNS Topic / Publisher / Subscriber

## 1. Pub/Sub

SNS의 핵심은 Publisher와 Subscriber를 Topic으로 분리하는 것이다.

```text
Publisher
    │
    ▼
 SNS Topic
    │
    ├─ Subscriber A
    ├─ Subscriber B
    └─ Subscriber C
```

Publisher는 각 Subscriber의 주소나 개수를 몰라도 된다.

## 2. Topic

Topic은 메시지를 받는 논리적 채널이다.

```text
Order Service
   │ publish "OrderCreated"
   ▼
order-events Topic
```

구독자는 Topic을 subscribe한다.

## 3. Push Model

SNS는 SQS와 달리 Subscriber가 Queue를 poll하는 구조가 아니라 Topic이 Subscriber로 메시지를 전달하는 **push model**이다.

```text
SNS
→ Subscriber에게 전달

SQS
← Consumer가 poll
```

## 4. 여러 Subscriber

같은 메시지를 여러 목적에 전달할 수 있다.

```text
OrderCreated
   │
   ▼
 SNS Topic
   ├→ Billing
   ├→ Shipping
   └→ Analytics
```

하나의 이벤트를 여러 시스템이 각각 받아야 할 때 적합하다.

## 기억할 문장

> SNS는 하나의 Topic에 publish한 메시지를 여러 Subscriber에게 push하는 Pub/Sub 서비스다.
