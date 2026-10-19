# u4. CloudFormation Service Role / IAM

CloudFormation Service Role은 CloudFormation이 사용자를 대신해 Stack resource를 생성/수정/삭제할 때 사용하는 IAM Role이다.

## 구조

```text
User
 ├─ cloudformation 권한
 └─ iam:PassRole
        ↓
CloudFormation
        ↓ assume
Service Role
        ↓
Create / Update / Delete AWS Resources
```

강의에서 이 구조의 목적은 **Least Privilege**다.

사용자에게 S3/EC2/RDS 등 모든 resource 권한을 직접 줄 필요 없이 CloudFormation을 사용할 권한과 Service Role 전달 권한을 줄 수 있다.

## 중요

```text
User
→ iam:PassRole 필요

Service Role
→ 실제 resource 생성 권한 필요
```

## 기억할 문장

> CloudFormation Service Role은 사용자의 직접 resource 권한과 Stack 생성 권한을 분리한다.
