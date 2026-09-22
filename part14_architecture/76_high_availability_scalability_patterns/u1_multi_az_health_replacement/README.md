# u1. Multi-AZ / Health Check / Replacement

High Availability의 기본은 **하나의 instance/AZ에 의존하지 않는 것**이다.

```text
ALB
├─ AZ-A EC2
└─ AZ-B EC2
```

ALB Health Check가 unhealthy target을 traffic에서 제외하고, ASG가 필요한 capacity를 복구한다.

## 역할 구분

```text
ALB Health Check
→ traffic을 healthy target으로 보냄

Auto Scaling Group
→ desired capacity 유지 / instance 교체

Multi-AZ
→ AZ failure blast radius 감소
```

## DB와 연결

RDS Multi-AZ는 read scaling이 아니라 availability/failover 목적이다.
