# u5. SQS vs SNS vs Kinesis

이 세 서비스는 시험에서 자주 같이 비교된다.

## 한 줄 구분

```text
SQS
= Queue / Pull / 작업 분배

SNS
= Pub/Sub / Push / 여러 Subscriber에 fan-out

Kinesis Data Streams
= Real-time Streaming / Retention / Replay
```

## 데이터 흐름 비교

### SQS

```text
Producer → Queue ← Consumer poll
                  ↓
            성공 후 delete
```

### SNS

```text
Publisher → Topic
             ├→ Subscriber A
             ├→ Subscriber B
             └→ Subscriber C
```

### Kinesis

```text
Producer → Stream
            ├→ Consumer A
            ├→ Consumer B
            └→ Consumer C

records remain for retention period
```

## 대표 문제

```text
이미지 처리 작업을 Worker Pool에 분배
→ SQS

주문 생성 이벤트를 Billing/Shipping/Analytics 모두에게 전달
→ SNS 또는 SNS + SQS fan-out

초당 계속 들어오는 clickstream을 실시간 분석하고 나중에 replay
→ Kinesis Data Streams

실시간 데이터를 S3/OpenSearch로 관리형 전달
→ Amazon Data Firehose
```

## 최종 선택표

| 요구사항 | 선택 |
|---|---|
| Consumer가 pull | SQS |
| 하나의 작업을 Worker들이 경쟁 처리 | SQS |
| 여러 Subscriber에 push | SNS |
| 같은 이벤트를 여러 Queue에 복제 | SNS + SQS |
| Subscription별 filtering | SNS |
| 실시간 streaming | Kinesis Data Streams |
| Retention / replay | Kinesis Data Streams |
| S3 / Redshift / OpenSearch delivery | Amazon Data Firehose |

## 기억할 문장

> SQS는 작업 Queue, SNS는 이벤트 배포, Kinesis는 실시간 Stream이다.
