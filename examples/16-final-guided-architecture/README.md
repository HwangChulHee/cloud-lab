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

## 요구사항

다음 조건을 만족하는 웹 서비스를 구축한다.

1. 하나의 VPC를 직접 만든다.
2. 2개 AZ를 사용한다.
3. 각 AZ에 Public/Private Subnet을 둔다.
4. Internet-facing ALB는 Public Subnet에 둔다.
5. 애플리케이션 EC2는 Private Subnet에 둔다.
6. EC2는 ASG가 최소 2대를 유지한다.
7. ALB만 EC2의 HTTP port에 접근할 수 있다.
8. RDS는 Private하게 배치하고 EC2 계층만 DB port 접근을 허용한다.
9. EC2는 Access Key 없이 IAM Role로 S3에 접근한다.
10. S3는 Public Access를 차단하고 Versioning을 활성화한다.
11. Route 53 + ACM으로 도메인 HTTPS 접속을 제공한다.
12. HTTP 요청은 HTTPS로 redirect한다.
13. CloudWatch에서 ALB/EC2/ASG/RDS 핵심 지표를 확인한다.
14. 최소 하나의 Alarm을 만든다.

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

## 가이드 없이 구축

다음 체크포인트만 사용한다.

### Network
- VPC CIDR과 subnet CIDR이 겹치지 않는다.
- Public RT는 IGW route를 가진다.
- Private EC2에는 Public IP를 주지 않는다.

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
- RDS 가용성 설정의 목적을 설명할 수 있다.

### Observability
- Target health
- ALB response/5xx
- EC2 CPU
- ASG desired/in-service
- RDS connections/storage

## 검증

구축 후 다음을 실제로 확인한다.

```text
[ ] 도메인 HTTPS 접속 성공
[ ] HTTP → HTTPS redirect
[ ] EC2 Public IP 없음
[ ] EC2 직접 접근 불가
[ ] ASG 최소 2대 healthy
[ ] DB INSERT/SELECT 성공
[ ] EC2 → S3 upload/download 성공
[ ] S3 public URL 접근 차단
[ ] CloudWatch metric 변화 확인
```

## 최종 장애 시험

아래에서 최소 4개를 무작위로 선택한다. 가능하면 장애를 만든 뒤 잠깐 쉬었다가 원인을 모르는 상태처럼 다시 진단한다.

1. EC2 한 대 terminate
2. nginx/app 중지
3. Health Check path 오류
4. EC2-SG의 ALB rule 제거
5. RDS-SG의 EC2 rule 제거
6. S3 IAM permission 제거
7. ASG scaling policy 오류
8. Route 53 record 오류

각 장애마다 기록한다.

```text
사용자에게 보인 증상:
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
- RDS Multi-AZ와 Read Replica의 목적 차이는?
- EC2가 S3에 접근할 때 왜 Access Key가 필요 없는가?
- ALB 503, DB timeout, S3 AccessDenied를 각각 어디부터 볼 것인가?

## 완료 기준

다음이 가능하면 Guided Examples 1차 과정 완료로 본다.

```text
구축할 수 있다
+ 왜 그렇게 설계했는지 설명할 수 있다
+ 일부러 망가뜨릴 수 있다
+ 증상을 보고 원인을 좁힐 수 있다
+ 복구하고 재발 방지를 설명할 수 있다
```

이후에는 `labs/`에서 정답 아키텍처를 먼저 보지 않고 요구사항만 보고 설계한다. SAA 이후에는 같은 구조를 Terraform과 CI/CD로 다시 구현한다.

## 비용 정리

최종 실습은 리소스가 많다. 다음 순서로 비용 리소스를 확인한다.

- RDS / Read Replica
- ALB
- ASG / EC2
- NAT Gateway가 있다면 NAT Gateway
- EBS
- S3 object/version
- CloudWatch Log 저장량
- Route 53 Hosted Zone 유지 여부
