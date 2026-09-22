# u2. Partition Key / Sort Key / Data Distribution

## 1. Partition Key

Partition Key는 Item이 어느 partition에 저장될지 결정하는 핵심 값이다.

좋은 Partition Key는 traffic/data를 여러 partition에 고르게 분산시키는 방향이어야 한다.

```text
좋은 분산
user-1
user-2
user-3
...

나쁜 분산 가능성
모든 요청이 같은 key
```

## 2. Sort Key

같은 Partition Key 안에서 여러 Item을 정렬/구분하는 데 사용한다.

예:

```text
Partition Key = user-42

Sort Key
2026-09-01
2026-09-02
2026-09-03
```

한 사용자의 시간순 기록처럼 묶을 수 있다.

## 3. Composite Key

```text
PK = User_ID
SK = Game_ID
```

같은 User_ID에 여러 Game_ID record를 저장할 수 있다.

## 4. Hot Partition 감각

한 Partition Key에 요청이 지나치게 집중되면 특정 partition이 병목이 될 수 있다.

따라서:

```text
traffic distribution
+
key uniqueness
+
access pattern
```

을 함께 고려한다.

## SAA 판단

```text
특정 key에 read/write 집중
→ Partition Key 설계 재검토

같은 entity의 여러 record를 정렬/범위 조회
→ Sort Key 활용
```
