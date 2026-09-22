# 24. Amazon SNS

SNS(Simple Notification Service)는 **Pub/Sub 기반 메시징 서비스**다.

하나의 Producer가 Topic에 메시지를 publish하면 여러 Subscriber에게 같은 이벤트를 전달할 수 있다.

```text
Publisher
   │ Publish
   ▼
 SNS Topic
   ├─→ SQS
   ├─→ Lambda
   ├─→ Email
   └─→ HTTP/S Endpoint
```

## Units

- [x] [u1. Topic / Publisher / Subscriber](./u1_topic_pubsub/README.md)
- [x] [u2. Fan-Out with SQS](./u2_fanout_sqs/README.md)
- [x] [u3. Message Filtering / FIFO](./u3_filtering_fifo/README.md)
- [x] [u4. Security & SAA Selection](./u4_security_saa_selection/README.md)

## 핵심

```text
SQS
→ Queue 하나를 Consumer들이 pull

SNS
→ Topic 하나에서 여러 Subscriber로 push
```

SNS 단독보다 **SNS + SQS fan-out** 구조가 시험과 실제 아키텍처에서 자주 등장한다.

## SAA 선택 기준

```text
한 이벤트를 여러 시스템에 동시에 전달
→ SNS

각 구독자가 독립적으로 처리/재시도/버퍼링
→ SNS + SQS

구독자별로 특정 메시지만 받고 싶다
→ SNS Subscription Filter Policy

Pub/Sub + 순서 요구
→ SNS FIFO + SQS FIFO 조합 고려
```
