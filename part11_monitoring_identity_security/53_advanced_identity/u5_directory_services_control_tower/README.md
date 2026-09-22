# u5. Directory Services / Control Tower

## AWS Directory Services

강의에서는 세 가지를 구분한다.

### AWS Managed Microsoft AD

```text
AWS 안에 managed Microsoft AD 생성
local users 관리
MFA 지원
on-premises AD와 trust 가능
```

### AD Connector

```text
Directory Gateway / Proxy
→ 인증 요청을 on-premises AD로 전달
→ 사용자는 on-premises AD에서 관리
```

### Simple AD

```text
AD-compatible managed directory
on-premises AD와 join/trust 불가
```

## IAM Identity Center와 AD

강의에서는 다음 연결을 다룬다.

```text
IAM Identity Center
→ AWS Managed Microsoft AD 직접 연결

Self-Managed AD
→ AWS Managed AD two-way trust
또는
→ AD Connector
```

---

## AWS Control Tower

여러 AWS Account를 best practice 기반으로 빠르게 구성하고 지속 governance하는 서비스다.

AWS Organizations를 사용해 Account를 만든다.

### Guardrails

강의 구분:

```text
Preventive Guardrail
→ SCP 사용
→ 예: 특정 Region 제한

Detective Guardrail
→ AWS Config 사용
→ 예: tag 없는 resource 탐지
```

Detective violation은 SNS/Lambda 등으로 remediation에 연결할 수 있다.

## 기억할 문장

> Organizations가 multi-account 기반이라면 Control Tower는 그 위에서 landing zone과 guardrail governance를 자동화하는 서비스다.
