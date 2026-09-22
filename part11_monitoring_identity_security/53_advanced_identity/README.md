# 53. Advanced Identity

이 단원은 IAM 기초를 넘어 **여러 AWS Account를 어떻게 조직하고, 권한 상한을 어떻게 걸고, 여러 계정에 SSO를 어떻게 제공하는지**를 정리한다.

## Units

- [ ] [u1. AWS Organizations / OU / Consolidated Billing](./u1_organizations_ou_billing/README.md)
- [ ] [u2. SCP / Tag Policies](./u2_scp_tag_policies/README.md)
- [ ] [u3. IAM Conditions / Permission Boundaries](./u3_conditions_permission_boundaries/README.md)
- [ ] [u4. IAM Identity Center / Permission Sets](./u4_identity_center_permission_sets/README.md)
- [ ] [u5. Directory Services / Control Tower](./u5_directory_services_control_tower/README.md)

## 전체 지도

```text
여러 AWS Account
    ↓
AWS Organizations
    ├→ OU
    ├→ Consolidated Billing
    └→ SCP

사용자/그룹 SSO
    ↓
IAM Identity Center
    ↓
Permission Sets
    ↓
각 AWS Account 접근

개별 User/Role 권한 상한
    ↓
Permission Boundary
```

## 가장 중요한 구분

```text
IAM Policy
→ 실제 권한을 부여

Permission Boundary
→ 특정 User/Role이 가질 수 있는 최대 권한

SCP
→ Organization / OU / Account 차원의 최대 권한 범위

IAM Identity Center
→ 여러 계정과 애플리케이션에 SSO
```
