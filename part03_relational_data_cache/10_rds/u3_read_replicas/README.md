# u3. RDS Read Replicas

## 지도 확인

Read Replica는 이름 그대로 **읽기 전용 복제본**이다.

Primary DB의 데이터를 복제해서 읽기 요청을 나눠 처리한다.

```text
             ┌→ Read Replica 1
Application ─┤
             └→ Read Replica 2
        │
        └────→ Primary RDS
              write
```

핵심 목적은 **Read Scalability**, 즉 읽기 확장이다.

---

## 1. 왜 Read Replica가 필요한가

쇼핑몰 DB를 생각해보자.

쓰기 요청:

```text
주문 생성
회원 정보 수정
상품 재고 변경
```

읽기 요청:

```text
상품 목록 조회
상품 상세 조회
주문 내역 조회
통계 조회
```

실제 서비스에서는 읽기가 쓰기보다 훨씬 많을 수 있다.

모든 요청이 Primary DB 한 대로 몰리면:

```text
SELECT
SELECT
SELECT
INSERT
SELECT
UPDATE
SELECT
...
```

Primary가 바빠진다.

이때 Read Replica를 두고 SELECT 요청 일부를 분산한다.

```text
Write
→ Primary

Read
→ Primary 또는 Read Replica
```

---

## 2. Replication이란

Replication은 **데이터를 다른 DB에 복제해서 따라가게 만드는 것**이다.

예:

```text
Primary
users = 100명
orders = 5,000건

↓ replication

Read Replica
users = 100명
orders = 5,000건
```

Primary에 새로운 주문이 들어오면 Replica에도 그 변경 내용이 전달된다.

---

## 3. ASYNC Replication

RDS Read Replica는 강의에서 **비동기(ASYNC) 복제**로 설명한다.

비동기는 쉽게 말하면:

> Primary가 Replica 반영 완료까지 기다리지 않고 먼저 일을 끝낸다.

예:

```text
1. 사용자 주문 생성
2. Primary에 주문 저장
3. 사용자에게 성공 응답
4. 잠시 뒤 Replica에 변경 반영
```

그래서 아주 짧은 시간 동안:

```text
Primary
order #100 있음

Replica
order #100 아직 없음
```

같은 상황이 생길 수 있다.

이 차이를 **Replica Lag**이라고 생각하면 된다.

---

## 4. Eventually Consistent

Read Replica가 비동기 복제를 사용하기 때문에 읽기는 **Eventually Consistent**할 수 있다.

뜻은:

> 지금 당장은 데이터가 약간 다를 수 있지만 시간이 지나면 결국 같아진다.

예를 들어 사용자가 방금 주문을 생성했다.

```text
POST /orders
→ Primary 저장 성공
```

그리고 바로:

```text
GET /orders/100
→ Read Replica 조회
```

했는데 복제가 아직 안 됐다면 잠시 조회되지 않을 수도 있다.

따라서 **쓰기 직후 반드시 최신 값이 필요한 조회**는 Primary를 읽도록 설계하는 경우도 있다.

---

## 5. Read Replica는 어디에 둘 수 있나

강의에서는 Read Replica를 다음처럼 구성할 수 있다고 설명한다.

```text
Same AZ
Cross AZ
Cross Region
```

즉 같은 AZ뿐 아니라 다른 AZ나 다른 Region에도 만들 수 있다.

Cross Region Read Replica는 다른 Region에서 읽기 성능을 높이거나 DR 설계와 연결될 수 있지만, 일반적인 같은 Region 복제보다 네트워크 비용/복잡도를 고려해야 한다.

---

## 6. Reporting Application 예시

Production DB가 정상적으로 서비스 중이라고 하자.

```text
Production App
      │
      ▼
Primary RDS
```

그런데 회사에서 매일 무거운 통계 SQL을 돌리기 시작했다.

```sql
SELECT ...
GROUP BY ...
JOIN ...
```

이걸 Primary에서 실행하면 실제 고객 서비스 DB에 부담을 준다.

그래서:

```text
Production App → Primary RDS

Reporting App  → Read Replica
```

로 분리한다.

고객 서비스 부하와 분석 조회 부하를 나누는 것이다.

---

## 7. Read Replica는 자동으로 애플리케이션이 사용하는 게 아니다

Read Replica를 만들었다고 해서 애플리케이션의 SELECT가 자동으로 분산되는 것은 아니다.

각 Replica는 별도의 DB Endpoint를 가진다.

예:

```text
Primary Endpoint
mydb.xxxx.rds.amazonaws.com

Replica Endpoint
mydb-read.xxxx.rds.amazonaws.com
```

애플리케이션이 읽기 연결을 Replica Endpoint로 보내도록 구성해야 한다.

즉:

```text
Read Replica 생성
≠ 자동 read load balancing
```

이다.

---

## 8. Replica Promotion

Read Replica를 독립적인 DB로 **Promote**할 수 있다.

Promote = 복제 관계를 끊고 독립된 일반 DB로 승격시키는 것.

```text
Primary
   ↓ replication
Read Replica

Promote
   ↓
독립 DB
```

Promote 이후에는 더 이상 기존 Primary의 변경사항을 따라가는 Read Replica가 아니다.

---

## 9. Read Replica와 Multi-AZ는 목적이 다르다

이 구분은 SAA에서 매우 중요하다.

```text
Read Replica
목적: 읽기 성능 확장
Replica에서 SELECT 가능
비동기 복제
애플리케이션이 Replica Endpoint를 사용

Multi-AZ
목적: 고가용성 / 장애 대응
Standby는 일반적으로 읽기 분산용이 아님
동기식 복제
장애 시 자동 Failover
```

문제에서:

```text
"read-heavy workload"
"reporting query"
"read scalability"
```

가 나오면 Read Replica를 먼저 떠올린다.

```text
"high availability"
"automatic failover"
```

가 나오면 Multi-AZ다.

---

## SAA 판단

```text
읽기 트래픽이 너무 많다
→ Read Replica

운영 DB에 영향 없이 통계/리포트 조회
→ Read Replica

다른 Region의 사용자에게 DB 읽기 지연 감소
→ Cross-Region Read Replica 고려

DB 장애 시 자동 전환
→ Read Replica가 아니라 Multi-AZ
```
