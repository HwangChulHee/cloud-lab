# 12. Amazon ElastiCache

SAA 강의의 `RDS, Aurora & ElastiCache` 섹션 중 **Amazon ElastiCache** 부분을 정리한다.

ElastiCache는 Redis 또는 Memcached를 관리형으로 제공하는 **in-memory cache** 서비스다. 강의에서는 **DB read load 감소**, **cache hit / miss**, **Lazy Loading**, **Write Through**, **Session Store**, **Redis와 Memcached 선택**, **보안과 HA**를 핵심으로 다룬다.

## Units

- [ ] u1. ElastiCache Overview & Cache Flow
- [ ] u2. Redis vs Memcached
- [ ] u3. Lazy Loading, Write Through & Invalidation
- [ ] u4. Session Store & Stateless Application
- [ ] u5. Security, HA & SAA Selection

## 전체 지도

```text
Application
    │
    ├─ Cache hit
    │     ↓
    │ ElastiCache
    │
    └─ Cache miss
          ↓
         RDS
          ↓
      write to cache
```

캐시의 목적은 DB를 없애는 것이 아니다.

```text
RDS / Aurora
→ source of truth

ElastiCache
→ 자주 읽는 데이터를 메모리에 두고 빠르게 반환
```

## 가장 중요한 SAA 구분

```text
DB read 부하가 너무 크다
→ ElastiCache

같은 데이터를 반복 조회한다
→ Cache

여러 App Instance가 로그인 세션을 공유해야 한다
→ ElastiCache Session Store

데이터를 처음 요청할 때만 cache에 적재
→ Lazy Loading

DB write 때 cache도 함께 갱신
→ Write Through

복제 / HA / richer data structures가 필요한 cache
→ Redis 계열을 먼저 고려

단순 분산 in-memory cache
→ Memcached 고려
```

## 대표 예시

상품 상세 조회가 매우 많다고 하자.

```text
GET /products/100
      ↓
ElastiCache 확인
      │
      ├─ hit  → 바로 반환
      │
      └─ miss → RDS 조회
                  ↓
              cache 저장
                  ↓
                반환
```

이 구조는 RDS read 부하를 줄이고 응답 지연을 낮출 수 있다.

다만 cache를 쓰면 애플리케이션 코드가 cache hit/miss, TTL, invalidation을 고려해야 하므로 구조가 단순히 "DB 하나 추가"로 끝나지는 않는다.
