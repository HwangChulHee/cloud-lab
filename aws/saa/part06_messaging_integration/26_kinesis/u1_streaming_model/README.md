# u1. Kinesis Streaming Model

## 1. Streaming이란?

작은 데이터가 계속 생성되고 이를 순차적으로 받아 처리하는 모델이다.

```text
Click
Click
Metric
Log
IoT Event
   │
   ▼
Kinesis Data Streams
   │
   ▼
Real-time Consumer
```

SQS가 "해야 할 작업"을 Queue에 넣는 느낌이라면 Kinesis는 **계속 흐르는 데이터 기록(stream)**에 가깝다.

## 2. Producer

Producer는 Stream에 Record를 쓴다.

예:

```json
{
  "userId": 42,
  "page": "/products/7",
  "event": "CLICK"
}
```

Producer는 애플리케이션, SDK, Kinesis Agent 등이 될 수 있다.

## 3. Consumer

Consumer는 Stream을 읽어 실시간으로 처리한다.

예:

```text
Kinesis Data Streams
   ├→ Lambda
   ├→ Consumer Application
   ├→ Amazon Data Firehose
   └→ Managed Service for Apache Flink
```

## 4. Queue와 Stream의 차이 감각

```text
SQS
message 처리 후 삭제
작업 분배/decoupling

Kinesis
stream record를 일정 기간 보관
여러 Consumer가 독립적으로 읽기 가능
replay 가능
실시간 데이터 처리
```

## 기억할 문장

> Kinesis Data Streams는 지속적으로 발생하는 실시간 데이터를 받아 저장하고 여러 Consumer가 처리할 수 있게 하는 streaming 서비스다.
