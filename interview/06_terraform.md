# 06. Terraform

## 핵심 질문

1. Infrastructure as Code(IaC)가 필요한 이유는 무엇인가요?
2. Bash/Python으로 자동화할 수 있는데 왜 Terraform을 사용하나요?
3. Terraform state란 무엇인가요?
4. state를 Git에 commit하면 안 되는 이유는 무엇인가요?
5. Remote Backend가 필요한 이유는 무엇인가요?
6. `terraform plan`과 `terraform apply`의 차이는 무엇인가요?
7. Infrastructure Drift란 무엇인가요?

## 기본 흐름

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

## 실전형 질문

### 왜 remote state를 사용하나요?

```text
로컬 state
→ 개인 PC에만 존재
→ 팀 협업 어려움
→ 동시 수정 충돌 위험

Remote backend
→ state 공유
→ locking
→ 중앙 관리
→ 협업 가능
```

state에는 민감한 값이 포함될 수 있으므로 저장 위치의 접근제어와 암호화도 함께 고려합니다.

### Terraform apply가 중간에 실패했습니다.

```text
현재 state 확인
 ↓
실제 cloud resource 확인
 ↓
terraform plan으로 차이 확인
 ↓
drift / 부분 생성 여부 파악
 ↓
필요하면 import/state 조정
 ↓
재실행
```

무작정 state 파일을 직접 수정하거나 리소스를 삭제하기보다 현재 Terraform state와 실제 인프라 상태를 먼저 비교합니다.
