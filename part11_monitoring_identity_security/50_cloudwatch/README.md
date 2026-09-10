# 50. CloudWatch

`examples/08`, `14`, `15`, `16`을 하기 전에 필요한 CloudWatch 핵심을 정리한다.

## 1. 역할

CloudWatch는 AWS 리소스와 애플리케이션의 상태를 관측하기 위한 서비스다.

핵심은 세 가지다.

```text
Metrics → 숫자로 상태 관찰
Logs    → 사건의 세부 내용 확인
Alarms  → 조건을 만족하면 상태 변화/후속 동작
```

장애 대응에서는 보통 다음 순서로 연결한다.

```text
증상 발생
→ Metric으로 어디가 이상한지 범위 축소
→ Log로 구체적인 원인 확인
→ 필요하면 Alarm/자동화로 재발 대응
```

## 2. Metrics

Metric은 시간에 따라 변하는 수치 데이터다.

실습에서 우선 볼 지표:

### EC2
- CPUUtilization
- NetworkIn / NetworkOut
- StatusCheckFailed 계열

### ALB
- RequestCount
- TargetResponseTime
- HTTPCode_ELB_5XX_Count
- HTTPCode_Target_5XX_Count
- HealthyHostCount / UnHealthyHostCount

### RDS
- CPUUtilization
- DatabaseConnections
- FreeStorageSpace
- FreeableMemory

### ASG
- GroupDesiredCapacity
- GroupInServiceInstances
- GroupTotalInstances

## 3. Dimension과 Namespace

Metric은 서비스별 namespace에 속하고 dimension으로 특정 리소스를 구분한다.

예:

```text
Namespace: AWS/EC2
Metric: CPUUtilization
Dimension: InstanceId=i-xxxx
```

같은 이름의 metric이라도 어떤 리소스의 값인지 dimension을 확인해야 한다.

## 4. Logs

CloudWatch Logs는 애플리케이션 로그나 AWS 서비스 로그를 모아 확인할 때 사용한다.

기본 구조:

```text
Log Group
  └─ Log Stream
       └─ Log Events
```

실습에서 중요한 질문:

- 요청이 ALB까지 왔는가?
- 애플리케이션이 오류를 남겼는가?
- DB 연결 오류인지 애플리케이션 오류인지 로그로 구분할 수 있는가?

EC2 OS/애플리케이션 로그는 기본적으로 모든 파일이 자동 전송되는 것이 아니다. 필요하면 CloudWatch Agent 등을 사용해 수집한다.

## 5. Alarms

Alarm은 metric을 일정 기간 관찰해 조건을 평가한다.

개념적으로:

```text
CPUUtilization > 70%
for 일정 기간
→ ALARM
```

상태:

```text
OK
ALARM
INSUFFICIENT_DATA
```

ASG는 CloudWatch metric/alarm과 scaling policy를 연결해 scale-out/scale-in할 수 있다.

## 6. 장애 상황별 첫 관찰 지점

### 서비스가 느리다

```text
ALB TargetResponseTime
→ EC2 CPU / Network
→ RDS CPU / Connections
→ application logs
```

### ALB 5xx가 증가한다

`ELB_5XX`와 `Target_5XX`를 구분한다.

```text
ELB 자체에서 발생한 5xx인가?
Target 애플리케이션이 반환한 5xx인가?
```

### Target이 줄었다

```text
HealthyHostCount / UnHealthyHostCount
→ Target Group health reason
→ EC2 process / SG / health endpoint
```

### DB가 의심된다

```text
DatabaseConnections
CPUUtilization
FreeableMemory
FreeStorageSpace
→ application DB error log
```

## 7. ASG와의 연결

예제에서 확인할 구조:

```text
EC2 Metric
   ↓
CloudWatch
   ↓
Scaling Policy
   ↓
ASG
   ↓
EC2 추가/제거
```

단순히 CPU가 높다는 것과 실제 scale-out이 일어나는 것은 다르다. ASG policy, target value, cooldown/warmup, min/max capacity도 함께 확인해야 한다.

## 8. 실습 전 Recall Check

- Metric과 Log는 무엇이 다른가?
- Alarm은 로그 내용을 직접 읽는 서비스인가?
- ALB 5xx와 Target 5xx를 왜 구분해야 하는가?
- RDS 연결 문제가 의심되면 어떤 지표를 볼 것인가?
- ASG가 scale-out하지 않을 때 CloudWatch 외에 무엇을 확인해야 하는가?

## 9. 완료 기준

- [ ] Metrics / Logs / Alarms 차이를 설명할 수 있다.
- [ ] EC2 / ALB / RDS의 핵심 metric을 몇 개 말할 수 있다.
- [ ] 증상에 따라 첫 확인 metric을 고를 수 있다.
- [ ] ALB의 ELB 5xx와 Target 5xx 차이를 설명할 수 있다.
- [ ] CloudWatch와 ASG scaling의 연결을 설명할 수 있다.
- [ ] Metric → Log → 원인 확인 흐름으로 장애를 접근할 수 있다.
