# 69. Pilot Light

Pilot Light는 **애플리케이션의 critical core만 cloud에서 항상 작게 실행**해 두는 DR 전략이다.

강의에서는 Backup & Restore와 매우 비슷하지만, 핵심 시스템이 이미 살아 있기 때문에 더 빠르게 복구할 수 있다고 설명한다.

## Units

- [ ] [u1. Pilot Light Architecture](./u1_architecture/README.md)
- [ ] [u2. Failover Flow](./u2_failover_flow/README.md)
- [ ] [u3. Backup & Restore와 비교](./u3_comparison_selection/README.md)

## 기본 구조

```text
Corporate Data Center
      ↓ data replication
AWS Cloud
├─ RDS (running)
├─ EC2 (not running)
└─ Route 53
```

## 핵심

```text
critical core
→ 항상 실행

나머지 application capacity
→ 재해 시 시작/확장
```

## 기억할 문장

> Pilot Light는 불씨처럼 핵심 구성만 계속 켜두고 재해 시 나머지 환경을 빠르게 복구하는 전략이다.
