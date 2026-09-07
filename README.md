# cloud-lab

AWS와 클라우드 인프라를 학습하고 직접 구축하며,
Cloud Engineer 취업에 필요한 기반 역량을 만드는 저장소.

단기적으로는 AWS Certified Solutions Architect - Associate(SAA) 취득,
중기적으로는 AWS 기반 쇼핑몰 인프라 포트폴리오 완성을 목표로 한다.

## 프로젝트의 두 축

이 저장소는 단순 강의 필기 저장소가 아니다.

### 1. SAA Coverage

Stéphane Maarek SAA-C03 강의를 기준으로 시험 범위를 가능한 한 빠짐없이 매핑한다.

강의에서 연속적으로 배우는 내용은 학습 순서도 가급적 강의 흐름을 따른다.
다만 저장소의 디렉터리 구조는 개념과 실무 활용성을 기준으로 정리할 수 있다.

### 2. Cloud Engineer Lab

실무적으로 중요한 서비스는 강의 Hands-on에서 끝내지 않고 다음 단계까지 확장한다.

> 이해 → 구축 → 예측 → 관측 → 장애 → 분석 → 복구 → 자동화

모든 AWS 서비스를 같은 깊이로 실습하지 않는다.

- **Coverage**: SAA 선택 기준과 개념을 이해하면 충분한 주제
- **Lab**: 직접 구축하고 상태를 관측할 주제
- **Core Lab**: 장애 실험, 복구, 자동화, 포트폴리오까지 연결할 핵심 주제

예를 들어 Rekognition이나 Polly는 Coverage 중심으로 학습하고,
EC2, VPC, RDS, ALB, ECS, CloudWatch 등은 Core Lab 수준까지 진행한다.

## 목표 역량

1. AWS 주요 서비스를 어떤 상황에서 왜 선택하는지 설명할 수 있다.
2. SAA 강의와 시험 범위를 누락 없이 따라갈 수 있다.
3. 쇼핑몰 웹 서비스를 AWS에 직접 배포하고 네트워크, 컴퓨팅, 데이터베이스, 보안 구조를 설계할 수 있다.
4. 장애 상황을 관측하고 원인을 추적하여 복구할 수 있다.
5. Docker, Terraform, CI/CD를 이용해 인프라 구축과 배포를 자동화할 수 있다.
6. 비용, 가용성, 보안, 운영 복잡도 사이의 trade-off를 설명할 수 있다.

## 학습 방식

각 주제는 Unit 단위로 진행한다.

기본적인 Unit은 필요에 따라 다음 요소를 가진다.

- **지도 확인**: 전체 아키텍처에서 이 주제가 어디에 위치하는지 확인
- **개념**: 서비스가 해결하는 문제와 동작 원리
- **강의 커버리지**: 강의에서 다루는 핵심 포인트 확인
- **SAA 연결**: 문제에서 서비스 선택 기준과 비교 포인트
- **최소 예제**: 정상 동작 환경 구축
- **관측**: CLI, 로그, 메트릭, 상태 확인
- **유제**: 스스로 판단하거나 구성
- **장애 실험**: 설정을 의도적으로 망가뜨리고 분석/복구
- **포트폴리오 반영**: 메인 쇼핑몰 프로젝트에 적용
- **3문장 요약**: 중요한 Unit에서 자신의 언어로 정리

쉬운 Coverage 주제는 개념 + SAA 연결만 보고 빠르게 지나간다.
중요한 Core Lab 주제는 실제 구축과 장애 실험까지 진행한다.

## 학습 자료

- AWS Certified Solutions Architect - Associate (SAA-C03)
- Stéphane Maarek - Ultimate AWS Certified Solutions Architect Associate
- AWS 공식 문서

강의와 저장소의 세밀한 대응 관계는 [CURRICULUM_MAPPING.md](./CURRICULUM_MAPPING.md)에 관리한다.

---

# Curriculum

## 0부 — Cloud & System Foundation

강의 외 보강 파트. 이후 EC2/VPC 장애 분석을 위한 최소 기반이다.

- [ ] 00. AWS와 클라우드의 전체 그림
  - [ ] u1. 클라우드란 무엇인가
  - [ ] u2. Region / Availability Zone / Edge Location
  - [ ] u3. AWS 서비스의 범위 — Global vs Regional
- [ ] 01. Linux 최소 기반
  - [ ] u1. Process와 Service
  - [ ] u2. Files, Directories와 Permission
  - [ ] u3. Port와 Linux 네트워크 확인
  - [ ] u4. SSH, Log와 Environment
- [ ] 02. 네트워크 최소 기반
  - [ ] u1. IP, Port와 Protocol
  - [ ] u2. Subnet, CIDR, Gateway와 NAT
  - [ ] u3. Routing, Firewall과 Troubleshooting
- [ ] 03. HTTP / DNS / TLS
  - [ ] u1. HTTP Request와 Response
  - [ ] u2. DNS Resolution
  - [ ] u3. TLS와 HTTPS

## 1부 — IAM & EC2 Basics

강의 초반 흐름을 최대한 그대로 따라간다.

- [ ] 04. IAM
  - [ ] u1. Users, Groups, Policies
  - [ ] u2. Policy Structure와 Inheritance
  - [ ] u3. Password Policy와 MFA
  - [ ] u4. Console, CLI, SDK와 Access Keys
  - [ ] u5. IAM Roles for Services
  - [ ] u6. Security Tools와 Best Practices
  - [ ] u7. Integrated Lab / Exercises
- [ ] 05. EC2
  - [ ] u1. Overview, Launch와 User Data
  - [ ] u2. Instance Types
  - [ ] u3. Security Groups와 SSH
  - [ ] u4. Purchasing Options
  - [ ] u5. Public IP, Private IP와 Elastic IP
  - [ ] u6. Placement Groups
  - [ ] u7. Elastic Network Interface (ENI)
  - [ ] u8. Lifecycle와 Hibernate
  - [ ] u9. Integrated Lab / Exercises
- [ ] 06. EC2 Instance Storage
  - [ ] EBS Volume / Snapshot
  - [ ] EBS Volume Types
  - [ ] Instance Store
  - [ ] AMI
  - [ ] EFS 기초 연결
- [ ] 07. Security Group 심화 / 운영
  - [ ] Stateful 동작
  - [ ] Security Group Reference
  - [ ] ALB → Application → DB 계층 권한
  - [ ] 접근 장애 실험

> EC2 Basics 단계에서 Security Group 기초를 먼저 배우고, 07에서 운영 관점으로 다시 확장한다.

## 2부 — High Availability & Scalability

- [ ] 08. Elastic Load Balancing
  - [ ] ALB / NLB / GWLB 비교
  - [ ] Target Group / Health Check
  - [ ] Sticky Session / Cross-Zone
  - [ ] TLS Listener / SNI
- [ ] 09. Auto Scaling
  - [ ] Auto Scaling Group
  - [ ] Scaling Policy
  - [ ] Dynamic / Predictive Scaling
  - [ ] ELB + ASG 통합

## 3부 — Relational Data & Cache

- [ ] 10. RDS
  - [ ] RDS 기본
  - [ ] Multi-AZ
  - [ ] Read Replica
  - [ ] Backup / Restore
  - [ ] RDS Proxy
- [ ] 11. Aurora
  - [ ] Aurora Architecture
  - [ ] Replica / HA
  - [ ] Serverless / Global Database
  - [ ] Aurora Machine Learning 개념
- [ ] 12. ElastiCache
  - [ ] Redis / Memcached
  - [ ] Cache Strategy
  - [ ] Session Store

## 4부 — Route 53, S3 & Global Delivery

- [ ] 13. Route 53
  - [ ] DNS Records
  - [ ] Routing Policies
  - [ ] Health Checks
  - [ ] Alias Records
- [ ] 14. S3 Core
  - [ ] Bucket / Object
  - [ ] Versioning
  - [ ] Replication
  - [ ] Storage Classes
  - [ ] Lifecycle
- [ ] 15. S3 Advanced & Security
  - [ ] Bucket Policy / IAM
  - [ ] Encryption
  - [ ] CORS
  - [ ] Presigned URL
  - [ ] Performance / Multipart Upload
  - [ ] Event Notification
- [ ] 16. CloudFront / Global Accelerator
  - [ ] CDN / Edge Cache
  - [ ] Origin / Cache Behavior
  - [ ] OAC/OAI 개념
  - [ ] Global Accelerator 비교
- [ ] 17. ACM / HTTPS

## 5부 — Storage Extras

강의 커버리지 중심. 필요한 항목만 짧게 실습한다.

- [ ] 18. EFS
- [ ] 19. FSx
- [ ] 20. Storage Gateway
- [ ] 21. DataSync / Transfer Family
- [ ] 22. Snow Family

## 6부 — Messaging & Integration

- [ ] 23. SQS
  - [ ] Standard / FIFO
  - [ ] Visibility Timeout
  - [ ] DLQ
  - [ ] Long Polling
- [ ] 24. SNS
- [ ] 25. EventBridge
- [ ] 26. Kinesis
- [ ] 27. Amazon MQ / Integration 선택 기준

## 7부 — Containers

- [ ] 28. Docker
- [ ] 29. ECR
- [ ] 30. ECS
  - [ ] EC2 Launch Type / Fargate
  - [ ] Task / Service
  - [ ] ALB 연동
  - [ ] Auto Scaling
- [ ] 31. EKS / App Runner 개념 비교

## 8부 — Serverless & NoSQL

- [ ] 32. Lambda
- [ ] 33. API Gateway
- [ ] 34. DynamoDB
  - [ ] Partition Key / Sort Key
  - [ ] Consistency
  - [ ] GSI / LSI
  - [ ] Streams
  - [ ] DAX
  - [ ] Global Tables
- [ ] 35. Step Functions / Cognito 등 Serverless 연계 서비스

## 9부 — Databases, Data & Analytics

강의 커버리지 중심. 서비스 이름과 사용 사례를 구분하는 것이 우선이다.

- [ ] 36. AWS Database 선택 지도
  - [ ] RDS / Aurora
  - [ ] DynamoDB
  - [ ] ElastiCache
  - [ ] DocumentDB
  - [ ] Neptune
  - [ ] Keyspaces
  - [ ] QLDB 등 강의 등장 서비스
- [ ] 37. Athena
- [ ] 38. Redshift
- [ ] 39. EMR
- [ ] 40. Glue
- [ ] 41. OpenSearch
- [ ] 42. Lake Formation / QuickSight / MSK 등 Analytics 서비스

## 10부 — Machine Learning for SAA

ML 모델 개발이 아니라 AWS ML 서비스 선택 문제를 위한 Coverage 파트다.

- [ ] 43. Rekognition
- [ ] 44. Transcribe / Polly / Translate
- [ ] 45. Comprehend
- [ ] 46. Lex
- [ ] 47. SageMaker
- [ ] 48. Textract
- [ ] 49. Kendra / Personalize 등 강의 등장 서비스

## 11부 — Monitoring, Advanced Identity & Security

- [ ] 50. CloudWatch
  - [ ] Metrics
  - [ ] Logs
  - [ ] Alarms
  - [ ] EventBridge 연결
- [ ] 51. CloudTrail
- [ ] 52. AWS Config
- [ ] 53. Advanced Identity
  - [ ] AWS Organizations / SCP
  - [ ] IAM Identity Center
  - [ ] Federation / STS
  - [ ] Directory Services
  - [ ] Resource Access Manager
- [ ] 54. KMS
- [ ] 55. Secrets Manager / Parameter Store
- [ ] 56. Systems Manager
- [ ] 57. WAF / Shield / Firewall Manager
- [ ] 58. GuardDuty / Inspector / Macie 등 Security Services

## 12부 — VPC & Networking

Core Lab 파트.

- [ ] 59. VPC
- [ ] 60. Subnet과 Route Table
- [ ] 61. Internet Gateway와 NAT Gateway
- [ ] 62. Security Group과 NACL
- [ ] 63. VPC Peering / Transit Gateway
- [ ] 64. VPC Endpoint / PrivateLink
- [ ] 65. VPN / Direct Connect
- [ ] 66. VPC Flow Logs / Networking Troubleshooting

## 13부 — Disaster Recovery & Migration

- [ ] 67. RPO / RTO
- [ ] 68. Backup & Restore
- [ ] 69. Pilot Light
- [ ] 70. Warm Standby
- [ ] 71. Multi-Site / Active-Active
- [ ] 72. DMS / SCT
- [ ] 73. Application Migration Service / Migration Strategies

## 14부 — Infrastructure as Code

강의 + 취업 포트폴리오 확장.

- [ ] 74. CloudFormation
- [ ] 75. Terraform

## 15부 — CI/CD

강의 범위를 넘어 Cloud Engineer 포트폴리오를 위한 확장 파트.

- [ ] 76. GitHub Actions
- [ ] 77. Docker Image Build / ECR Push
- [ ] 78. ECS Deployment Pipeline
- [ ] 79. Rollback Strategy

## 16부 — Architecture & Well-Architected

강의의 Classic Solutions Architecture, More Solutions Architecture,
Disaster Recovery, White Papers / Architectures를 종합하는 파트다.

- [ ] 80. Classic Architecture Patterns
- [ ] 81. High Availability
- [ ] 82. Scalability / Decoupling
- [ ] 83. Serverless Architecture
- [ ] 84. Global Architecture
- [ ] 85. 비용 최적화
- [ ] 86. AWS Well-Architected Framework
- [ ] 87. SAA 종합 설계 문제
- [ ] 88. Final Architecture Review

---

# Portfolio — Cloud Shop

메인 포트폴리오 도메인은 **쇼핑몰**로 고정한다.

애플리케이션 기능 자체보다 하나의 서비스를 AWS에서 어떻게 배포하고,
확장하고, 보안하고, 관측하고, 자동화하는지를 보여주는 것이 목적이다.

초기 도메인 모델은 최소한으로 유지한다.

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

자세한 포트폴리오 계획은 [portfolio/README.md](./portfolio/README.md)에 관리한다.

## Portfolio Stages

### Stage 1 — Single EC2

FastAPI 쇼핑몰 API를 EC2 한 대에 배포한다.

```text
Internet → Security Group → EC2 → FastAPI
```

Linux process, systemd, Nginx, User Data, SSH, 로그와 포트를 직접 확인한다.

### Stage 2 — Database Separation

PostgreSQL을 RDS로 분리한다.

```text
Internet → EC2 → RDS
```

Application과 Database Security Group을 분리하고 접근 경로를 검증한다.

### Stage 3 — High Availability

ALB + Auto Scaling + Multi-AZ 구조로 확장한다.

```text
             ALB
            /   \
         App     App
           \     /
             RDS
```

Health Check와 인스턴스 장애 복구를 실험한다.

### Stage 4 — Object Storage & CDN

상품 이미지를 S3에 저장하고 CloudFront로 제공한다.

### Stage 5 — Asynchronous Processing

주문 후 이메일/후처리 작업을 SQS와 Worker로 분리한다.

```text
Order API → SQS → Worker
```

### Stage 6 — Containers

애플리케이션과 Worker를 Docker로 만들고 ECR/ECS로 이전한다.

### Stage 7 — Infrastructure as Code

VPC, Subnet, Security Group, ALB, ECS, RDS 등을 Terraform으로 코드화한다.

### Stage 8 — CI/CD

GitHub Actions로 테스트 → 이미지 빌드 → ECR → ECS 배포 파이프라인을 구성한다.

### Stage 9 — Observability & Failure Lab

CloudWatch 기반 로그, 메트릭, Alarm을 구성하고 장애 실험을 수행한다.

예:

```text
DB Security Group 차단
→ DB connection 실패
→ 로그/메트릭 관측
→ 원인 진단
→ 복구

ALB Health Check 경로 오류
→ Target unhealthy
→ 요청 실패
→ Target Group 관측
→ 수정

Application process 종료
→ Health Check 실패
→ 서비스 복구 과정 관측
```

### Stage 10 — Portfolio Polish

학습용 프로젝트를 취업용 포트폴리오로 재가공한다.

- Architecture Diagram
- Requirements
- AWS Service 선택 이유
- Network / Security Design
- CI/CD
- Terraform 구조
- Monitoring
- Failure Experiments
- Troubleshooting 기록
- 비용 / 가용성 trade-off
- 개선 가능성

필요하면 이후 AI 추천, 상품 설명 생성, 이미지 태깅 등의 기능을 선택적으로 붙일 수 있지만,
프로젝트의 본체는 AWS 인프라와 운영이다.

## 최종적으로 답할 수 있어야 하는 질문

- 왜 이 AWS 서비스를 선택했는가?
- 다른 대안 대신 이것을 선택한 이유는 무엇인가?
- 장애가 발생하면 어떤 현상이 나타나는가?
- 어디에서 문제를 관측할 수 있는가?
- 어떤 순서로 원인을 좁히는가?
- 어떻게 복구하는가?
- 더 많은 트래픽을 처리하려면 어떻게 변경해야 하는가?
- 비용과 안정성 사이에 어떤 trade-off가 존재하는가?
- 이 인프라를 다시 만들거나 배포하려면 얼마나 자동화되어 있는가?
