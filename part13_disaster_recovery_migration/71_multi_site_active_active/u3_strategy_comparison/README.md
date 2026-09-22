# u3. DR Strategy 최종 비교

강의의 네 가지 DR 전략을 한 번에 정리한다.

| 전략 | 평상시 DR 환경 | 복구 속도 감각 | 비용 감각 |
|---|---|---|---|
| Backup & Restore | backup 중심 | 가장 느림 | 가장 낮음 |
| Pilot Light | critical core 실행 | 더 빠름 | 낮음~중간 |
| Warm Standby | 전체 stack 최소 크기 실행 | 빠름 | 중간~높음 |
| Multi-Site / Hot Site | production scale 실행 | 가장 빠름 | 가장 높음 |

## 선택 순서

```text
1. RPO 요구사항 확인
2. RTO 요구사항 확인
3. 허용 비용 확인
4. standby infrastructure 수준 결정
```

## 기억할 문장

> 더 짧은 RTO를 원할수록 더 많은 infrastructure를 평상시부터 실행해 두어야 한다.
