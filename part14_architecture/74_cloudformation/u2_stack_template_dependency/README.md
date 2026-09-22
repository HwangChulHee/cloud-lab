# u2. Stack / Template / Dependency

## Template

필요한 AWS resource와 configuration을 선언한다.

## Stack

Template을 실제 AWS resource 집합으로 생성한 결과다.

```text
Template
  ↓ deploy
Stack
  ↓
AWS Resources
```

## Dependency

강의의 예처럼 EC2가 Security Group을 사용하고 ELB가 EC2 앞에 있으면 resource 사이 dependency가 생긴다.

CloudFormation은 선언된 관계를 바탕으로 적절한 생성 순서를 처리한다.

## Lifecycle

```text
Create Stack
Update Stack
Delete Stack
```

Stack을 삭제하면 template로 관리되는 resource를 함께 정리하는 구조를 만들 수 있다.

## 기억할 문장

> Template은 설계도, Stack은 그 설계도로 실제 생성된 AWS resource 집합이다.
