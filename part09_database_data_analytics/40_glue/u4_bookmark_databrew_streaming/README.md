# u4. Glue Job Bookmark / DataBrew / Studio / Streaming

강의의 고수준 기능을 정리한다.

## Job Bookmark

이전에 처리한 데이터를 다시 처리하지 않도록 진행 상태를 기억한다.

```text
Old Data
→ 이미 처리
→ skip

New Data
→ process
```

## Glue DataBrew

pre-built transformation을 사용해 데이터를 clean / normalize하는 서비스로 설명한다.

## Glue Studio

GUI를 이용해 Glue ETL job을 만들고 실행·모니터링할 수 있다.

## Glue Streaming ETL

Apache Spark Structured Streaming 기반이다.

강의에서 호환 source로 다음을 언급한다.

```text
Kinesis Data Streams
Kafka
Amazon MSK
```

## 기억할 것

```text
중복 ETL 방지
→ Job Bookmark

GUI ETL
→ Glue Studio

데이터 정리/normalize
→ DataBrew

streaming ETL
→ Glue Streaming
```
