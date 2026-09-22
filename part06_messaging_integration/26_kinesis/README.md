# 26. Amazon Kinesis

SAA 강의의 Kinesis 영역은 **실시간 streaming 데이터**를 처리하는 선택 기준을 이해하는 것이 핵심이다.

```text
Producers
   │
   ▼
Kinesis Data Streams
   │
   ├→ Consumer App
   ├→ Lambda
   └→ Amazon Data Firehose
```

## Units

- [ ] [u1. Streaming Model & Data Streams](./u1_streaming_model/README.md)
- [ ] [u2. Shard / Partition / Ordering / Capacity](./u2_shards_partition_capacity/README.md)
- [ ] [u3. Consumers / Retention / Replay](./u3_consumers_retention_replay/README.md)
- [ ] [u4. Amazon Data Firehose](./u4_data_firehose/README.md)
- [ ] [u5. SQS vs SNS vs Kinesis](./u5_selection_comparison/README.md)

## 대표 사용 사례

```text
Click Stream
IoT Device Events
Application Metrics
Logs
Real-time Analytics
```

## 핵심 구분

```text
Kinesis Data Streams
→ 실시간 stream 저장
→ Producer / Consumer
→ retention
→ replay 가능
→ shard / capacity 개념

Amazon Data Firehose
→ destination으로 전달하는 managed delivery
→ near real-time
→ 자동 scaling
→ S3 / Redshift / OpenSearch 등
→ replay용 stream 저장소가 아님
```
