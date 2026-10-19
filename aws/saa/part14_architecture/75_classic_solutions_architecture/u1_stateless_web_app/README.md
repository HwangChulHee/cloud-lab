# u1. Stateless Web App

강의의 Stateless Web App 예시는 단일 EC2에서 시작해 **Load Balancer → Auto Scaling → Multi-AZ**로 확장한다.

```text
Route 53 Alias
      ↓
ELB + Health Checks
      ↓
Auto Scaling Group
├─ EC2 in AZ-A
├─ EC2 in AZ-B
└─ EC2 in AZ-C
```

## 왜 Stateless가 중요한가?

요청 처리 상태가 특정 EC2 하나에 묶이지 않으면 어느 instance로 요청이 가도 처리할 수 있다.

```text
instance failure
→ ELB health check 실패
→ ASG replacement
→ 다른 healthy instance가 요청 처리
```

## 비용 연결

강의에서는 minimum capacity처럼 항상 필요한 baseline capacity는 Reserved Instance 등 장기 할인 옵션과 연결할 수 있다고 설명한다.

## 기억할 문장

> Stateless web tier는 ELB와 ASG가 instance를 자유롭게 교체하고 scale할 수 있게 만든다.
