# u1. ElastiCache Overview & Cache Flow

## 지도 확인

ElastiCache는 Redis 또는 Memcached를 AWS가 관리형으로 제공하는 **in-memory data store**다.

강의에서는 RDS가 관계형 DB를 관리형으로 제공하는 것처럼, ElastiCache는 cache engine을 관리형으로 제공한다고 설명한다.

```text
Application
   ↓
ElastiCache
   ↓ cache miss
RDS / Aurora
```

---

## 1. 왜 Cache를 쓰는가

메모리는 디스크보다 빠르다.

자주 조회되는 데이터를 메모리에 저장하면 매번 DB까지 가지 않아도 된다.

예:

```text
상품 상세 조회 100만 번

Cache 없음
→ 100만 번 DB 조회 가능

Cache 있음
→ 첫 조회는 DB
→ 이후 많은 조회는 Cache
```

그래서 ElastiCache는 **read-heavy workload에서 DB 부하를 줄이고 latency를 낮추는 데** 사용한다.

---

## 2. Cache Hit

원하는 데이터가 cache에 이미 있으면 Cache Hit다.

```text
Application
   ↓ GET product:100
ElastiCache
   ↓ found
Response
```

DB에 가지 않아도 되므로 빠르게 응답할 수 있다.

---

## 3. Cache Miss

원하는 데이터가 cache에 없으면 Cache Miss다.

```text
Application
   ↓
ElastiCache
   ↓ miss
RDS
   ↓ read
Application
   ↓
ElastiCache에 저장
```

이후 같은 요청은 hit가 될 수 있다.

---

## 4. Source of Truth는 누구인가

일반적인 DB cache 구조에서 원본 데이터는 RDS/Aurora에 있고 ElastiCache는 복사본을 가진다.

```text
RDS / Aurora
→ source of truth

ElastiCache
→ temporary cached copy
```

따라서 cache 데이터가 사라져도 DB에서 다시 읽어 채울 수 있는 구조를 많이 사용한다.

---

## 5. 관리형 서비스

강의에서는 AWS가 다음과 같은 관리 작업을 담당한다고 설명한다.

```text
OS maintenance / patching
setup / configuration
monitoring
failure recovery
backup 등
```

하지만 애플리케이션은 여전히 cache 사용 로직을 알아야 한다.

```text
cache lookup
hit / miss 처리
TTL
invalidation
fallback to DB
```

그래서 강의는 **ElastiCache를 사용하면 애플리케이션 코드 변경이 많이 필요할 수 있다**고 강조한다.

---

## SAA 판단

```text
read-heavy workload
DB 조회 결과를 반복 사용
낮은 latency 필요
→ ElastiCache 고려

관계형 SQL/transaction 자체가 필요
→ RDS / Aurora
```

## Recall Check

- Cache Hit와 Cache Miss는 무엇인가?
- ElastiCache가 DB load를 줄이는 이유는?
- 일반적인 cache 구조에서 source of truth는 어디인가?
- ElastiCache를 추가하면 왜 애플리케이션 코드 변경이 필요할 수 있는가?
