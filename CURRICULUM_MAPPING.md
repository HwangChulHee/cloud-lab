# SAA Course Coverage Mapping

이 문서는 Stéphane Maarek SAA-C03 강의와 `cloud-lab` 커리큘럼의 대응 관계를 관리한다.

현재 우선순위는 **SAA 취득**이다.
강의 커버리지를 세밀하게 따라가되, 핵심 AWS 심화 실습과 포트폴리오는 단계적으로 분리한다.

## Depth Legend

- **C — Coverage**: 개념 + SAA 선택 기준 중심
- **H — Hands-on**: 강의에서 제공하는 실습 또는 최소 확인
- **DP — Deep Practice**: `examples/` 또는 포트폴리오에서 구축 + 관측 + 장애 + 복구까지 반복

`DP` 대상도 SAA 강의 진행 중에는 우선 C/H 수준으로 학습하고, 핵심 이론을 확보한 뒤 `examples/`에서 깊게 다룬다.

---

## Course → cloud-lab Mapping

| 강의 큰 섹션 | cloud-lab 대응 | 시험 전 | 이후 |
|---|---|---:|---:|
| Cloud / Global Infrastructure Intro | 00부 Foundation / 00 AWS Overview | C | 필요 시 보강 |
| IAM | 01부 / 04 IAM | C~H | DP |
| EC2 Basics | 01부 / 05 EC2 | C~H | DP |
| EC2 Associate | 01부 / 05 EC2 | C~H | 필요 시 심화 |
| EC2 Instance Storage | 01부 / 06 EC2 Instance Storage | C~H | DP |
| High Availability & Scalability | 02부 / ELB, Auto Scaling | C~H | DP |
| RDS, Aurora, ElastiCache | 03부 | C~H | RDS 중심 DP |
| Route 53 | 04부 / Route 53 | C~H | DP |
| Classic Solutions Architecture | 14부 + 각 관련 서비스 | C | 포트폴리오 설계에 활용 |
| S3 | 04부 / S3 Core | C~H | DP |
| S3 Advanced | 04부 / S3 Advanced & Security | C~H | 핵심 기능 DP |
| S3 Security | 04부 / S3 Advanced & Security | C~H | DP |
| CloudFront & Global Accelerator | 04부 | C~H | 필요 시 심화 |
| Storage Extras | 05부 | C~H | 필요 시 심화 |
| Messaging / Integration | 06부 | C~H | SQS 중심 포트폴리오 확장 |
| Containers | 07부 | C~H | ECS 중심 포트폴리오 확장 |
| Serverless | 08부 | C~H | 필요 시 심화 |
| Databases in AWS | 09부 Database 선택 지도 | C | 필요 시 보강 |
| Data & Analytics | 09부 | C | 필요 시 보강 |
| Machine Learning | 10부 | C | 선택 |
| Monitoring | 11부 | C~H | CloudWatch 중심 DP |
| Advanced Identity | 11부 | C~H | 필요 시 심화 |
| Security & Encryption | 11부 | C~H | KMS 중심 DP |
| VPC | 12부 | C~H | DP |
| Disaster Recovery & Migrations | 13부 | C~H | 필요 시 심화 |
| More Solutions Architecture | 14부 | C | 포트폴리오 설계에 활용 |
| Other Services | 14부 또는 해당 기능별 파트 | C | 선택 |
| White Papers & Architectures | 14부 | C | 포트폴리오 설계에 활용 |

---

## 학습 단계

```text
1. part00~14
   SAA 개념 / 선택 기준 / 강의 Hands-on

2. examples/01~16
   핵심 AWS 반복 구축 / 관측 / 장애 / 복구 / CLI 검증

3. portfolio/
   실제 애플리케이션 + Terraform + Docker/ECS + CI/CD + 운영 자동화
```

## 시험 전 운영 원칙

### 1. 강의 순서를 우선한다

강의에서 연속적으로 등장하는 내용은 학습 순서도 가능한 한 맞춘다.
디렉터리 구조는 개념적으로 정리하되 강의 흐름을 방해하지 않는다.

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

강의 1회독 후의 모의고사, 종합 문제, 오답 정리, 시험 직전 복습은 별도 시험 자료를 활용한다.

---

## Deep Practice 대상

`examples/`에서 우선 깊게 반복할 핵심은 다음과 같다.

```text
IAM
EC2
EBS / AMI
Security Group
ALB / Target Group / Health Check
Auto Scaling
RDS
S3
Route 53 / ACM
CloudWatch
Systems Manager
VPC
```

11부에서는 추가로 다음을 깊게 본다.

```text
CloudTrail — 변경 주체와 API 호출 감사
KMS        — S3/EBS/RDS 암호화와 IAM 권한 연결
```

Deep Practice의 기본 흐름:

> 구축 → 예측 → 관측 → 장애 → 분석 → 복구 → CLI 검증

---

## 포트폴리오에서 확장할 것

`examples/`를 끝낸 뒤 다음을 실제 애플리케이션에 연결한다.

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

### Automation / Runtime

- Docker
- Terraform
- GitHub Actions
- ECR / ECS 배포 파이프라인
- Rollback 전략

### Portfolio

강의 Hands-on을 그대로 제출하지 않는다.
Java/Spring 기반 Cloud Shop을 단계적으로 발전시키고 AWS 서비스 선택 근거, 장애 실험, 비용/가용성 trade-off를 문서화한다.

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

`examples/`와 포트폴리오 반영 여부는 해당 핵심 이론을 학습한 뒤 진행한다.
