# u4. Messaging / Integration 최종 선택 지도

6부 전체를 요구사항 기준으로 정리한다.

## 1. SQS

```text
핵심 단어
Queue
Pull
Decoupling
Buffer
Worker
DLQ
Visibility Timeout
```

대표 문제:

```text
API 요청 이후 무거운 작업을 비동기로 처리
→ SQS
```

## 2. SNS

```text
핵심 단어
Pub/Sub
Push
Fan-Out
Subscribers
Filter Policy
```

대표 문제:

```text
하나의 주문 이벤트를 여러 시스템에 전파
→ SNS
```

Consumer마다 durable queue가 필요하면:

```text
SNS → SQS A
    → SQS B
    → SQS C
```

## 3. EventBridge

```text
핵심 단어
Event Bus
Rules
AWS Events
Schedule
SaaS Integration
Routing
```

대표 문제:

```text
EC2 state change나 S3 event를 조건에 따라 Lambda/ECS/SNS로 routing
→ EventBridge
```

## 4. Kinesis Data Streams

```text
핵심 단어
Real-time
Stream
Shard
Partition Key
Retention
Replay
```

대표 문제:

```text
clickstream을 실시간 분석하고 과거 데이터 재처리
→ Kinesis Data Streams
```

## 5. Amazon Data Firehose

```text
핵심 단어
Managed Delivery
Near Real-Time
Automatic Scaling
S3 / Redshift / OpenSearch
```

대표 문제:

```text
streaming 데이터를 코드/Shard 관리 없이 S3로 전달
→ Amazon Data Firehose
```

## 6. Amazon MQ

```text
핵심 단어
Existing Application
Message Broker
MQTT / AMQP / STOMP / OpenWire / WSS
Migration
Minimal Code Change
```

대표 문제:

```text
기존 on-premises broker 기반 애플리케이션을 최소 변경으로 AWS 이전
→ Amazon MQ
```

## 최종 비교

| 요구사항 | 선택 |
|---|---|
| 작업 Queue / Worker decoupling | SQS |
| 여러 Subscriber에게 동일 이벤트 배포 | SNS |
| AWS/SaaS 이벤트 rule routing | EventBridge |
| 실시간 데이터 stream + replay | Kinesis Data Streams |
| Streaming 데이터를 destination에 전달 | Amazon Data Firehose |
| 기존 broker protocol 유지 | Amazon MQ |

## 기억할 문장

> SQS는 작업 Queue, SNS는 이벤트 배포, EventBridge는 이벤트 Routing, Kinesis는 실시간 Stream, Amazon MQ는 기존 Message Broker 호환이다.
