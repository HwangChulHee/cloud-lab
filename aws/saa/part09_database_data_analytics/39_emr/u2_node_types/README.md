# u2. EMR Node Types

강의에서는 EMR cluster의 node를 세 종류로 구분한다.

## Master Node

```text
cluster 관리
작업 coordination
health 관리
long-running
```

## Core Node

```text
task 실행
data 저장
long-running
```

## Task Node

```text
task만 실행
optional
data 저장 역할 없음
Spot 사용에 적합
```

## 구조

```text
Master
  │
  ├─ Core 1
  ├─ Core 2
  ├─ Core 3
  ├─ Task A
  └─ Task B
```

## SAA 판단

```text
cluster coordination
→ Master

compute + data storage
→ Core

추가 compute만 필요
→ Task
```
