# Portfolio — Cloud Shop

`cloud-lab`의 메인 포트폴리오는 **쇼핑몰(Cloud Shop)** 을 AWS에서 운영 가능한 시스템으로 단계적으로 발전시키는 프로젝트다.

앱 자체의 기능 경쟁보다 **인프라 설계, 운영, 장애 대응, 자동화**를 보여주는 것이 목적이다.

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
                 ECS App       ECS App
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
     ECS Worker

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

## Stage 1 — Single EC2

### 목표

가장 단순한 형태로 애플리케이션을 실제 AWS에 올린다.

```text
Internet
   │
Security Group
   │
  EC2
   │
FastAPI
```

### 확인할 것

- EC2 launch
- User Data
- SSH
- Linux process
- listening port
- `curl localhost`
- 외부 요청
- systemd
- Nginx
- Application log

### 질문

```text
EC2가 running인데 서비스가 죽어 있을 수 있는 이유는?
외부 요청 timeout이면 어디부터 확인하는가?
127.0.0.1과 0.0.0.0 bind 차이는?
```

---

## Stage 2 — RDS Separation

Application과 Database를 분리한다.

```text
Internet
   │
  EC2
   │
  RDS
```

### 목표

- PostgreSQL → RDS
- DB credentials 관리
- Application SG / DB SG 분리
- DB 외부 직접 접근 최소화
- Backup / Multi-AZ 개념 연결

### 장애 실험

DB Security Group에서 application 접근을 차단한다.

```text
정상
→ SG 변경
→ DB connection 실패
→ Application log 확인
→ SG 원인 진단
→ 복구
```

---

## Stage 3 — High Availability

```text
                 ALB
              /       \
           App         App
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

### 장애 실험

- Health Check path 오설정
- Application process 종료
- 한 인스턴스 장애

관측:

```text
Target healthy / unhealthy
HTTP response
Application log
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
Order API
  │
 SQS
  │
Worker
```

예시 후처리:

- 주문 완료 이메일
- 주문 이벤트 기록
- 이미지/문서 처리와 같은 느린 작업

### 목표

- SQS
- Visibility Timeout
- Retry
- DLQ
- API와 Worker decoupling

### 장애 실험

Worker를 중지한 상태에서 주문 이벤트를 쌓고 복구 후 처리되는지 확인한다.

---

## Stage 6 — Containerization

```text
Source
  │
Docker
  │
 ECR
  │
 ECS
```

### 목표

- Dockerfile
- Local container test
- ECR
- ECS Task Definition
- ECS Service
- ALB integration
- Application / Worker 분리

EC2 직접 운영 방식과 ECS 운영 방식의 차이를 기록한다.

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
Test
   │
Docker Build
   │
ECR Push
   │
ECS Deploy
```

### 목표

- 테스트 실패 시 배포 중단
- Docker image tag/version 관리
- ECR push
- ECS deployment
- 최소한의 rollback 전략

---

## Stage 9 — Observability & Failure Lab

CloudWatch를 이용해 단순히 "로그가 있다" 수준이 아니라 실제 장애 분석 흐름을 만든다.

### 관측 대상

- Application logs
- ALB metrics
- Target health
- ECS/EC2 CPU / memory
- HTTP 4xx / 5xx
- RDS 상태
- Queue backlog

### 대표 장애 실험

```text
Security Group misconfiguration
Application process failure
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
- 최종 Architecture Diagram
- 단계별 Architecture Evolution
- AWS 서비스 선택 이유
- Network 설계
- Security 설계
- Database 설계
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

> 단일 EC2에 배포한 쇼핑몰 서비스를 시작으로 RDS 분리, Multi-AZ/Auto Scaling, S3/CloudFront, 비동기 처리, ECS, Terraform, CI/CD, CloudWatch 기반 장애 대응까지 단계적으로 발전시킨 AWS 클라우드 인프라 프로젝트.
