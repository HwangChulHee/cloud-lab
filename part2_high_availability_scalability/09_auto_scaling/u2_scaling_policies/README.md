# u2. Scaling Policies

## 지도 확인

ASG가 자동으로 EC2 수를 조절하려면 **언제 늘리고 언제 줄일지에 대한 기준**이 필요하다.

이 기준을 **Scaling Policy**라고 한다.

```text
현재 EC2 수
  ↓
어떤 기준을 감시
  ↓
Scaling Policy 판단
  ↓
Scale Out 또는 Scale In
```

강의에서는 대표적으로 다음 정책들을 구분한다.

```text
Target Tracking Scaling
Simple / Step Scaling
Scheduled Scaling
Predictive Scaling
```

이름이 많아 보여도 핵심은 간단하다.

```text
목표값 유지
조건 발생 시 증감
시간표대로 증감
미래 부하 예측 후 미리 증감
```

---

## 1. Target Tracking Scaling

**Target Tracking**은 특정 지표를 목표값 근처에 유지하도록 ASG가 자동으로 인스턴스 수를 조절하는 방식이다.

예:

```text
목표:
ASG 평균 CPU 사용률을 약 40%로 유지
```

현재 CPU가 너무 높다면:

```text
CPU 75%
→ 서버가 바쁨
→ Scale Out
→ EC2 증가
→ 서버 한 대당 부하 감소
```

반대로 CPU가 너무 낮다면:

```text
CPU 10%
→ 서버가 많이 남음
→ Scale In
→ EC2 감소
```

자동차의 크루즈 컨트롤처럼 생각하면 쉽다.

```text
목표 속도 100km/h
→ 느리면 가속
→ 빠르면 감속
```

Target Tracking에서는 우리가 "CPU가 70이면 몇 대 추가" 같은 세부 규칙을 일일이 직접 정하기보다, **유지하고 싶은 목표값**을 정하는 데 초점이 있다.

### 예시

쇼핑몰 서버가 있다고 하자.

```text
ASG 평균 CPU 목표 = 40%
Min = 2
Max = 8
```

점심시간 주문이 몰려 CPU가 계속 높아지면 ASG가 인스턴스를 늘려 평균 부하를 목표값 방향으로 낮추려고 한다.

시험에서 다음과 같은 표현이 나오면 Target Tracking을 떠올린다.

```text
CPU를 40% 근처로 유지
Request 수를 특정 목표값 근처로 유지
특정 metric의 target value를 유지
```

---

## 2. Simple / Step Scaling

이 방식은 **조건이 발생했을 때 정해진 수량만큼 늘리거나 줄이는 것**에 가깝다.

강의 예시:

```text
CPU > 70%
→ EC2 2대 추가

CPU < 30%
→ EC2 1대 제거
```

이때 보통 CloudWatch Alarm이 조건을 감시한다.

```text
CloudWatch Alarm
      ↓
조건 충족
      ↓
Scaling Policy
      ↓
ASG 크기 변경
```

### Step Scaling을 쉽게 이해하기

부하가 얼마나 심한지에 따라 단계별로 다른 조치를 취한다고 생각하면 된다.

예:

```text
CPU 60~70%
→ 1대 추가

CPU 70~85%
→ 2대 추가

CPU 85% 이상
→ 4대 추가
```

즉 **Step = 구간별 대응**이라는 느낌이다.

Target Tracking과 비교하면:

```text
Target Tracking
→ 목표값을 유지하게 맡긴다

Step Scaling
→ 특정 조건/구간마다 내가 조정량을 정한다
```

---

## 3. Scheduled Scaling

Scheduled Scaling은 **언제 부하가 증가할지 이미 알고 있을 때** 사용한다.

예:

```text
매주 금요일 오후 5시
이벤트 시작
→ 사용자가 늘어남
```

트래픽이 실제로 증가한 뒤 CPU를 보고 대응하는 대신 미리 서버를 늘릴 수 있다.

```text
16:55
EC2 2대

17:00
Scheduled Scaling 실행
→ Min Capacity를 10으로 증가

17:00 이후
EC2 10대 준비 완료
```

핵심은 **예측 가능한 일정**이다.

```text
매일 오전 9시
매주 금요일 17시
정기 배치 시간
정기 세일 시작 시간
```

같이 시간 패턴이 명확하다면 Scheduled Scaling이 잘 맞는다.

---

## 4. Predictive Scaling

Predictive Scaling은 **과거의 사용 패턴을 바탕으로 앞으로 필요한 용량을 예측하고 미리 확장**하는 방식이다.

예:

```text
최근 여러 주 동안
매일 12시 트래픽 급증
```

이 패턴을 바탕으로:

```text
11:50쯤 미리 Scale Out
→ 12시 트래픽 도착 전에 준비
```

할 수 있다.

Scheduled Scaling과 비슷해 보이지만 차이는 다음처럼 잡으면 된다.

```text
Scheduled Scaling
→ 사람이 이미 알고 있는 시간표

Predictive Scaling
→ 시스템이 과거 패턴을 보고 미래 부하를 예측
```

---

## 5. Dynamic Scaling이라는 큰 범주

강의에서는 Target Tracking과 Simple / Step Scaling을 **Dynamic Scaling** 문맥에서 설명한다.

Dynamic이라는 말은 부하나 metric 같은 현재 상태 변화에 반응해서 조절한다고 이해하면 쉽다.

```text
현재 metric 변화
→ 판단
→ Scale Out / Scale In
```

반면 Scheduled Scaling은 미리 정한 시간표, Predictive Scaling은 예측 결과를 기반으로 한다.

---

## SAA 판단

```text
평균 CPU 40% 유지
→ Target Tracking

CPU > 70%면 2대 추가
→ Simple / Step Scaling

부하 구간별로 다른 수량 증감
→ Step Scaling

매주 금요일 17시에 미리 확장
→ Scheduled Scaling

과거 패턴을 분석해 미래 부하 전에 확장
→ Predictive Scaling
```
