# 67. RPO / RTO

재해복구 전략을 선택하기 전에 먼저 **RPO와 RTO**를 구분해야 한다.

## Units

- [ ] [u1. RPO](./u1_rpo/README.md)
- [ ] [u2. RTO](./u2_rto/README.md)
- [ ] [u3. RPO / RTO와 DR 전략 선택](./u3_strategy_selection/README.md)

## 핵심 정의

```text
RPO = Recovery Point Objective
→ 재해 발생 시 허용 가능한 데이터 손실 범위

RTO = Recovery Time Objective
→ 재해 발생 후 서비스 복구까지 허용 가능한 다운타임
```

## 시간축으로 보기

```text
마지막 복구 가능 시점 ---- 재해 발생 ---- 서비스 복구
         |<-- RPO -->|<------ RTO ------>|

RPO
→ 얼마나 과거 시점까지 데이터가 되돌아가도 되는가?

RTO
→ 얼마나 오래 서비스가 멈춰 있어도 되는가?
```

## DR 전략과의 관계

강의는 DR 전략을 다음 순서로 비교한다.

```text
Backup & Restore
→ Pilot Light
→ Warm Standby
→ Multi-Site / Hot Site

오른쪽으로 갈수록 일반적으로 RTO가 더 짧아짐
대신 비용과 상시 운영 자원이 증가
```
