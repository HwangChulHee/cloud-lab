# u5. Sticky Sessions & Cross-Zone Load Balancing

## 1. Sticky Sessions

Sticky Session(Session Affinity)은 같은 클라이언트의 요청을 같은 Target으로 계속 보내는 기능이다.

```text
Client A → Target 1
Client A → Target 1
Client A → Target 1
```

세션 정보를 인스턴스 로컬에 저장하는 애플리케이션에서 사용자가 다른 서버로 이동하면서 세션을 잃는 문제를 줄일 수 있다.

하지만 특정 Target으로 요청이 몰려 부하가 불균형해질 수 있다.

강의에서는 CLB, ALB, NLB에서 stickiness를 사용할 수 있다고 설명한다. ALB/CLB의 경우 cookie 기반 설정이 중요하다.

---

## 2. Cookie 유형

강의에서 구분하는 주요 형태는 다음과 같다.

```text
Application-based cookie
Duration-based cookie
```

애플리케이션 기반 쿠키는 애플리케이션 또는 Load Balancer와 연결해 사용할 수 있고, Duration-based cookie는 Load Balancer가 생성해 일정 시간 동안 affinity를 유지한다.

시험에서는 세부 쿠키 이름보다 **stickiness = 같은 사용자를 같은 backend로 보내는 기능**이라는 의미를 먼저 잡는다.

---

## 3. Cross-Zone Load Balancing

여러 Availability Zone에 Target 수가 다르면 Zone별로만 분산할 경우 Target당 부하가 달라질 수 있다.

Cross-Zone Load Balancing을 사용하면 Load Balancer node가 다른 AZ의 Target까지 포함해 전체 Target에 트래픽을 분산할 수 있다.

```text
AZ-A LB node ─┬→ AZ-A Targets
              └→ AZ-B Targets

AZ-B LB node ─┬→ AZ-A Targets
              └→ AZ-B Targets
```

---

## 4. 강의 기준 기본 동작

강의의 구분은 다음과 같다.

```text
ALB
→ Cross-Zone 기본 활성화

NLB / GWLB
→ 기본 비활성화
```

ALB는 Target Group 수준에서 설정을 조정할 수 있다.

---

## SAA 판단

```text
같은 사용자를 같은 backend로 보내야 함
→ Sticky Session

Sticky Session 사용 후 backend 부하가 치우침
→ 가능한 부작용

AZ마다 Target 수가 다르지만 전체 Target에 균등 분배 필요
→ Cross-Zone Load Balancing
```
