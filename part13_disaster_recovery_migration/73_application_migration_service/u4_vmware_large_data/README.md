# u4. VMware Cloud on AWS / Large Data Migration

## VMware Cloud on AWS

기존 on-premises VMware vSphere 환경을 유지하면서 AWS로 확장하거나 migration할 수 있는 구조를 강의에서 다룬다.

대표 use case:

```text
VMware vSphere workload를 AWS로 migration
private / public / hybrid VMware 환경 운영
DR strategy
```

강의 diagram에서는 Direct Connect와 함께 EC2, S3, FSx, RDS, Redshift 같은 AWS 서비스와 연결한다.

---

## Large Data Transfer

강의에서는 200 TB 데이터를 옮기는 예로 network 방식과 Snowball을 비교한다.

핵심 결론은 다음과 같다.

```text
일회성 대규모 데이터
+ network로 너무 오래 걸림
→ Snowball 고려

ongoing replication / transfer
→ Site-to-Site VPN 또는 Direct Connect
  + DMS 또는 DataSync
```

Snowball은 DMS와 조합할 수도 있다고 설명한다.

## 기억할 문장

> 대규모 migration은 application/server뿐 아니라 data volume과 network transfer time까지 함께 설계해야 한다.
