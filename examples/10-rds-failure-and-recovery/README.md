# Example 10 — RDS 장애, 백업, 복구 이해하기

이번에는 RDS를 단순히 연결하는 데서 끝내지 않고 **고가용성, 읽기 확장, 백업/복구의 목적 차이**를 직접 확인한다.

## Recall Check
- RDS를 Private하게 배치한 이유는?
- EC2 → RDS 연결에서 SG는 어떻게 설정했나?
- 연결 timeout이 났을 때 어떤 순서로 확인했나?

## 새로 배우는 것
- Multi-AZ
- Read Replica
- Automated Backup / Snapshot
- Point-in-Time Recovery(PITR)
- Failover

## 반복하는 것
RDS endpoint, RDS-SG, 애플리케이션 DB 연결, CloudWatch 기본 지표 확인을 다시 수행한다.

새로 만드는 태그 가능 리소스에는 가능한 한 다음을 적용한다.

```text
Project=cloud-lab
Stage=examples
Example=10
```

Name은 `example-10-*` 형식을 사용한다.

## 리소스 이름표

| 리소스 | 이름 |
| --- | --- |
| Primary RDS | `example-10-primary` |
| Manual Snapshot | `example-10-manual-snapshot` |
| Snapshot Restore DB | `example-10-restored` |
| PITR Restore DB | `example-10-pitr-restored` |
| Read Replica | `example-10-read-replica` |

Example 09의 VPC/DB Subnet Group/RDS Security Group을 재사용한다면 기존 이름을 유지한다. Multi-AZ Standby는 AWS가 관리하므로 별도 이름을 짓지 않는다.

## 핵심 구분
```text
Multi-AZ      = 가용성 / 장애 복구
Read Replica  = 읽기 확장
Backup/PITR   = 데이터 복구
```

## 실험 A — Backup과 Snapshot 확인
1. Automated Backup 설정과 retention을 확인한다.
2. Manual Snapshot을 하나 만든다.
3. Snapshot에서 restore하면 기존 DB를 덮는지 새 DB가 만들어지는지 확인한다.
4. PITR 화면에서 복구 가능한 시간 범위를 확인한다.

## 실험 B — Multi-AZ
비용을 고려해 가능할 때만 실제 Multi-AZ를 활성화한다.

확인할 것:
- 애플리케이션은 어떤 endpoint를 사용하고 있는가?
- Standby를 읽기 용도로 직접 사용할 수 있는가?
- Failover가 발생하면 애플리케이션이 DB 주소를 수동 변경해야 하는가?

가능하면 reboot with failover 등의 기능으로 failover를 관찰하고 연결 끊김/복구 시간을 기록한다. Endpoint 이름은 유지되더라도 기존 DB connection은 끊길 수 있으므로 애플리케이션의 reconnect 동작도 관찰한다.

## 실험 C — Read Replica
가능하면 Read Replica를 생성한다.

```text
Primary --async replication--> Read Replica
```

Primary에 데이터를 쓰고 Replica에서 읽는다. 복제 지연이 발생할 수 있다는 점을 확인한다.

## 비교 질문
- 읽기 요청이 너무 많다 → Multi-AZ인가 Read Replica인가?
- AZ 장애가 걱정된다 → 무엇을 쓸까?
- 사용자가 실수로 데이터를 삭제했다 → 무엇이 필요한가?
- Read Replica의 데이터가 항상 즉시 최신이라고 보장할 수 있는가?

## 장애 실험 — DB 연결 추적
Failover 또는 일시적 DB 중단 시 애플리케이션 로그, RDS 상태, CloudWatch DBConnections 등을 함께 본다.

## CLI 구축/복구 검증

### 1. Primary / Multi-AZ / Replica 관계

```bash
aws rds describe-db-instances --region $AWS_REGION \
  --query "DBInstances[?contains(DBInstanceIdentifier, 'example-10')].{Id:DBInstanceIdentifier,Status:DBInstanceStatus,MultiAZ:MultiAZ,AZ:AvailabilityZone,SecondaryAZ:SecondaryAvailabilityZone,ReplicaSource:ReadReplicaSourceDBInstanceIdentifier,ReadReplicas:ReadReplicaDBInstanceIdentifiers,BackupRetention:BackupRetentionPeriod,Endpoint:Endpoint.Address}"
```

이 출력 하나로 다음을 구분한다.

```text
MultiAZ
→ standby/failover 구성 여부

ReadReplicaSourceDBInstanceIdentifier
→ 이 DB가 어떤 Primary의 Replica인지

ReadReplicaDBInstanceIdentifiers
→ 이 DB가 가진 Replica 목록

BackupRetentionPeriod
→ Automated Backup 보존 기간
```

### 2. Failover 관련 Event

```bash
aws rds describe-events --region $AWS_REGION \
  --source-type db-instance \
  --duration 180 \
  --query 'Events[].{Time:Date,Source:SourceIdentifier,Message:Message}' \
  --output table
```

최근 180분 동안의 RDS Instance Event를 조회한다. Failover를 수행했다면 **시간 순서와 Message**를 애플리케이션 연결 끊김/복구 시점과 맞춰 본다.

### 3. Snapshot

```bash
aws rds describe-db-snapshots --region $AWS_REGION \
  --snapshot-type manual \
  --query "DBSnapshots[?contains(DBSnapshotIdentifier, 'example-10')].[DBSnapshotIdentifier,Status,SnapshotCreateTime]"
```

Manual Snapshot이 실제 생성되었고 `available`인지 확인한다.

실습 종료 시 DB Instance와 Snapshot을 **각각 따로 조회**한다. Instance가 없다고 비용/데이터 리소스가 모두 사라진 것은 아니다.

## 기억만으로 설명하기
Multi-AZ와 Read Replica를 `복제 방식 / 목적 / 앱 연결 / 장애 시 동작` 기준으로 설명한다.

## 완료 체크
- [ ] Backup retention과 snapshot을 확인했다.
- [ ] Restore가 새 DB를 만든다는 점을 확인했다.
- [ ] PITR의 목적을 설명할 수 있다.
- [ ] Multi-AZ와 Read Replica를 구분할 수 있다.
- [ ] 가능하면 failover 또는 replica를 직접 관찰했다.
- [ ] CLI로 RDS/Replica/Snapshot 상태를 검증했다.

## 비용 정리와 삭제 검증

Multi-AZ/Replica는 비용이 커질 수 있으므로 실습 후 즉시 정리한다. 특히 다음을 따로 확인한다.

```text
Primary/복구 DB instance
Read Replica
Manual Snapshot
```

삭제 후 [CLI Verification Guide](../CLI_VERIFICATION.md)의 Example 10 삭제 검증을 실행한다. Manual Snapshot은 DB instance를 삭제해도 별도로 남을 수 있으므로 반드시 따로 확인한다.

---
