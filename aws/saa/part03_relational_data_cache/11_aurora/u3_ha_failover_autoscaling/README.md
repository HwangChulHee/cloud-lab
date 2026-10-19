# u3. Aurora High Availability, Failover & Auto Scaling

## 지도 확인

Aurora는 storage와 compute 양쪽에서 가용성을 높이는 구조를 가진다.

```text
Storage
→ 3 AZ / 6 copies

Compute
→ Writer + Readers across AZs
```

---

## 1. Writer 장애

현재 Writer Instance에 장애가 생기면 Aurora는 Reader 중 하나를 새 Writer로 승격시키는 방식으로 failover할 수 있다.

```text
Before
Writer-A
Reader-B
Reader-C

Writer-A failure
      ↓
Reader-B promoted
      ↓
Writer-B
Reader-C
```

애플리케이션은 Writer Endpoint를 사용하므로 특정 instance hostname에 강하게 묶이지 않게 설계할 수 있다.

---

## 2. Reader가 있는 이유는 읽기 확장 + Failover 후보

Reader는 단순히 SELECT 처리량을 늘리는 역할만 있는 게 아니다.

```text
평상시
→ read scaling

Writer 장애 시
→ promotion candidate
```

따라서 여러 AZ에 Reader를 두면 가용성 설계와 연결된다.

---

## 3. Auto Scaling of Read Replicas

강의에서는 Aurora가 read workload에 맞춰 Reader 수를 자동 확장할 수 있다고 설명한다.

```text
Reader CPU / Connections 증가
        ↓
Auto Scaling
        ↓
Reader 추가
        ↓
Reader Endpoint를 통해 분산
```

반대로 부하가 줄어들면 Reader 수를 줄이는 방향으로 설정할 수 있다.

---

## 4. Storage Auto Scaling과 구분

둘은 목적이 다르다.

```text
Storage Auto Scaling
→ 저장할 데이터 양 증가 대응

Read Replica Auto Scaling
→ 읽기 처리량 증가 대응
```

시험에서 `storage is growing`과 `read traffic is growing`을 구분한다.

---

## 5. Backup / Restore도 Aurora에서 중요

강의는 Aurora에서도 backup & restore 옵션을 알아야 한다고 강조한다.

RDS에서 배운 개념과 연결한다.

```text
자동 백업
Snapshot
Restore
PITR
```

여기서는 Aurora 전용 구조에 집중하고, 백업의 기본 원리는 RDS 단원 내용을 재사용한다.

---

## RDS Multi-AZ와 비교

```text
RDS Multi-AZ
→ Primary + Standby
→ HA / failover 목적

Aurora
→ shared distributed storage
→ Writer + Readers
→ Reader가 failover candidate가 될 수 있음
→ Reader Endpoint로 read scaling도 수행
```

## SAA 판단

```text
DB 장애 자동 복구 + MySQL/PostgreSQL compatible Aurora
→ Writer Endpoint + multi-AZ readers 구조 이해

읽기 부하 자동 확장
→ Aurora Read Replica Auto Scaling

데이터 양 증가
→ Aurora storage auto scaling
```

## Recall Check

- Writer 장애 시 어떤 일이 일어나는가?
- Reader는 평상시와 장애 시 각각 어떤 역할을 할 수 있는가?
- Read Replica Auto Scaling과 Storage Auto Scaling의 차이는?
