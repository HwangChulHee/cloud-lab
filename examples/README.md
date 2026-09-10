# AWS Guided Examples

`labs/`에 들어가기 전에, AWS 콘솔에서 직접 따라 만들면서 핵심 인프라를 반복 구축하고 장애까지 다뤄보는 누적형 학습 과정이다.

Lab이 **상황을 보고 스스로 설계하는 문제**라면, Example은 **정해진 구조를 따라 만들되, 같은 핵심 작업을 반복하면서 점점 가이드를 줄여 체화하는 과정**이다.

> 따라 만들기 → 기억만으로 다시 해보기 → 요청/지표 관찰 → 일부러 망가뜨리기 → 원인 추적 → 복구 → 설명하기

## 목적

- EC2, VPC, ALB, ASG, RDS, S3, IAM, Route 53, CloudWatch를 깊게 익힌다.
- 같은 핵심 작업을 여러 챕터에서 반복해 콘솔 조작과 트래픽 흐름을 체화한다.
- 서비스 이름이 아니라 **왜 이 구조인지, 어디서 장애가 났는지** 설명할 수 있게 한다.
- 뒤로 갈수록 클릭 가이드를 줄여 마지막에는 요구사항만 보고 직접 구축한다.
- `labs/`에서 정답 구조 없이 설계 문제를 풀기 위한 기반을 만든다.

## 학습 원칙

1. 초반에는 Console 중심으로 상세하게 따라 한다.
2. 새 개념보다 기존 핵심 구조를 반복하는 비중을 높인다.
3. 각 챕터 시작 전에 이전 개념을 기억만으로 회상한다.
4. 반복 작업은 뒤로 갈수록 가이드를 줄인다.
5. 구축만 하지 않고 반드시 실제 요청, Target 상태, Metric, Log를 관찰한다.
6. 가능한 모든 챕터에서 장애를 일부러 만든 뒤 원인을 추적하고 복구한다.
7. 실습이 끝나면 비용이 발생하는 리소스를 직접 정리한다.
8. Terraform은 SAA 이후 같은 구조를 재구축하는 단계에서 사용한다.

## 가이드 감소 방식

```text
초반: 클릭 위치와 값까지 제공
  ↓
중반: 조건만 제공하고 익숙한 작업은 스스로 수행
  ↓
후반: 증상/요구사항만 제공
  ↓
최종: 전체 아키텍처를 거의 무가이드로 재구축
  ↓
labs/: 정답 구조 없이 설계
```

## 커리큘럼

| # | Example | 새로 배우는 것 | 반복하는 것 | 깊이 포인트 |
| --- | --- | --- | --- | --- |
| 01 | [Single EC2 Web](./01-single-ec2-web/README.md) | EC2, User Data, Public/Private IP | - | SG 차단 vs 앱 중지 증상 비교 |
| 02 | [ALB + Two EC2](./02-alb-two-ec2/README.md) | ALB, Listener, Target Group | EC2, SG, User Data | 요청 분산과 단일 진입점 |
| 03 | [ALB Health Check](./03-alb-health-check/README.md) | Health Check, threshold | ALB, Target Group, EC2 | 정상 서버도 잘못된 HC로 격리될 수 있음 |
| 04 | [Security Group Layering](./04-security-group-layering/README.md) | SG Reference | ALB, EC2, Target Group | ALB만 EC2에 접근하도록 계층 분리 |
| 05 | [VPC Public/Private Subnets](./05-vpc-public-private-subnets/README.md) | CIDR, Subnet, Route Table, IGW | EC2, SG | Public Subnet의 실제 조건 이해 |
| 06 | [Private EC2 Access](./06-private-ec2-access/README.md) | Private EC2, NAT/SSM 개념 | VPC, ALB, SG, EC2 | 인터넷 노출 없이 서비스 운영 |
| 07 | [ALB + Auto Scaling](./07-alb-asg/README.md) | Launch Template, ASG | ALB, TG, EC2, SG | 수동 2대 → 자동 인스턴스 관리 |
| 08 | [Scaling & Recovery](./08-asg-scaling-and-recovery/README.md) | Scaling Policy, 자동 복구 | ASG, ALB, CloudWatch | 장애 교체와 scale-out 직접 관찰 |
| 09 | [Private RDS](./09-private-rds/README.md) | RDS, DB Subnet Group | VPC, EC2, SG | App 계층만 DB 접근 허용 |
| 10 | [RDS Failure & Recovery](./10-rds-failure-and-recovery/README.md) | Multi-AZ, Backup, PITR, Replica | RDS, SG, 앱 연결 | 확장과 HA의 차이 체감 |
| 11 | [S3 + IAM Role](./11-s3-iam-role/README.md) | IAM Role, S3 권한 | EC2, IAM | Access Key 없이 S3 접근 |
| 12 | [S3 Security & Recovery](./12-s3-security-and-recovery/README.md) | Bucket Policy, Versioning, Lifecycle | S3, IAM | AccessDenied와 삭제 복구 |
| 13 | [Route 53 + ACM + HTTPS](./13-route53-acm-https/README.md) | DNS, Alias, ACM, HTTPS | ALB, SG | 실제 도메인을 서비스 진입점으로 |
| 14 | [CloudWatch Observability](./14-cloudwatch-observability/README.md) | Metrics, Logs, Alarms | ALB, EC2, RDS, ASG | 증상에서 어떤 지표를 볼지 판단 |
| 15 | [Troubleshooting Web Stack](./15-troubleshooting-web-stack/README.md) | 종합 장애 진단 | 전체 핵심 서비스 | 증상 → 가설 → 관찰 → 복구 |
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
9. 기억만으로 설명하기
10. 완료 체크
11. 비용 정리
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

## 핵심 과정에서 제외하는 것

1차 취업 준비용 Guided Examples는 핵심 웹 인프라에 집중한다.

- CloudFront
- SQS / SNS
- ECS / Fargate
- Lambda
- DynamoDB
- EKS

이들은 핵심 과정을 완주한 뒤 `advanced` 예제 또는 별도 프로젝트에서 확장한다.

## Examples와 Labs의 차이

| 구분 | Examples | Labs |
| --- | --- | --- |
| 목적 | 반복 구축 + 원리 + 장애대응 체화 | 설계 판단 연습 |
| 구조 | 정답 구조가 존재 | 정답을 먼저 보지 않음 |
| 진행 | 초반 상세 → 후반 최소 가이드 | 요구사항 중심 |
| 실패 실험 | 지정 장애를 재현하고 추적 | 장애 시나리오도 스스로 판단 |
| 난이도 | 낮음 → 높음 | 중간 → 높음 |

권장 흐름:

```text
SAA 개념 학습
   ↓
Guided Example
   ↓
Recall + 반복 구축
   ↓
장애 재현/복구
   ↓
Scenario Lab
   ↓
SAA 이후 Terraform으로 재구축
```
