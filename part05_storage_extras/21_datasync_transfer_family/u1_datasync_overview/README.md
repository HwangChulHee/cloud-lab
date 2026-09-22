# u1. AWS DataSync 기본 구조

AWS DataSync는 **대량 데이터를 AWS와 on-premises/다른 cloud 사이 또는 AWS storage 간에 이동·동기화**하는 서비스다.

## 구조

```text
On-Premises / Other Cloud
        ↓
     DataSync
        ↓
S3 / EFS / FSx
```

강의에서는 다음 source를 예로 든다.

```text
NFS
SMB
HDFS
S3 API
```

## 목적

```text
large-scale data movement
migration
replication
synchronization
```

## 기억할 문장

> DataSync는 storage interface를 계속 제공하는 서비스가 아니라 데이터를 실제로 복사/동기화하는 managed transfer 서비스다.
