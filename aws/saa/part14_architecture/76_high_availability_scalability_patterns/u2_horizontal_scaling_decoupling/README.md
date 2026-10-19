# u2. Horizontal Scaling / Decoupling

## Horizontal Scaling

```text
1 large server만 키움
→ Vertical Scaling

여러 server를 추가/제거
→ Horizontal Scaling
```

AWS에서는 ELB + ASG가 대표적인 horizontal scaling 구조다.

## Decoupling

동기 호출만 이어지면 downstream spike가 전체 system에 전파될 수 있다.

```text
Producer
  ↓
SQS
  ↓
Consumers / Workers
```

Queue를 넣으면 producer와 consumer 처리 속도를 분리할 수 있다.

## 기억할 문장

> Scale-out은 compute 수를 늘리고, decoupling은 component 사이의 시간적 결합을 줄인다.
