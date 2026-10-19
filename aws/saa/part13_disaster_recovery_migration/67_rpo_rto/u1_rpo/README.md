# u1. RPO — Recovery Point Objective

RPO는 **재해로 인해 얼마만큼의 데이터 손실을 허용할 수 있는가**를 나타낸다.

예를 들어:

```text
매 6시간마다 backup
재해가 backup 직전이 아니라 중간에 발생
→ 최대 수 시간의 data loss 가능
```

즉 backup/replication 주기가 RPO와 직접 연결된다.

## 감각적으로

```text
RPO 24시간
→ 하루치 data loss까지 허용 가능

RPO 5분
→ 거의 실시간에 가까운 replication 필요
```

## DR 설계와 연결

RPO를 줄이려면 보통:

```text
더 잦은 backup
continuous replication
cross-region replication
```

같은 전략이 필요하다.

## 기억할 문장

> RPO는 "얼마나 많은 과거 데이터 손실을 감수할 수 있는가"다.
