# u2. Redis vs Memcached

## 지도 확인

ElastiCache는 강의에서 **Redis 또는 Memcached를 관리형으로 제공하는 서비스**로 소개한다.

둘 다 in-memory cache지만 시험에서는 요구사항에 따라 어떤 engine이 더 자연스러운지 구분해야 한다.

```text
ElastiCache
├─ Redis
└─ Memcached
```

---

## 1. 공통점

둘 다 애플리케이션과 DB 사이에서 자주 읽는 데이터를 메모리에 보관해 latency와 DB read load를 줄이는 데 사용할 수 있다.

```text
Application
   ↓
Redis / Memcached
   ↓ cache miss
RDS / Aurora
```

둘 다 SQL 관계형 DB를 대체하는 서비스로 이해하면 안 된다.

---

## 2. Redis 쪽에서 강의가 강조하는 것

강의 요약에서는 Redis에 대해 다음 키워드가 함께 등장한다.

```text
Clustering
Multi-AZ
Read Replicas
Security / Redis Auth
Backup / Snapshot / PITR
```

또한 Redis Sorted Set을 이용한 real-time leaderboard 예시도 나온다.

```text
Game score update
      ↓
Redis Sorted Set
      ↓
real-time ranking
```

따라서 단순 cache를 넘어 복제/가용성/특정 자료구조 활용이 강조되는 문제에서는 Redis를 먼저 떠올린다.

---

## 3. Memcached는 어디에 놓고 볼까

강의에서는 ElastiCache가 Redis뿐 아니라 Memcached도 관리형으로 제공한다는 점을 알아야 한다.

SAA에서는 둘의 모든 내부 구현을 외우기보다 다음처럼 기억하는 편이 안전하다.

```text
고급 Redis 기능이 명시됨
→ Redis

단순 managed in-memory cache가 필요
→ Redis / Memcached 후보를 비교
```

---

## 4. 선택할 때 먼저 보는 것

```text
단순히 DB read load를 줄이는가?
복제와 HA가 중요한가?
Redis 전용 자료구조가 필요한가?
세션 저장 같은 key/value cache인가?
```

문제의 기능 요구사항을 보고 engine을 선택한다.

---

## SAA 판단

```text
real-time leaderboard
→ Redis Sorted Set

Multi-AZ / replica / richer Redis feature가 강조됨
→ Redis

일반적인 managed cache
→ ElastiCache를 먼저 떠올리고 Redis/Memcached 요구사항 비교
```

## Recall Check

- ElastiCache가 관리형으로 제공하는 두 engine은?
- Redis가 강의에서 더 자주 연결되는 HA/replica 키워드는?
- Redis leaderboard 예시는 어떤 자료구조를 사용하는가?
