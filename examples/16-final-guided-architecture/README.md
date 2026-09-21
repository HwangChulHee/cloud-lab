# Example 16 — 전체 아키텍처 거의 무가이드로 다시 만들기

마지막 Guided Example이다. 이번에는 클릭 위치를 거의 알려주지 않는다. 지금까지 반복한 핵심 AWS 웹 인프라를 요구사항만 보고 처음부터 다시 만든다.

이 실습에서는 실제 보유 도메인의 별도 서브도메인을 사용한다.

```text
app.chulheehwang.com
```

`chulheehwang.com` 루트 도메인 자체는 장애 실험 대상으로 사용하지 않는다.

## 시작 전 Recall

빈 종이에 다음을 먼저 그린다.

```text
Internet
  ↓
app.chulheehwang.com
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
11. Route 53 + ACM으로 `app.chulheehwang.com` HTTPS 접속을 제공한다.
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
             app.chulheehwang.com
                       ↓
                   Route 53
                       ↓
                 A Alias → ALB
                       ↓
                    HTTPS
                 ACM certificate
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

## Domain / HTTPS 조건

Example 13에서 확인한 `chulheehwang.com` Hosted Zone을 재사용한다.

```text
Hosted Zone: chulheehwang.com
Record     : app.chulheehwang.com
Type       : A Alias
Target     : example-16 ALB
```

ALB가 위치한 Region에서 `app.chulheehwang.com`용 ACM public certificate를 발급하고 DNS Validation을 완료한다.

최종적으로 다음 두 요청을 실제로 확인한다.

```bash
curl -I http://app.chulheehwang.com
curl -I https://app.chulheehwang.com
```

HTTP는 HTTPS로 redirect되고 HTTPS는 정상 응답해야 한다.

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
[ ] app.chulheehwang.com DNS resolution 성공
[ ] https://app.chulheehwang.com 접속 성공
[ ] HTTP → HTTPS redirect
[ ] ACM certificate hostname 일치
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

최종 Example에서는 CLI 출력만 보고 아키텍처를 머릿속에 다시 그리는 것이 목표다.

### 1. VPC와 Subnet

\`\`\`bash
aws ec2 describe-vpcs --region $AWS_REGION \
  --filters 'Name=tag:Example,Values=16' \
  --query 'Vpcs[].{Name:Tags[?Key==\`Name\`]|[0].Value,Id:VpcId,CIDR:CidrBlock}' \
  --output table

aws ec2 describe-subnets --region $AWS_REGION \
  --filters 'Name=tag:Example,Values=16' \
  --query 'Subnets[].{Name:Tags[?Key==\`Name\`]|[0].Value,Id:SubnetId,CIDR:CidrBlock,AZ:AvailabilityZone,PublicIP:MapPublicIpOnLaunch}' \
  --output table
\`\`\`

2AZ와 public/private subnet 구성을 읽는다.

### 2. EC2 / ALB / ASG

\`\`\`bash
aws ec2 describe-instances --region $AWS_REGION \
  --filters 'Name=tag:Example,Values=16' 'Name=instance-state-name,Values=running' \
  --query 'Reservations[].Instances[].{Name:Tags[?Key==\`Name\`]|[0].Value,Id:InstanceId,PublicIP:PublicIpAddress,PrivateIP:PrivateIpAddress,AZ:Placement.AvailabilityZone,SG:SecurityGroups[].GroupId}' \
  --output table

aws elbv2 describe-load-balancers --region $AWS_REGION \
  --query "LoadBalancers[?contains(LoadBalancerName, 'example-16')].{Name:LoadBalancerName,Scheme:Scheme,State:State.Code,DNS:DNSName,AZ:AvailabilityZones[].ZoneName}"

aws autoscaling describe-auto-scaling-groups --region $AWS_REGION \
  --auto-scaling-group-names example-16-asg \
  --query 'AutoScalingGroups[].{Min:MinSize,Desired:DesiredCapacity,Max:MaxSize,Subnets:VPCZoneIdentifier,Instances:Instances[].{Id:InstanceId,Health:HealthStatus,Lifecycle:LifecycleState},Metrics:EnabledMetrics}'
\`\`\`

여기서 **public ALB + private EC2 + ASG 2AZ**를 증명한다.

### 3. RDS / S3

\`\`\`bash
aws rds describe-db-instances --region $AWS_REGION \
  --query "DBInstances[?contains(DBInstanceIdentifier, 'example-16')].{Id:DBInstanceIdentifier,Status:DBInstanceStatus,Public:PubliclyAccessible,MultiAZ:MultiAZ,Endpoint:Endpoint.Address,Subnets:DBSubnetGroup.Subnets[].SubnetIdentifier}"

aws s3api get-public-access-block --bucket <bucket-name>
aws s3api get-bucket-versioning --bucket <bucket-name>
aws s3api get-bucket-encryption --bucket <bucket-name>
\`\`\`

RDS가 private인지, S3가 public 차단/versioned/encrypted인지 각각 확인한다.

### 4. 실제 도메인

\`\`\`bash
dig app.chulheehwang.com
curl -I http://app.chulheehwang.com
curl -I https://app.chulheehwang.com
\`\`\`

\`dig\`는 DNS, 첫 \`curl\`은 HTTP→HTTPS redirect, 두 번째는 실제 HTTPS 서비스 응답을 확인한다.

### 5. CloudWatch Alarm

\`\`\`bash
aws cloudwatch describe-alarms --region $AWS_REGION \
  --alarm-name-prefix example-16 \
  --query 'MetricAlarms[].{Name:AlarmName,State:StateValue,Metric:MetricName}' \
  --output table
\`\`\`

최종적으로 CLI 출력만 보고 다음 연결을 설명한다.

\`\`\`text
Route 53 → ALB Listener → Target Group → ASG/EC2
                                   ↓
                                  RDS

EC2 → IAM Role → S3
CloudWatch → 전체 상태 관측
\`\`\`

## 최종 장애 시험

아래에서 최소 5개를 무작위로 선택한다. 가능하면 장애를 만든 뒤 잠깐 쉬었다가 원인을 모르는 상태처럼 다시 진단한다.

1. EC2 한 대 terminate
2. nginx/app 중지
3. Health Check path 오류
4. EC2-SG의 ALB rule 제거
5. RDS-SG의 EC2 rule 제거
6. S3 IAM permission 제거
7. ASG scaling policy 오류
8. `app.chulheehwang.com` Route 53 Alias 오류
9. HTTPS Listener 또는 443 SG 오류
10. Target Group의 등록 Target 제거 → 503 관찰
11. 모든 Target unhealthy → fail-open 동작 관찰
12. Private EC2의 NAT route 제거 → outbound/bootstrap 관련 증상 분석

DNS 장애 실험은 `app.chulheehwang.com`에서만 하고 `chulheehwang.com` 루트 record는 건드리지 않는다.

각 장애마다 기록한다.

```text
사용자에게 보인 증상:
DNS resolution 성공 여부:
TLS/HTTPS 상태:
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

- 사용자가 `https://app.chulheehwang.com`을 입력한 순간부터 RDS까지 요청 흐름을 설명하라.
- Registrar, Route 53 Hosted Zone, Alias Record의 관계는?
- DNS 정상과 HTTPS 정상은 왜 별개인가?
- Public/Private Subnet을 왜 나눴는가?
- ALB와 ASG는 각각 어떤 장애/확장 문제를 해결하는가?
- EC2가 죽으면 어떤 AWS 구성 요소들이 어떤 순서로 반응하는가?
- Private EC2 bootstrap에서 NAT가 필요한 경우와 필요 없는 경우는?
- Target이 0개인 경우와 모든 Target이 unhealthy인 경우 ALB 동작은 어떻게 다른가?
- RDS Multi-AZ와 Read Replica의 목적 차이는?
- EC2가 S3에 접근할 때 왜 Access Key가 필요 없는가?
- `ListBucket`과 `ListAllMyBuckets` 차이는?
- ALB 503, DB timeout, S3 AccessDenied, DNS failure를 각각 어디부터 볼 것인가?

## 완료 기준

다음이 가능하면 Guided Examples 1차 과정 완료로 본다.

```text
구축할 수 있다
+ 실제 도메인으로 HTTPS 서비스를 제공할 수 있다
+ 왜 그렇게 설계했는지 설명할 수 있다
+ CLI 출력으로 실제 연결 관계를 검증할 수 있다
+ 일부러 망가뜨릴 수 있다
+ 증상을 보고 원인을 좁힐 수 있다
+ 복구하고 재발 방지를 설명할 수 있다
+ 삭제 후 과금 리소스가 남지 않았는지 확인할 수 있다
```

이후에는 `portfolio/`로 바로 넘어간다. 실제 애플리케이션 요구사항에 지금까지 배운 구조를 적용하고, 같은 인프라를 Terraform과 CI/CD로 재구축한다.

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
Route 53 실습 record
ACM certificate 유지 여부
```

`chulheehwang.com` Hosted Zone은 실제 도메인에 사용할 수 있으므로 자동 삭제 대상으로 보지 않는다. 실습용 `app.chulheehwang.com` record는 이후 사용 계획에 따라 유지/삭제를 판단한다.

특히 Versioning이 켜진 S3는 object 목록이 비어 보여도 old version/delete marker가 남을 수 있다.

```bash
aws s3api list-object-versions --bucket <bucket-name>
```

모든 정리 후 [CLI Verification Guide](../CLI_VERIFICATION.md)의 **전체 잔존 리소스 검사**를 실행한다. 그 출력이 최종 종료 증거다.

---
