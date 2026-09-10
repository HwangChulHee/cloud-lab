# Example 16 — 전체 아키텍처 거의 무가이드로 다시 만들기

마지막 Guided Example이다. 이번에는 클릭 위치를 거의 알려주지 않는다. 지금까지 반복한 핵심 AWS 웹 인프라를 요구사항만 보고 처음부터 다시 만든다.

## 시작 전 Recall
빈 종이에 다음을 먼저 그린다.

```text
Internet
  ↓
DNS / HTTPS
  ↓
Load Balancer
  ↓
Auto Scaling Web/App
  ↓
Database

App → Object Storage
Monitoring / IAM / VPC가 전체를 감싼다.
```

각 화살표에 어떤 AWS 서비스와 어떤 Security Group 관계가 필요한지 기억만으로 적는다.

모든 태그 가능 리소스에는 아래 태그를 붙인다.

```text
Project=cloud-lab
Stage=examples
Example=16
```

Name은 `example-16-*` 형식을 사용한다.

## 요구사항

다음 조건을 만족하는 웹 서비스를 구축한다.

1. 하나의 VPC를 직접 만든다.
2. 2개 AZ를 사용한다.
3. 각 AZ에 Public/Private Subnet을 둔다.
4. Internet-facing ALB는 Public Subnet에 둔다.
5. 애플리케이션 EC2는 Private Subnet에 둔다.
6. EC2는 ASG가 최소 2대를 유지한다.
7. ALB만 EC2의 HTTP/app port에 접근할 수 있다.
8. RDS는 Private하게 배치하고 EC2 계층만 DB port 접근을 허용한다.
9. EC2는 Access Key 없이 IAM Role로 S3에 접근한다.
10. S3는 Public Access를 차단하고 Versioning을 활성화한다.
11. Route 53 + ACM으로 도메인 HTTPS 접속을 제공한다.
12. HTTP 요청은 HTTPS로 redirect한다.
13. CloudWatch에서 ALB/EC2/ASG/RDS 핵심 지표를 확인한다.
14. ASG group metric collection을 활성화한다.
15. 최소 하나의 Alarm을 만든다.
16. Private EC2 bootstrap이 외부 다운로드에 의존한다면 NAT Gateway 또는 사전 준비 AMI를 사용한다.
17. 가능하면 App → RDS 연결을 확인하는 `/db-health` 같은 endpoint를 둔다.

## 목표 구조

```text
                    Internet
                       ↓
                   Route 53
                       ↓
                    HTTPS
                       ↓
                 ALB (public)
                   /       \
                AZ-A       AZ-B
                  ↓          ↓
              EC2/ASG    EC2/ASG
                 \          /
                     ↓
                 RDS Multi-AZ

EC2 ──IAM Role──→ S3(private, versioned)

CloudWatch: ALB / ASG / EC2 / RDS
```

## Bootstrap 조건

Private EC2의 User Data가 `dnf install`, 외부 repository, package download에 의존한다면 다음 중 하나를 선택한다.

```text
A. Private RT → NAT Gateway → IGW
B. 필요한 패키지가 포함된 AMI
C. 외부 다운로드가 필요 없는 bootstrap
```

ASG가 replacement를 만들 때도 같은 방식으로 정상 기동되어야 한다.

## 가이드 없이 구축

다음 체크포인트만 사용한다.

### Network
- VPC CIDR과 subnet CIDR이 겹치지 않는다.
- Public RT는 IGW route를 가진다.
- Private EC2에는 Public IP를 주지 않는다.
- NAT를 쓴다면 NAT Gateway는 Public Subnet에 있고 Private RT가 NAT를 가리킨다.

### Security
```text
Internet → ALB-SG :443
ALB-SG → EC2-SG :app port
EC2-SG → RDS-SG :DB port
EC2 → IAM Role → S3
```

### Availability
- ALB가 2AZ를 사용한다.
- ASG가 2개 Private Subnet을 사용한다.
- RDS Multi-AZ를 사용할 경우 목적을 설명할 수 있다.
- replacement 인스턴스가 bootstrap 후 healthy가 된다.

### Observability
- Target health
- ALB response/5xx
- EC2 CPU
- ASG Desired/InService/Total
- RDS connections/storage
- Application/CloudWatch Logs

ASG group metric은 필요하면 다음으로 활성화한다.

```bash
aws autoscaling enable-metrics-collection \
  --region $AWS_REGION \
  --auto-scaling-group-name <asg-name> \
  --granularity 1Minute
```

## 검증

구축 후 다음을 실제로 확인한다.

```text
[ ] 도메인 HTTPS 접속 성공
[ ] HTTP → HTTPS redirect
[ ] EC2 Public IP 없음
[ ] EC2 직접 접근 불가
[ ] ASG 최소 2대 healthy
[ ] replacement EC2도 정상 bootstrap
[ ] DB INSERT/SELECT 성공
[ ] 가능하면 /db-health 성공
[ ] EC2 → S3 upload/download 성공
[ ] S3 public URL 접근 차단
[ ] S3 Versioning 동작 확인
[ ] CloudWatch metric 변화 확인
[ ] ASG group metric 확인
[ ] Alarm 상태 변화 확인
```

## CLI 구축 검증

[CLI Verification Guide](../CLI_VERIFICATION.md)의 Example 16 검증 명령을 실행하고 출력을 저장한다.

출력만 보고 다음을 설명할 수 있어야 한다.

```text
VPC/Subnet/Route 관계
ALB/Listener/Target 관계
ASG/Launch Template/EC2 관계
RDS private 배치
IAM Role/S3 접근
CloudWatch Alarm
```

## 최종 장애 시험

아래에서 최소 5개를 무작위로 선택한다. 가능하면 장애를 만든 뒤 잠깐 쉬었다가 원인을 모르는 상태처럼 다시 진단한다.

1. EC2 한 대 terminate
2. nginx/app 중지
3. Health Check path 오류
4. EC2-SG의 ALB rule 제거
5. RDS-SG의 EC2 rule 제거
6. S3 IAM permission 제거
7. ASG scaling policy 오류
8. Route 53 record 오류
9. Target Group의 등록 Target 제거 → 503 관찰
10. 모든 Target unhealthy → fail-open 동작 관찰
11. Private EC2의 NAT route 제거 → outbound/bootstrap 관련 증상 분석

각 장애마다 기록한다.

```text
사용자에게 보인 증상:
HTTP 상태/timeout 여부:
CloudWatch/Console에서 보인 신호:
첫 가설:
확인 순서:
실제 원인:
복구 방법:
재발 방지:
```

## 최종 구술 테스트

README를 보지 않고 답한다.

- 사용자가 도메인을 입력한 순간부터 RDS까지 요청 흐름을 설명하라.
- Public/Private Subnet을 왜 나눴는가?
- ALB와 ASG는 각각 어떤 장애/확장 문제를 해결하는가?
- EC2가 죽으면 어떤 AWS 구성 요소들이 어떤 순서로 반응하는가?
- Private EC2 bootstrap에서 NAT가 필요한 경우와 필요 없는 경우는?
- Target이 0개인 경우와 모든 Target이 unhealthy인 경우 ALB 동작은 어떻게 다른가?
- RDS Multi-AZ와 Read Replica의 목적 차이는?
- EC2가 S3에 접근할 때 왜 Access Key가 필요 없는가?
- `ListBucket`과 `ListAllMyBuckets` 차이는?
- ALB 503, DB timeout, S3 AccessDenied를 각각 어디부터 볼 것인가?

## 완료 기준

다음이 가능하면 Guided Examples 1차 과정 완료로 본다.

```text
구축할 수 있다
+ 왜 그렇게 설계했는지 설명할 수 있다
+ CLI 출력으로 실제 연결 관계를 검증할 수 있다
+ 일부러 망가뜨릴 수 있다
+ 증상을 보고 원인을 좁힐 수 있다
+ 복구하고 재발 방지를 설명할 수 있다
+ 삭제 후 과금 리소스가 남지 않았는지 확인할 수 있다
```

이후에는 `labs/`에서 정답 아키텍처를 먼저 보지 않고 요구사항만 보고 설계한다. SAA 이후에는 같은 구조를 Terraform과 CI/CD로 다시 구현한다.

## 비용 정리

최종 실습은 리소스가 많다. 다음 순서로 비용 리소스를 확인한다.

```text
RDS / Read Replica / Manual Snapshot
ALB / Target Group
ASG / EC2 / Launch Template
NAT Gateway / Elastic IP
EBS volume
S3 object / old version / delete marker
CloudWatch Alarm / Log Group
Route 53 Hosted Zone 유지 여부
```

특히 Versioning이 켜진 S3는 object 목록이 비어 보여도 old version/delete marker가 남을 수 있다.

```bash
aws s3api list-object-versions --bucket <bucket-name>
```

모든 정리 후 [CLI Verification Guide](../CLI_VERIFICATION.md)의 **전체 잔존 리소스 검사**를 실행한다. 그 출력이 최종 종료 증거다.
