# cloud-lab

AWS와 클라우드 인프라를 학습하고 직접 구축하며,
Cloud Engineer 취업에 필요한 기반 역량을 만드는 저장소.

단기적으로 AWS Certified Solutions Architect - Associate(SAA) 취득과
AWS 기반 인프라 포트폴리오 완성을 목표로 한다.

## 목표 역량

1. AWS의 주요 서비스를 단순히 사용하는 것을 넘어 어떤 상황에서 왜 선택하는지 설명할 수 있다.
2. 웹 애플리케이션을 AWS에 직접 배포하고 네트워크, 컴퓨팅, 데이터베이스, 보안 구조를 설계할 수 있다.
3. 장애 상황을 관측하고 원인을 추적하여 복구할 수 있다.
4. Docker, Terraform, CI/CD를 이용해 인프라 구축과 배포를 자동화할 수 있다.
5. SAA에서 요구하는 AWS 아키텍처 선택 문제를 원리를 바탕으로 판단할 수 있다.

## 학습 방식

각 주제는 유닛(Unit) 단위로 진행한다.

기본적인 유닛은 다음 구조를 따른다.

- **개념**: 서비스가 해결하는 문제와 동작 원리를 이해한다.
- **SAA 연결**: 시험에서 요구하는 서비스 선택 기준과 비교 포인트를 정리한다.
- **예제**: 최소한의 정상 동작 환경을 직접 구축한다.
- **관측**: CLI, 로그, 메트릭 등을 통해 실제 동작을 확인한다.
- **유제**: 배운 내용을 이용해 스스로 환경을 구성하거나 수정한다.
- **장애 실험**: 설정을 의도적으로 변경하거나 장애를 발생시킨 뒤 원인을 분석한다.
- **포트폴리오 반영**: 배운 내용을 메인 AWS 프로젝트에 적용한다.
- **3문장 요약**: 학습한 내용을 자신의 언어로 정리한다.

가능하면 다음 순서를 따른다.

> 이해 → 구축 → 예측 → 관측 → 장애 → 분석 → 복구

강의의 Hands-on은 개념을 익히기 위한 첫 예제로 사용하고,
포트폴리오는 이를 그대로 복제하지 않고 직접 설계하고 확장한다.

## 학습 자료

- AWS Certified Solutions Architect - Associate (SAA-C03)
- Stéphane Maarek - Ultimate AWS Certified Solutions Architect Associate
- AWS 공식 문서

## 진행

### 0부 — 클라우드와 시스템 기반

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

### 1부 — Identity & Compute

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
- [ ] 06. EBS
- [ ] 07. Security Group 심화 / 운영

### 2부 — High Availability

- [ ] 08. Elastic Load Balancing
- [ ] 09. Auto Scaling

### 3부 — Data

- [ ] 10. RDS
- [ ] 11. Aurora
- [ ] 12. ElastiCache

### 4부 — Web & Storage

- [ ] 13. S3
- [ ] 14. Route 53
- [ ] 15. CloudFront
- [ ] 16. ACM / HTTPS

### 5부 — Messaging

- [ ] 17. SQS
- [ ] 18. SNS
- [ ] 19. EventBridge

### 6부 — Containers

- [ ] 20. Docker
- [ ] 21. ECR
- [ ] 22. ECS

### 7부 — Serverless

- [ ] 23. Lambda
- [ ] 24. API Gateway
- [ ] 25. DynamoDB

### 8부 — Operations & Security

- [ ] 26. CloudWatch
- [ ] 27. CloudTrail
- [ ] 28. KMS
- [ ] 29. Systems Manager
- [ ] 30. Secrets Management

### 9부 — Networking

- [ ] 31. VPC
- [ ] 32. Subnet과 Route Table
- [ ] 33. Internet Gateway와 NAT Gateway
- [ ] 34. Security Group과 NACL
- [ ] 35. VPC Endpoint / PrivateLink

### 10부 — Infrastructure as Code

- [ ] 36. CloudFormation
- [ ] 37. Terraform

### 11부 — CI/CD

- [ ] 38. GitHub Actions
- [ ] 39. Container Build & Deployment Pipeline

### 12부 — Architecture

- [ ] 40. High Availability
- [ ] 41. Disaster Recovery
- [ ] 42. 비용 최적화
- [ ] 43. AWS Well-Architected

## Portfolio

학습 과정에서 하나의 웹 서비스를 단계적으로 발전시킨다.

### Stage 1

EC2 단일 서버에 애플리케이션 배포.

### Stage 2

ALB와 Auto Scaling을 이용한 Multi-AZ 구성.

### Stage 3

RDS를 분리하고 Private Network 구성.

### Stage 4

Docker / ECR / ECS 기반으로 이전.

### Stage 5

Terraform으로 AWS 인프라를 코드화.

### Stage 6

GitHub Actions를 이용해 CI/CD 구축.

### Stage 7

CloudWatch 기반 모니터링과 장애 대응 실험.

최종적으로 다음 질문에 답할 수 있는 시스템을 만든다.

- 왜 이 AWS 서비스를 선택했는가?
- 장애가 발생하면 어떤 현상이 나타나는가?
- 어디에서 문제를 관측할 수 있는가?
- 어떻게 복구하는가?
- 더 많은 트래픽을 처리하려면 어떻게 변경해야 하는가?
- 비용과 안정성 사이에서 어떤 trade-off가 존재하는가?
