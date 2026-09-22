# 22. AWS Snow Family

AWS Snow Family는 **네트워크만으로 옮기기 어려운 대용량 데이터를 physical device로 이동하거나, 연결이 제한된 edge location에서 compute/storage를 수행**하는 서비스군이다.

강의의 핵심은 Snowball Edge를 이용한 offline migration과 edge computing이다.

## Units

- [ ] [u1. Snowball Data Migration](./u1_snowball_migration/README.md)
- [ ] [u2. Snowball Edge Storage vs Compute Optimized](./u2_storage_compute_optimized/README.md)
- [ ] [u3. Edge Computing](./u3_edge_computing/README.md)
- [ ] [u4. Snowball → Glacier / SAA Selection](./u4_glacier_selection/README.md)

## 기본 구조

```text
On-Premises
   ↓ local copy
Snowball Edge
   ↓ physical shipping
AWS
   ↓
Amazon S3
```

## 강의 핵심

```text
offline data migration
petabyte-scale
limited connectivity
limited bandwidth
high network cost
unstable connection
edge computing
```

## 대표 판단

강의에서는 **network transfer가 1주 이상 걸린다면 Snowball을 고려**하라고 설명한다.
