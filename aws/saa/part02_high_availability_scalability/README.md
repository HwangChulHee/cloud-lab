# 02부 — High Availability & Scalability

Elastic Load Balancing과 Auto Scaling을 중심으로 고가용성과 확장성의 기본 패턴을 정리한다.

## Chapters

- [x] [08. Elastic Load Balancing](./08_elb/README.md)
- [x] [09. Auto Scaling](./09_auto_scaling/README.md)

## 전체 흐름

```text
Client
  ↓
Load Balancer
  ↓
Auto Scaling Group
├─ EC2
├─ EC2
└─ EC2
```

## 핵심 구분

```text
ELB
→ 여러 Target으로 traffic 분산
→ Health Check

ASG
→ desired capacity 유지
→ traffic/metric에 따라 scale out / scale in
```

다음 파트의 RDS / Aurora / ElastiCache로 이어진다.
