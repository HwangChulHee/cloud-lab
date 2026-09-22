# u4. Lambda Concurrency / Throttling / Cold Start

## 1. Concurrency

Concurrency는 동시에 실행되는 Lambda invocation 수다.

강의에서는 Region당 기본 concurrency limit 예시로 1000을 설명한다.

```text
동시에 1000 invocation
→ limit 도달
→ 추가 요청 throttling
```

## 2. Reserved Concurrency

Function 단위로 concurrency를 예약/제한할 수 있다.

```text
Function A
reserved concurrency = 100
```

이는 두 가지 의미를 가진다.

```text
A가 account concurrency를 전부 쓰지 못하게 제한
+
A에게 필요한 concurrency를 확보
```

## 3. Throttling

강의의 구분:

```text
Synchronous invocation
→ throttle 시 429

Asynchronous invocation
→ 자동 retry
→ 이후 failure destination / DLQ 계열 처리
```

## 4. Cold Start

새 execution environment를 만들 때 다음 과정이 필요하다.

```text
code load
dependencies load
handler 밖 initialization
```

첫 요청 latency가 높아질 수 있다.

## 5. Provisioned Concurrency

미리 concurrency를 준비해 cold start를 줄인다.

```text
Provisioned Concurrency
→ invocation 전에 environment 준비
→ 낮은 latency
```

강의에서는 Application Auto Scaling으로 schedule 또는 utilization 기반 관리도 가능하다고 설명한다.

## SAA 판단

```text
예측 가능한 low latency가 매우 중요
→ Provisioned Concurrency

특정 Lambda가 account concurrency를 독점
→ Reserved Concurrency 고려

429
→ concurrency / throttling 확인
```
