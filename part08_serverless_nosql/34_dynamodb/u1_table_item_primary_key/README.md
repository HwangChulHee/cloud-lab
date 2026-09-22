# u1. DynamoDB Table / Item / Attribute / Primary Key

## 1. Table

DynamoDB의 가장 큰 저장 단위다.

```text
Users Table
Orders Table
Sessions Table
```

## 2. Item

관계형 DB의 row와 비슷한 개념으로 생각할 수 있다.

```json
{
  "UserId": "u-100",
  "Name": "Logan",
  "Age": 30
}
```

## 3. Attribute

Item 내부의 각 필드다.

```text
UserId
Name
Age
```

## 4. Primary Key

DynamoDB는 각 Item을 Primary Key로 식별한다.

두 형태:

```text
Simple Primary Key
→ Partition Key 하나

Composite Primary Key
→ Partition Key + Sort Key
```

강의 예시:

```text
User_ID = Partition Key
Game_ID = Sort Key
```

같은 Partition Key 아래 여러 Item을 Sort Key로 구분할 수 있다.

## 기억할 문장

> DynamoDB의 설계 출발점은 schema 전체보다 먼저 Primary Key와 access pattern을 정하는 것이다.
