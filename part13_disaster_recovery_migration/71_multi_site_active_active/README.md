# 71. Multi-Site / Active-Active

Multi-Site 또는 Hot Site 전략은 **여러 환경이 production scale로 이미 실행 중인 가장 빠른 DR 전략**이다.

강의에서는 매우 낮은 RTO를 제공하지만 매우 비싸다고 설명한다.

## Units

- [ ] [u1. Multi-Site / Hot Site Architecture](./u1_architecture/README.md)
- [ ] [u2. AWS Multi-Region](./u2_aws_multiregion/README.md)
- [ ] [u3. DR Strategy 최종 비교](./u3_strategy_comparison/README.md)

## 기본 구조

```text
Site A / Region A
Production Scale
      ↕ data replication
Site B / Region B
Production Scale

Route 53
→ traffic failover / active-active
```

## 강의 핵심

```text
Very low RTO
→ minutes or seconds

Full production scale
→ already running

Cost
→ very high
```
