# u3. Cache Key, TTL, Cache Policy & Invalidation

CloudFront 캐시는 단순히 URL 하나만 보고 저장하는 것이 아니다. 어떤 요청을 같은 캐시로 볼지 결정하는 기준이 필요하다.

## 1. Cache Key

Cache Key는 "이 요청을 어떤 캐시 항목으로 구분할 것인가"를 결정하는 기준이다.

예를 들어 같은 `/products` 요청이라도 query string이 다를 수 있다.

```text
/products?page=1
/products?page=2
```

Query String을 Cache Key에 포함하면 서로 다른 캐시로 저장할 수 있다.

Headers나 Cookies도 필요에 따라 Cache Key에 포함할 수 있다.

다만 너무 많은 값을 포함하면 요청마다 Cache Key가 달라져 cache hit 비율이 떨어질 수 있다.

## 2. TTL

TTL(Time To Live)은 캐시가 얼마나 오래 유효한지를 뜻한다.

```text
TTL = 1시간
```

이면 Edge에 저장된 객체를 일정 시간 재사용한다.

TTL이 길면 Origin 요청과 비용을 줄이기 쉽지만, 원본 변경이 늦게 반영될 수 있다.

```text
TTL 길게
→ cache hit 증가
→ Origin 부하 감소
→ 최신성은 낮아질 수 있음

TTL 짧게
→ 최신성 증가
→ Origin 요청 증가
```

## 3. Cache Policy

Cache Policy는 Cache Key와 TTL 등 캐싱 동작을 정의한다.

예:

```text
상품 이미지
→ Query/Cookie 거의 필요 없음
→ 긴 TTL

사용자별 동적 페이지
→ Cookie/Header가 중요할 수 있음
→ 캐싱 여부를 더 신중히 결정
```

## 4. Cache Invalidation

Origin의 파일을 바꿨는데 TTL이 남아 있으면 Edge에는 과거 파일이 남아 있을 수 있다.

```text
S3: app.js 새 버전
CloudFront Edge: app.js 옛 버전
```

Invalidation을 실행하면 특정 경로의 캐시를 무효화해 다음 요청 때 Origin에서 새 콘텐츠를 가져오게 할 수 있다.

```text
/app.js
/images/*
```

실무에서는 파일 이름에 버전을 포함하는 방식도 많이 쓴다.

```text
app-v1.js
→ app-v2.js
```

이 경우 새 URL이므로 기존 캐시와 충돌하지 않는다.

## SAA 판단

```text
캐시 유효시간 조절
→ TTL

Query/Header/Cookie 중 어떤 값을 캐시 구분에 사용할지 결정
→ Cache Key / Cache Policy

Origin은 변경됐지만 Edge의 옛 파일 즉시 제거
→ Invalidation

캐시 무효화를 반복하지 않고 새 콘텐츠 배포
→ Versioned filename 고려
```
