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
- ALB / Target Group / Health Check
- ASG / EC2
- VPC / Route Table / SG
- RDS
- IAM / S3
- CloudWatch

## 이번에는 도움 없이
각 장애 Case는 먼저 README 아래쪽의 힌트를 보지 않고 다음 양식으로 기록한다.

```text
증상:
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
- Route/DNS 문제
- 잘못된 endpoint 사용

핵심은 `timeout`이라는 증상만 보고 바로 정답을 찍지 않는 것이다.

## Case 2 — ALB 503
Target을 모두 unhealthy 상태로 만든다. Target Group 상태와 HealthyHostCount를 보고 원인을 좁힌다.

## Case 3 — Target Unhealthy
다음 중 하나를 랜덤하게 선택해 장애를 만든다.
- nginx 중지
- Health Check path 오류
- EC2-SG에서 ALB-SG 차단
- 앱이 health endpoint에서 500 반환

같은 `unhealthy`라도 원인이 여러 개라는 점을 확인한다.

## Case 4 — App은 뜨지만 DB 연결 실패
다음 후보를 하나씩 실험한다.
- RDS-SG 차단
- 잘못된 endpoint
- 잘못된 port
- credential 오류

네트워크 timeout과 인증 오류의 차이를 로그에서 구분한다.

## Case 5 — S3 Upload AccessDenied
EC2와 네트워크는 정상인데 S3 작업만 실패하도록 IAM Action/Resource를 잘못 설정한다. Role, Policy, Bucket Policy를 순서대로 본다.

## Case 6 — 새 EC2가 계속 Unhealthy
ASG가 replacement를 생성했지만 Target Group에 정상 편입되지 않는 상황을 만든다.

확인 후보:
- Launch Template
- User Data 실행 실패
- SG
- Health Check path/port
- 애플리케이션 시작 실패

## Case 7 — CPU 90%인데 Scale-out 안 됨
CPU 부하를 주고 Scaling Policy를 잘못 구성한다. CloudWatch Metric → Policy → ASG Activity 순서로 확인한다.

## Case 8 — HTTPS 접속 실패
다음 중 하나를 점검한다.
- 443 Listener
- ALB-SG 443
- ACM certificate/domain
- Route 53 Alias

## 공통 진단 순서
정답은 아니지만 기본 틀로 사용한다.

```text
1. 사용자 증상 정의
2. DNS/진입점 확인
3. ALB Listener/Target 상태
4. 네트워크(SG/Route)
5. EC2/애플리케이션
6. DB/IAM 같은 하위 의존성
7. CloudWatch Metric/Log로 증거 확인
```

## 최종 구술 연습
다음 질문에 1~2분씩 말로 답한다.

- ALB 503이면 어디부터 볼 것인가?
- Timeout과 Connection Refused는 어떤 후보 원인이 다른가?
- EC2가 healthy인데 API만 500이면 어느 계층 문제일 가능성이 큰가?
- DB 연결 실패에서 SG 문제와 credential 문제를 어떻게 구분할 것인가?
- S3 AccessDenied에서 무엇을 확인할 것인가?

## 완료 체크
- [ ] 최소 5개 Case를 직접 재현했다.
- [ ] 정답을 보기 전에 가설을 세웠다.
- [ ] CloudWatch/Target Group/로그로 증거를 찾았다.
- [ ] 복구 후 정상 상태를 다시 확인했다.
- [ ] 각 장애의 재발 방지 방법을 적었다.
- [ ] 증상만 듣고 진단 순서를 설명할 수 있다.

## 비용 정리
모든 테스트 리소스를 정상 복구하거나 삭제한다.
