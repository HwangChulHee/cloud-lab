# u2. DynamoDB + OpenSearch Pattern

강의의 대표 architecture:

```text
Application
   ├→ CRUD
   │    ↓
   │ DynamoDB
   │    ↓
   │ DynamoDB Streams
   │    ↓
   │  Lambda
   │    ↓
   └→ OpenSearch

Search API
   ↓
OpenSearch
```

## 역할 분리

```text
DynamoDB
→ source of application items
→ key-based CRUD

OpenSearch
→ search index
→ flexible search
```

## 왜 둘 다 쓰나?

DynamoDB를 full-text search engine처럼 사용하려 하면 access pattern이 맞지 않는다.

OpenSearch를 transaction source of truth처럼 사용하는 것도 강의가 강조하는 패턴이 아니다.

따라서:

```text
CRUD storage
→ DynamoDB

Search
→ OpenSearch
```

로 역할을 나눈다.

## 동기화

DynamoDB Streams의 item change를 Lambda가 받아 OpenSearch index를 업데이트하는 형태다.

## SAA 판단

```text
DynamoDB data를 partial/full-text search
→ DynamoDB Streams + Lambda + OpenSearch
```
