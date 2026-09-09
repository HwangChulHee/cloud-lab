# u1. RDS Overview & Managed Database

## 지도 확인

RDS는 **Relational Database Service**의 약자다.

쉽게 말하면:

> PostgreSQL, MySQL 같은 관계형 데이터베이스를 직접 EC2에 설치해서 운영하지 않고 AWS가 관리해주는 서비스

이다.

```text
직접 운영
EC2
 └── Linux
      └── PostgreSQL

RDS
AWS가 관리하는 DB Instance
 └── PostgreSQL
```

---

## 1. 관계형 데이터베이스가 뭐냐

관계형 데이터베이스는 데이터를 테이블 형태로 저장하고 관계를 맺어 사용하는 데이터베이스다.

예:

```text
users
id | name
1  | 철수

orders
id | user_id | amount
10 | 1       | 30000
```

`orders.user_id = 1`을 통해 사용자와 주문을 연결할 수 있다.

이런 구조에서 SQL을 사용한다.

```sql
SELECT * FROM orders WHERE user_id = 1;
```

RDS는 이런 **RDBMS(Relational Database Management System)** 를 관리형으로 제공한다.

---

## 2. RDS에서 사용할 수 있는 DB Engine

DB Engine은 실제 데이터베이스 소프트웨어 종류라고 생각하면 된다.

예:

```text
PostgreSQL
MySQL
MariaDB
Oracle
Microsoft SQL Server
IBM Db2
```

예를 들어 애플리케이션이 PostgreSQL을 쓴다면:

```text
Spring Boot
   │ JDBC
   ▼
RDS PostgreSQL
```

형태로 연결한다.

RDS는 SQL 문법 자체를 새로 만드는 서비스가 아니다.

기존 PostgreSQL/MySQL 등을 AWS가 관리형으로 제공하는 것이다.

---

## 3. Managed Service란 무엇인가

`Managed`는 AWS가 운영 업무의 상당 부분을 대신한다는 뜻이다.

EC2에 PostgreSQL을 직접 설치하면 사용자가 이런 일을 해야 한다.

```text
Linux 설치/관리
DB 설치
DB patch
백업 구성
디스크 용량 관리
장애 대응
DB process 관리
모니터링
```

RDS에서는 AWS가 많은 부분을 대신 처리한다.

그래서 사용자는 DB 자체 운영보다:

```text
어떤 Instance 크기를 쓸지
어떤 Storage를 쓸지
Multi-AZ를 켤지
Read Replica가 필요한지
Security Group을 어떻게 구성할지
```

같은 설계에 집중한다.

### 예시

쇼핑몰을 직접 EC2 + PostgreSQL로 운영한다고 하자.

```text
EC2 장애
→ PostgreSQL도 같이 죽음
→ OS 상태 확인
→ DB process 확인
→ backup 확인
→ 직접 복구
```

RDS를 사용하면 이런 인프라 운영의 일부를 AWS가 관리한다.

즉 RDS의 핵심 가치는:

> **DB 기능 자체보다 DB 운영 부담을 줄여주는 것**

이라고 보면 된다.

---

## 4. DB Instance

RDS에서는 실행되는 DB 서버 단위를 **DB Instance**라고 부른다.

```text
RDS DB Instance
├── CPU
├── Memory
├── Network
└── Database Engine
```

EC2에서 `t3.micro`, `m5.large`처럼 instance type을 고르듯 RDS도 DB Instance Class를 선택한다.

예를 들어:

```text
db.t3.micro
→ 작은 개발/테스트

db.r6g.large
→ 메모리가 중요한 DB workload
```

정확한 제품명보다 시험에서는:

```text
DB 부하가 커짐
→ 더 큰 DB instance class로 vertical scaling 가능
```

정도를 이해하면 된다.

---

## 5. RDS는 일반적인 OLTP에 적합하다

`OLTP`는 Online Transaction Processing의 약자다.

처음 보면 거창하지만 실제로는:

> 사용자의 일상적인 요청을 빠르게 처리하는 업무용 DB

정도로 보면 된다.

예:

```text
회원가입
주문 생성
상품 수정
결제 상태 변경
재고 변경
```

이런 요청은:

```sql
INSERT
UPDATE
DELETE
SELECT
```

을 자주 수행한다.

그래서 쇼핑몰, CRM, 사내 업무 시스템 같은 서비스와 RDS가 잘 맞는다.

반대로 수십 TB 데이터를 대규모 분석하는 데이터 웨어하우스 목적이라면 Redshift 같은 다른 서비스가 더 적합할 수 있다.

---

## 6. Transaction

관계형 DB에서 중요한 개념이다.

예를 들어 주문 생성 과정이:

```text
1. 주문 저장
2. 주문 상품 저장
3. 재고 감소
```

라고 하자.

2번에서 오류가 났는데 1번만 DB에 남으면 데이터가 이상해진다.

Transaction을 사용하면:

```text
전부 성공
→ COMMIT

중간에 실패
→ ROLLBACK
```

처럼 처리할 수 있다.

RDS는 이런 관계형 DB의 transaction 기능을 그대로 사용할 수 있다.

---

## SAA 판단

```text
기존 PostgreSQL / MySQL 같은 관계형 DB를 AWS에서 관리형으로 사용
→ RDS

SQL, JOIN, Transaction이 중요
→ RDS / Aurora 계열 고려

OS까지 직접 관리하고 DB를 세세하게 커스터마이징
→ 일반 RDS보다 EC2 직접 운영 또는 RDS Custom 검토
```

이번 유닛에서는 **RDS = 관계형 DB의 관리형 서비스**라는 큰 그림을 잡으면 된다.
