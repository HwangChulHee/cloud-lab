# u1. Warm Standby Architecture

Warm Standby에서는 **application 전체가 DR 환경에 이미 존재하고 실행**된다.

```text
AWS DR Environment
├─ Load Balancer: Running
├─ App Servers: Running at minimum size
├─ Database Secondary: Running
└─ Data Replication: Active
```

Pilot Light와 달리 application tier도 이미 실행 중이라는 점이 중요하다.

## 평상시

```text
full architecture
+ reduced capacity
```

이 구조 때문에 Pilot Light보다 비용은 높지만 failover 시간이 더 짧아질 수 있다.
