# u2. RTO — Recovery Time Objective

RTO는 **재해 발생 후 서비스를 얼마 만에 다시 살려야 하는가**를 나타낸다.

예:

```text
RTO = 8시간
→ 재해 후 8시간 안에 서비스 복구

RTO = 1분
→ 거의 즉시 전환 가능한 구조 필요
```

## DR 전략과 연결

강의 흐름상:

```text
Backup & Restore
→ 복구 시 resource를 새로 만들어야 함
→ RTO가 큼

Pilot Light
→ 핵심 system 일부가 이미 실행 중
→ 더 빠름

Warm Standby
→ 전체 system이 작은 크기로 실행 중
→ 더 빠름

Multi-Site / Hot Site
→ production scale이 이미 실행 중
→ 매우 낮은 RTO
```

## 기억할 문장

> RTO는 "서비스가 얼마나 오래 멈춰 있어도 되는가"다.
