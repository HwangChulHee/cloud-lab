# 68. Backup & Restore

Backup & Restore는 가장 기본적인 DR 전략이다.

강의에서는 **높은 RPO를 허용할 수 있고, 복구 시 resource를 다시 만들어도 되는 경우**의 전략으로 설명한다.

## Units

- [ ] [u1. Backup & Restore Architecture](./u1_architecture/README.md)
- [ ] [u2. AWS Backup](./u2_aws_backup/README.md)
- [ ] [u3. Backup Vault Lock / Cross-Region / Cross-Account](./u3_vault_lock_cross_region/README.md)
- [ ] [u4. SAA Selection](./u4_saa_selection/README.md)

## 구조

```text
Production
   ↓ scheduled backup / snapshot
S3 / Glacier / EBS Snapshot / RDS Snapshot / AMI
   ↓ disaster
Restore
   ↓
새 EC2 / RDS / Application Environment
```

## 강의에서 언급한 backup 수단

```text
EBS Snapshots
RDS automated backups / snapshots
AMI
S3 / S3 IA / Glacier
Lifecycle Policy
Cross-Region Replication
Snowball
Storage Gateway
```

## 특징

```text
상시 standby 환경이 거의 없음
비용 낮음
복구 시 restore/build 필요
RTO 큼
```
