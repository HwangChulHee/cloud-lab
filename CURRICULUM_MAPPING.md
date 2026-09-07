# SAA Course Coverage Mapping

이 문서는 Stéphane Maarek SAA-C03 강의와 `cloud-lab` 커리큘럼의 대응 관계를 관리한다.

현재 우선순위는 **SAA 취득**이다.
강의 커버리지를 세밀하게 따라가되, 포트폴리오용 심화 실습은 시험 이후로 미룬다.

## Depth Legend

- **C — Coverage**: 개념 + SAA 선택 기준 중심
- **H — Hands-on**: 강의에서 제공하는 실습 또는 최소 확인
- **CL — Core Lab (시험 후)**: 구축 + 관측 + 장애 실험 + 복구 + 포트폴리오 연결

`CL`로 표시된 주제라도 SAA 취득 전에는 C/H까지만 진행한다.

---

## Course → cloud-lab Mapping

| 강의 큰 섹션 | cloud-lab 대응 | 시험 전 | 시험 후 |
|---|---|---:|---:|
| Cloud / Global Infrastructure Intro | 0부 Foundation / 00 AWS Overview | C | 필요 시 보강 |
| IAM | 1부 / 04 IAM | C~H | CL 가능 |
| EC2 Basics | 1부 / 05 EC2 | C~H | CL |
| EC2 Associate | 1부 / 05 EC2 | C~H | 필요 시 심화 |
| EC2 Instance Storage | 1부 / 06 EC2 Instance Storage | C~H | CL |
| High Availability & Scalability | 2부 / ELB, Auto Scaling | C~H | CL |
| RDS, Aurora, ElastiCache | 3부 | C~H | CL |
| Route 53 | 4부 / Route 53 | C~H | L |
| Classic Solutions Architecture | 14부 + 각 관련 서비스 | C | 포트폴리오 설계에 활용 |
| S3 | 4부 / S3 Core | C~H | CL 가능 |
| S3 Advanced | 4부 / S3 Advanced & Security | C~H | L |
| S3 Security | 4부 / S3 Advanced & Security | C~H | L |
| CloudFront & Global Accelerator | 4부 | C~H | L |
| Storage Extras | 5부 | C~H | 필요 시 L |
| Messaging / Integration | 6부 | C~H | SQS 중심 CL |
| Containers | 7부 | C~H | ECS 중심 CL |
| Serverless | 8부 | C~H | 필요 시 L~CL |
| Databases in AWS | 9부 Database 선택 지도 | C | 필요 시 보강 |
| Data & Analytics | 9부 | C | 필요 시 보강 |
| Machine Learning | 10부 | C | 선택 |
| Monitoring | 11부 | C~H | CloudWatch 중심 CL |
| Advanced Identity | 11부 | C~H | 필요 시 L |
| Security & Encryption | 11부 | C~H | 필요 시 L |
| VPC | 12부 | C~H | CL |
| Disaster Recovery & Migrations | 13부 | C~H | 필요 시 L |
| More Solutions Architecture | 14부 | C | 포트폴리오 설계에 활용 |
| Other Services | 14부 또는 해당 기능별 파트 | C | 선택 |
| White Papers & Architectures | 14부 | C | 포트폴리오 설계에 활용 |

---

## 시험 전 운영 원칙

### 1. 강의 순서를 우선한다

강의에서 연속적으로 등장하는 내용은 학습 순서도 가능한 한 맞춘다.
디렉터리 구조는 개념적으로 정리하되 강의 흐름을 방해하지 않는다.

예:

```text
EC2 Launch
→ Instance Type
→ Security Group / SSH
→ Purchasing Options
→ IP / EIP
```

### 2. 강의 Hands-on까지만 기본 수행한다

시험 전에는 별도의 대형 시스템을 만들지 않는다.
중요 서비스라도 우선은 다음 정도면 충분하다.

```text
개념 이해
→ 선택 기준 정리
→ 강의 Hands-on
→ 필요한 최소 관측
→ 다음 강의
```

### 3. 시험 전용 서비스는 과도하게 실습하지 않는다

예:

```text
Rekognition
Polly
Translate
Comprehend
Kendra
```

다음 질문에 답할 수 있으면 우선 충분하다.

```text
무슨 문제를 해결하는가?
어떤 키워드가 나오면 선택하는가?
헷갈리는 서비스와 차이는 무엇인가?
```

### 4. 시험 복습은 이 저장소가 담당하지 않는다

강의 1회독 후의 다음 작업은 별도의 시험 강의를 사용한다.

- 모의고사
- 종합 문제
- 오답 정리
- 시험 직전 복습

따라서 `cloud-lab`에는 별도의 Phase 2 시험 복습 커리큘럼을 만들지 않는다.

---

## SAA 취득 후 다시 깊게 다룰 Core Lab

다음 서비스는 시험 전에는 C/H 수준으로 학습하지만,
Cloud Shop 포트폴리오를 만들면서 다시 깊게 다룬다.

```text
IAM
EC2
EBS
Security Group
ALB
Auto Scaling
RDS
S3
SQS
ECS
CloudWatch
VPC
```

그때 다음 흐름을 적용한다.

> 구축 → 예측 → 관측 → 장애 → 분석 → 복구 → 자동화

추가로 강의 범위를 넘어:

```text
Java / Spring Boot
Docker
Terraform
GitHub Actions
CI/CD
운영 문서화
```

를 포트폴리오에 연결한다.

---

## 강의와 별개로 추가되는 학습 — 시험 후

### Spring / Backend

- Java 21 최소 기반
- Spring Boot / Web
- JPA / Transaction
- Validation / Security
- Actuator

### Operations

- 장애 원인 계층화
- 로그/메트릭 관측
- Security Group 오설정 실험
- Health Check 실패 실험
- Application process 종료 실험
- DB connection 장애 실험

### Automation

- Docker
- Terraform
- GitHub Actions
- ECR / ECS 배포 파이프라인
- Rollback 전략

### Portfolio

강의 Hands-on을 그대로 제출하지 않는다.
Java/Spring 기반 쇼핑몰 시스템을 단계적으로 발전시킨다.

자세한 내용은 `portfolio/README.md`를 참고한다.

---

## 강의 진행 중 체크 방법

강의 섹션 하나를 끝낼 때마다 다음만 확인한다.

```text
[ ] 강의에서 다룬 서비스가 curriculum에 존재하는가?
[ ] 핵심 선택 기준이 정리되어 있는가?
[ ] 강의 Hands-on이 있다면 필요한 만큼 따라갔는가?
[ ] 헷갈리는 비교 대상은 무엇인가?
```

포트폴리오 반영 여부와 장애 실험 여부는 **SAA 취득 후** 다시 판단한다.
