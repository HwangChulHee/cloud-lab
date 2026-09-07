# SAA Course Coverage Mapping

이 문서는 Stéphane Maarek SAA-C03 강의와 `cloud-lab` 커리큘럼의 대응 관계를 관리한다.

목표는 두 가지다.

1. 강의에서 다루는 시험 범위를 빠뜨리지 않는다.
2. 모든 주제를 같은 깊이로 실습하지 않고 Cloud Engineer 관점에서 중요도에 따라 깊이를 조절한다.

## Depth Legend

- **C — Coverage**: 개념 + SAA 선택 기준 중심
- **L — Lab**: 직접 구축/확인까지 진행
- **CL — Core Lab**: 구축 + 관측 + 장애 실험 + 복구 + 포트폴리오 연결

---

## Course → cloud-lab Mapping

| 강의 큰 섹션 | cloud-lab 대응 | 깊이 |
|---|---|---|
| Cloud / Global Infrastructure Intro | 0부 Foundation / 00 AWS Overview | C |
| IAM | 1부 / 04 IAM | L |
| EC2 Basics | 1부 / 05 EC2 | CL |
| EC2 Associate | 1부 / 05 EC2 | C~L |
| EC2 Instance Storage | 1부 / 06 EC2 Instance Storage | CL |
| High Availability & Scalability | 2부 / ELB, Auto Scaling | CL |
| RDS, Aurora, ElastiCache | 3부 | CL |
| Route 53 | 4부 / Route 53 | L |
| Classic Solutions Architecture | 16부 Architecture + 각 Core Lab | C~CL |
| S3 | 4부 / S3 Core | L |
| S3 Advanced | 4부 / S3 Advanced & Security | L |
| S3 Security | 4부 / S3 Advanced & Security | L |
| CloudFront & Global Accelerator | 4부 | L |
| Storage Extras | 5부 | C~L |
| Messaging / Integration | 6부 | SQS는 CL, 나머지는 C~L |
| Containers | 7부 | ECS는 CL, EKS/App Runner는 C |
| Serverless | 8부 | Lambda/API Gateway/DynamoDB는 L~CL |
| Databases in AWS | 9부 Database 선택 지도 | C |
| Data & Analytics | 9부 | C |
| Machine Learning | 10부 | C |
| Monitoring | 11부 / CloudWatch, CloudTrail, Config | CL |
| Advanced Identity | 11부 / Advanced Identity | C~L |
| Security & Encryption | 11부 / KMS, Secrets, WAF, Security Services | C~L |
| VPC | 12부 | CL |
| Disaster Recovery & Migrations | 13부 | L |
| More Solutions Architecture | 16부 | C~CL |
| Other Services | 해당 기능별 파트에 분산 | C |
| White Papers & Architectures | 16부 | C~L |

---

## 강의 순서 적용 원칙

강의를 듣는 동안 다음 원칙을 적용한다.

### 1. 연속되는 강의 내용은 학습 순서를 맞춘다

예를 들어 EC2 Basics에서 Security Group이 바로 등장하면 `cloud-lab`에서도 EC2 내부 Unit으로 먼저 학습한다.

```text
EC2 Launch
→ Instance Type
→ Security Group / SSH
→ Purchasing Options
→ IP / EIP
...
```

이후 Security Group은 별도 심화 Unit에서 다시 다룰 수 있다.

### 2. 디렉터리 구조와 학습 순서는 완전히 같을 필요가 없다

강의에서는 한 번 다루지만 실무적으로 여러 주제와 연결되는 내용은 다른 파트에서 재등장할 수 있다.

예:

```text
Security Group
1) EC2 Basics — 기본 inbound/outbound
2) Security Group 심화 — SG reference / 계층 접근
3) VPC — SG vs NACL
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

이런 서비스는 다음 질문에 답할 수 있으면 우선 충분하다.

```text
무슨 문제를 해결하는가?
문제에서 어떤 키워드가 나오면 선택하는가?
헷갈리는 서비스와 차이는 무엇인가?
```

### 4. Core Lab은 반복해서 깊어진다

다음 서비스는 강의 Hands-on보다 더 깊게 진행한다.

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
Terraform
GitHub Actions
```

---

## 강의와 별개로 추가되는 학습

### Foundation

- Linux process / service
- Linux permission / logs
- `ss`, `curl`, `ip` 기반 네트워크 관측
- HTTP / DNS / TLS 최소 기반

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
쇼핑몰 도메인의 하나의 시스템을 단계적으로 발전시킨다.

자세한 내용은 `portfolio/README.md`를 참고한다.

---

## 체크 방법

강의 섹션 하나를 끝낼 때마다 다음을 확인한다.

```text
[ ] 강의에서 다룬 서비스가 curriculum에 존재하는가?
[ ] 핵심 비교 포인트가 README에 정리되어 있는가?
[ ] 이 주제는 C / L / CL 중 어디까지 해야 하는가?
[ ] 지금 포트폴리오에 붙일 내용인가, 나중에 붙일 내용인가?
[ ] 시험 문제에서 헷갈릴 비교 대상은 무엇인가?
```

강의 전체 1회독 이후에는 이 문서를 기준으로 누락된 서비스와 선택 기준을 다시 점검한다.
