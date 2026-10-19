# u3. Lazy Loading, Write Through & Cache Invalidation

## 지도 확인

ElastiCache를 쓴다고 자동으로 cache가 채워지는 것은 아니다. 애플리케이션이 **언제 cache를 읽고, 언제 DB를 읽고, 언제 cache를 갱신할지** 정해야 한다.

강의에서 핵심 패턴은 세 가지다.

```text
Lazy Loading
Write Through
Cache Invalidation
```

---

## 1. Lazy Loading

Lazy Loading은 데이터가 필요할 때 cache를 확인하고, 없으면 DB에서 읽어 cache에 저장하는 방식이다.

```text
Application
   ↓
Cache 조회
   │
   ├─ hit  → 반환
   │
   └─ miss → DB 조회
               ↓
           Cache 저장
               ↓
              반환
```

장점은 실제로 읽히는 데이터만 cache에 들어간다는 점이다.

단점은 cache 데이터가 오래되어 stale할 수 있다는 점이다.

---

## 2. Write Through

Write Through는 DB에 데이터를 쓸 때 cache도 함께 갱신하는 방식이다.

```text
Application
   ↓ write
Database
   ↓
Cache도 update
```

강의에서는 이 패턴을 **DB write 시 cache도 갱신해서 stale data를 줄이는 방식**으로 설명한다.

---

## 3. Cache Invalidation

DB의 원본 데이터가 바뀌었는데 cache가 예전 값을 가지고 있으면 문제가 생긴다.

```text
DB
price = 12000

Cache
price = 10000
```

그래서 cache에는 **무효화 전략(invalidation strategy)**이 필요하다.

대표적으로 생각할 수 있는 질문:

```text
언제 cache를 지울 것인가?
언제 새 값으로 덮어쓸 것인가?
얼마나 오래 보관할 것인가?
```

---

## 4. TTL과 연결해서 보기

Session Store나 일반 cache에서 TTL을 사용하면 일정 시간이 지난 데이터가 자동으로 만료되도록 설계할 수 있다.

```text
key 저장
↓
TTL 경과
↓
cache에서 만료
```

TTL도 stale data를 오래 유지하지 않게 하는 수단 중 하나다.

---

## SAA 판단

```text
처음 읽을 때만 cache에 적재
→ Lazy Loading

DB write 때 cache도 즉시 갱신
→ Write Through

오래된 cache 데이터가 문제
→ Invalidation / TTL 전략
```

## Recall Check

- Lazy Loading의 cache miss 흐름은?
- Write Through는 언제 cache를 갱신하는가?
- cache invalidation이 필요한 이유는?
