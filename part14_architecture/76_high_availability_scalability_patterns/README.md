# 76. High Availability / Scalability Patterns

이 단원은 앞에서 배운 개별 서비스들을 **가용성, 확장성, 성능** 요구로 다시 묶는다.

## Units

- [ ] [u1. Multi-AZ / Health Check / Replacement](./u1_multi_az_health_replacement/README.md)
- [ ] [u2. Horizontal Scaling / Decoupling](./u2_horizontal_scaling_decoupling/README.md)
- [ ] [u3. Read Scaling / Caching](./u3_read_scaling_caching/README.md)
- [ ] [u4. Static Content Offloading](./u4_static_content_offloading/README.md)

## 판단 지도

```text
instance 장애 대응
→ ELB Health Check + ASG Replacement

AZ 장애 대응
→ Multi-AZ

traffic 증가
→ horizontal scaling

DB read 부하
→ Read Replica / Cache

static content 대량 전송
→ CloudFront

component 간 spike 완충
→ SQS 등 asynchronous decoupling
```
