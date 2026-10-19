# u4. Idle Resource / Cost Visibility

## 사용하지 않는 시간 줄이기

강의에서 CloudFormation 예로 Dev environment를 업무 시간에만 만들고 삭제하는 전략을 언급한다.

Other Services 섹션에서는 **Instance Scheduler on AWS** 솔루션도 소개한다.

```text
업무 시간
→ EC2 / ASG / RDS 실행

업무 외 시간
→ 자동 stop/start
```

Instance Scheduler는 CloudFormation으로 배포되는 AWS Solution이며 EC2, ASG, RDS 등의 schedule을 tag와 DynamoDB/Lambda를 이용해 관리한다.

## Cost Visibility

강의에서는 Cost Explorer로 비용/사용량을 시각화하고 Savings Plan 선택과 forecast에 활용하는 개념을 다룬다.

Trusted Advisor는 account-level recommendation에서 Cost Optimization 항목도 제공한다.

## 기억할 문장

> 사용하지 않는 resource를 끄고, 비용 데이터를 관측해 실제 사용 패턴에 맞게 구매/구성 결정을 반복한다.
