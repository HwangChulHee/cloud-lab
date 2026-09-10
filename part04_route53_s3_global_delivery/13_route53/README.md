# 13. Amazon Route 53

Route 53는 AWS의 관리형 DNS 서비스다.

이번 단원에서는 단순히 "도메인을 IP로 바꿔준다" 수준을 넘어, DNS 레코드와 Hosted Zone이 무엇인지, 여러 Routing Policy가 어떤 상황에서 필요한지, Health Check와 Failover가 어떻게 연결되는지까지 이해한다.

## Units

- [x] u1. DNS와 Route 53 기본
- [x] u2. DNS Record Types와 TTL
- [x] u3. Hosted Zone, Registrar, Alias
- [x] u4. Simple / Weighted / Latency Routing
- [x] u5. Failover / Geolocation / Geoproximity Routing
- [x] u6. Multi-Value Routing
- [x] u7. Health Checks와 DNS Failover

## SAA 선택 지도

```text
일반적인 단일 응답
→ Simple

트래픽을 비율로 나누기
→ Weighted

사용자에게 가장 낮은 latency의 Region
→ Latency-based

Primary 장애 시 Secondary
→ Failover

사용자의 국가/대륙 기준
→ Geolocation

리소스 위치 + bias로 교통량 조절
→ Geoproximity

여러 healthy IP를 DNS 응답으로 반환
→ Multi-Value

AWS 리소스를 zone apex에서 가리키기
→ Alias
```

Route 53에서 가장 중요한 것은 정책 이름을 외우는 것보다, **문제의 요구사항을 보고 어떤 Routing Policy를 골라야 하는지 판단하는 것**이다.
