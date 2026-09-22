# u3. RPO / RTO와 DR 전략 선택

DR 전략은 단순히 가장 빠른 것을 고르는 문제가 아니다.

## Trade-off

```text
낮은 RPO / 낮은 RTO
→ replication / standby infrastructure 증가
→ 비용 증가

높은 RPO / 높은 RTO 허용
→ backup 중심 구조 가능
→ 비용 감소
```

## 강의 전략 비교

```text
Backup & Restore
→ 높은 RPO / 높은 RTO 쪽
→ 가장 단순하고 저렴

Pilot Light
→ 핵심 core만 항상 실행
→ Backup & Restore보다 빠름

Warm Standby
→ 전체 system이 minimum size로 실행
→ scale-up만 하면 됨

Multi-Site / Hot Site
→ full production scale
→ 매우 낮은 RTO
→ 매우 비쌈
```

## 시험 접근

문제에서 먼저 찾는다.

```text
허용 가능한 data loss는?
→ RPO

허용 가능한 downtime은?
→ RTO

비용 제한은?
→ 어느 DR tier까지 유지 가능한가?
```
