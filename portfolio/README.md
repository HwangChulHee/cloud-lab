# Portfolio — Cloud Shop

`cloud-lab`의 메인 포트폴리오는 **쇼핑몰(Cloud Shop)** 을 AWS에서 운영 가능한 시스템으로 단계적으로 발전시키는 프로젝트다.

앱 자체의 기능 경쟁보다 **인프라 설계, 운영, 장애 대응, 자동화**를 보여주는 것이 목적이다.

백엔드는 취업 포트폴리오를 고려해 **Java 21 + Spring Boot + PostgreSQL**을 기본 스택으로 사용한다.
Spring 경험이 없는 상태에서 시작하므로 프로젝트 구현과 병행해 [Spring 최소 학습 트랙](../spring_minimum/README.md)을 진행한다.

## 기술 스택

```text
Backend
├── Java 21
├── Spring Boot
├── Spring Web
├── Spring Data JPA
├── Validation
├── Spring Security (인증이 필요해지는 시점에 도입)
└── Actuator (운영/헬스체크 단계에서 도입)

Database
└── PostgreSQL

Infrastructure
├── AWS
├── Docker
├── Terraform
├── GitHub Actions
└── CloudWatch
```

처음부터 모든 Spring 기능을 공부한 뒤 프로젝트를 시작하지 않는다.
AWS 학습을 계속 진행하면서 Cloud Shop에 필요한 Java/Spring 기능을 그때그때 익히는 방식으로 진행한다.

---

## 도메인 범위

초기 기능은 작게 유지한다.

```text
User
Product
Cart
Order
OrderItem
```

초기 API 예시:

```text
GET  /products
GET  /products/{id}
POST /cart
POST /orders
GET  /orders/{id}
GET  /health
```

처음부터 결제, 쿠폰, 정산, 복잡한 재고 동시성, 추천 시스템을 모두 구현하지 않는다.
그런 기능은 인프라 학습을 방해하지 않는 범위에서 나중에 선택적으로 확장한다.

---

## 최종 목표 아키텍처

```text
                        Internet
                           │
                    Route 53 / HTTPS
                           │
                      CloudFront
                           │
                          ALB
                    ┌──────┴──────┐
                    │             │
               Spring App    Spring App
                    │             │
                    └──────┬──────┘
                           │
                     Private RDS
                      PostgreSQL

S3
└── Product Images

SQS
└── Order / Notification Jobs
        │
   Spring Worker

ECR
└── Docker Images

GitHub Actions
└── CI/CD

Terraform
└── Infrastructure as Code

CloudWatch
└── Logs / Metrics / Alarms
```

최종 구조는 학습 결과에 따라 달라질 수 있다. 중요한 것은 처음부터 최종 아키텍처를 복사하는 것이 아니라, 각 단계에서 왜 구조를 변경했는지 설명할 수 있는 것이다.

---

## Stage 0 — Spring Minimum

EC2 프로젝트를 시작하기 전에 Java/Spring을 따로 몇 달 공부하지 않는다.
대신 Cloud Shop v1을 만들 수 있는 최소 수준까지만 빠르게 익힌다.

```text
Java
→ class / interface
→ collections / exception / generics

Spring Boot
→ Controller
→ Service
→ Repository
→ Dependency Injection
→ Configuration
→ JPA
→ Transaction
→ Validation
→ Exception Handling
```

학습 내용은 `spring_minimum/`에 정리하고, 곧바로 Cloud Shop 코드에 적용한다.

---

## Stage 1 — Single EC2

### 목표

가장 단순한 형태로 Spring Boot 애플리케이션을 실제 AWS에 올린다.

```text
Internet
   │
Security Group
   │
  EC2
   │
Spring Boot
   │
PostgreSQL
```

초기에는 학습 속도를 위해 애플리케이션과 PostgreSQL을 한 EC2에서 시작할 수 있다.
이후 RDS 파트에서 DB를 분리한다.

### 확인할 것

- Spring Boot application build / run
- EC2 launch
- User Data
- SSH
- Linux process
- JVM process
- listening port
- `curl localhost`
- 외부 요청
- systemd
- Nginx reverse proxy
- Application log
- `/actuator/health` 또는 단순 `/health`

### 질문

```text
EC2가 running인데 Spring 애플리케이션이 죽어 있을 수 있는 이유는?
외부 요청 timeout이면 어디부터 확인하는가?
127.0.0.1과 0.0.0.0 bind 차이는?
Spring Boot가 어느 포트에서 listen 중인지 어떻게 확인하는가?
```

---

## Stage 2 — RDS Separation

Application과 Database를 분리한다.

```text
Internet
   │
Spring Boot on EC2
   │
  RDS PostgreSQL
```

### 목표

- Local PostgreSQL → RDS PostgreSQL
- Spring datasource 설정
- DB credentials 관리
- Application SG / DB SG 분리
- DB 외부 직접 접근 최소화
- JPA transaction과 connection 문제 관측
- Backup / Multi-AZ 개념 연결

### 장애 실험

DB Security Group에서 application 접근을 차단한다.

```text
정상
→ SG 변경
→ DB connection 실패
→ Spring application log 확인
→ SG 원인 진단
→ 복구
```

---

## Stage 3 — High Availability

```text
                 ALB
              /       \
        Spring App  Spring App
            │           │
            └─────┬─────┘
                  │
                 RDS
```

### 목표

- ALB
- Target Group
- Health Check
- Auto Scaling Group
- Multi-AZ application deployment
- stateless application 구조
- Spring session/state를 application instance에 의존하지 않게 설계

### 장애 실험

- Health Check path 오설정
- Spring application process 종료
- 한 인스턴스 장애

관측:

```text
Target healthy / unhealthy
HTTP response
Spring application log
CloudWatch metric
Auto Scaling 동작
```

---

## Stage 4 — S3 & CloudFront

상품 이미지를 application server의 로컬 디스크에서 분리한다.

```text
Product Image
    │
    ▼
   S3
    │
CloudFront
    │
  User
```

### 목표

- Spring에서 S3 연동
- S3 object storage
- Bucket access control
- Presigned URL 또는 upload architecture
- CloudFront cache
- HTTPS

### 설명할 질문

```text
왜 상품 이미지를 EC2 disk에 저장하지 않았는가?
왜 S3와 CloudFront를 분리했는가?
캐싱이 오래되면 어떤 문제가 생기는가?
```

---

## Stage 5 — Async Order Processing

주문 API와 후처리를 분리한다.

```text
Client
  │
Spring Order API
  │
 SQS
  │
Spring Worker
```

예시 후처리:

- 주문 완료 이메일
- 주문 이벤트 기록
- 이미지/문서 처리와 같은 느린 작업

### 목표

- Spring과 SQS 연동
- Visibility Timeout
- Retry
- DLQ
- API와 Worker decoupling
- transaction과 비동기 메시지 사이의 경계 고민

### 장애 실험

Worker를 중지한 상태에서 주문 이벤트를 쌓고 복구 후 처리되는지 확인한다.

---

## Stage 6 — Containerization

```text
Spring Source
  │
Gradle Build
  │
Docker
  │
 ECR
  │
 ECS
```

### 목표

- Spring Boot executable JAR
- Dockerfile
- Local container test
- ECR
- ECS Task Definition
- ECS Service
- ALB integration
- Application / Worker 분리

EC2에서 JVM 프로세스를 직접 운영하는 방식과 ECS로 컨테이너를 운영하는 방식의 차이를 기록한다.

---

## Stage 7 — Terraform

AWS Console에서 만든 인프라를 코드로 재구성한다.

목표 리소스 예:

```text
VPC
Public / Private Subnet
Route Table
Internet Gateway
NAT Gateway (필요성 판단)
Security Group
ALB
ECS
RDS
S3
IAM
CloudWatch
```

### 목표

```bash
terraform plan
terraform apply
terraform destroy
```

의 결과를 예측하고 변경 내용을 설명할 수 있어야 한다.

Console 작업과 IaC의 차이, state 관리와 secret 처리도 기록한다.

---

## Stage 8 — CI/CD

```text
Git Push
   │
GitHub Actions
   │
Gradle Test
   │
Docker Build
   │
ECR Push
   │
ECS Deploy
```

### 목표

- Gradle test 실패 시 배포 중단
- Java/Spring build artifact 관리
- Docker image tag/version 관리
- ECR push
- ECS deployment
- 최소한의 rollback 전략

---

## Stage 9 — Observability & Failure Lab

CloudWatch를 이용해 단순히 "로그가 있다" 수준이 아니라 실제 장애 분석 흐름을 만든다.

### 관측 대상

- Spring application logs
- Actuator health
- ALB metrics
- Target health
- ECS/EC2 CPU / memory
- JVM/application 상태
- HTTP 4xx / 5xx
- RDS 상태
- Queue backlog

### 대표 장애 실험

```text
Security Group misconfiguration
Spring application process failure
ALB health check failure
DB connection failure
Worker failure / queue backlog
잘못된 배포
```

각 장애는 아래 형식으로 기록한다.

```text
1. 예상 현상
2. 장애 발생
3. 실제 현상
4. 관측 지점
5. 원인 진단
6. 복구
7. 재발 방지
```

---

## Stage 10 — 취업 포트폴리오 정리

학습 과정의 모든 기록을 그대로 보여주는 것이 아니라 핵심 내용을 재구성한다.

최종 README에 포함할 내용:

- 문제와 요구사항
- Java/Spring 애플리케이션 구조
- 최종 Architecture Diagram
- 단계별 Architecture Evolution
- AWS 서비스 선택 이유
- Network 설계
- Security 설계
- Database / Transaction 설계
- CI/CD
- Terraform
- Monitoring / Alerting
- Failure Experiments
- Troubleshooting 사례
- Cost / Availability / Complexity trade-off
- 한계와 개선 방향

---

## Optional Extensions

기본 프로젝트가 완성된 뒤 공고나 관심 직무에 맞게 선택적으로 추가한다.

### Backend Depth

- Spring Security
- 테스트 전략
- 주문/재고 동시성
- Redis cache
- Outbox Pattern
- 대용량 조회 / 성능 튜닝

클라우드 프로젝트의 본체를 완성한 뒤 백엔드 지원 비중에 따라 강화한다.

### AI

- 상품 설명 생성
- 상품 이미지 태깅
- 간단한 추천

AI 자체가 프로젝트 본체는 아니다. AI 기능을 AWS 인프라 위에서 어떻게 배포/운영하는지 보여주는 확장으로 사용한다.

### Kubernetes

ECS 버전을 먼저 완성한 뒤 필요하면 EKS 버전으로 확장한다.

### Reliability

- Blue/Green Deployment
- Canary Deployment
- Multi-Region DR
- Chaos / Failure experiment 확대

---

## 이 프로젝트를 한 문장으로 설명하기

> Java/Spring Boot 쇼핑몰 서비스를 단일 EC2 배포에서 시작해 RDS 분리, Multi-AZ/Auto Scaling, S3/CloudFront, 비동기 처리, ECS, Terraform, CI/CD, CloudWatch 기반 장애 대응까지 단계적으로 발전시킨 AWS 클라우드 인프라 프로젝트.
