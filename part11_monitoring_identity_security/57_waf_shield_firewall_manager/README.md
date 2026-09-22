# 57. WAF / Shield / Firewall Manager

이 단원은 AWS의 **Web/DDoS/조직 단위 보안 정책**을 구분한다.

## Units

- [ ] [u1. AWS WAF](./u1_waf/README.md)
- [ ] [u2. AWS Shield / Shield Advanced](./u2_shield/README.md)
- [ ] [u3. AWS Firewall Manager](./u3_firewall_manager/README.md)
- [ ] [u4. WAF vs Shield vs Firewall Manager](./u4_comparison_selection/README.md)
- [ ] [u5. AWS Network Firewall](./u5_network_firewall/README.md)

## 핵심 구분

```text
WAF
→ Layer 7 HTTP request filtering

Shield
→ DDoS protection

Firewall Manager
→ 여러 AWS Account에 보안 정책 중앙 적용

Network Firewall
→ VPC 전체 트래픽 L3~L7 검사
```
