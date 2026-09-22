# 13부 — Disaster Recovery & Migration

SAA 강의의 **Disaster Recovery & Migrations** 영역을 정리한다.

이 파트는 크게 두 덩어리로 본다.

```text
Disaster Recovery
→ RPO / RTO
→ Backup & Restore
→ Pilot Light
→ Warm Standby
→ Multi-Site / Hot Site

Migration
→ DMS / SCT
→ Application Discovery Service / Migration Hub
→ Application Migration Service (MGN)
→ Elastic Disaster Recovery (DRS)
→ Large Data Transfer 전략
```

## Chapters

- [ ] [67. RPO / RTO](./67_rpo_rto/README.md)
- [ ] [68. Backup & Restore](./68_backup_restore/README.md)
- [ ] [69. Pilot Light](./69_pilot_light/README.md)
- [ ] [70. Warm Standby](./70_warm_standby/README.md)
- [ ] [71. Multi-Site / Active-Active](./71_multi_site_active_active/README.md)
- [ ] [72. DMS / SCT](./72_dms_sct/README.md)
- [ ] [73. Application Migration Service / Migration Services](./73_application_migration_service/README.md)

## DR 전략 전체 지도

```text
비용 낮음
  │
  ▼
Backup & Restore
  ↓
Pilot Light
  ↓
Warm Standby
  ↓
Multi-Site / Hot Site
  │
  ▼
비용 높음

일반적으로 아래로 갈수록
→ RTO 감소
→ standby infrastructure 증가
```

## 먼저 구분할 것

```text
RPO
→ 허용 가능한 data loss 범위

RTO
→ 허용 가능한 downtime

Backup & Restore
→ backup에서 복구

Pilot Light
→ critical core만 항상 실행

Warm Standby
→ 전체 system을 minimum size로 실행

Multi-Site / Hot Site
→ full production scale을 여러 site에 실행
```

## Migration 전체 지도

```text
Migration Planning
→ Application Discovery Service
→ Migration Hub

Server Rehost
→ Application Migration Service (MGN)

Server Disaster Recovery
→ Elastic Disaster Recovery (DRS)

Database Data Migration
→ DMS

Database Schema Conversion
→ SCT

Large Offline Data Transfer
→ Snowball

Ongoing File/Data Synchronization
→ DataSync
```

## 시험에서 특히 중요한 비교

```text
RPO
vs
RTO
→ data loss vs downtime

Backup & Restore
vs Pilot Light
vs Warm Standby
vs Multi-Site
→ 평상시 어느 정도의 DR environment를 실행해 두는가?

DMS
vs SCT
→ data migration/replication vs schema conversion

MGN
vs DRS
→ server migration/cutover vs disaster recovery/failover

Snowball
vs DataSync
→ physical offline transfer vs network-based ongoing transfer
```

## 학습 순서

```text
67 RPO / RTO
      ↓
68 Backup & Restore
      ↓
69 Pilot Light
      ↓
70 Warm Standby
      ↓
71 Multi-Site
      ↓
72 DMS / SCT
      ↓
73 Server / Application Migration
```

## DR 설계에서 같이 떠올릴 AWS 기능

강의에서는 DR building block으로 다음을 함께 언급한다.

```text
EBS Snapshot / AMI
RDS Backup / Snapshot
S3 / Glacier / Lifecycle / Cross-Region Replication
Route 53
RDS Multi-AZ
RDS Cross-Region Replication
Aurora Global Database
Storage Gateway
Snowball
CloudFormation / Elastic Beanstalk
CloudWatch
Lambda
Site-to-Site VPN / Direct Connect
```

각 서비스 자체가 곧 하나의 DR 전략이라는 뜻은 아니고, 선택한 DR 전략을 구현하는 구성 요소로 본다.

## 학습 깊이

이 파트는 **Coverage ~ Hands-on 수준**이다.

시험 전에는 특히 다음 질문에 답할 수 있으면 된다.

```text
RPO와 RTO가 각각 무엇인가?
비용과 RTO 요구에 따라 어떤 DR 전략을 선택하는가?
Pilot Light와 Warm Standby는 무엇이 다른가?
DMS와 SCT는 각각 무엇을 담당하는가?
MGN과 DRS는 무엇이 다른가?
대량 migration에서 network와 Snowball 중 무엇을 선택할 것인가?
```

현재 첨부 강의 자료에서 Application Migration Service는 **lift-and-shift (rehost)**로 명시되어 있다. 전체 7R migration strategy 분류는 해당 자료 검색 결과에서 명확히 확인되지 않아 이 파트에는 별도 외부 지식으로 추가하지 않았다.
