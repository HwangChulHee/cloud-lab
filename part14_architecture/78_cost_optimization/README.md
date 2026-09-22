# 78. 비용 최적화 개념

비용 최적화는 단순히 가장 싼 서비스를 고르는 것이 아니라 **workload 성격에 맞는 구매 옵션, scaling, caching, storage tier, 운영 시간**을 조합하는 문제다.

## Units

- [ ] [u1. EC2 Purchasing Options](./u1_ec2_purchasing_options/README.md)
- [ ] [u2. Caching / Offloading / Scaling](./u2_caching_offloading_scaling/README.md)
- [ ] [u3. Storage Lifecycle / Data Transfer](./u3_storage_lifecycle_transfer/README.md)
- [ ] [u4. Idle Resource / Cost Visibility](./u4_idle_resource_cost_visibility/README.md)

## 핵심 질문

```text
항상 필요한가?
중단 가능 workload인가?
traffic이 변하는가?
static content를 origin이 반복 전송하고 있는가?
data access 빈도가 낮아지는가?
사용하지 않는 시간에도 resource가 켜져 있는가?
```
