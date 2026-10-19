# u3. Amazon Managed Service for Apache Flink

과거 이름은 **Kinesis Data Analytics for Apache Flink**였다.

Apache Flink는 stream processing framework다.

## 역할

```text
Kinesis Data Streams / Amazon MSK
          ↓
Managed Service for Apache Flink
          ↓
Real-Time Stream Processing
```

## 강의 핵심

```text
Java / Scala / SQL
managed Flink cluster
parallel processing
automatic scaling
checkpoints / snapshots
stream transformation
```

## Data Firehose와 구분

강의는 Flink가 Amazon Data Firehose를 source로 직접 읽는 서비스가 아니라고 강조한다.

```text
Kinesis Data Streams
→ Flink 가능

Amazon MSK
→ Flink 가능

Data Firehose
→ source로 사용 X
```

## 언제 쓰나?

```text
streaming data를 실시간 변환
→ Managed Service for Apache Flink

단순 destination delivery
→ Amazon Data Firehose
```

## 기억할 문장

> Managed Service for Apache Flink는 Kinesis/MSK stream을 실시간으로 처리하고 변환하는 managed stream-processing 서비스다.
