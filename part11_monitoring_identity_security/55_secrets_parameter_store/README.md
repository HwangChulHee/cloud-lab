# 55. Secrets Manager / SSM Parameter Store

이 단원은 **애플리케이션 설정과 비밀값을 어디에 저장하고 어떻게 관리할지**를 구분한다.

## Units

- [ ] [u1. SSM Parameter Store 기본 구조](./u1_parameter_store_basics/README.md)
- [ ] [u2. Hierarchy / Standard vs Advanced](./u2_hierarchy_tiers_policies/README.md)
- [ ] [u3. AWS Secrets Manager / Rotation](./u3_secrets_manager_rotation/README.md)
- [ ] [u4. Multi-Region Secrets / SAA Selection](./u4_multiregion_selection/README.md)

## 핵심 구분

```text
SSM Parameter Store
→ configuration + secret 저장
→ plaintext / encrypted 가능
→ hierarchy
→ version tracking

Secrets Manager
→ secret 전용
→ rotation
→ RDS integration
→ KMS encryption
```

## 가장 중요한 선택 기준

```text
일반 설정값 / 계층형 config
→ Parameter Store

DB password 자동 rotation
→ Secrets Manager
```
