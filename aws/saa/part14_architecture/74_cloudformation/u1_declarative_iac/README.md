# u1. Declarative Infrastructure as Code

CloudFormation은 **Declarative** 방식이다.

```text
"어떤 순서로 API를 호출할까?"
가 아니라

"최종적으로 어떤 리소스가 있어야 하는가?"
를 작성
```

예:

```text
Security Group 필요
EC2 2대 필요
S3 Bucket 필요
앞단에 ELB 필요
```

CloudFormation이 실제 생성 순서와 orchestration을 처리한다.

## IaC의 장점

```text
수동 생성 감소
변경사항을 code review 가능
같은 환경 재생성 가능
환경 차이 감소
```

## 기억할 문장

> CloudFormation은 절차를 직접 작성하는 명령형보다 원하는 인프라 상태를 선언하는 방식이다.
