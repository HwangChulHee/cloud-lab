# u4. RDS Multi-AZ & Failover

## 지도 확인

Multi-AZ는 **가용성을 높이기 위한 구성**이다.

Primary DB를 한 Availability Zone에 두고, 다른 AZ에 Standby DB를 둔다.

```text
AZ-A
Primary RDS
    │
    │ synchronous replication
    ▼
AZ-B
Standby RDS
```

핵심 목적은 **성능 확장보다 장애 대응**이다.

---

## 1. 왜 다른 AZ에 Standby를 두나

한 AZ에만 DB가 있다면:

```text
AZ-A 장애
→ DB 사용 불가
→ 애플리케이션 영향
```

Multi-AZ에서는 다른 AZ에 Standby가 있기 때문에 Primary에 문제가 생겼을 때 대체할 수 있다.

```text
AZ-A Primary 장애
        ↓
Failover
        ↓
AZ-B Standby가 새 Primary 역할
```

---

## 2. Standby란 무엇인가

Standby는 말 그대로 **대기 중인 DB**다.

중요한 점:

> 일반적인 Multi-AZ Standby는 Read Replica처럼 읽기 트래픽을 분산하기 위해 두는 것이 아니다.

즉:

```text
Application
   │
   ▼
Primary
   │ replication
   ▼
Standby
```

애플리케이션의 평상시 읽기/쓰기는 Primary로 간다.

Standby는 장애 시 대체하기 위한 목적이 중심이다.

---

## 3. Synchronous Replication

Multi-AZ는 강의에서 동기식 복제로 설명한다.

동기식은 개념적으로:

```text
Primary에 쓰기
→ Standby에도 반영
→ 쓰기 완료 처리
```

처럼 데이터 일관성을 더 강하게 맞춘다.

Read Replica의 비동기 복제와 대비하면 된다.

```text
Read Replica
→ ASYNC
→ 읽기 확장

Multi-AZ Standby
→ SYNC
→ 고가용성
```

---

## 4. Failover란

Failover는 장애가 난 주 시스템 대신 대기 시스템으로 **자동 전환**하는 것이다.

예를 들어:

```text
Primary DB host 장애
```

가 발생하면 Multi-AZ 구성에서 AWS가 Standby 쪽으로 전환한다.

애플리케이션 관점에서는 기존 RDS Endpoint를 계속 사용하고, AWS가 그 Endpoint가 새 Primary를 가리키도록 처리한다.

개념적으로:

```text
Before
mydb.rds.amazonaws.com
        ↓
Primary in AZ-A

After Failover
mydb.rds.amazonaws.com
        ↓
New Primary in AZ-B
```

그래서 애플리케이션이 새 DB IP를 직접 찾아서 설정을 바꾸는 방식이 아니다.

---

## 5. 어떤 상황에서 Failover가 일어날 수 있나

대표적으로 다음 같은 장애를 생각하면 된다.

```text
Primary DB instance 장애
AZ 장애
네트워크 문제
DB instance 교체가 필요한 유지보수
```

시험에서는 세부 트리거를 모두 외우기보다:

> **Primary를 사용할 수 없을 때 Standby로 자동 전환**

이라는 목적을 이해하면 된다.

---

## 6. 예시 — 주문 DB

주문 DB가 한 AZ에만 있다고 하자.

```text
Users
  ↓
Application
  ↓
RDS in AZ-A
```

AZ-A가 장애 나면 주문 생성이 멈춘다.

Multi-AZ로 구성하면:

```text
              AZ-A
Application → Primary RDS
                 │
                 ▼ sync
              AZ-B
              Standby RDS
```

Primary 장애 시:

```text
AZ-A Primary X
      ↓ failover
AZ-B Standby → Primary
```

가 된다.

---

## 7. Read Replica와 헷갈리지 않기

### 문제 1

"쇼핑몰 상품 조회 요청이 너무 많아 DB CPU가 높다."

```text
답: Read Replica
```

읽기를 분산해야 하기 때문이다.

### 문제 2

"DB 인스턴스 또는 AZ 장애가 발생해도 서비스가 계속되어야 한다."

```text
답: Multi-AZ
```

자동 Failover가 필요하기 때문이다.

### 문제 3

"Reporting용 SELECT를 별도 DB에서 실행하고 싶다."

```text
답: Read Replica
```

Multi-AZ Standby를 조회용으로 쓰는 문제가 아니다.

---

## 8. Read Replica를 Multi-AZ로 구성할 수도 있다

둘은 목적이 다르지만 서로 완전히 배타적인 기능은 아니다.

예를 들어 큰 서비스에서는:

```text
Primary RDS
├── Multi-AZ → HA
└── Read Replica → read scaling
```

처럼 둘 다 사용할 수 있다.

시험에서는:

```text
Multi-AZ냐 Read Replica냐
```

를 이름으로 고르는 것이 아니라 **문제가 성능인지 가용성인지** 먼저 판단한다.

---

## SAA 판단

```text
High Availability
Automatic Failover
AZ 장애 대비
→ Multi-AZ

Read Scalability
Reporting
SELECT 부하 분산
→ Read Replica
```

가장 중요한 한 줄:

> **Multi-AZ = 장애 대비, Read Replica = 읽기 확장**
