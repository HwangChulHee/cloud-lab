# u4. Amazon Data Firehose

강의에서는 과거 이름인 **Kinesis Data Firehose**도 함께 언급한다.

현재 개념은 streaming 데이터를 목적지로 전달하는 **fully managed delivery service**로 이해하면 된다.

## 구조

```text
Producers
   │
   ▼
Amazon Data Firehose
   │
   ├→ S3
   ├→ Redshift
   ├→ OpenSearch
   ├→ 3rd-party
   └→ Custom HTTP Endpoint
```

## 1. Fully Managed

Data Streams처럼 shard를 직접 관리하는 것이 아니라 delivery와 scaling을 관리형으로 제공한다.

```text
자동 scaling
serverless
사용량 기반
```

## 2. Near Real-Time

Data Firehose는 buffering을 사용하기 때문에 Data Streams의 실시간 처리와 구분해서 **near real-time**으로 본다.

```text
Record
Record
Record
   │
   ▼
Buffer
(size / time)
   │
   ▼
Destination에 batch write
```

## 3. Transformation

Lambda를 이용해 delivery 전에 데이터를 변환할 수 있다.

예:

```text
CSV
→ Lambda Transform
→ JSON
→ S3
```

강의에서는 format conversion과 compression도 함께 다룬다.

## 4. Data Streams와 함께 사용

```text
Producer
   ↓
Kinesis Data Streams
   ↓
Amazon Data Firehose
   ↓
S3
```

Streams는 실시간 수집/보관/replay 역할, Firehose는 destination delivery 역할로 나눌 수 있다.

## 선택 기준

```text
실시간 Consumer 코드 / replay
→ Kinesis Data Streams

S3/Redshift/OpenSearch에 관리형으로 전달
→ Amazon Data Firehose

직접 shard 관리 없이 destination delivery
→ Firehose
```
