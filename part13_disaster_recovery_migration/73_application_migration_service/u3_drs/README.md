# u3. AWS Elastic Disaster Recovery (DRS)

AWS Elastic Disaster Recovery는 과거 **CloudEndure Disaster Recovery**라는 이름으로 제공되던 DR 서비스다.

## 역할

Physical / Virtual / Cloud-based server를 AWS로 빠르게 복구한다.

강의 use case:

```text
Oracle / MySQL / SQL Server 같은 critical database
SAP 같은 enterprise application
ransomware 대응을 위한 recovery
```

## 구조

```text
Source Server
Disks + OS + Apps + DB
       ↓
AWS Replication Agent
       ↓ continuous block-level replication
AWS Staging
Low-cost EC2 + EBS
       ↓ failover
AWS Production
Target EC2 + EBS
```

강의 diagram은 replication이 seconds 수준으로 계속되고 failover가 minutes 수준으로 가능한 구조를 보여준다.

Failback도 지원하는 흐름으로 설명된다.

## MGN과 차이

```text
MGN
→ Migration / cutover

DRS
→ Disaster Recovery / failover / failback
```

두 서비스 모두 continuous replication 개념을 사용하지만 목적이 다르다.
