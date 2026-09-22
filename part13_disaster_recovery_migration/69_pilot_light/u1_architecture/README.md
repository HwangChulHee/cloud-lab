# u1. Pilot Light Architecture

강의 diagram의 핵심은 **database 같은 critical core는 AWS에서 이미 실행하고, application compute는 아직 full production 상태가 아니라는 것**이다.

```text
Primary Environment
      ↓ continuous/data replication
AWS DR Region
├─ Database: Running
├─ Compute: Stopped / minimal
└─ DNS: Route 53
```

## Backup & Restore보다 빠른 이유

Backup & Restore는 재해 후 database와 application을 restore해야 한다.

Pilot Light는 critical system이 이미 실행 중이므로 일부 restore/start 작업을 줄일 수 있다.

## 비용 감각

```text
Backup & Restore보다 높음
Warm Standby보다 낮음
```

상시 전체 application stack을 운영하지 않기 때문이다.
