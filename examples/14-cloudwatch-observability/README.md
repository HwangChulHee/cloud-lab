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

## 반복하는 것
ALB, ASG, EC2, RDS, Health Check, 장애 재현을 다시 사용한다.

## 이번에는 도움 없이
기존 전체 구조가 없다면 최소한 `ALB → ASG/EC2 → RDS`를 다시 구성한다.

## 1. ALB 지표 보기
다음을 찾아 그래프를 확인한다.

- RequestCount
- TargetResponseTime
- HTTPCode_ELB_5XX
- HTTPCode_Target_5XX
- HealthyHostCount / UnHealthyHostCount

요청을 여러 번 보내 그래프 변화를 본다.

## 2. EC2/ASG 지표 보기
- CPUUtilization
- NetworkIn / NetworkOut
- GroupDesiredCapacity / GroupInServiceInstances

부하 테스트를 짧게 실행해 CPU와 ASG 변화가 어떻게 연결되는지 본다.

## 3. RDS 지표 보기
- CPUUtilization
- DatabaseConnections
- FreeStorageSpace
- FreeableMemory

애플리케이션 연결을 여러 번 만들어 DBConnections 변화가 보이는지 확인한다.

## 4. Logs 보기
애플리케이션 또는 웹 서버 로그를 CloudWatch Logs로 보낼 수 있다면 연결한다. 최소한 다음 질문에 답할 수 있어야 한다.

```text
Metric: 무엇이 이상한지 알려줌
Log: 왜 이상한지 추적하는 단서
```

## 5. Alarm 만들기
예시:
- EC2 CPU가 일정 수준 이상
- ALB UnHealthyHostCount > 0
- RDS FreeStorageSpace 임계값 이하

Alarm 상태 `OK → ALARM → OK` 변화를 직접 확인한다.

## 장애 실험 A — nginx 중지
한 EC2의 nginx를 중지하고 다음을 동시에 본다.

```text
Target Group 상태
ALB HealthyHostCount
CloudWatch Alarm
Application 요청 결과
```

## 장애 실험 B — Application 5xx
애플리케이션이 500을 반환하도록 테스트 endpoint를 만들고 `ELB 5xx`와 `Target 5xx`의 차이를 확인한다.

## 판단 연습
- 사용자가 "느리다"고 한다 → 어떤 지표부터 볼까?
- 503이 발생한다 → HealthyHostCount는 어떤 단서인가?
- Target 5xx만 증가한다 → ALB 자체 문제일 가능성이 높은가?
- DBConnections만 급증한다 → 어떤 문제를 의심할 수 있을까?

## 기억만으로 설명하기
`사용자 증상 → ALB → Target → EC2 앱 → RDS` 순서로 어디에서 무엇을 관찰할지 설명한다.

## 완료 체크
- [ ] ALB 핵심 metric을 확인했다.
- [ ] EC2/ASG metric을 확인했다.
- [ ] RDS metric을 확인했다.
- [ ] Alarm을 만들고 상태 변화를 봤다.
- [ ] 장애 발생 시 여러 화면의 신호를 연결해봤다.
- [ ] Metric과 Log의 역할을 구분할 수 있다.

## 비용 정리
불필요한 Alarm/Log Group과 테스트 인프라를 정리한다.
