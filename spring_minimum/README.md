# Spring Minimum Track

Cloud Shop의 백엔드를 **Java 21 + Spring Boot**로 구현하기 위한 최소 학습 트랙이다.

현재는 SAA 취득이 우선이므로 이 트랙은 **SAA 취득 후 시작한다.**
시험 전에는 Spring 학습 때문에 AWS 강의 흐름을 끊지 않는다.

---

## 시작 시점

```text
SAA 강의 1회독
→ 별도 시험 강의로 복습 / 문제풀이
→ SAA 취득
→ Spring Minimum Track 시작
→ Cloud Shop과 병행
```

Spring을 따로 몇 달 완강한 뒤 프로젝트를 시작하는 방식은 지양한다.
SAA 취득 후 Cloud Shop v1을 만들 수 있는 수준까지만 빠르게 배우고 곧바로 적용한다.

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

## 1. Java 최소 기반

- class / object
- constructor
- interface
- access modifier / package
- collection (`List`, `Set`, `Map`)
- exception
- generics
- enum
- lambda / stream 기초
- null과 `Optional` 기초

목표 구조:

```text
Controller
   ↓
Service
   ↓
Repository
   ↓
Domain / Entity
```

## 2. Spring Boot 기본

- Spring Boot project 구조
- Dependency Injection / Bean
- `@Component`, `@Service`, `@Repository`
- `@RestController`
- Configuration
- application properties / yaml
- profile / environment variable 기초

최소 API:

```text
GET  /products
GET  /products/{id}
POST /orders
GET  /orders/{id}
GET  /health
```

## 3. Spring Web

- `@RestController`
- `@RequestMapping`
- `@GetMapping` / `@PostMapping`
- Path Variable / Request Parameter / Request Body
- Response Entity
- DTO
- HTTP status code

## 4. Spring Data JPA

- `@Entity`
- primary key
- repository interface
- basic CRUD
- relationship (`ManyToOne`, `OneToMany`)
- lazy loading 개념
- transaction boundary
- N+1 문제의 존재와 기본 대응

초기 domain:

```text
Product
Order
OrderItem
```

`User`, `Cart`는 프로젝트 진행 상황에 따라 추가한다.

## 5. Transaction

쇼핑몰에서 특히 중요한 Spring 주제다.

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

## 6. Validation & Exception Handling

- Bean Validation
- `@Valid`
- 입력값 검증
- custom exception
- `@ControllerAdvice`
- 일관된 error response

## 7. Configuration & Secrets

코드에 다음 값을 하드코딩하지 않는다.

```text
DB URL
DB username/password
AWS credential
external API key
```

초기에는 environment variable로 분리하고,
Cloud Shop 인프라 단계에서 Systems Manager Parameter Store / Secrets Manager와 연결한다.

## 8. Testing Minimum

- JUnit 기초
- service unit test
- repository/integration test 기초
- API test 기초

CI/CD 단계에서:

```text
./gradlew test
```

실패 시 배포가 중단되도록 연결한다.

## 9. Spring Security — 필요할 때 도입

초기 v1에서는 인증 없이 product/order 흐름부터 만들 수 있다.
사용자 인증 기능을 추가하는 시점에 학습한다.

- Authentication / Authorization
- Security Filter Chain 개념
- Password hashing
- Session vs JWT
- Role 기반 접근 제어

## 10. Actuator & Operations

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
