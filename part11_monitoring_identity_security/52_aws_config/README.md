# 52. AWS Config

AWS Config는 **AWS 리소스의 설정과 변경 이력을 기록하고, 원하는 규칙에 맞는지 Compliance를 평가**하는 서비스다.

강의에서 Config는 CloudWatch/CloudTrail과 함께 비교해서 이해하는 것이 핵심이다.

## Units

- [ ] [u1. Configuration Recording / Timeline](./u1_configuration_recording_timeline/README.md)
- [ ] [u2. Config Rules / Compliance](./u2_rules_compliance/README.md)
- [ ] [u3. Remediation / Notifications](./u3_remediation_notifications/README.md)
- [ ] [u4. CloudWatch vs CloudTrail vs Config](./u4_comparison_selection/README.md)

## AWS Config가 답하는 질문

강의 예시:

```text
Security Group에 unrestricted SSH가 열려 있는가?

S3 Bucket에 public access가 있는가?

ALB 설정이 시간에 따라 어떻게 바뀌었는가?
```

## 전체 흐름

```text
AWS Resources
    ↓ configuration recording
AWS Config
    ├→ Configuration History
    ├→ Compliance Evaluation
    └→ NON_COMPLIANT
          ↓
   EventBridge / SNS
          ↓
      Remediation
```

## 특징

```text
resource configuration 기록
change history
compliance evaluation
per-Region service
multi-account / multi-region aggregation 가능
configuration data를 S3에 저장 가능
```

## 중요한 주의

> AWS Config Rule은 잘못된 작업 자체를 막는 Deny 기능이 아니다.

리소스가 생성/변경된 뒤 규칙을 평가하고 NON_COMPLIANT 상태를 탐지하는 방식이다.
