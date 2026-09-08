# u3. Network Load Balancer (NLB)

## 지도 확인

Network Load Balancer는 Layer 4 수준에서 TCP/UDP/TLS 트래픽을 처리한다.

```text
Client
  ↓ TCP / UDP / TLS
NLB
  ↓
Target Group
  ↓
EC2 / IP / ALB
```

---

## 1. Layer 4 Load Balancer

NLB는 HTTP의 Path나 Host를 해석해서 라우팅하는 것이 핵심이 아니다.

대신 다음 요구에 적합하다.

```text
매우 높은 처리량
낮은 지연시간
TCP/UDP 트래픽
고정 IP 요구
```

---

## 2. Target Group

강의 기준으로 NLB Target Group에는 다음과 같은 대상을 둘 수 있다.

```text
EC2 Instances
Private IP Addresses
Application Load Balancer
```

Health Check는 TCP, HTTP, HTTPS를 사용할 수 있다.

---

## 3. Static IP

NLB는 각 Availability Zone마다 고정 IP를 가질 수 있고 Elastic IP를 연결할 수도 있다.

따라서 문제에서 다음과 같은 요구가 나오면 NLB를 떠올린다.

```text
고정 IP 필요
IP allowlist에 등록해야 함
DNS 이름이 아니라 예측 가능한 IP 필요
```

---

## 4. NLB + ALB

NLB Target으로 ALB를 둘 수 있다.

```text
Client
  ↓
NLB
  ↓
ALB
  ↓
Application
```

이렇게 하면 NLB의 네트워크 특성과 ALB의 Layer 7 라우팅을 함께 사용할 수 있다.

---

## SAA 판단

```text
HTTP path / host routing
→ ALB

TCP/UDP + 초고성능
→ NLB

고정 IP / Elastic IP 요구
→ NLB

Layer 4 특성 + Layer 7 routing을 같이 사용
→ NLB → ALB
```
