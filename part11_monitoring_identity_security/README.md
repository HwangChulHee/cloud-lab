# 11부 — Monitoring, Advanced Identity & Security

이 파트는 SAA 강의의 Monitoring / Advanced Identity / Security 영역을 정리한다.

현재 `examples/` 실습을 시작하기 전에 우선 깊게 볼 것은 다음 네 챕터다.

- [50. CloudWatch](./50_cloudwatch/README.md)
- [51. CloudTrail](./51_cloudtrail/README.md)
- [54. KMS](./54_kms/README.md)
- [56. Systems Manager](./56_systems_manager/README.md)

이 네 주제는 단순 시험 암기보다 실제 실습과 운영 판단에 직접 연결된다.

```text
CloudWatch
→ 현재 시스템이 어떤 상태인가?
→ Metric / Log / Alarm

CloudTrail
→ 누가 AWS 설정을 바꿨는가?
→ API 호출 / 변경 추적 / Audit

KMS
→ 데이터가 어떤 키로 암호화되고 누가 그 키를 사용할 수 있는가?
→ S3 / EBS / RDS / IAM과 연결

Systems Manager
→ Public IP/SSH 없이 EC2를 어떻게 운영 접근하는가?
→ Session Manager
```

나머지 AWS Config, Advanced Identity, Secrets Manager / Parameter Store, WAF / Shield / Firewall Manager, GuardDuty / Inspector / Macie는 SAA 강의 순서에 맞춰 Coverage 중심으로 학습한다. 중요하지 않다는 뜻이 아니라, 현재 `examples/01~16`의 선행조건으로서 우선순위가 상대적으로 낮다는 뜻이다.

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

KMS
  → examples/11 IAM Role + S3
  → examples/12 S3 Security / Encryption
  → examples/15 S3 권한과 KMS 권한 장애 구분
  → examples/16 보안 설계 근거

Systems Manager / Session Manager
  → examples/06 Private EC2 Access
  → private subnet의 EC2 운영 접근
```

## 이 파트의 완료 기준

실습 전에 최소한 다음 질문에 답할 수 있어야 한다.

- Metric, Log, Alarm의 역할은 각각 무엇인가?
- ALB/EC2/RDS/ASG 장애에서 어떤 지표부터 볼 것인가?
- CloudWatch와 CloudTrail의 차이는 무엇인가?
- Security Group이나 EC2 설정이 바뀌었을 때 누가 변경했는지 어떻게 추적하는가?
- SSE-S3와 SSE-KMS는 무엇이 다른가?
- `s3:GetObject` 권한이 있어도 KMS 권한 때문에 읽기가 실패할 수 있는 이유는?
- private subnet의 EC2에 public IP/SSH 없이 어떻게 접속할 수 있는가?
- Session Manager를 쓰기 위해 EC2와 IAM 측에 무엇이 필요한가?

## 학습 우선순위

```text
깊게 학습
50 CloudWatch
51 CloudTrail
54 KMS
56 Systems Manager

Coverage 중심
52 AWS Config
53 Advanced Identity
55 Secrets Manager / Parameter Store
57 WAF / Shield / Firewall Manager
58 GuardDuty / Inspector / Macie
```
