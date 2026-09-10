# u2. Security Group Reference

## 지도 확인

Security Group의 Source/Destination에는 IP 주소뿐 아니라 **다른 Security Group**을 참조할 수 있다.

이 기능은 서버 IP를 일일이 관리하기보다 **역할 단위로 접근 관계를 표현**할 때 중요하다.

```text
Internet
   ↓
ALB SG
   ↓
APP SG
   ↓
DB SG
```

---

## 1. IP 기반 규칙

가장 단순한 방식은 IP/CIDR을 Source로 지정하는 것이다.

예:

```text
SSH 22
Source: 203.0.113.10/32
```

이 방식은 특정 관리자 IP처럼 대상이 명확할 때 유용하다.

하지만 Auto Scaling처럼 인스턴스가 계속 늘고 줄거나 IP가 바뀌는 환경에서는 서버 IP 목록을 직접 관리하기 불편하다.

---

## 2. Security Group을 Source로 참조

강의에서는 Security Group rule이 IP뿐 아니라 다른 Security Group을 참조할 수 있다고 설명한다.

예를 들어 Application EC2가 ALB에서 오는 HTTP 요청만 받아야 한다면:

```text
ALB
Security Group: sg-alb
        │
        │ TCP 8080
        ▼
Application
Security Group: sg-app
```

`sg-app`의 inbound를 다음처럼 설계할 수 있다.

```text
TCP 8080
Source: sg-alb
```

의미는:

> 특정 IP에서 오는 모든 트래픽을 허용하는 것이 아니라, `sg-alb`가 연결된 리소스에서 오는 해당 트래픽을 허용한다.

이다.

---

## 3. Security Group Reference의 장점

IP 기반 접근:

```text
10.0.1.10
10.0.1.11
10.0.1.12
...
```

역할 기반 접근:

```text
ALB SG
→ APP SG
```

Auto Scaling으로 Application 인스턴스가 교체되어도 각 인스턴스의 IP를 규칙에 다시 넣을 필요가 없다.

그래서 다음처럼 생각하면 편하다.

```text
IP Reference
→ "이 주소를 허용"

Security Group Reference
→ "이 역할을 가진 리소스를 허용"
```

---

## 4. 같은 Security Group을 참조하는 경우

같은 Security Group에 속한 리소스끼리 통신해야 하는 경우에도 SG 자체를 Source로 참조하는 패턴이 있다.

중요한 점은 **같은 Security Group을 붙였다는 사실만으로 서로의 모든 통신이 자동 허용되는 것은 아니라는 것**이다.

필요한 Protocol/Port에 대한 rule이 있어야 한다.

---

## 5. SAA에서 보는 패턴

다음 구조가 나오면 Security Group Reference를 먼저 떠올린다.

```text
Internet
   ↓
Load Balancer
   ↓
Application EC2
```

요구사항:

```text
Application은 인터넷에서 직접 접근되면 안 됨
Load Balancer를 통한 요청만 허용
```

설계:

```text
ALB SG
Inbound 80/443 ← Internet

APP SG
Inbound Application Port ← ALB SG
```

IP 대역을 직접 박는 것보다 구조가 명확하고 인스턴스 교체에도 대응하기 쉽다.

---

## SAA 연결

```text
고정 관리자 IP 허용
→ IP /32

ALB에서 오는 요청만 Application에 허용
→ ALB Security Group Reference

Auto Scaling으로 IP가 자주 바뀜
→ 개별 IP보다 SG Reference가 자연스러움

같은 SG를 연결한 인스턴스끼리 통신
→ 필요한 rule 없이는 자동 허용 아님
```

이번 유닛은 선택 패턴이 핵심이므로 별도 유제는 생략한다.
