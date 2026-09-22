# u4. WAF vs Shield vs Firewall Manager

## WAF

```text
HTTP request 내용 검사
SQLi / XSS / IP / Geo / Rate limit
Layer 7
```

## Shield

```text
DDoS protection
Layer 3/4 중심
Advanced는 추가 대응/지원
```

## Firewall Manager

```text
Organizations 전체에 보안 정책 중앙 적용
WAF / Shield / SG / Network Firewall 관리
```

## 선택 기준

```text
ALB/API Gateway/CloudFront에 HTTP 공격 차단
→ WAF

DDoS 방어
→ Shield

여러 AWS Account에 WAF 규칙을 동일 적용
→ Firewall Manager + WAF

새 Account/Resource에도 보안 정책 자동 적용
→ Firewall Manager
```

## 기억할 문장

> WAF는 요청 필터링, Shield는 DDoS 방어, Firewall Manager는 조직 전체 중앙 관리다.
