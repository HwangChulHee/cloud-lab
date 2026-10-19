# u1. AWS WAF

AWS WAF는 **Layer 7 HTTP 요청을 검사해 일반적인 web exploit을 막는 Web Application Firewall**이다.

## 적용 대상

강의에서는 다음을 언급한다.

```text
Application Load Balancer
API Gateway
CloudFront
AppSync GraphQL API
Cognito User Pool
```

## Web ACL Rule

```text
IP Set
HTTP header
HTTP body
URI string
size constraint
geo-match
rate-based rule
```

대표 공격:

```text
SQL Injection
Cross-Site Scripting (XSS)
```

## 중요한 제한

```text
WAF
→ Layer 7
→ NLB에는 직접 적용하지 않음
```

ALB와 사용할 때 Web ACL은 ALB와 같은 Region에 있어야 한다.

## 기억할 문장

> HTTP 요청 내용 자체를 기준으로 차단해야 하면 WAF다.
