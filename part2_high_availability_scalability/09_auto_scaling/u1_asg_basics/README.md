# u1. Auto Scaling Group 기본 구조

## 지도 확인

Auto Scaling Group, 줄여서 **ASG**는 EC2 인스턴스 여러 대를 하나의 그룹으로 묶고, 필요한 수량을 자동으로 유지하거나 조절하는 기능이다.

예를 들어 쇼핑몰 서버가 평소에는 2대면 충분하지만 점심시간에 주문이 몰릴 때 5대가 필요하다고 해보자.

```text
평소
EC2 2대

트래픽 증가
↓
EC2 5대

트래픽 감소
↓
EC2 2대
```

사람이 매번 콘솔에 들어가 EC2를 만들고 지우는 대신 ASG가 이 수량 조절을 자동화한다.

---

## 1. Auto Scaling이 필요한 이유

서버 수를 항상 최대치로 유지하면 안정적일 수는 있지만 비용이 낭비된다.

반대로 서버 수를 항상 최소치로 유지하면 트래픽이 갑자기 늘었을 때 처리하지 못할 수 있다.

ASG의 목적은 이 두 문제 사이에서 필요한 만큼만 서버를 유지하는 것이다.

```text
트래픽 적음
→ 인스턴스 수 감소
→ 비용 절감

트래픽 많음
→ 인스턴스 수 증가
→ 처리 용량 확보
```

이때 인스턴스를 늘리는 것을 **Scale Out**, 줄이는 것을 **Scale In**이라고 한다.

```text
Scale Out = 서버 수 늘리기
Scale In  = 서버 수 줄이기
```

CPU 성능이 더 큰 인스턴스로 바꾸는 것은 보통 **Vertical Scaling**, 인스턴스 대수를 늘리는 것은 **Horizontal Scaling**이라고 생각하면 된다.

ASG는 주로 Horizontal Scaling을 자동화한다.

---

## 2. ASG는 어떤 EC2를 만들지 알아야 한다

ASG가 새 EC2를 자동으로 생성하려면 어떤 형태의 EC2를 만들어야 하는지 기준이 필요하다.

예:

```text
AMI
Instance Type
Security Group
Key Pair
User Data
```

즉 "서버 하나 만들 때 필요한 설계도"가 있어야 한다.

이 역할을 **Launch Template**이 담당한다.

```text
Launch Template
├── AMI
├── Instance Type
├── Security Group
├── User Data
└── 기타 EC2 설정

        ↓
Auto Scaling Group
        ↓
EC2 A / EC2 B / EC2 C ...
```

예를 들어 Launch Template에 다음이 들어 있다고 하자.

```text
AMI: Amazon Linux
Instance Type: t3.micro
Security Group: web-sg
User Data: 웹 서버 자동 설치
```

그러면 ASG가 Scale Out할 때 같은 기준으로 새 EC2를 생성할 수 있다.

---

## 3. Minimum / Desired / Maximum Capacity

ASG에서 가장 기본적으로 이해해야 하는 값은 세 가지다.

### Minimum Capacity

ASG가 절대로 이보다 적게 내려가지 않도록 하는 최소 인스턴스 수다.

```text
Min = 2
```

이라면 트래픽이 아무리 없어도 최소 2대는 유지한다.

왜 0대로 만들지 않을까?

서비스를 항상 켜두어야 한다면 최소 서버 수가 필요하기 때문이다.

---

### Desired Capacity

현재 ASG가 유지하려고 하는 목표 인스턴스 수다.

예:

```text
Min     = 2
Desired = 3
Max     = 6
```

현재는 3대를 유지하려고 한다.

인스턴스 한 대가 죽어서 2대가 되면 ASG는 Desired Capacity 3을 맞추기 위해 새 인스턴스를 생성하려고 한다.

```text
원래 3대
↓
1대 장애
↓
현재 2대
↓
ASG가 새 EC2 1대 생성
↓
다시 3대
```

즉 Desired Capacity는 "지금 그룹이 목표로 하는 크기"라고 이해하면 쉽다.

---

### Maximum Capacity

Scale Out이 되더라도 넘지 않도록 하는 최대 인스턴스 수다.

```text
Max = 6
```

이면 트래픽이 많이 늘어도 ASG가 무제한으로 EC2를 만들지 않고 최대 6대까지만 늘어난다.

따라서 세 값을 함께 보면:

```text
Min     = 최소 보장 수량
Desired = 현재 목표 수량
Max     = 최대 허용 수량
```

이라고 보면 된다.

---

## 4. 여러 Availability Zone에 분산

ASG는 여러 Availability Zone에 EC2를 배치하는 구조와 함께 사용할 수 있다.

```text
Region
├── AZ-A
│   ├── EC2
│   └── EC2
│
└── AZ-B
    ├── EC2
    └── EC2
```

한 AZ에만 서버를 몰아두면 그 AZ에 문제가 생겼을 때 서비스 전체가 영향을 받을 수 있다.

따라서 고가용성 구조에서는 여러 AZ에 인스턴스를 분산하는 방식이 중요하다.

ASG가 ELB와 함께 사용되는 이유도 이 구조와 연결된다.

```text
Users
  ↓
ELB
  ↓
ASG
├── EC2 in AZ-A
└── EC2 in AZ-B
```

---

## SAA 판단

```text
EC2 수량을 자동으로 유지/조절
→ Auto Scaling Group

새 EC2를 어떤 설정으로 생성할지 정의
→ Launch Template

최소 인스턴스 수
→ Minimum Capacity

현재 목표 인스턴스 수
→ Desired Capacity

최대 인스턴스 수
→ Maximum Capacity

인스턴스 수 증가
→ Scale Out

인스턴스 수 감소
→ Scale In
```
