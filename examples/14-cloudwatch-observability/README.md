# Example 14 — CloudWatch로 전체 구조 관측하기

새로운 인프라를 많이 추가하지 않고, 지금까지 만든 ALB/EC2/ASG/RDS 구조를 **어떻게 관측하고 장애 징후를 찾는지** 연습한다.

## Recall Check
- ALB target unhealthy는 어디서 확인했나?
- ASG scale-out은 어떤 metric과 연결할 수 있었나?
- RDS 연결 장애와 네트워크 장애는 어떤 증상 차이가 있었나?

## 새로 배우는 것
- CloudWatch Metrics
- CloudWatch Logs
- Alarm
- 서비스별 핵심 지표
- Auto Scaling Group metric collection 활성화

## 반복하는 것
ALB, ASG, EC2, RDS, Health Check, 장애 재현을 다시 사용한다.

모든 태그 가능 리소스에는 `Project=cloud-lab`, `Stage=examples`, `Example=14`를 붙인다.

## 이번에는 도움 없이
기존 전체 구조가 없다면 최소한 `ALB → ASG/EC2 → RDS`를 다시 구성한다.

Private EC2의 bootstrap이 외부 다운로드에 의존하면 NAT 또는 사전 준비 AMI를 사용한다.

## 1. ALB 지표 보기
다음을 찾아 그래프를 확인한다.

- RequestCount
- TargetResponseTime
- HTTPCode_ELB_5XX
- HTTPCode_Target_5XX
- HealthyHostCount / UnHealthyHostCount

요청을 여러 번 보내 그래프 변화를 본다.

## 2. EC2 지표 보기
- CPUUtilization
- NetworkIn / NetworkOut

부하 테스트를 짧게 실행해 CPU 변화가 어떻게 보이는지 확인한다.

## 3. ASG Group Metric 활성화

`GroupDesiredCapacity`, `GroupInServiceInstances` 같은 Auto Scaling Group 지표를 보려면 group metric collection을 활성화한다.

```bash
aws autoscaling enable-metrics-collection \
  --region $AWS_REGION \
  --auto-scaling-group-name <asg-name> \
  --granularity 1Minute
```

그다음 CloudWatch에서 다음을 확인한다.

- GroupDesiredCapacity
- GroupInServiceInstances
- GroupTotalInstances

이 지표가 EC2의 `CPUUtilization`과 같은 종류의 지표가 아니라 **ASG 자체 상태 지표**라는 점을 구분한다.

## 4. RDS 지표 보기
- CPUUtilization
- DatabaseConnections
- FreeStorageSpace
- FreeableMemory

애플리케이션 연결을 여러 번 만들어 DatabaseConnections 변화가 보이는지 확인한다.

Example 09에서 `/db-health` 같은 endpoint를 만들었다면 정상/장애 상태에서 함께 호출한다.

## 5. Logs 보기
애플리케이션 또는 웹 서버 로그를 CloudWatch Logs로 보낼 수 있다면 연결한다. 최소한 다음 질문에 답할 수 있어야 한다.

```text
Metric: 무엇이 이상한지 알려주는 신호
Log: 왜 이상한지 추적하는 단서
```

CloudWatch Agent 또는 애플리케이션 로그 전송 설정을 사용하는 경우 Log Group 이름을 `example-14-*` 형식으로 맞춘다.

## 6. Alarm 만들기
예시:
- EC2 CPU가 일정 수준 이상
- ALB UnHealthyHostCount > 0
- RDS FreeStorageSpace 임계값 이하

Alarm 상태 `OK → ALARM → OK` 변화를 직접 확인한다.

## 장애 실험 A — nginx/app 중지
한 EC2의 nginx 또는 app을 중지하고 다음을 동시에 본다.

```text
Target Group 상태
ALB HealthyHostCount
CloudWatch Alarm
Application 요청 결과
```

## 장애 실험 B — Application 5xx
애플리케이션이 500을 반환하도록 테스트 endpoint를 만들고 `HTTPCode_ELB_5XX`와 `HTTPCode_Target_5XX`의 차이를 확인한다.

## 장애 실험 C — DB 연결 실패
Example 09의 `/db-health`가 있다면 RDS-SG를 잠시 차단하고 다음을 함께 본다.

```text
ALB target health
Application 5xx/log
RDS DatabaseConnections
RDS 자체 상태
```

ALB target이 healthy라고 해서 애플리케이션의 모든 하위 의존성이 정상이라는 뜻은 아니라는 점을 확인한다.

## 판단 연습
- 사용자가 "느리다"고 한다 → 어떤 지표부터 볼까?
- 503이 발생한다 → Listener/Target 상태와 HealthyHostCount를 어떻게 볼까?
- Target 5xx만 증가한다 → ALB 자체 문제일 가능성이 높은가?
- DatabaseConnections만 급증한다 → 어떤 문제를 의심할 수 있을까?
- GroupDesiredCapacity와 GroupInServiceInstances가 다르면 무엇을 의미할 수 있을까?

## CLI 구축 검증
[CLI Verification Guide](../CLI_VERIFICATION.md)의 Example 14 명령을 실행한다.

## 기억만으로 설명하기
`사용자 증상 → ALB → Target → EC2 앱 → RDS` 순서로 어디에서 어떤 metric/log를 볼지 설명한다.

## 완료 체크
- [ ] ALB 핵심 metric을 확인했다.
- [ ] EC2 metric을 확인했다.
- [ ] ASG metric collection을 활성화했다.
- [ ] ASG group metric을 확인했다.
- [ ] RDS metric을 확인했다.
- [ ] Alarm을 만들고 상태 변화를 봤다.
- [ ] 장애 발생 시 여러 화면의 신호를 연결해봤다.
- [ ] Metric과 Log의 역할을 구분할 수 있다.

## 비용 정리
불필요한 Alarm/Log Group과 테스트 인프라를 정리한다. Log Group은 리소스를 지워도 자동으로 남을 수 있으므로 별도로 확인한다.

삭제 후 CLI 삭제 검증을 실행한다.
