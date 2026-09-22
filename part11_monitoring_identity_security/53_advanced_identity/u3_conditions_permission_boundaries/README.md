# u3. IAM Conditions / Permission Boundaries

## 1. IAM Conditions

Policy를 단순 Action/Resource뿐 아니라 **조건**으로 제한할 수 있다.

강의 예:

```text
aws:SourceIp
→ 특정 client IP에서만 API 호출

aws:RequestedRegion
→ 특정 Region에서만 API 호출

ec2:ResourceTag
→ resource tag 기준 제어

aws:MultiFactorAuthPresent
→ MFA 사용 여부
```

## 2. Permission Boundary

IAM User/Role이 가질 수 있는 **최대 권한 범위**를 managed policy 형태로 설정한다.

```text
IAM Policy
        ∩
Permission Boundary
        ↓
실제로 가능한 최대 범위
```

지원 대상:

```text
IAM Users
IAM Roles

Groups는 지원하지 않음
```

## 대표 use case

강의에서 다음을 강조한다.

```text
개발자가 IAM policy를 스스로 붙일 수 있게 함
하지만 admin으로 privilege escalation은 못 하게 제한

비관리자에게 IAM 관리 일부 위임
```

## SCP와 차이

```text
Permission Boundary
→ 특정 User / Role

SCP
→ OU / Account 전체
```

## 기억할 문장

> IAM Policy는 권한을 주고, Permission Boundary는 개별 User/Role의 최대 권한을 제한한다.
