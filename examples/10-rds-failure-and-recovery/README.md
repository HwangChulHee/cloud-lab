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

가능하면 reboot with failover 등의 기능으로 failover를 관찰하고 연결 끊김/복구 시간을 기록한다.

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

## 기억만으로 설명하기
Multi-AZ와 Read Replica를 `복제 방식 / 목적 / 앱 연결 / 장애 시 동작` 기준으로 설명한다.

## 완료 체크
- [ ] Backup retention과 snapshot을 확인했다.
- [ ] Restore가 새 DB를 만든다는 점을 확인했다.
- [ ] PITR의 목적을 설명할 수 있다.
- [ ] Multi-AZ와 Read Replica를 구분할 수 있다.
- [ ] 가능하면 failover 또는 replica를 직접 관찰했다.

## 비용 정리
Multi-AZ/Replica는 비용이 커질 수 있으므로 실습 후 즉시 정리한다.
