# u4. Security Services 선택 지도

11부의 security monitoring 서비스를 요구사항 기준으로 구분한다.

## GuardDuty

```text
누군가 이상한 API call을 하는가?
수상한 network traffic이 있는가?
DNS 기반 이상 행동이 있는가?
→ GuardDuty
```

## Inspector

```text
EC2 OS/package에 CVE가 있는가?
ECR image dependency가 취약한가?
Lambda package가 취약한가?
→ Inspector
```

## Macie

```text
S3 안에 PII / sensitive data가 있는가?
→ Macie
```

## AWS Config

```text
Resource configuration이 policy를 준수하는가?
→ Config
```

## WAF / Shield

```text
악성 HTTP request를 차단
→ WAF

DDoS 방어
→ Shield
```

## 최종 비교

| 질문 | 서비스 |
|---|---|
| 수상한 AWS account/network activity? | GuardDuty |
| EC2/ECR/Lambda vulnerability? | Inspector |
| S3 sensitive data / PII? | Macie |
| resource configuration compliance? | AWS Config |
| Layer 7 web request filtering? | WAF |
| DDoS protection? | Shield |

## 기억할 문장

> GuardDuty는 위협 탐지, Inspector는 취약점 탐지, Macie는 민감 데이터 탐지다.
