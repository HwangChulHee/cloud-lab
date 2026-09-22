# 58. GuardDuty / Inspector / Macie 등 Security Services

이 단원은 AWS의 managed security services를 **무엇을 검사하는가** 기준으로 구분한다.

## Units

- [ ] [u1. Amazon GuardDuty](./u1_guardduty/README.md)
- [ ] [u2. Amazon Inspector](./u2_inspector/README.md)
- [ ] [u3. Amazon Macie](./u3_macie/README.md)
- [ ] [u4. Security Services 선택 지도](./u4_security_selection/README.md)

## 핵심 구분

```text
GuardDuty
→ account / network / activity 기반 threat detection

Inspector
→ EC2 / ECR / Lambda의 vulnerability assessment

Macie
→ S3의 sensitive data / PII discovery
```

## 한 줄 기억

> 위협 행동을 찾으면 GuardDuty, 소프트웨어 취약점을 찾으면 Inspector, S3의 민감정보를 찾으면 Macie다.
