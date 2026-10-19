# u2. Caching / Offloading / Scaling

비용 최적화는 compute 가격만 낮추는 것이 아니다.

## CloudFront Offloading

강의의 software update 예시:

```text
Users
 ↓
CloudFront
 ↓ cache miss only
Existing EC2 / EFS Application
```

static file을 edge에 cache하면 origin EC2/network 부하와 ASG scaling을 줄일 수 있다.

## Auto Scaling

```text
필요한 때만 capacity 증가
traffic 감소 시 capacity 축소
```

항상 peak capacity를 유지하는 것보다 효율적이다.

## Database Cache

```text
Application
→ ElastiCache
→ cache miss만 RDS
```

반복 query가 database까지 도달하는 횟수를 줄여 resource pressure를 낮춘다.

## 기억할 문장

> 비용 최적화는 cache와 managed scaling을 사용해 불필요한 origin/compute 작업 자체를 줄이는 것이 중요하다.
