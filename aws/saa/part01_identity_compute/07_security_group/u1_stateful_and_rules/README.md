# u1. Security Group — Stateful과 Rule 모델

## 지도 확인

EC2에서 Security Group의 기본 사용법은 이미 확인했다.
이번 유닛에서는 Security Group이 실제로 어떤 기준으로 트래픽을 허용하는지 조금 더 구조적으로 정리한다.

```text
Client
  ↓
Security Group
  ↓
EC2 / ENI
```

강의에서 강조하는 핵심은 Security Group이 EC2 네트워크 보안의 기본 요소이며, inbound/outbound 트래픽을 **허용 규칙**으로 제어한다는 점이다.

---

## 1. Security Group은 허용 규칙으로 동작한다

Security Group에는 허용할 트래픽을 정의한다.

```text
Inbound
→ 외부에서 리소스로 들어오는 트래픽

Outbound
→ 리소스에서 외부로 나가는 트래픽
```

규칙을 판단할 때는 주로 다음을 본다.

```text
Protocol
Port
Source / Destination
```

예:

```text
TCP 22  ← 내 IP/32
TCP 80  ← 0.0.0.0/0
TCP 443 ← 0.0.0.0/0
```

강의 기준 기본 동작은 다음과 같이 기억한다.

```text
Inbound
→ 기본적으로 허용 규칙이 없으면 차단

Outbound
→ 기본 Security Group 설정에서는 전체 허용
```

---

## 2. Security Group은 EC2 밖에서 트래픽을 필터링한다

강의에서 중요한 장애 판단 포인트다.

Security Group에서 트래픽이 차단되면 애플리케이션까지 요청이 도달하지 않는다.

따라서 일반적으로:

```text
timeout
→ 네트워크 경로 / Security Group 같은 계층 의심

connection refused
→ 서버까지 도달했지만 해당 port에서 process가 listen하지 않는 상황 등을 의심
```

라고 계층을 나눠 생각할 수 있다.

물론 실제 장애에서는 Route Table, NACL, OS firewall, process 상태 등도 함께 확인해야 한다.

---

## 3. Stateful

> 이 부분은 강의의 Security Group 설명을 이해하기 위한 AWS 동작 보강이다.

Security Group은 **stateful**하게 동작한다.

즉 허용된 연결로 들어온 요청에 대한 응답 트래픽은 별도의 반대 방향 규칙을 하나씩 작성하지 않아도 반환될 수 있다.

예를 들어:

```text
Client
  │ TCP 443
  ▼
EC2
```

EC2의 inbound에서 HTTPS 요청을 허용했다면, 그 요청에 대한 응답 트래픽은 연결 상태를 추적해 처리된다.

이 특성은 뒤의 VPC 파트에서 다룰 **NACL의 stateless 동작**과 비교할 때 중요하다.

지금은 다음만 기억하면 된다.

```text
Security Group
→ stateful

NACL
→ 나중에 비교
```

---

## 4. 하나의 Security Group을 여러 리소스에 연결할 수 있다

강의에서는 하나의 Security Group을 여러 인스턴스에 연결할 수 있다고 설명한다.

반대로 하나의 EC2 네트워크 인터페이스에 여러 Security Group을 연결해 허용 규칙을 조합할 수도 있다.

중요한 사고방식은:

```text
"서버 하나마다 방화벽 하나"
```

가 아니라,

```text
"역할이 같은 리소스에 공통 접근 정책을 적용"
```

이라고 이해하는 것이다.

---

## 5. Region / VPC 범위

강의에서는 Security Group이 Region/VPC 조합에 묶여 있다는 점을 강조한다.

따라서 다른 VPC에 있는 Security Group을 아무 곳에서나 그대로 가져다 붙이는 개념으로 생각하면 안 된다.

이후 VPC Peering, Transit Gateway 같은 네트워크 구성을 배울 때도 Security Group의 범위와 참조 가능 조건을 따로 확인해야 한다.

---

## SAA 연결

```text
EC2 접근 제어
→ Security Group

허용된 연결의 응답 트래픽
→ stateful 특성

요청이 timeout
→ SG / 네트워크 계층 확인

connection refused
→ application / process / listening port 확인

Inbound 기본
→ 허용 규칙 없으면 차단

기본 Outbound
→ 전체 허용
```

이번 유닛은 개념 구분이 핵심이므로 별도 유제는 생략한다.
