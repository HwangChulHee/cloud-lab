# u1. Database 선택 질문

강의는 Database를 선택할 때 다음 질문을 던지라고 한다.

## Workload

```text
Read-heavy?
Write-heavy?
Balanced?

Throughput은?
낮/밤 traffic 차이는?
자동 scale이 필요한가?
```

## Data Size / Retention

```text
얼마나 저장?
얼마나 오래?
성장 속도는?
Object 평균 크기는?
```

## Durability / Source of Truth

```text
이 데이터가 원본인가?
cache인가?
복구 가능해야 하는가?
```

## Latency / Concurrency

```text
sub-millisecond?
single-digit millisecond?
seconds도 괜찮은 analytics?

동시 사용자는?
```

## Data Model / Query

```text
Join 필요?
SQL 필요?
Key-value?
Document?
Graph?
Full-text search?
Time-series?
```

## Schema / Reporting / Cost

```text
Strong schema?
Flexible schema?
Reporting / BI?
License cost?
Cloud-native DB로 전환 가능한가?
```

## 핵심

서비스 이름을 외우기 전에 **요구사항을 먼저 분류**한다.
