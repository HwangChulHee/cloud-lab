# 10. Amazon RDS

SAA 강의의 `RDS, Aurora & ElastiCache` 섹션 중 **Amazon RDS** 부분을 정리한다.

RDS는 관계형 데이터베이스를 AWS가 관리형 서비스로 제공하는 서비스다. 시험에서는 단순히 "AWS의 DB"라고 외우기보다 **Read Replica와 Multi-AZ의 목적 차이**, **백업/복구**, **스토리지 확장**, **보안**, **RDS Proxy**를 구분하는 것이 중요하다.

이번 단원은 생소한 개념이 많으므로 각 유닛에서 용어를 먼저 풀고 실제 예시로 연결한다.

## Units

- [ ] u1. RDS Overview & Managed Database
- [ ] u2. Storage & Storage Auto Scaling
- [ ] u3. Read Replicas
- [ ] u4. Multi-AZ & Failover
- [ ] u5. Backups, Snapshots & Restore
- [ ] u6. Security, Encryption & Authentication
- [ ] u7. RDS Proxy & RDS Custom

## 전체 지도

```text
Application
    │
    ▼
Amazon RDS
├── PostgreSQL
├── MySQL
├── MariaDB
├── Oracle
├── SQL Server
└── DB2
```

RDS가 대신 관리하는 대표 영역:

```text
DB 설치
OS / DB 패치
백업
모니터링
장애 대응 일부
스토리지 관리
Multi-AZ 구성
```

사용자가 여전히 결정해야 하는 것:

```text
어떤 DB 엔진을 쓸지
DB Instance 크기
스토리지 유형과 크기
Multi-AZ 여부
Read Replica 여부
Security Group
백업 정책
애플리케이션 연결 구조
```

## 가장 중요한 SAA 구분

```text
읽기 부하를 분산하고 싶다
→ Read Replica

DB 장애 시 자동 Failover가 필요하다
→ Multi-AZ

특정 시점으로 DB를 복구하고 싶다
→ Automated Backup + Point-in-Time Restore

장기간 보관용 백업이 필요하다
→ Manual Snapshot

DB 연결 수가 너무 많아진다
→ RDS Proxy

RDS가 관리하는 OS/DB 환경에 직접 접근해 커스터마이징해야 한다
→ RDS Custom
```

## 대표 예시

쇼핑몰 DB를 생각하면 된다.

```text
Spring App
   │
   ▼
RDS PostgreSQL
   │
   ├── 상품
   ├── 주문
   └── 사용자
```

처음에는 RDS 하나로 충분할 수 있다.

사용자가 늘어난 뒤 상품 조회가 매우 많아지면:

```text
Write
Spring App ─────→ Primary RDS

Read
Spring App ─────→ Read Replica
```

장애 대응이 중요해지면:

```text
AZ-A
Primary RDS
    │ synchronous replication
    ▼
AZ-B
Standby RDS
```

이 구조가 Multi-AZ다.

다음 단원은 Aurora로 이어진다.
