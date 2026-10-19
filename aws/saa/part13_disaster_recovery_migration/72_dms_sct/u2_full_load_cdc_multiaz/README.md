# u2. DMS Full Load / CDC / Multi-AZ

## Full Load

기존 source database의 데이터를 target으로 처음 복사한다.

```text
Source DB
   ↓ Full Load
Target DB
```

## CDC — Change Data Capture

Migration 중 source DB에 계속 발생하는 변경을 target으로 복제한다.

```text
Source DB
   ↓ initial Full Load
Target DB

Source DB의 INSERT / UPDATE / DELETE
   ↓ CDC
Target DB에 지속 반영
```

이 방식 때문에 source database를 migration 동안 계속 사용할 수 있다.

## DMS Replication Instance

강의에서는 replication task를 수행하기 위해 DMS replication instance를 생성한다고 설명한다.

```text
Source DB
   ↓
DMS Replication Instance
   ↓
Target DB
```

## Multi-AZ

Multi-AZ를 활성화하면 DMS가 다른 AZ에 synchronous standby replica를 유지한다.

강의에서 언급한 장점:

```text
Data Redundancy
I/O freeze 제거
latency spike 최소화
```

## 기억할 문장

> Full Load로 기존 데이터를 옮기고 CDC로 migration 중 발생하는 변경을 따라잡는다.
