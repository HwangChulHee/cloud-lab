# 11부 — Monitoring, Advanced Identity & Security

이 파트는 SAA 강의의 Monitoring / Advanced Identity / Security 영역을 정리한다.

현재 `examples/` 실습을 시작하기 전에 우선 깊게 볼 것은 다음 두 챕터다.

- [50. CloudWatch](./50_cloudwatch/README.md)
- [56. Systems Manager](./56_systems_manager/README.md)

나머지 CloudTrail, Config, Advanced Identity, KMS, Secrets Manager, WAF/Shield, GuardDuty/Inspector/Macie는 SAA 강의 순서에 맞춰 Coverage 중심으로 학습한다.

## 실습 연결

```text
CloudWatch
  → examples/08 ASG scaling
  → examples/14 Observability
  → examples/15 Troubleshooting
  → examples/16 Final Architecture

Systems Manager / Session Manager
  → examples/06 Private EC2 Access
  → private subnet의 EC2 운영 접근
```

## 이 파트의 완료 기준

실습 전에 최소한 다음 질문에 답할 수 있어야 한다.

- Metric, Log, Alarm의 역할은 각각 무엇인가?
- ALB/EC2/RDS/ASG 장애에서 어떤 지표부터 볼 것인가?
- private subnet의 EC2에 public IP/SSH 없이 어떻게 접속할 수 있는가?
- Session Manager를 쓰기 위해 EC2와 IAM 측에 무엇이 필요한가?
