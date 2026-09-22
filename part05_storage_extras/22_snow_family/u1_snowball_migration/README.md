# u1. Snowball Data Migration

Snowball은 secure portable device에 데이터를 복사한 뒤 장비 자체를 AWS로 보내는 방식이다.

## 왜 필요한가?

강의에서 제시하는 문제:

```text
limited connectivity
limited bandwidth
high network cost
shared bandwidth
connection stability
```

대량 data를 인터넷으로 전송하면 너무 오래 걸릴 수 있다.

강의 예시:

```text
100 TB
100 Mbps
→ 124 days

100 TB
1 Gbps
→ 12 days

100 TB
10 Gbps
→ 30 hours
```

## Offline Migration

```text
Client
  ↓ local high-speed copy
Snowball
  ↓ ship
AWS
  ↓ import
S3
```

## SAA 판단

```text
network transfer > 1 week
→ Snowball 고려

PB-scale migration
→ Snowball

온라인 transfer가 충분히 빠르고 안정적
→ DataSync / direct transfer 등 우선 검토
```
