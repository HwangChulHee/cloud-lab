# u6. ELB + ASG 통합

## 지도 확인

Auto Scaling Group은 인스턴스 수를 조절하고, Elastic Load Balancer는 사용자 요청을 여러 인스턴스에 분산한다.

둘을 함께 사용하면 다음 구조가 된다.

```text
Users
  ↓
Elastic Load Balancer
  ↓
Target Group
  ↓
Auto Scaling Group
├── EC2 A
├── EC2 B
└── EC2 C
```

역할을 나누면:

```text
ELB
→ 요청을 어느 인스턴스로 보낼지 결정

ASG
→ 인스턴스가 몇 대 있어야 하는지 결정
```

---

## 1. Scale Out이 일어날 때

현재 EC2가 2대라고 하자.

```text
ELB
├── EC2 A
└── EC2 B
```

트래픽이 늘어 ASG가 Scale Out하면 새 EC2가 생성된다.

```text
ASG
→ EC2 C 생성
```

새 인스턴스가 Target Group에 등록되고 Health Check를 통과하면 ELB가 이 인스턴스에도 요청을 보낼 수 있다.

```text
ELB
├── EC2 A
├── EC2 B
└── EC2 C
```

즉 서버 수가 늘어나는 것만으로 끝나는 것이 아니라, 새 서버가 실제 트래픽 분산 대상에 참여해야 한다.

---

## 2. Health Check와 ASG

ELB는 Target Group의 Health Check를 통해 각 Target이 요청을 처리할 수 있는지 확인한다.

```text
ELB
→ /health 요청
→ 200 OK
→ healthy
```

반대로 애플리케이션이 죽었거나 Health Check가 실패하면 Target은 unhealthy 상태가 될 수 있다.

```text
EC2 실행 중
하지만 애플리케이션 중지
→ ELB Health Check 실패
→ unhealthy
```

ASG와 ELB를 함께 사용하면 이런 상태 정보를 바탕으로 비정상 인스턴스를 교체하는 구조를 만들 수 있다.

개념적으로:

```text
인스턴스 비정상
→ ELB가 요청 대상에서 제외
→ ASG가 원하는 수량 유지
→ 필요하면 새 인스턴스 생성
```

이 때문에 ELB + ASG 조합은 고가용성 아키텍처에서 매우 자주 등장한다.

---

## 3. ASG만 있으면 충분하지 않은 이유

ASG는 서버 수를 유지할 수 있지만 사용자가 어느 서버로 접속해야 하는지를 해결하지는 않는다.

예를 들어 ASG가 EC2를 새로 만들면 새 인스턴스의 주소가 생긴다.

사용자가 매번 새 주소를 알아서 찾아갈 수는 없다.

ELB를 앞에 두면 사용자는 고정된 Load Balancer endpoint만 바라보면 된다.

```text
User
→ ELB DNS Name
→ 현재 healthy EC2들
```

뒤에서 EC2가 추가되거나 제거되어도 사용자의 접속 지점은 ELB로 유지된다.

---

## 4. ELB만 있으면 충분하지 않은 이유

반대로 ELB만 있다고 서버 수가 자동으로 늘어나는 것은 아니다.

```text
ELB
├── EC2 A
└── EC2 B
```

트래픽이 10배 증가해도 EC2가 그대로 2대라면 두 서버가 과부하될 수 있다.

ASG를 연결하면 부하에 따라 인스턴스를 늘릴 수 있다.

```text
ELB
  ↓
ASG
2대 → 5대
```

따라서 둘의 역할은 다르지만 서로 보완적이다.

---

## 5. Multi-AZ와 함께 보기

고가용성 구조에서는 여러 Availability Zone에 Target을 분산한다.

```text
             ELB
          /       \
       AZ-A       AZ-B
       EC2         EC2
       EC2         EC2
```

ASG가 여러 AZ에 걸쳐 인스턴스를 유지하고 ELB가 healthy Target으로 요청을 분산하면 한 인스턴스나 한 AZ에 문제가 생겼을 때 영향을 줄일 수 있다.

---

## 6. 시험에서 자주 연결되는 흐름

```text
트래픽 증가
→ CloudWatch metric 상승
→ ASG Scale Out
→ 새 EC2 생성
→ Target Group 등록
→ Health Check 통과
→ ELB가 새 EC2에도 트래픽 분산
```

반대로:

```text
EC2/애플리케이션 장애
→ Health Check 실패
→ ELB가 해당 Target으로 요청 중단
→ ASG가 capacity 유지
→ 새 EC2로 교체 가능
```

이 전체 흐름을 하나의 그림으로 이해하면 된다.

---

## SAA 판단

```text
요청 분산
→ ELB

EC2 수량 자동 조절
→ ASG

새 인스턴스가 실제 요청을 받게 함
→ Target Group + Health Check

장애 난 인스턴스로 요청 중지
→ ELB Health Check

필요한 인스턴스 수 유지
→ ASG

고가용성 + 자동 확장
→ Multi-AZ + ELB + ASG
```
