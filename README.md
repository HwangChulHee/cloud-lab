# cloud-lab

AWS와 클라우드 인프라를 학습하고 직접 구축하며,
Cloud Engineer 취업에 필요한 기반 역량을 만드는 저장소.

현재 우선순위는 **AWS Certified Solutions Architect - Associate(SAA) 취득**이다.
SAA 취득 전에는 강의 커버리지와 강의 Hands-on에 집중하고,
취득 후 Java/Spring 기반 Cloud Shop 포트폴리오를 본격적으로 진행한다.

## 진행 원칙

이 저장소는 두 단계로 운영한다.

### Phase 1 — SAA Certification

Stéphane Maarek SAA-C03 강의를 기준으로 시험 범위를 가능한 한 빠짐없이 세밀하게 매핑한다.

시험 전에는 다음에 집중한다.

- 강의 진도
- 강의에서 다루는 AWS 서비스와 선택 기준 정리
- 강의 Hands-on
- 중요한 개념의 최소 관측/확인

별도의 대형 프로젝트, Terraform 심화, GitHub Actions 기반 CI/CD, Spring 학습은 이 단계에서 진행하지 않는다.
강의 이후의 복습, 모의고사, 종합 문제 풀이는 별도 시험 강의를 활용하므로 이 저장소의 커리큘럼에서 관리하지 않는다.

### Phase 2 — Portfolio after SAA

SAA 취득 후에는 강의에서 배운 AWS 지식을 실제 운영 가능한 시스템으로 확장한다.

> 이해 → 구축 → 예측 → 관측 → 장애 → 분석 → 복구 → 자동화

이 단계에서 다음을 본격적으로 진행한다.

- Java 21 / Spring Boot 최소 학습
- Cloud Shop 구현
- Docker / ECR / ECS
- Terraform
- GitHub Actions CI/CD
- CloudWatch 기반 운영/장애 실험
- 취업용 포트폴리오 문서화

자세한 계획은 [portfolio/README.md](./portfolio/README.md)와 [spring_minimum/README.md](./spring_minimum/README.md)에 보관한다.

## 학습 깊이

모든 AWS 서비스를 같은 깊이로 다루지 않는다.

- **Coverage**: 개념과 SAA 선택 기준을 이해하면 충분한 주제
- **Hands-on**: 강의 실습을 따라 직접 확인할 주제
- **Core Lab (시험 후)**: 구축, 관측, 장애 실험, 복구, 자동화, 포트폴리오까지 연결할 핵심 주제

Rekognition, Polly 같은 서비스는 Coverage 중심으로 빠르게 지나가고,
EC2, VPC, RDS, ALB, ECS, CloudWatch 등은 시험 후 Core Lab으로 다시 깊게 다룬다.

## 학습 자료

- AWS Certified Solutions Architect - Associate (SAA-C03)
- Stéphane Maarek - Ultimate AWS Certified Solutions Architect Associate
- AWS 공식 문서

강의와 저장소의 세밀한 대응 관계는 [CURRICULUM_MAPPING.md](./CURRICULUM_MAPPING.md)에 관리한다.

---

# Phase 1 Curriculum — SAA Coverage

## 0부 — Cloud & System Foundation

강의 외 최소 보강 파트. 이미 학습한 기반은 이후 AWS 개념을 이해하는 데 활용한다.

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
- [ ] 07. Security Group 심화 개념
  - [ ] Stateful 동작
  - [ ] Security Group Reference
  - [ ] 계층별 접근 제어 개념

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

SAA 시험 전에는 강의가 요구하는 AWS 컨테이너 서비스의 개념과 선택 기준이 우선이다.

- [ ] 28. Docker 최소 개념
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

- [ ] 36. AWS Database 선택 지도
  - [ ] RDS / Aurora
  - [ ] DynamoDB
  - [ ] ElastiCache
  - [ ] DocumentDB
  - [ ] Neptune
  - [ ] Keyspaces
  - [ ] 기타 강의 등장 서비스
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

## 14부 — Remaining SAA Architecture & Services

강의 후반의 Architecture / Other Services / White Papers 관련 **강의 커버리지**를 매핑한다.
별도의 모의고사나 종합 문제 세트는 이 저장소에서 만들지 않는다.

- [ ] 74. CloudFormation / AWS IaC 개념
- [ ] 75. Classic Solutions Architecture에서 등장하는 패턴
- [ ] 76. More Solutions Architecture에서 등장하는 패턴
- [ ] 77. High Availability / Scalability 선택 기준
- [ ] 78. 비용 최적화
- [ ] 79. AWS Well-Architected Framework
- [ ] 80. Other Services / White Papers에서 강의가 다루는 시험 포인트

> 강의 1회독 이후 시험 복습, 모의고사와 종합 문제 풀이는 별도 시험 강의를 사용한다.

---

# Phase 2 — Portfolio after SAA Certification

SAA 취득 전에는 아래 항목을 본격적으로 진행하지 않는다.
설계만 보존해두고 자격증 취득 후 하나씩 구현한다.

## Spring Minimum

- Java 21 최소 기반
- Spring Boot / Spring Web
- Spring Data JPA / Transaction
- Validation / Exception Handling
- Spring Security 필요 범위
- Actuator / 운영 연결

## Cloud Shop

백엔드 기본 스택:

```text
Java 21
Spring Boot
PostgreSQL
```

도메인:

```text
User
Product
Cart
Order
OrderItem
```

인프라 발전 흐름:

```text
Spring Boot + EC2
→ RDS
→ ALB + Auto Scaling
→ S3 + CloudFront
→ SQS + Worker
→ Docker + ECR + ECS
→ Terraform
→ GitHub Actions
→ CloudWatch + Failure Lab
→ 취업용 포트폴리오 정리
```

자세한 내용은 [portfolio/README.md](./portfolio/README.md)에 관리한다.

## 시험 이후 추가 학습

- Terraform
- GitHub Actions / CI/CD
- 장애 실험과 복구
- 운영 관측 심화
- 필요 시 EKS / Kubernetes
- 필요 시 Spring 백엔드 심화

최종 목표는 단순히 AWS 서비스를 사용한 기록이 아니라,
**Java/Spring 쇼핑몰 서비스를 AWS에서 설계·배포·운영·자동화하고 그 의사결정을 설명할 수 있는 취업 포트폴리오**를 만드는 것이다.
