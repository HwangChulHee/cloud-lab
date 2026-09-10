# u3. CloudWatch Alarms와 Scale Out / Scale In

## 지도 확인

ASG는 CloudWatch Alarm과 연결해 현재 부하를 보고 자동으로 인스턴스 수를 조절할 수 있다.

구조를 단순화하면 다음과 같다.

```text
EC2 여러 대
  ↓ metric
CloudWatch
  ↓ alarm
Scaling Policy
  ↓
ASG
  ↓
EC2 추가 또는 제거
```

---

## 1. Metric이란?

**Metric**은 시스템 상태를 숫자로 표현한 값이다.

예:

```text
CPUUtilization = 72%
RequestCount = 1200
NetworkIn = 특정 바이트 수
```

ASG에서는 개별 EC2 한 대가 아니라 **그룹 전체의 평균값**을 기준으로 보는 경우가 중요하다.

예를 들어 EC2가 3대이고 CPU가 다음과 같다고 하자.

```text
EC2 A = 50%
EC2 B = 70%
EC2 C = 60%
```

평균은 약 60%다.

Scaling Policy가 평균 CPU를 기준으로 한다면 이 전체 그룹의 상태를 보고 판단한다.

---

## 2. CloudWatch Alarm이란?

CloudWatch Alarm은 metric을 계속 감시하다가 특정 조건을 만족하면 상태가 바뀌는 기능이다.

예:

```text
조건:
Average CPU > 70%
```

CPU가 기준을 넘으면 Alarm이 발생하고, 이 Alarm을 Scaling Policy와 연결할 수 있다.

```text
Average CPU > 70%
→ Alarm
→ Scale Out Policy
→ EC2 추가
```

반대로:

```text
Average CPU < 30%
→ Alarm
→ Scale In Policy
→ EC2 제거
```

---

## 3. Scale Out

Scale Out은 인스턴스 수를 늘리는 것이다.

예:

```text
현재 EC2 2대
CPU 평균 85%
```

부하가 높다고 판단하면:

```text
Scale Out
→ EC2 2대 추가
→ 총 4대
```

서버가 늘어나면 요청이 더 많은 인스턴스로 분산되어 한 대당 부담을 낮출 수 있다.

---

## 4. Scale In

Scale In은 인스턴스 수를 줄이는 것이다.

예:

```text
현재 EC2 6대
CPU 평균 12%
```

서버가 너무 많이 남는다면:

```text
Scale In
→ EC2 2대 제거
→ 총 4대
```

이 과정은 비용 절감과 연결된다.

하지만 무조건 줄이지는 않는다.

ASG의 Minimum Capacity보다 아래로 내려갈 수는 없다.

```text
Min = 2
현재 = 2
```

인 상황에서는 Scale In 조건이 생겨도 최소 2대는 유지해야 한다.

---

## 5. Custom Metric

강의에서는 CPU 같은 기본 metric뿐 아니라 **Custom Metric**을 사용할 수 있다는 점도 다룬다.

Custom Metric은 애플리케이션이나 운영자가 직접 정의한 지표라고 생각하면 된다.

예:

```text
현재 대기 중인 작업 수
현재 접속 사용자 수
특정 비즈니스 이벤트 수
```

CPU가 낮아도 작업 큐가 너무 많이 쌓이는 시스템이라면 CPU만으로 Scale Out하는 것이 적절하지 않을 수 있다.

따라서 워크로드 특성에 맞는 metric을 선택하는 것이 중요하다.

---

## SAA 판단

```text
CloudWatch에서 CPU나 custom metric을 감시
→ CloudWatch Alarm

Alarm 조건 만족 시 서버 증가
→ Scale Out

Alarm 조건 만족 시 서버 감소
→ Scale In

ASG 전체 평균 CPU 기반으로 조절
→ 그룹 단위 metric 이해
```
