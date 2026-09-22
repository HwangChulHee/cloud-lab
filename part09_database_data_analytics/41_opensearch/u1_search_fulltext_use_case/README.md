# u1. OpenSearch Search / Full-Text Use Case

OpenSearch의 핵심은 **검색**이다.

## Database Query와 Search의 차이

예를 들어 DynamoDB는 key/index access pattern이 중심이다.

```text
PK = user-42
GSI = email
```

반면 OpenSearch는:

```text
title contains "cloud"
description partial match
log message free-text
여러 field 검색
```

같은 검색 요구에 적합하다.

## 대표 use case

```text
application search
log search
free-text search
partial match
analytics visualization
```

## SQL

강의에서는 OpenSearch가 SQL을 native 핵심 interface로 사용하는 서비스는 아니며 plugin으로 SQL 기능을 활성화할 수 있다고 설명한다.

## 기억할 문장

> OpenSearch는 transaction database를 대체하기보다, 임의 field / partial match / full-text search가 필요한 경우 database 옆에 붙는 검색 엔진으로 이해한다.
