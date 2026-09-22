# u4. DynamoDB GSI / LSI / Query / Scan

DynamoDB에서 Primary Key 외의 access pattern을 지원하기 위해 Secondary Index를 사용한다.

## 1. Query

Query는 key 조건을 사용해 특정 partition 범위의 데이터를 찾는 방식이다.

```text
PK = user-42
→ 해당 user의 items 조회
```

일반적으로 Scan보다 효율적인 접근이다.

## 2. Scan

Table 전체 또는 넓은 범위를 읽으며 조건에 맞는 Item을 찾는다.

```text
Table 전체 읽기
→ filter
```

많은 read capacity를 소비할 수 있어 대규모 table에서는 주의한다.

## 3. LSI

Local Secondary Index.

```text
같은 Partition Key
+
다른 Sort Key
```

기존 Partition Key를 유지하면서 다른 정렬 기준으로 조회할 때 사용한다.

## 4. GSI

Global Secondary Index.

```text
원본 table과 다른 Partition Key / Sort Key
```

새로운 access pattern을 만들 수 있다.

## 감각적 비교

```text
LSI
→ same partition key

GSI
→ different partition key 가능
```

## SAA 판단

```text
Primary Key로 바로 조회 가능
→ Query

전체 table을 조건으로 훑음
→ Scan

같은 PK + 다른 sort 기준
→ LSI

완전히 다른 key access pattern
→ GSI
```
