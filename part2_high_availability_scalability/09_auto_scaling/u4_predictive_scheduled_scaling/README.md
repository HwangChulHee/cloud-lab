# u4. Predictive Scaling과 Scheduled Scaling

## 지도 확인

Auto Scaling은 현재 부하에 반응하는 것뿐 아니라 **앞으로 부하가 늘어날 것을 알고 있거나 예측할 수 있을 때 미리 확장**할 수도 있다.

대표적으로 두 가지를 구분한다.

```text
Scheduled Scaling
Predictive Scaling
```

둘 다 "트래픽이 이미 몰린 뒤"가 아니라 **미리 준비한다**는 공통점이 있다.

---

## 1. Scheduled Scaling

Scheduled Scaling은 사람이 이미 알고 있는 일정에 맞춰 ASG의 크기를 바꾸는 방식이다.

예:

```text
매주 금요일 17시
라이브 커머스 시작
```

매번 실제 CPU가 오를 때까지 기다릴 필요 없이 17시 전에 서버를 늘릴 수 있다.

```text
평소
Min = 2
Desired = 2

금요일 17시
Min = 10
Desired = 10
```

즉 **시간표 기반 자동 확장**이다.

### 잘 맞는 상황

```text
매일 오전 9시 업무 시작
매주 금요일 정기 이벤트
월말 정산 시간
정기 배치 시간
```

처럼 반복 일정이 명확한 경우다.

---

## 2. Predictive Scaling

Predictive Scaling은 과거 부하 패턴을 바탕으로 앞으로 필요한 용량을 예측하고 미리 확장한다.

예를 들어 최근 몇 주 동안 계속 다음 패턴이 있었다고 하자.

```text
11:30 트래픽 증가 시작
12:00 최고점
13:30 다시 감소
```

Predictive Scaling은 이런 반복 패턴을 바탕으로 필요한 시점 전에 인스턴스를 준비하도록 한다.

```text
11:20
미리 Scale Out

12:00
트래픽 도착 시 이미 서버 준비
```

핵심은 **forecast = 미래 부하 예측**이다.

---

## 3. Scheduled vs Predictive

둘의 차이를 쉽게 보면:

```text
Scheduled Scaling
→ 사람이 시간표를 안다

Predictive Scaling
→ 시스템이 과거 패턴을 보고 미래 부하를 예측한다
```

예시:

```text
"매주 금요일 17시 세일 시작"
→ Scheduled

"최근 몇 주간 매일 12시쯤 트래픽이 몰림"
→ Predictive
```

---

## 4. 왜 미리 Scale Out해야 하나?

새 EC2가 만들어진다고 바로 요청을 받을 수 있는 것은 아니다.

대략 다음 과정이 필요할 수 있다.

```text
EC2 Launch
→ OS 부팅
→ User Data 실행
→ 애플리케이션 시작
→ Health Check 통과
→ 실제 요청 처리 가능
```

따라서 부하가 이미 폭증한 뒤에 Scale Out하면 새 인스턴스가 준비되는 동안 기존 인스턴스가 계속 과부하 상태일 수 있다.

Scheduled / Predictive Scaling은 이 준비 시간을 고려해 미리 capacity를 늘리는 데 의미가 있다.

---

## SAA 판단

```text
정해진 시간에 capacity 변경
→ Scheduled Scaling

과거 패턴을 바탕으로 미래 부하를 forecast
→ Predictive Scaling

부하가 오기 전에 미리 서버를 준비
→ Scheduled / Predictive 공통 목적
```
