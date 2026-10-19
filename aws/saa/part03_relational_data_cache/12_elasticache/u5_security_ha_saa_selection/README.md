# u5. Security, High Availability & SAA Selection

## 지도 확인

ElastiCache도 VPC 안에서 애플리케이션과 연결되는 데이터 계층이므로 **누가 접근할 수 있는지**, **장애 시 어떻게 복구되는지**, **어떤 cache engine을 선택할지**를 함께 본다.

강의 요약에서는 ElastiCache의 보안과 가용성 관련 키워드를 다음처럼 정리한다.

```text
Security Groups
IAM
KMS
Redis Auth
Multi-AZ
Read Replicas
Backup / Snapshot / PITR
```

---

## 1. Security Group

웹 애플리케이션 구조에서는 ElastiCache를 인터넷에 직접 노출하기보다 애플리케이션 계층만 접근하도록 제한한다.

```text
Internet
   ↓
ALB
   ↓
EC2 / App SG
   ↓
ElastiCache SG
source = App SG
```

강의의 Stateful Web App 예시에서도 ElastiCache로의 접근을 EC2 Security Group에서 온 트래픽으로 제한한다.

핵심은:

```text
사용자 → ElastiCache 직접 접근
X

Application → ElastiCache
O
```

이다.

---

## 2. Encryption / Authentication

강의 요약에서는 다음을 보안 요소로 제시한다.

```text
KMS
Redis Auth
IAM
Security Groups
```

시험에서는 네트워크 접근 제어와 인증/암호화가 서로 다른 계층이라는 점을 구분한다.

```text
Security Group
→ 네트워크 접근 제어

Auth / IAM
→ 인증 및 권한

KMS
→ 저장 데이터 암호화와 연결
```

---

## 3. High Availability

강의에서는 Redis 쪽에서 Multi-AZ와 Read Replica, clustering 같은 확장/가용성 기능을 함께 다룬다.

```text
Primary
   ↓ replication
Replica
```

가용성이 중요한 cache라면 단일 node 한 대만 두는 구조보다 복제와 Multi-AZ 구성을 고려한다.

---

## 4. Backup / Snapshot / Recovery

강의 요약에는 ElastiCache의 Backup / Snapshot / Point-in-Time Restore 기능도 포함된다.

캐시는 흔히 재생성 가능한 데이터라고 생각하기 쉽지만, 실제 요구사항과 engine 기능에 따라 backup/recovery 옵션이 중요할 수 있다.

시험에서는 서비스 특성상 "cache니까 무조건 backup이 필요 없다"고 단정하지 않는다.

---

## 5. RDS / Aurora / ElastiCache 선택 지도

```text
관계형 SQL / transaction
→ RDS 또는 Aurora

MySQL/PostgreSQL compatible + Aurora 전용 분산 구조
→ Aurora

DB read 결과를 메모리에 cache
→ ElastiCache

여러 앱 인스턴스가 session 공유
→ ElastiCache

real-time leaderboard
→ Redis Sorted Set
```

---

## 완료 체크

- [ ] ElastiCache가 DB read load를 줄이는 흐름을 설명할 수 있다.
- [ ] Cache Hit / Miss를 설명할 수 있다.
- [ ] Lazy Loading과 Write Through를 구분할 수 있다.
- [ ] Session Store가 stateless app에 왜 도움이 되는지 설명할 수 있다.
- [ ] Security Group으로 App 계층만 ElastiCache에 접근시키는 구조를 설명할 수 있다.
- [ ] Redis 관련 Multi-AZ / Read Replica / clustering 키워드를 기억한다.
- [ ] RDS/Aurora와 ElastiCache의 역할을 구분할 수 있다.

## 기억만으로 설명하기

다음 두 그림을 빈 종이에 그린다.

```text
Application → ElastiCache → RDS/Aurora
```

그리고:

```text
ALB → App A/B/C → shared Session Store
```

각 화살표가 왜 필요한지 설명한다.
