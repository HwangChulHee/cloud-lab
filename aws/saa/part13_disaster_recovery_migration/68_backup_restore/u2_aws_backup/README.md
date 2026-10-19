# u2. AWS Backup

AWS Backup은 여러 AWS 서비스의 backup을 **중앙에서 관리하고 자동화**하는 fully managed service다.

## 강의에서 언급한 대상

```text
EC2 / EBS
S3
RDS / Aurora
DynamoDB
DocumentDB
Neptune
EFS
FSx
Storage Gateway Volume Gateway
```

## Backup Plan

```text
AWS Backup
   ↓
Backup Plan
   ├→ Frequency
   ├→ Backup Window
   ├→ Cold Storage Transition
   └→ Retention Period
```

강의에서는 다음 frequency 예시를 든다.

```text
every 12 hours
daily
weekly
monthly
cron expression
```

지원되는 서비스에서는 PITR도 사용할 수 있다.

## Policy 적용

Tag-based backup policy로 resource를 묶어 관리할 수 있다.

## 기억할 문장

> AWS Backup은 서비스별 backup script를 따로 만들지 않고 여러 AWS resource의 backup policy를 중앙화한다.
