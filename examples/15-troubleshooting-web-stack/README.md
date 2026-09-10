# Example 15 — 전체 Web Stack 장애 진단하기

이번 챕터에서는 새로운 서비스를 배우지 않는다. 지금까지 만든 구조를 일부러 망가뜨리고 **증상만 보고 원인을 좁혀가는 연습**을 한다.

## Recall Check
그림을 보지 않고 다음 요청 흐름을 적는다.

```text
User → ? → ? → ? → RDS
EC2 → ? → S3
```

그리고 각 구간에서 어떤 설정이 트래픽을 허용/차단하는지 적는다.

## 반복하는 것
- Route 53
- ALB / Listener / Target Group / Health Check
- ASG / EC2
- VPC / Route Table / SG
- RDS
- IAM / S3
- CloudWatch

모든 태그 가능 리소스에는 `Project=cloud-lab`, `Stage=examples`, `Example=15`를 붙인다.

## 이번에는 도움 없이
각 장애 Case는 먼저 README의 설명을 다시 읽지 않고 다음 양식으로 기록한다.

```text
증상:
HTTP 상태/timeout 여부:
첫 확인 지점:
가설 1:
가설 2:
관찰한 증거:
원인:
복구:
재발 방지:
```

## Case 1 — 브라우저가 Timeout
가능한 원인 중 하나를 실제로 만든다.

- ALB-SG inbound 제거
- DNS가 올바른 ALB를 가리키지 않음
- 잘못된 endpoint 사용

핵심은 `timeout`이라는 증상만 보고 바로 정답을 찍지 않는 것이다.

## Case 2 — ALB 503: Target이 없는 상태

503을 확실히 관찰하려면 Listener가 forward하는 Target Group에서 등록 Target을 모두 제거하거나, ASG/Target Group 연결을 끊어 **사용 가능한 등록 Target 자체가 없는 상태**를 만든다.

```text
Listener
  ↓
Target Group
  ↓
등록 Target 없음
```

확인:

```text
HTTP status
Listener action
Target Group 등록 대상 수
ASG와 Target Group 연결 여부
```

복구 후 Target이 다시 등록되고 healthy가 된 뒤 정상 응답이 돌아오는지 확인한다.

## Case 3 — 일부 Target Unhealthy

Target 두 개 이상 중 하나만 unhealthy로 만든다.

- nginx/app 중지
- Health Check path 오류
- EC2-SG에서 ALB-SG 차단
- 앱이 health endpoint에서 500 반환

healthy Target으로 요청이 계속 전달되는지 확인한다.

## Case 4 — 모든 Target Unhealthy와 ALB fail-open

모든 등록 Target을 unhealthy 상태로 만든다.

중요: ALB는 **모든 Target이 unhealthy일 때 단순히 항상 503을 반환한다고 가정하면 안 된다.** Target Group에 등록된 Target이 모두 unhealthy인 상황에서는 fail-open 동작으로 unhealthy Target에 요청을 전달할 수 있다.

따라서 아래를 직접 비교한다.

```text
A. 등록 Target 없음
B. 일부 Target unhealthy
C. 모든 등록 Target unhealthy
```

각 상태에서 HTTP 결과와 `describe-target-health` 출력을 기록한다.

## Case 5 — App은 뜨지만 DB 연결 실패
다음 후보를 하나씩 실험한다.

- RDS-SG 차단
- 잘못된 endpoint
- 잘못된 port
- credential 오류

Example 09의 `/db-health`가 있다면 같이 사용한다. 네트워크 timeout과 인증 오류의 차이를 로그에서 구분한다.

## Case 6 — S3 Upload AccessDenied
EC2와 네트워크는 정상인데 S3 작업만 실패하도록 IAM Action/Resource 또는 Bucket Policy를 잘못 설정한다.

확인 순서:

```text
사용 중인 Role
→ IAM Policy Action
→ Resource ARN
→ Bucket Policy
→ Explicit Deny 여부
```

## Case 7 — 새 EC2가 계속 Unhealthy
ASG가 replacement를 생성했지만 Target Group에 정상 편입되지 않는 상황을 만든다.

확인 후보:

```text
Launch Template
→ AMI/User Data
→ Private EC2 outbound/NAT
→ Security Group
→ application process
→ Health Check path/port
```

특히 Private Subnet에서 package download 기반 User Data를 사용한다면 NAT/outbound 누락을 반드시 후보에 넣는다.

## Case 8 — CPU가 높은데 Scale-out 안 됨

한 인스턴스만 CPU가 높은 경우와 ASG 평균 CPU가 높은 경우를 구분한다.

```text
개별 EC2 CPU
→ ASG 평균 CPU
→ Target Tracking 설정
→ ASG Activity
```

Policy를 일부러 잘못 구성하거나 평균 CPU가 목표에 못 미치는 상황을 만들어 원인을 설명한다.

## Case 9 — HTTPS 접속 실패
다음을 점검한다.

- Route 53 Alias
- DNS resolution
- 443 Listener
- ALB-SG 443
- ACM certificate/domain match
- Target Group health

DNS/TLS/ALB backend 문제를 한 덩어리로 취급하지 않는다.

## 공통 진단 순서
정답은 아니지만 기본 틀로 사용한다.

```text
1. 사용자 증상 정의: timeout / 4xx / 5xx / DNS / TLS
2. DNS/진입점 확인
3. ALB Listener/Target 상태
4. 네트워크(SG/Route)
5. EC2/애플리케이션/bootstrap
6. DB/IAM 같은 하위 의존성
7. CloudWatch Metric/Log로 증거 확인
```

## CLI 장애 검증

[CLI Verification Guide](../CLI_VERIFICATION.md)의 Example 15 명령을 사용해 다음을 출력한다.

```text
ALB / Listener
Target Group / Target Health
ASG Activity
EC2 상태
RDS 상태
CloudWatch Alarm
```

장애 전/중/복구 후 출력을 비교한다.

## 최종 구술 연습
다음 질문에 1~2분씩 말로 답한다.

- ALB 503이면 Target unhealthy라고 바로 결론 내려도 되는가?
- Target이 0개인 상태와 모든 Target이 unhealthy인 상태는 어떻게 다른가?
- Timeout과 Connection Refused는 어떤 후보 원인이 다른가?
- EC2가 healthy인데 API만 500이면 어느 계층 문제일 가능성이 큰가?
- DB 연결 실패에서 SG 문제와 credential 문제를 어떻게 구분할 것인가?
- 새 ASG 인스턴스가 unhealthy일 때 bootstrap과 NAT를 왜 확인하는가?
- S3 AccessDenied에서 무엇을 확인할 것인가?

## 완료 체크
- [ ] 최소 6개 Case를 직접 재현했다.
- [ ] Target 0개 / 일부 unhealthy / 전체 unhealthy를 비교했다.
- [ ] ALB fail-open 개념을 실제 결과와 연결했다.
- [ ] 정답을 보기 전에 가설을 세웠다.
- [ ] CloudWatch/Target Group/로그로 증거를 찾았다.
- [ ] 복구 후 정상 상태를 다시 확인했다.
- [ ] 각 장애의 재발 방지 방법을 적었다.
- [ ] 증상만 듣고 진단 순서를 설명할 수 있다.

## 비용 정리
모든 테스트 리소스를 정상 복구한 뒤 필요 없는 인프라를 삭제한다. NAT Gateway, RDS, ALB, EC2/ASG, EBS, S3 versions, Log Group을 특히 확인한다.

삭제 후 CLI 전체 잔존 리소스 검사를 실행한다.
