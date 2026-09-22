# u1. Multi-Site / Hot Site Architecture

강의의 Hot Site 예시는 on-premises와 AWS 양쪽에 **full production scale**을 유지한다.

```text
Corporate Data Center
├─ Application Servers
└─ Primary DB
        ↕ data replication
AWS Cloud
├─ ELB
├─ EC2 Auto Scaling (production)
└─ RDS Secondary (running)
```

Route 53 등을 이용해 failover할 수 있다.

## 왜 빠른가?

재해 후 infrastructure를 새로 복원하거나 scale-up할 필요가 거의 없기 때문이다.

```text
이미 production capacity 존재
→ traffic 전환 중심
→ 매우 낮은 RTO
```
