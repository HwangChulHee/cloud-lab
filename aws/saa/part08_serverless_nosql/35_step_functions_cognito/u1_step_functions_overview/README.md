# u1. AWS Step Functions Overview

AWS Step Functions는 여러 작업을 하나의 **visual workflow**로 orchestration하는 서비스다.

강의에서는 Lambda orchestration을 대표 예로 설명한다.

## 구조

```text
Start
  ↓
Lambda A
  ↓
Condition
 ├─ Yes → Lambda B
 └─ No  → Lambda C
  ↓
End
```

## 주요 기능

강의에서 다음을 강조한다.

```text
Sequence
Parallel
Conditions
Timeouts
Error Handling
```

즉 application code 안에서 workflow 상태를 직접 관리하는 대신 workflow engine이 실행 순서를 관리한다.

## 왜 필요한가?

Lambda 여러 개를 코드로 직접 chaining하면:

```text
A가 B 호출
B가 C 호출
C가 실패
→ 상태/재시도/오류 분기 관리가 복잡
```

Step Functions를 사용하면:

```text
Workflow Definition
→ 순서
→ 조건
→ 병렬
→ timeout
→ error path
```

를 별도 orchestration 계층으로 관리한다.

## 기억할 문장

> Step Functions는 여러 AWS 작업을 stateful workflow로 연결해 sequence, parallel, condition, timeout, error handling을 관리하는 orchestration 서비스다.
