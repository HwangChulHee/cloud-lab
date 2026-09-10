# AWS Guided Examples

AWS 콘솔에서 직접 따라 만들면서 핵심 인프라를 반복 구축하고 장애까지 다뤄보는 누적형 학습 과정이다.

초반에는 정해진 구조를 상세 가이드로 따라가고, 뒤로 갈수록 같은 핵심 작업을 반복하면서 가이드를 줄인다. 후반부에는 증상과 요구사항만 보고 스스로 진단하고 구축하는 수준까지 올라간다.

> 따라 만들기 → 기억만으로 다시 해보기 → 요청/지표 관찰 → 일부러 망가뜨리기 → 원인 추적 → 복구 → 설명하기

## 목적

- EC2, VPC, ALB, ASG, RDS, S3, IAM, Route 53, CloudWatch를 깊게 익힌다.
- 같은 핵심 작업을 여러 챕터에서 반복해 콘솔 조작과 트래픽 흐름을 체화한다.
- 서비스 이름이 아니라 **왜 이 구조인지, 어디서 장애가 났는지** 설명할 수 있게 한다.
- 뒤로 갈수록 클릭 가이드를 줄여 마지막에는 요구사항만 보고 직접 구축한다.
- 15~16에서 장애 진단과 무가이드 구축까지 수행한 뒤 `portfolio/`에서 실제 시스템에 적용할 기반을 만든다.

## 공통 리소스 태그 규칙

CLI 검증과 비용 정리를 정확하게 하기 위해, 태그를 지원하는 모든 실습 리소스에는 가능한 한 아래 태그를 붙인다.

```text
Project = cloud-lab
Stage   = examples
Example = 01   # 챕터 번호에 맞게 변경
```

Name은 `example-NN-*` 형식을 사용한다.

```text
example-06-vpc
example-06-alb
example-06-web-sg
example-09-db
```

태그를 지원하지 않거나 API에서 Name 필터가 더 안정적인 리소스는 `example-NN-*` 이름 규칙을 사용한다.

## 학습 원칙

1. 초반에는 Console 중심으로 상세하게 따라 한다.
2. 새 개념보다 기존 핵심 구조를 반복하는 비중을 높인다.
3. 각 챕터 시작 전에 이전 개념을 기억만으로 회상한다.
4. 반복 작업은 뒤로 갈수록 가이드를 줄인다.
5. 구축만 하지 않고 반드시 실제 요청, Target 상태, Metric, Log를 관찰한다.
6. 가능한 모든 챕터에서 장애를 일부러 만든 뒤 원인을 추적하고 복구한다.
7. 실습이 끝나면 비용이 발생하는 리소스를 직접 정리한다.
8. 구축 후와 삭제 후에는 [CLI Verification Guide](./CLI_VERIFICATION.md)의 명령으로 실제 상태를 검증한다.
9. Terraform은 SAA 이후 같은 구조를 재구축하는 단계에서 사용한다.

## Private Subnet Bootstrap 규칙

Private EC2가 인터넷에서 패키지를 내려받아야 하는 경우, 단순히 Private Subnet에 넣는 것만으로는 `dnf install`, 외부 저장소 접근 등이 되지 않는다.

따라서 06 이후에는 다음 중 하나를 명시적으로 선택한다.

```text
A. NAT Gateway를 통해 outbound 인터넷 경로 제공
B. 필요한 패키지를 미리 설치한 AMI 사용
C. 인터넷 다운로드가 필요 없는 User Data 사용
```

이 차이를 숨기지 않고 실습에서 직접 관찰한다.

## 가이드 감소 방식

```text
초반: 클릭 위치와 값까지 제공
  ↓
중반: 조건만 제공하고 익숙한 작업은 스스로 수행
  ↓
후반: 증상/요구사항만 제공
  ↓
15: 전체 Web Stack 장애 진단
  ↓
16: 전체 아키텍처를 거의 무가이드로 재구축
  ↓
portfolio/: 실제 시스템에 적용
```

## 커리큘럼

| # | Example | 새로 배우는 것 | 반복하는 것 | 깊이 포인트 |
| --- | --- | --- | --- | --- |
| 01 | [Single EC2 Web](./01-single-ec2-web/README.md) | EC2, User Data, Public/Private IP | - | SG 차단 vs 앱 중지 증상 비교 |
| 02 | [ALB + Two EC2](./02-alb-two-ec2/README.md) | ALB, Listener, Target Group | EC2, SG, User Data | 요청 분산과 단일 진입점 |
| 03 | [ALB Health Check](./03-alb-health-check/README.md) | Health Check, threshold | ALB, Target Group, EC2 | 정상 서버도 잘못된 HC로 격리될 수 있음 |
| 04 | [Security Group Layering](./04-security-group-layering/README.md) | SG Reference | ALB, EC2, Target Group | ALB만 EC2에 접근하도록 계층 분리 |
| 05 | [VPC Public/Private Subnets](./05-vpc-public-private-subnets/README.md) | CIDR, Subnet, Route Table, IGW | EC2, SG | Public Subnet의 실제 조건 이해 |
| 06 | [Private EC2 Access](./06-private-ec2-access/README.md) | Private EC2, NAT/SSM, bootstrap | VPC, ALB, SG, EC2 | 인터넷 노출 없이 서비스 운영 |
| 07 | [ALB + Auto Scaling](./07-alb-asg/README.md) | Launch Template, ASG | ALB, TG, EC2, SG | bootstrap 가능한 ASG 구성 |
| 08 | [Scaling & Recovery](./08-asg-scaling-and-recovery/README.md) | Scaling Policy, 자동 복구 | ASG, ALB, CloudWatch | 평균 CPU와 scale-out 직접 관찰 |
| 09 | [Private RDS](./09-private-rds/README.md) | RDS, DB Subnet Group | VPC, EC2, SG | App 계층만 DB 접근 허용 |
| 10 | [RDS Failure & Recovery](./10-rds-failure-and-recovery/README.md) | Multi-AZ, Backup, PITR, Replica | RDS, SG, 앱 연결 | 확장과 HA의 차이 체감 |
| 11 | [S3 + IAM Role](./11-s3-iam-role/README.md) | IAM Role, S3 권한 | EC2, IAM | 특정 Bucket 최소 권한 |
| 12 | [S3 Security & Recovery](./12-s3-security-and-recovery/README.md) | Bucket Policy, Versioning, Lifecycle, Encryption | S3, IAM | AccessDenied와 삭제 복구 |
| 13 | [Route 53 + ACM + HTTPS](./13-route53-acm-https/README.md) | DNS, Alias, ACM, HTTPS | ALB, SG | 실제 도메인을 서비스 진입점으로 |
| 14 | [CloudWatch Observability](./14-cloudwatch-observability/README.md) | Metrics, Logs, Alarms | ALB, EC2, RDS, ASG | ASG group metric까지 관측 |
| 15 | [Troubleshooting Web Stack](./15-troubleshooting-web-stack/README.md) | 종합 장애 진단 | 전체 핵심 서비스 | ALB fail-open 포함 실제 동작 구분 |
| 16 | [Final Guided Architecture](./16-final-guided-architecture/README.md) | 거의 무가이드 재구축 | 전체 | 요구사항만 보고 아키텍처 완성 |

## 각 챕터의 공통 구조

각 README는 가능하면 다음 순서를 따른다.

```text
1. 시작 전 Recall Check
2. 이번 챕터의 새 개념
3. 이번 챕터에서 반복할 개념
4. 이번에는 도움 없이 해볼 것
5. 단계별 구축
6. 요청/상태/Metric 관찰
7. 장애 실험
8. 원인 추적 및 복구
9. CLI 구축 검증
10. 기억만으로 설명하기
11. 완료 체크
12. 비용 정리
13. CLI 삭제 검증
```

## 반복 학습 규칙

같은 작업을 의도적으로 반복한다.

```text
매우 자주 반복
- EC2 생성/상태 확인
- Security Group
- Subnet 선택
- Target Group
- ALB Listener
- IAM Role 연결
- CloudWatch에서 상태 확인

중간중간 반복
- VPC / Route Table / IGW
- Launch Template / ASG
- RDS Security Group
- Route 53 Alias

몇 번만 반복
- NAT Gateway
- ACM
- Multi-AZ / PITR
```

반복할 때마다 설명은 줄인다. 이전 챕터에서 충분히 다룬 작업은 상세한 클릭 순서를 생략하고 조건만 제시한다.

## 비용/삭제 원칙

실습 종료는 브라우저에서 페이지가 닫히는 시점이 아니라 **과금 리소스가 정리된 것을 CLI로 확인한 시점**이다.

특히 다음은 반드시 확인한다.

```text
EC2 / EBS
ALB / Target Group
ASG / Launch Template
NAT Gateway / Elastic IP
RDS / Read Replica / Manual Snapshot
S3 Object Versions / Delete Markers
CloudWatch Alarm / Log Group
Route 53 Hosted Zone 유지 여부
```

## 핵심 과정에서 제외하는 것

1차 취업 준비용 Guided Examples는 핵심 웹 인프라에 집중한다.

- CloudFront
- SQS / SNS
- ECS / Fargate
- Lambda
- DynamoDB
- EKS

이들은 핵심 과정을 완주한 뒤 `advanced` 예제 또는 `portfolio/`에서 필요에 따라 확장한다.

## Examples 이후

별도의 Scenario Lab 디렉터리는 두지 않는다. Example 15가 종합 장애 진단, Example 16이 요구사항 기반 무가이드 구축 역할을 담당한다.

Examples를 완료하면 같은 장난감 아키텍처를 한 번 더 푸는 대신 실제 포트폴리오 시스템에 적용한다.

```text
SAA 개념 학습
   ↓
Guided Examples 01~14
   ↓
15: 종합 장애 진단
   ↓
16: 거의 무가이드 재구축
   ↓
portfolio/
   ↓
Terraform / CI/CD / Containers / 운영 심화
```
