# u4. Amazon MSK

Amazon MSK는 **Managed Streaming for Apache Kafka**다.

강의에서는 Kinesis Data Streams의 대안으로 소개한다.

## 역할

```text
Producers
   ↓
MSK Cluster
├─ Broker 1
├─ Broker 2
└─ Broker 3
   ↓
Consumers
```

## AWS가 관리하는 것

강의 핵심:

```text
Kafka broker nodes
ZooKeeper nodes
cluster create / update / delete
common Kafka failure recovery
```

## Network / HA

```text
VPC에 배치
Multi-AZ
최대 3 AZ
```

으로 구성해 high availability를 확보할 수 있다.

## Storage

Kafka data는 EBS volume에 원하는 기간 동안 저장할 수 있다고 설명한다.

## MSK Serverless

```text
Kafka capacity 직접 관리 안 함
AWS가 compute/storage provision 및 scale
```

## Kinesis와 비교

```text
Kinesis Data Streams
→ AWS-native streaming
→ shard model

Amazon MSK
→ Apache Kafka
→ broker/topic/partition model
→ Kafka ecosystem compatibility
```

## SAA 판단

```text
기존 Kafka workload
→ Amazon MSK

Kafka API / ecosystem 유지
→ MSK

AWS-native managed stream
→ Kinesis Data Streams
```
