# u1. AWS Organizations / OU / Consolidated Billing

AWS Organizations는 여러 AWS Account를 중앙에서 관리하는 **global service**다.

## 구조

```text
Organization Root
├─ Management Account
├─ OU Dev
│   ├─ Dev Account A
│   └─ Dev Account B
└─ OU Prod
    ├─ Prod Account A
    └─ Prod Account B
```

강의 핵심:

```text
Management Account
→ Organization을 관리

Member Account
→ 하나의 Organization에만 소속 가능

OU
→ Account를 논리적으로 묶음
```

## Consolidated Billing

여러 Account의 비용을 하나의 payment method로 처리한다.

강의에서는 aggregated usage에 따른 volume discount와 Reserved Instances / Savings Plans discount sharing을 장점으로 설명한다.

## 운영 장점

```text
multi-account 분리
central billing
central CloudTrail
central CloudWatch Logs
cross-account admin role
tagging standard
```

## 기억할 문장

> AWS Organizations는 여러 Account를 OU 구조로 묶고 billing과 governance를 중앙화하는 서비스다.
