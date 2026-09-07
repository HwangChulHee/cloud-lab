# Portfolio — Cloud Shop

`cloud-lab`의 메인 취업 포트폴리오는 **쇼핑몰(Cloud Shop)** 을 AWS에서 운영 가능한 시스템으로 단계적으로 발전시키는 프로젝트다.

> **시작 시점: SAA 취득 후**

현재는 SAA 강의와 자격증 취득에 집중한다. 이 문서는 이후 진행할 프로젝트 설계를 보존하기 위한 것이며, 시험 전에는 본격 구현하지 않는다.

앱 기능 경쟁보다 **Java/Spring 백엔드 + AWS 인프라 설계, 운영, 장애 대응, 자동화**를 보여주는 것이 목적이다.

## 기술 스택

```text
Backend
├── Java 21
├── Spring Boot
├── Spring Web
├── Spring Data JPA
├── Validation
├── Spring Security (필요 시)
└── Actuator

Database
└── PostgreSQL

Infrastructure
├── AWS
├── Docker
├── ECR / ECS
├── Terraform
├── GitHub Actions
└── CloudWatch
```

SAA 취득 후 [Spring Minimum Track](../spring_minimum/README.md)을 시작하고 Cloud Shop 구현과 병행한다.

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

결제, 쿠폰, 정산, 복잡한 재고 동시성, 추천 시스템 등은 기본 인프라 프로젝트가 완성된 뒤 선택적으로 확장한다.

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

S3 ── Product Images

SQS ── Order / Notification Jobs ── Spring Worker

ECR ── Docker Images
GitHub Actions ── CI/CD
Terraform ── Infrastructure as Code
CloudWatch ── Logs / Metrics / Alarms
```

처음부터 최종 아키텍처를 복사하지 않는다. 단순한 시스템에서 시작해 각 단계에서 **왜 구조를 변경했는지** 설명할 수 있도록 발전시킨다.

---

## Stage 0 — Spring Minimum

SAA 취득 직후 시작한다.

```text
Java 최소 기반
→ Spring Boot / Web
→ JPA
→ Transaction
→ Validation / Exception Handling
```

Spring을 몇 달간 별도로 끝낸 뒤 프로젝트를 시작하지 않고, Cloud Shop v1을 만들 수 있는 수준에서 Stage 1과 연결한다.

## Stage 1 — Single EC2

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

확인할 것:

- Spring Boot build / run
- EC2 / SSH / Security Group
- Linux/JVM process
- listening port
- `curl localhost`
- systemd
- Nginx reverse proxy
- application log
- `/actuator/health`

## Stage 2 — RDS Separation

```text
Internet → Spring Boot on EC2 → RDS PostgreSQL
```

- Local PostgreSQL → RDS
- Spring datasource 설정
- Application SG / DB SG 분리
- DB 외부 직접 접근 최소화
- JPA transaction / connection 문제 관측
- Backup / Multi-AZ 연결

대표 장애 실험:

```text
DB SG에서 application 접근 차단
→ DB connection 실패
→ Spring log 관측
→ 원인 진단
→ 복구
```

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

- Target Group / Health Check
- Auto Scaling Group
- Multi-AZ
- stateless application
- instance/process failure 관측 및 복구

## Stage 4 — S3 & CloudFront

상품 이미지를 application local disk에서 분리한다.

```text
Product Image → S3 → CloudFront → User
```

- Spring + S3 연동
- Bucket access control
- Presigned URL 또는 upload architecture
- CloudFront cache
- HTTPS

## Stage 5 — Async Order Processing

```text
Client → Spring Order API → SQS → Spring Worker
```

- Visibility Timeout
- Retry / DLQ
- API와 Worker decoupling
- transaction과 비동기 메시지 경계
- Worker 중지 / backlog / 복구 실험

## Stage 6 — Containerization

```text
Spring Source
→ Gradle Build
→ Docker
→ ECR
→ ECS
```

- executable JAR / Dockerfile
- ECR
- ECS Task / Service
- ALB integration
- Application / Worker 분리

## Stage 7 — Terraform

Console에서 만든 핵심 인프라를 코드로 재구성한다.

```text
VPC
Subnets
Route Tables
Security Groups
ALB
ECS
RDS
S3
IAM
CloudWatch
```

`terraform plan / apply / destroy`, state, secret 처리를 설명할 수 있어야 한다.

## Stage 8 — CI/CD

```text
Git Push
→ GitHub Actions
→ Gradle Test
→ Docker Build
→ ECR Push
→ ECS Deploy
```

- 테스트 실패 시 배포 중단
- image version 관리
- deployment
- 최소 rollback 전략

## Stage 9 — Observability & Failure Lab

관측 대상:

- Spring application logs
- Actuator health
- ALB metrics / Target health
- ECS/EC2 CPU / memory
- HTTP 4xx / 5xx
- RDS 상태
- SQS backlog

장애 기록 형식:

```text
1. 예상 현상
2. 장애 발생
3. 실제 현상
4. 관측 지점
5. 원인 진단
6. 복구
7. 재발 방지
```

대표 실험은 SG 오설정, Spring process 종료, ALB health check 오류, DB connection 실패, Worker 장애, 잘못된 배포 등으로 구성한다.

## Stage 10 — 취업 포트폴리오 정리

최종 README에는 다음을 재구성한다.

- 문제와 요구사항
- Java/Spring 애플리케이션 구조
- Architecture Diagram / Evolution
- AWS 서비스 선택 이유
- Network / Security Design
- Database / Transaction Design
- Terraform
- CI/CD
- Monitoring / Alerting
- Failure Experiments / Troubleshooting
- Cost / Availability / Complexity trade-off
- 한계와 개선 방향

---

## Optional Extensions

기본 프로젝트 이후 지원 공고에 따라 선택한다.

- Spring Security / 테스트 / 주문·재고 동시성 / Redis / Outbox
- AI 상품 설명 / 이미지 태깅 / 추천
- EKS / Kubernetes
- Blue/Green / Canary / Multi-Region DR

---

## 한 문장 설명

> Java/Spring Boot 쇼핑몰 서비스를 단일 EC2 배포에서 시작해 RDS 분리, Multi-AZ/Auto Scaling, S3/CloudFront, 비동기 처리, ECS, Terraform, CI/CD, CloudWatch 기반 장애 대응까지 단계적으로 발전시킨 AWS 클라우드 인프라 프로젝트.
