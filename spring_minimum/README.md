# Spring Minimum Track

Cloud Shop의 백엔드를 **Java 21 + Spring Boot**로 구현하기 위한 최소 학습 트랙이다.

목표는 Spring을 별도로 몇 달 공부한 뒤 AWS 프로젝트를 시작하는 것이 아니다.
AWS 학습을 계속 진행하면서 **Cloud Shop v1을 만들 수 있는 만큼만 배우고 곧바로 적용**한다.

---

## 학습 원칙

```text
Java/Spring 개념 학습
        ↓
작은 예제
        ↓
Cloud Shop 적용
        ↓
문제 발생
        ↓
필요한 개념 추가 학습
```

초반에는 프레임워크 내부 구조를 깊게 파기보다 애플리케이션을 만들고 배포할 수 있는 수준을 우선한다.

---

## 1. Java 최소 기반

### 반드시 익힐 것

- class / object
- constructor
- interface
- inheritance보다 composition 우선 사고
- access modifier
- package
- collection (`List`, `Set`, `Map`)
- exception
- generics
- enum
- lambda / stream 기초
- null과 `Optional` 기초

### 목표

다음 구조를 자연스럽게 읽고 작성할 수 있으면 된다.

```text
Controller
   ↓
Service
   ↓
Repository
   ↓
Domain / Entity
```

---

## 2. Spring Boot 기본

### 핵심 개념

- Spring Boot project 구조
- Dependency Injection
- Bean
- `@Component`, `@Service`, `@Repository`
- `@RestController`
- Configuration
- application properties / yaml
- profile / environment variable 기초

### 최소 API

Cloud Shop에서 우선 다음 API를 구현한다.

```text
GET  /products
GET  /products/{id}
POST /orders
GET  /orders/{id}
GET  /health
```

---

## 3. Spring Web

익힐 것:

- `@RestController`
- `@RequestMapping`
- `@GetMapping` / `@PostMapping`
- Path Variable
- Request Parameter
- Request Body
- Response Entity
- DTO
- HTTP status code

0부에서 배운 HTTP Request / Response 개념과 연결해서 본다.

---

## 4. Spring Data JPA

Cloud Shop이 PostgreSQL을 사용하므로 JPA는 실습 필수다.

### 핵심

- `@Entity`
- primary key
- repository interface
- basic CRUD
- relationship (`ManyToOne`, `OneToMany`)
- lazy loading 개념
- transaction boundary
- N+1 문제는 존재와 기본 대응 정도만 먼저 이해

초기 domain:

```text
Product
Order
OrderItem
```

`User`, `Cart`는 프로젝트 진행 상황에 따라 추가한다.

---

## 5. Transaction

쇼핑몰에서 특히 중요한 Spring 주제다.

우선 다음을 이해한다.

```text
주문 생성
├── Order 저장
├── OrderItem 저장
└── 실패 시 전체 rollback
```

- `@Transactional`
- transaction boundary
- commit / rollback
- DB transaction과 SQS 같은 외부 시스템의 transaction이 같지 않다는 점

고급 동시성/Outbox Pattern은 기본 프로젝트가 완성된 뒤 확장한다.

---

## 6. Validation & Exception Handling

- Bean Validation
- `@Valid`
- 입력값 검증
- custom exception
- `@ControllerAdvice`
- 일관된 error response

Cloud Shop에서는 최소한 다음 오류를 구분한다.

```text
상품 없음
잘못된 주문 요청
DB 오류
서버 내부 오류
```

---

## 7. Configuration & Secrets

AWS 배포와 직접 연결되는 부분이다.

코드에 다음 값을 하드코딩하지 않는다.

```text
DB URL
DB username/password
AWS credential
external API key
```

초기에는 environment variable로 분리하고,
AWS 학습이 진행되면 Systems Manager Parameter Store / Secrets Manager와 연결한다.

---

## 8. Testing Minimum

초기부터 테스트를 거대하게 만들 필요는 없지만 CI/CD를 위해 최소 테스트는 필요하다.

- JUnit 기초
- service unit test
- repository/integration test 기초
- API test 기초

GitHub Actions 단계에서:

```text
./gradlew test
```

실패 시 배포가 중단되도록 연결한다.

---

## 9. Spring Security — 필요할 때 도입

Cloud Shop 초기 v1에서는 인증 없이 product/order 흐름부터 만들 수 있다.

사용자 인증 기능을 추가하는 시점에 학습한다.

- Authentication / Authorization
- Security Filter Chain 개념
- Password hashing
- Session vs JWT
- Role 기반 접근 제어

보안 구현 자체가 클라우드 학습을 지연시키지 않도록 도입 시점을 늦출 수 있다.

---

## 10. Actuator & Operations

클라우드 운영 프로젝트에서 Spring Actuator는 중요도가 높다.

확인할 것:

```text
/actuator/health
/actuator/info
metrics
```

이후 다음과 연결한다.

```text
ALB Health Check
CloudWatch
ECS Health Check
Application Monitoring
```

단, actuator endpoint를 외부에 무분별하게 공개하지 않는다.

---

# 학습 시점

## 지금

SAA 강의를 우선 진행한다.

```text
IAM
→ EC2
→ Security Group
→ EBS
```

이 흐름을 끊지 않는다.

## Cloud Shop Stage 1 시작 직전

Java 최소 기반 + Spring Boot / Web / JPA를 빠르게 익힌다.

목표는 "Spring 강의 완강"이 아니라:

> **Product와 Order API를 PostgreSQL과 연결해 실행할 수 있는가?**

이다.

## 프로젝트 진행 중

필요한 순간에 다음을 추가한다.

```text
RDS
→ datasource / transaction

ALB
→ Actuator health

S3
→ AWS SDK integration

SQS
→ async worker

ECS
→ container configuration

CI/CD
→ Gradle test/build

Secrets Manager
→ configuration/secrets
```

---

# 완료 기준

다음 질문에 설명하고 구현할 수 있으면 이 최소 트랙의 목적을 달성한 것이다.

1. Controller / Service / Repository를 왜 나누는가?
2. Dependency Injection이 무엇인가?
3. JPA Entity와 Repository는 어떤 역할을 하는가?
4. Transaction은 주문 처리에서 왜 중요한가?
5. 환경변수와 secret을 코드와 분리해야 하는 이유는 무엇인가?
6. Spring Boot process가 실제 어느 port에서 listen하는지 Linux에서 확인할 수 있는가?
7. `/actuator/health`를 ALB/ECS health check와 어떻게 연결할 수 있는가?
8. Gradle test/build 결과를 CI/CD와 연결할 수 있는가?

이후 더 깊은 Spring 학습은 Cloud Shop에서 실제 필요가 생길 때 진행한다.
