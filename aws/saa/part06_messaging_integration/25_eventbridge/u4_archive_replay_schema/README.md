# u4. Archive / Replay / Schema Registry

## Archive

EventBridge Event Bus로 들어온 event를 archive할 수 있다.

강의에서는:

```text
모든 event
또는
filter된 event
```

를 보관할 수 있고, 보관 기간을 지정하거나 장기간 유지할 수 있다고 설명한다.

## Replay

Archive된 event를 다시 Event Bus로 replay할 수 있다.

```text
Original Events
    ↓
EventBridge Archive
    ↓ later
Replay
    ↓
Event Bus
    ↓
Rules / Targets 재처리
```

장애 이후 재처리나 event-driven flow 재검증에 활용할 수 있다.

## Schema Registry

EventBridge는 Event Bus의 event를 분석해 schema를 추론할 수 있다.

강의 핵심:

```text
Schema Registry
→ event structure 파악
→ application code generation 지원
→ schema versioning
```

즉 producer/consumer가 event JSON 구조를 예측 가능하게 다룰 수 있도록 돕는다.

## 기억할 문장

> Archive/Replay는 event 재처리, Schema Registry는 event 구조 관리에 사용한다.
