# 11부 — Monitoring, Advanced Identity & Security

> ✅ Deep 학습 완료 — CloudWatch / CloudTrail / KMS / Systems Manager  
> 📚 Coverage 문서 작성 완료 — AWS Config / Advanced Identity / Secrets / Network Security / Security Services

이 파트는 SAA 강의의 Monitoring / Advanced Identity / Security 영역을 정리한다.

## Chapters

### Deep

- [x] [50. CloudWatch](./50_cloudwatch/README.md)
- [x] [51. CloudTrail](./51_cloudtrail/README.md)
- [x] [54. KMS](./54_kms/README.md)
- [x] [56. Systems Manager](./56_systems_manager/README.md)

### Coverage

- [ ] [52. AWS Config](./52_aws_config/README.md)
- [ ] [53. Advanced Identity](./53_advanced_identity/README.md)
- [ ] [55. Secrets Manager / Parameter Store](./55_secrets_parameter_store/README.md)
- [ ] [57. WAF / Shield / Firewall Manager](./57_waf_shield_firewall_manager/README.md)
- [ ] [58. GuardDuty / Inspector / Macie 등 Security Services](./58_guardduty_inspector_macie/README.md)

## 전체 지도

```text
CloudWatch
→ 현재 시스템이 어떤 상태인가?
→ Metric / Log / Alarm

CloudTrail
→ 누가 AWS 설정을 바꿨는가?
→ API 호출 / Audit

AWS Config
→ 설정이 어떻게 바뀌었고 정책을 준수하는가?
→ Configuration Timeline / Compliance

Advanced Identity
→ 여러 Account와 권한 상한을 어떻게 관리하는가?
→ Organizations / SCP / Identity Center / Permission Boundary

KMS
→ 어떤 키로 암호화하고 누가 그 키를 사용하는가?

Secrets Manager / Parameter Store
→ secret과 configuration을 어디에 저장하는가?

Systems Manager
→ SSH 없이 EC2를 어떻게 운영하는가?

WAF / Shield / Firewall Manager
→ Web 공격 / DDoS / 조직 단위 보안 정책

GuardDuty / Inspector / Macie
→ Threat / Vulnerability / Sensitive Data 탐지
```

## 실습 연결

```text
CloudWatch
  → examples/08 ASG Scaling
  → examples/14 Observability
  → examples/15 Troubleshooting
  → examples/16 Final Architecture

CloudTrail
  → examples/15 설정 변경 원인 추적
  → examples/16 SG/IAM/EC2 변경 이력 확인

AWS Config
  → 설정 변경 timeline
  → compliance / auto-remediation 개념

KMS
  → examples/11 IAM Role + S3
  → examples/12 S3 Security / Encryption
  → examples/15 S3 권한과 KMS 권한 장애 구분
  → examples/16 보안 설계 근거

Secrets Manager / Parameter Store
  → application config / DB credential 설계

Systems Manager / Session Manager
  → examples/06 Private EC2 Access
  → private subnet의 EC2 운영 접근

WAF / Shield
  → ALB / CloudFront / API Gateway 보호 구조

GuardDuty / Inspector / Macie
  → 운영 보안 탐지 서비스 선택
```

## 시험에서 특히 중요한 비교

```text
CloudWatch vs CloudTrail vs Config
→ 상태 vs 행위 vs 설정/Compliance

IAM Policy vs Permission Boundary vs SCP
→ 권한 부여 vs 개별 User/Role 상한 vs Account/OU 상한

Parameter Store vs Secrets Manager
→ configuration 중심 vs rotation 중심 secret

WAF vs Shield vs Firewall Manager
→ HTTP filtering vs DDoS vs 중앙 정책 관리

GuardDuty vs Inspector vs Macie
→ Threat Detection vs Vulnerability vs Sensitive Data
```

## 학습 우선순위

```text
Deep 완료
50 CloudWatch
51 CloudTrail
54 KMS
56 Systems Manager

이제 Coverage 진행
52 AWS Config
53 Advanced Identity
55 Secrets Manager / Parameter Store
57 WAF / Shield / Firewall Manager
58 GuardDuty / Inspector / Macie
```

Coverage 챕터는 모든 세부 기능을 외우기보다 **무슨 문제를 해결하는 서비스인지, 무엇과 헷갈리는지, 어떤 키워드에서 선택하는지**를 설명할 수 있으면 우선 충분하다.
