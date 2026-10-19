# u3. Consumers / Retention / Replay

## 1. Retention

Kinesis Data Streams는 데이터를 일정 기간 보관한다.

강의에서는 최대 365일까지 retention을 늘릴 수 있다고 설명한다.

이게 SQS와 중요한 차이다.

```text
SQS
Consumer 처리 + DeleteMessage
→ message 제거

Kinesis
Record가 retention 기간 동안 stream에 남음
→ Consumer가 다시 읽을 수 있음
```

## 2. Replay

이미 처리한 데이터를 다시 읽어 재처리할 수 있다.

예:

```text
실시간 분석 코드에 버그 발견
→ 수정
→ 과거 Stream 데이터를 다시 읽음
→ 분석 결과 재생성
```

이것이 Kinesis의 강한 선택 기준 중 하나다.

## 3. Multiple Consumers

같은 Stream을 여러 Consumer가 서로 다른 목적으로 읽을 수 있다.

```text
Kinesis Stream
   ├→ Fraud Detection
   ├→ Analytics
   └→ Monitoring
```

SQS처럼 하나의 메시지를 Worker들이 경쟁 소비하는 모델과 다르다.

## 4. Standard vs Enhanced Fan-Out

강의의 비교에서는:

```text
Standard Consumer
→ shard의 read throughput 공유

Enhanced Fan-Out
→ consumer별 전용 read throughput
→ 더 많은 Consumer / 낮은 지연 요구에 적합
```

## 5. 삭제 방식 차이

Stream의 개별 Record를 Consumer가 처리했다고 삭제하는 모델이 아니다.

Record는 retention이 지나면 만료된다.

## SAA 판단

```text
과거 데이터를 다시 처리
→ Kinesis Data Streams

여러 analytics Consumer가 동일 stream을 독립적으로 읽음
→ Kinesis

작업 완료 후 메시지를 삭제하는 queue
→ SQS
```
