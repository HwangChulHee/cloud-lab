# u3. Config Remediation / Notifications

NON_COMPLIANT resource를 탐지한 뒤 remediation으로 연결할 수 있다.

## Auto-Remediation

강의에서는 **SSM Automation Documents**를 사용한다고 설명한다.

```text
NON_COMPLIANT Resource
        ↓
     AWS Config
        ↓
SSM Automation Document
        ↓
 Remediation Action
```

AWS Managed Automation Document 또는 custom Automation Document를 사용할 수 있다.

Custom Automation Document에서 Lambda를 호출하는 것도 가능하다.

## Retry

자동 remediation 후에도 여전히 NON_COMPLIANT라면 remediation retry 횟수를 설정할 수 있다.

## Notification

강의에서는 두 패턴을 다룬다.

### EventBridge

```text
AWS Config
   ↓ NON_COMPLIANT
EventBridge
   ├→ Lambda
   ├→ SNS
   └→ SQS
```

### SNS

Configuration Change / Compliance State 같은 Config event를 SNS로 보낼 수 있다.

## SAA 판단

```text
Config Rule 위반 발견
→ Config

자동 수정
→ Config + SSM Automation

NON_COMPLIANT 알림/후속 처리
→ EventBridge / SNS
```
