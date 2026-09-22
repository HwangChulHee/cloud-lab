# 74. AWS CloudFormation

AWS CloudFormation은 AWS 인프라를 **선언형(Declarative) 코드로 정의하고 Stack 단위로 생성/수정/삭제**하는 Infrastructure as Code 서비스다.

## Units

- [ ] [u1. Declarative Infrastructure as Code](./u1_declarative_iac/README.md)
- [ ] [u2. Stack / Template / Dependency](./u2_stack_template_dependency/README.md)
- [ ] [u3. Benefits / Cost / Productivity](./u3_benefits_cost_productivity/README.md)
- [ ] [u4. Service Role / IAM](./u4_service_role_iam/README.md)

## 기본 구조

```text
Template
  ↓
CloudFormation
  ↓
Stack
├─ Security Group
├─ EC2
├─ S3
└─ ELB
```

강의 핵심은 **무엇을 만들지 선언하면 CloudFormation이 dependency와 생성 순서를 처리한다**는 점이다.

## 기억할 문장

> CloudFormation은 AWS 리소스를 수동 생성하는 대신 template에 원하는 최종 상태를 선언하고 Stack 단위로 관리한다.
