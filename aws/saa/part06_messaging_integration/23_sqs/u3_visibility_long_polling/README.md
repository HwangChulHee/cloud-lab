# u3. Visibility Timeout / Long Polling

## 1. Visibility Timeout

Consumer가 SQS에서 메시지를 가져오면 그 메시지는 일정 시간 동안 다른 Consumer에게 보이지 않게 된다.

```text
Queue
  │
  │ ReceiveMessage
  ▼
Worker A

Message = invisible for a while
Worker B → 같은 message를 바로 가져가지 못함
```

강의에서는 기본 Visibility Timeout을 30초로 설명한다.

## 왜 필요한가?

Consumer가 처리 중인 메시지를 다른 Consumer가 동시에 처리하지 않게 하기 위해서다.

하지만 처리 시간이 Visibility Timeout보다 길어지면:

```text
Worker A가 처리 중
→ Visibility Timeout 만료
→ Message가 다시 visible
→ Worker B가 같은 message 수신
→ 중복 처리 가능
```

따라서 작업 시간과 Visibility Timeout을 맞춰야 한다.

필요하면 `ChangeMessageVisibility` API로 처리 시간을 연장할 수 있다.

## 너무 길면?

```text
Visibility Timeout 너무 김
→ Worker가 죽었을 때
→ 다른 Worker가 다시 가져오기까지 오래 기다림
```

## 너무 짧으면?

```text
Visibility Timeout 너무 짧음
→ 아직 처리 중인데 다시 visible
→ duplicate processing 가능
```

---

## 2. Long Polling

Queue가 비어 있는데 Consumer가 계속 즉시 요청을 반복하면 불필요한 API 호출이 늘어난다.

Long Polling은 메시지가 없다면 일정 시간 기다렸다가 응답하도록 한다.

```text
Consumer → ReceiveMessage
             │
             ├─ message 있음 → 즉시 반환
             │
             └─ 없음 → 잠시 기다림
```

강의에서는 최대 20초까지 기다릴 수 있고 Long Polling을 Short Polling보다 선호한다고 설명한다.

효과:

```text
불필요한 ReceiveMessage 호출 감소
비어 있는 응답 감소
효율 개선
```

## SAA 판단

```text
같은 메시지가 처리 중인데 다시 보인다
→ Visibility Timeout 확인

작업 시간이 가변적이다
→ ChangeMessageVisibility 고려

빈 Queue를 너무 자주 polling한다
→ Long Polling
```
