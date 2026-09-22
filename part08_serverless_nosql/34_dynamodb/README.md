# 34. Amazon DynamoDB

Amazon DynamoDB는 AWS의 **serverless NoSQL database**다.

강의에서는 DynamoDB를 관계형 DB처럼 JOIN 중심으로 보는 것이 아니라, **Primary Key 설계 / Capacity Mode / Consistency / Index / DAX / Streams / Global Tables**를 중심으로 본다.

## Units

- [ ] [u1. Table / Item / Attribute / Primary Key](./u1_table_item_primary_key/README.md)
- [ ] [u2. Partition Key / Sort Key / Data Distribution](./u2_partition_sort_key/README.md)
- [ ] [u3. Read / Write Capacity Modes & Consistency](./u3_capacity_consistency/README.md)
- [ ] [u4. GSI / LSI / Query / Scan](./u4_indexes_query_scan/README.md)
- [ ] [u5. DAX / Cache](./u5_dax_cache/README.md)
- [ ] [u6. Streams / Global Tables / TTL](./u6_streams_global_tables_ttl/README.md)
- [ ] [u7. Backup / Import / Export / SAA Selection](./u7_backup_import_export_selection/README.md)

## 기본 구조

```text
DynamoDB Table
├─ Item
│  ├─ Partition Key
│  ├─ Sort Key (optional)
│  └─ Attributes
├─ Item
└─ Item
```

## 대표 serverless 구조

```text
Client
  ↓
API Gateway
  ↓
Lambda
  ↓
DynamoDB
```

## 가장 중요한 선택 기준

```text
serverless key-value / document database
→ DynamoDB

unpredictable traffic
→ On-Demand Capacity

predictable traffic
→ Provisioned + Auto Scaling

microseconds cache
→ DAX

item 변경 이벤트
→ DynamoDB Streams

multi-region active-active
→ Global Tables
```
