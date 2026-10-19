# u3. Specialized Databases

## Amazon DocumentDB

강의는 DocumentDB를 **MongoDB용 managed database 선택지**로 분류한다.

```text
기존 MongoDB 계열 workload
→ Amazon DocumentDB 고려
```

## Amazon Neptune

Graph database다.

대표 use case:

```text
fraud detection
recommendation engines
social networking
```

관계 자체가 중요한 데이터에 적합하다.

Neptune Streams는 graph data 변경을 실시간 순서대로 제공하는 기능으로 설명된다.

## Amazon Keyspaces

Apache Cassandra-compatible managed database다.

강의 핵심:

```text
serverless
scalable
multi-AZ replication
CQL
on-demand / provisioned
single-digit millisecond latency
PITR
```

대표 use case:

```text
IoT device information
time-series-like large distributed data
```

## Amazon Timestream

serverless time-series database다.

강의 핵심:

```text
IoT
operational metrics
real-time analytics
SQL compatibility
recent data in memory
historical data in cost-optimized storage
```

## Amazon QLDB

강의 Database Types 분류에서 **Ledger database**로 구분한다.

이 파트에서는 서비스 선택 수준으로만 기억한다.
