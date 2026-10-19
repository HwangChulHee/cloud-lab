# u2. Service Control Policies / Tag Policies

## 1. SCP

Service Control Policy는 OU 또는 Account에 적용해 **그 아래 IAM User/Role이 가질 수 있는 권한의 최대 범위**를 제한한다.

```text
Organization Root
   ↓ SCP
OU
   ↓ SCP
Account
   ↓
IAM User / Role
```

강의 핵심:

- Management Account에는 SCP가 적용되지 않는다.
- SCP 자체가 권한을 부여하는 것은 아니다.
- Root → OU → Account 경로에서 필요한 Allow 범위 안에 있어야 한다.
- Explicit Deny는 아래로 상속되어 제한한다.

예:

```text
Sandbox OU
→ Deny S3

Account 내부 IAM Role에 s3:* Allow
→ 그래도 S3 사용 불가
```

## 2. Tag Policies

AWS Organizations에서 tag key와 허용 value를 표준화하는 데 사용한다.

강의에서 강조:

```text
consistent tags
cost allocation
ABAC 지원
non-compliant tag audit/report
EventBridge로 non-compliant tag monitoring
```

## 핵심 구분

```text
SCP
→ 권한 범위 제한

Tag Policy
→ tagging 표준 관리
```
