# 73. Application Migration Service / Migration Services

이 단원은 database가 아니라 **server/application 자체를 AWS로 이전하는 서비스와 migration planning 도구**를 정리한다.

현재 첨부 강의에서 명확히 다루는 내용은 Application Discovery Service, Migration Hub, Application Migration Service(MGN), VMware Cloud on AWS, 대용량 data transfer 선택이다.

## Units

- [ ] [u1. Application Discovery Service / Migration Hub](./u1_discovery_migration_hub/README.md)
- [ ] [u2. Application Migration Service (MGN)](./u2_mgn/README.md)
- [ ] [u3. Elastic Disaster Recovery (DRS)](./u3_drs/README.md)
- [ ] [u4. VMware Cloud / Large Data Migration](./u4_vmware_large_data/README.md)
- [ ] [u5. Migration 서비스 선택 지도](./u5_selection/README.md)

## 전체 지도

```text
Migration Planning
→ Application Discovery Service
→ Migration Hub

Server Lift-and-Shift
→ Application Migration Service (MGN)

Server Disaster Recovery
→ Elastic Disaster Recovery (DRS)

Database Migration
→ DMS / SCT

Large Offline Data Transfer
→ Snowball

Ongoing Data Transfer
→ VPN / Direct Connect + DMS or DataSync
```

## Migration Strategy 범위

이 강의 자료에서 명시적으로 이름 붙여 설명하는 전략은 **MGN의 lift-and-shift (rehost)**다.

7R 전체 분류는 현재 첨부 자료 검색 결과에서 확인되지 않아 이 문서에는 억지로 추가하지 않았다.
