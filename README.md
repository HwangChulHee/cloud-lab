# cloud-lab

AWS와 클라우드 인프라를 학습하고 직접 구축하며,
Cloud Engineer 취업에 필요한 기반 역량을 만드는 저장소.

현재 우선순위는 **AWS Certified Solutions Architect - Associate(SAA) 취득**이다.
SAA 취득 전에는 강의 커버리지와 강의 Hands-on에 집중하고,
이후 `examples/`에서 핵심 AWS를 반복 구축한 뒤 `portfolio/`에서 실제 프로젝트로 확장한다.

## 저장소 구조

```text
part00~part14/
  → SAA 강의 이론 / 서비스별 선택 기준

examples/
  → 핵심 AWS 반복 구축 / 관측 / 장애 / 복구 / CLI 검증

portfolio/
  → 실제 애플리케이션 + IaC + CI/CD + 운영 자동화

spring_minimum/
  → 포트폴리오에 필요한 Java / Spring 최소 기반

interview/
  → 클라우드 / DevOps 면접 대비
```

학습 흐름은 다음과 같다.

```text
SAA 이론(part00~14)
        ↓
핵심 AWS 실습(examples/01~16)
        ↓
실제 프로젝트(portfolio/)
        ↓
Terraform / Docker / ECS / CI/CD / 운영 심화
```

## 진행 원칙

### Phase 1 — SAA Certification

Stéphane Maarek SAA-C03 강의를 기준으로 시험 범위를 가능한 한 빠짐없이 세밀하게 매핑한다.

시험 전에는 다음에 집중한다.

- 강의 진도
- 강의에서 다루는 AWS 서비스와 선택 기준 정리
- 강의 Hands-on
- 중요한 개념의 최소 관측/확인

별도의 대형 프로젝트, Terraform 심화, GitHub Actions 기반 CI/CD, Spring 학습은 이 단계에서 진행하지 않는다.
강의 이후의 복습, 모의고사, 종합 문제 풀이는 별도 시험 강의를 활용하므로 이 저장소의 커리큘럼에서 관리하지 않는다.

### Phase 1B — Core AWS Examples

SAA 핵심 이론을 확보한 뒤 [`examples/`](./examples/)에서 EC2, VPC, ALB, ASG, RDS, S3, IAM, Route 53, CloudWatch를 실제로 반복 구축한다.

> 따라 만들기 → 기억만으로 반복 → 관측 → 장애 재현 → 분석 → 복구 → CLI 검증

후반 Example은 가이드를 줄여 요구사항만 보고 전체 구조를 다시 만들 수 있게 한다.

### Phase 2 — Portfolio

핵심 실습 이후에는 강의에서 배운 AWS 지식을 실제 운영 가능한 시스템으로 확장한다.

> 이해 → 구축 → 예측 → 관측 → 장애 → 분석 → 복구 → 자동화

이 단계에서 다음을 본격적으로 진행한다.

- Java 21 / Spring Boot 최소 학습
- Cloud Shop 구현
- RDS / S3 연동
- ALB / Auto Scaling / Multi-AZ
- SQS / Worker
- Docker / ECR / ECS
- Terraform
- GitHub Actions CI/CD
- CloudWatch 기반 운영/장애 실험
- 취업용 포트폴리오 문서화

자세한 계획은 [portfolio/README.md](./portfolio/README.md)와 [spring_minimum/README.md](./spring_minimum/README.md)에 보관한다.

## 학습 깊이

모든 AWS 서비스를 같은 깊이로 다루지 않는다.

- **Coverage (C)**: 개념과 SAA 선택 기준을 이해하면 충분한 주제
- **Hands-on (H)**: 강의 실습 또는 최소 확인까지 직접 수행할 주제
- **Deep Practice (DP)**: `examples/` 또는 포트폴리오에서 구축, 관측, 장애, 복구까지 반복할 핵심 주제

Rekognition, Polly 같은 서비스는 Coverage 중심으로 빠르게 지나가고,
EC2, VPC, RDS, ALB, S3, IAM, CloudWatch 등은 Deep Practice 대상으로 다시 깊게 다룬다.

## 학습 자료

- AWS Certified Solutions Architect - Associate (SAA-C03)
- Stéphane Maarek - Ultimate AWS Certified Solutions Architect Associate
- AWS 공식 문서

강의와 저장소의 세밀한 대응 관계는 [CURRICULUM_MAPPING.md](./CURRICULUM_MAPPING.md)에 관리한다.

---

# Phase 1 Curriculum — SAA Coverage

## 0부 — Cloud & System Foundation

강의 외 최소 보강 파트. 이미 학습한 기반은 이후 AWS 개념을 이해하는 데 활용한다.

- [x] 00. AWS와 클라우드의 전체 그림
  - [x] u1. 클라우드란 무엇인가
  - [x] u2. Region / Availability Zone / Edge Location
  - [x] u3. AWS 서비스의 범위 — Global vs Regional
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

- [x] 04. IAM
- [x] 05. EC2
- [x] 06. EC2 Instance Storage
- [x] 07. Security Group 심화 개념

## 2부 — High Availability & Scalability

- [x] 08. Elastic Load Balancing
- [x] 09. Auto Scaling

## 3부 — Relational Data & Cache

- [x] 10. RDS
- [ ] 11. Aurora
- [ ] 12. ElastiCache

## 4부 — Route 53, S3 & Global Delivery

- [x] 13. Route 53
  - [x] DNS Records
  - [x] Routing Policies
  - [x] Health Checks
  - [x] Alias Records
- [x] 14. S3 Core
  - [x] Bucket / Object
  - [x] Versioning
  - [x] Replication
  - [x] Storage Classes
  - [x] Lifecycle
- [ ] 15. S3 Advanced & Security
  - [ ] Bucket Policy / IAM
  - [ ] Encryption
  - [ ] CORS
  - [ ] Presigned URL
  - [ ] Performance / Multipart Upload
  - [ ] Event Notification
- [ ] 16. CloudFront / Global Accelerator
- [ ] 17. ACM / HTTPS

## 5부 — Storage Extras

- [ ] 18. EFS
- [ ] 19. FSx
- [ ] 20. Storage Gateway
- [ ] 21. DataSync / Transfer Family
- [ ] 22. Snow Family

## 6부 — Messaging & Integration

- [ ] 23. SQS
- [ ] 24. SNS
- [ ] 25. EventBridge
- [ ] 26. Kinesis
- [ ] 27. Amazon MQ / Integration 선택 기준

## 7부 — Containers

- [ ] 28. Docker
- [ ] 29. ECR
- [ ] 30. ECS
- [ ] 31. EKS / App Runner 개념 비교

## 8부 — Serverless & NoSQL

- [ ] 32. Lambda
- [ ] 33. API Gateway
- [ ] 34. DynamoDB
- [ ] 35. Step Functions / Cognito 등 Serverless 연계 서비스

## 9부 — Databases, Data & Analytics

- [ ] 36. AWS Database 선택 지도
- [ ] 37. Athena
- [ ] 38. Redshift
- [ ] 39. EMR
- [ ] 40. Glue
- [ ] 41. OpenSearch
- [ ] 42. Lake Formation / QuickSight / MSK 등 Analytics 서비스

## 10부 — Machine Learning for SAA

- [ ] 43. Rekognition
- [ ] 44. Transcribe / Polly / Translate
- [ ] 45. Comprehend
- [ ] 46. Lex
- [ ] 47. SageMaker
- [ ] 48. Textract
- [ ] 49. Kendra / Personalize 등 강의 등장 서비스

## 11부 — Monitoring, Advanced Identity & Security

실습과 운영 이해를 위해 **50 CloudWatch, 51 CloudTrail, 54 KMS, 56 Systems Manager는 우선 깊게 학습**한다. 나머지는 우선 SAA Coverage 중심으로 본다.

- [ ] 50. CloudWatch — Deep
- [ ] 51. CloudTrail — Deep
- [ ] 52. AWS Config — Coverage
- [ ] 53. Advanced Identity — Coverage
- [ ] 54. KMS — Deep
- [ ] 55. Secrets Manager / Parameter Store — Coverage
- [ ] 56. Systems Manager — Deep
- [ ] 57. WAF / Shield / Firewall Manager — Coverage
- [ ] 58. GuardDuty / Inspector / Macie 등 Security Services — Coverage

## 12부 — VPC & Networking

실습 전에 구조를 충분히 이해한다.

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

## 14부 — CloudFormation & Architecture Coverage

- [ ] 74. CloudFormation
- [ ] 75. Classic Solutions Architecture
- [ ] 76. High Availability / Scalability Patterns
- [ ] 77. Serverless / Global Architecture Patterns
- [ ] 78. 비용 최적화 개념
- [ ] 79. AWS Well-Architected Framework
- [ ] 80. More Solutions Architecture / White Papers Coverage

---

# Phase 2 Curriculum — Portfolio

## P0 — Java / Spring Minimum

- Java 21 최소 기반
- Spring Boot / Web
- Spring Data JPA
- Transaction
- Validation / Exception Handling
- Actuator

## P1 — Cloud Shop Build & Operations

- 실제 Spring 애플리케이션 배포
- RDS / S3 연동
- ALB / Auto Scaling / Multi-AZ
- SQS / Worker
- Docker / ECR / ECS
- CloudWatch 관측 및 장애 실험

## P2 — Infrastructure as Code

- Terraform

## P3 — CI/CD

- GitHub Actions
- Docker Image Build / ECR Push
- ECS Deployment Pipeline
- Rollback Strategy

## P4 — Portfolio Polish

- Architecture Diagram
- AWS 서비스 선택 근거
- Network / Security Design
- Monitoring / Failure Experiments
- Cost / Availability / Complexity trade-off

자세한 단계별 설계는 [portfolio/README.md](./portfolio/README.md)를 참고한다.
