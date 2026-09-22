# 42. Lake Formation / QuickSight / MSK 등 Analytics 서비스

이 단원은 Data & Analytics 파트의 나머지 서비스를 **역할 중심으로 묶어서 비교**한다.

강의의 핵심 축:

```text
Lake Formation
→ Data Lake 구축 / 권한 관리

QuickSight
→ BI / Dashboard

Managed Service for Apache Flink
→ Stream Processing

Amazon MSK
→ Managed Apache Kafka
```

## Units

- [ ] [u1. AWS Lake Formation](./u1_lake_formation/README.md)
- [ ] [u2. Amazon QuickSight](./u2_quicksight/README.md)
- [ ] [u3. Managed Service for Apache Flink](./u3_managed_flink/README.md)
- [ ] [u4. Amazon MSK](./u4_msk/README.md)
- [ ] [u5. Analytics 서비스 최종 선택 지도](./u5_analytics_selection/README.md)

## 전체 그림

```text
Data Sources
   ↓
Glue / Lake Formation
   ↓
Data Lake on S3
   ├→ Athena
   ├→ Redshift
   ├→ EMR
   └→ QuickSight

Streaming
   ├→ Kinesis Data Streams
   ├→ Amazon MSK
   └→ Managed Service for Apache Flink
```
