# 70. Warm Standby

Warm Standby는 **전체 application stack이 항상 실행 중이지만 minimum size로 유지**되는 DR 전략이다.

강의에서는 disaster 발생 시 production load를 감당할 수 있도록 scale-up한다고 설명한다.

## Units

- [ ] [u1. Warm Standby Architecture](./u1_architecture/README.md)
- [ ] [u2. Failover / Scale-Up](./u2_failover_scaleup/README.md)
- [ ] [u3. Pilot Light와 비교](./u3_comparison_selection/README.md)

## 기본 구조

```text
Primary Environment
      ↓ data replication
AWS DR Environment
├─ RDS Secondary (running)
├─ ELB
├─ EC2 Auto Scaling (minimum)
└─ Route 53
```

## 핵심

```text
전체 system
→ 이미 실행 중

capacity
→ minimum size

재해 발생
→ production size로 scale-out
→ traffic failover
```
