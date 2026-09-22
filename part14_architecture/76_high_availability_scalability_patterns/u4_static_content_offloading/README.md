# u4. Static Content Offloading

강의에서는 EC2 application이 software update file을 대량 배포하면서 CPU와 network 비용이 커지는 상황을 예로 든다.

기존 architecture를 크게 바꾸지 않고 CloudFront를 앞에 둔다.

```text
Users
  ↓
CloudFront
  ↓ cache miss
Existing Application / File Origin
```

## 효과

```text
static file을 edge에 cache
→ origin request 감소
→ EC2 scaling 감소
→ network bandwidth 부담 감소
→ global delivery 개선
```

강의는 CloudFront가 serverless하게 scale하므로 기존 EC2 ASG의 부하와 비용을 줄이는 방법으로 설명한다.

## 기억할 문장

> 변하지 않는 대용량 콘텐츠를 application server가 반복 전송하게 하지 말고 CloudFront로 offload한다.
