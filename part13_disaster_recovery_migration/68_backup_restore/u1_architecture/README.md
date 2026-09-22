# u1. Backup & Restore Architecture

Backup & Restore의 핵심은 **평소에는 backup만 보관하고, 재해가 발생하면 resource를 다시 만드는 것**이다.

## 예시

```text
On-Prem / AWS Workload
      ↓ scheduled backup
S3 / Glacier / Snapshot / AMI
      ↓
   보관

재해 발생
      ↓
Restore Snapshot / AMI
      ↓
EC2 / RDS 재생성
      ↓
서비스 복구
```

강의 diagram에서는 Storage Gateway, Snowball, S3/Glacier, EBS Snapshot, RDS snapshot/backup, AMI 등을 함께 연결한다.

## 특징

```text
장점
→ 평상시 비용 낮음

단점
→ 재해 후 restore/build 시간이 필요
→ RTO가 큼
```

## 언제 적합한가?

```text
복구에 시간이 걸려도 괜찮음
backup data loss 범위 허용 가능
비용을 낮게 유지해야 함
```
