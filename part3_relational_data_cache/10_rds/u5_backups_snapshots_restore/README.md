# u5. RDS Backups, Snapshots & Restore

## 1. 왜 백업이 필요한가

DB 장애는 서버 자체 문제만 있는 게 아니다.

예를 들어:

```text
운영자가 실수로 데이터 삭제
잘못된 배포가 대량 UPDATE 실행
테이블 데이터 손상
특정 시점으로 되돌릴 필요 발생
```

이런 경우에는 Multi-AZ가 있어도 해결되지 않을 수 있다.

Multi-AZ는 장애 시 계속 서비스하기 위한 고가용성 기능이고, **잘못 변경된 데이터 자체를 과거로 되돌리는 기능은 백업/복구 영역**이다.

---

## 2. Automated Backup

RDS는 자동 백업을 지원한다.

자동 백업을 사용하면 일정 보존 기간 안에서 과거 시점으로 복구할 수 있다.

강의에서는 Point-in-Time Restore를 최대 35일 범위까지 사용할 수 있다고 설명한다.

```text
월요일 10:00 정상
월요일 13:00 잘못된 DELETE 실행

복구 목표
→ 월요일 12:59 상태
```

이처럼 특정 시점을 지정해서 복구하는 것을 **Point-in-Time Restore(PITR)** 라고 한다.

---

## 3. Point-in-Time Restore란

이름을 그대로 보면 된다.

```text
Point in Time
= 특정 시점

Restore
= 복구
```

즉:

> "어제 백업본"처럼 딱 하나의 파일만 고르는 것이 아니라 보존 범위 안의 특정 시간으로 DB를 복원

하는 개념이다.

예:

```text
09:00 주문 100건
09:30 주문 120건
10:00 실수로 주문 테이블 삭제

복구 시점
09:59
```

처럼 사고 직전 상태를 목표로 잡을 수 있다.

---

## 4. Manual DB Snapshot

Snapshot은 DB 상태를 특정 시점에 저장한 백업본이라고 보면 된다.

```text
RDS
 ↓ snapshot
Manual Snapshot
```

Manual Snapshot은 자동 백업 보존 기간과 별개로 장기간 보관 목적으로 사용할 수 있다.

예:

```text
서비스 대규모 마이그레이션 직전
→ 수동 Snapshot 생성

중요 버전 배포 전
→ 수동 Snapshot 생성
```

---

## 5. Automated Backup과 Manual Snapshot 차이

```text
Automated Backup
→ AWS가 자동 수행
→ 보존 기간 설정
→ Point-in-Time Restore 가능

Manual Snapshot
→ 사용자가 직접 생성
→ 장기 보관에 적합
→ 필요할 때 Snapshot에서 Restore
```

시험에서는:

```text
"특정 시점으로 복구"
→ Automated Backup + PITR

"장기간 보관할 DB 백업"
→ Manual Snapshot
```

으로 구분하면 된다.

---

## 6. Restore는 기존 DB를 되감는 게 아니다

복구에서 중요한 사고방식이다.

RDS Restore는 일반적으로 기존 DB 안의 데이터를 제자리에서 과거 상태로 되돌리는 개념보다, **복구된 새 DB를 만드는 것**으로 이해하는 것이 좋다.

예:

```text
현재 RDS
mydb-prod

Snapshot Restore
    ↓
새 RDS
mydb-restored
```

그 다음 애플리케이션 연결을 새 DB Endpoint로 전환하는 식으로 운영할 수 있다.

즉:

```text
Restore 완료
≠ 애플리케이션이 자동으로 새 DB를 사용
```

이다.

---

## 7. Multi-AZ와 Backup은 서로 대체하지 않는다

이 부분도 자주 헷갈린다.

```text
Multi-AZ
→ DB 서버/AZ 장애 대응

Backup / Snapshot
→ 데이터 손실이나 과거 상태 복구
```

예를 들어 사용자가 실수로 전체 주문을 삭제했다.

Multi-AZ에서는 그 삭제도 Standby에 복제될 수 있다.

```text
Primary
DELETE orders
   ↓ replication
Standby
orders도 삭제됨
```

따라서 이런 문제는 Multi-AZ가 아니라 백업에서 해결해야 한다.

---

## 8. 예시 — 배포 사고

금요일 밤 신규 배포 후 잘못된 SQL이 실행됐다고 하자.

```sql
UPDATE products SET price = 0;
```

모든 상품 가격이 0원이 되었다.

가능한 대응 흐름:

```text
1. 문제 발생 시점 확인
2. 사고 직전 시점으로 PITR
3. 새 RDS 생성
4. 데이터 검증
5. Application 연결 전환
```

이런 식으로 백업/복구는 **장애 복구뿐 아니라 데이터 논리 오류 복구**에도 중요하다.

---

## SAA 판단

```text
DB 장애 시 자동 Failover
→ Multi-AZ

읽기 성능 확장
→ Read Replica

특정 시점으로 데이터 복구
→ Point-in-Time Restore

장기간 보관용 DB 백업
→ Manual Snapshot
```
