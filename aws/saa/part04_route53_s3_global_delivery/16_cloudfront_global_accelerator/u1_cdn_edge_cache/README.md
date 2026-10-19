# u1. CloudFront, CDN, Edge Location & Cache

CloudFront는 AWS의 CDN(Content Delivery Network)이다.

CDN은 원본 서버의 콘텐츠를 전 세계 여러 Edge Location에 캐시해 사용자와 가까운 곳에서 전달하는 구조다.

```text
Origin: 서울 S3

미국 사용자
 ↓
미국 근처 CloudFront Edge
 ↓ cache hit
파일 반환
```

## Edge Location

Edge Location은 Region/AZ와 달리 사용자의 요청을 가까운 위치에서 처리하기 위한 글로벌 거점이다.

CloudFront는 이곳에 콘텐츠를 Cache한다.

## Cache

Cache는 원본 데이터를 가까운 곳에 복사해 두었다가 반복 요청에 재사용하는 것이다.

```text
첫 요청
User → Edge → Origin → 파일 가져옴
              ↓
            Cache 저장

두 번째 요청
User → Edge Cache → 바로 반환
```

첫 요청처럼 Origin까지 가야 하는 경우를 흔히 `cache miss`, Edge에 이미 있어 바로 반환할 수 있는 경우를 `cache hit`라고 이해하면 된다.

## 무엇이 좋아지는가

```text
사용자와 데이터 사이 거리 감소
→ Latency 감소

Origin까지 가는 반복 요청 감소
→ Origin 부하 감소

정적 콘텐츠 반복 전달
→ 효율 증가
```

CloudFront는 Shield 및 AWS WAF와 연계해 글로벌 엣지 계층에서 보호하는 구조도 만들 수 있다.

## 예시

쇼핑몰 상품 이미지가 S3에 있다고 하자.

```text
S3
└── product-1.jpg
```

한국, 미국, 유럽 사용자가 모두 S3 Origin까지 직접 요청하는 대신:

```text
User
 ↓
가까운 CloudFront Edge
 ↓ 필요할 때만
S3 Origin
```

으로 제공할 수 있다.

## SAA 판단

```text
글로벌 사용자에게 정적 콘텐츠 빠르게 제공
→ CloudFront

Edge에서 캐시해 Origin 부하 감소
→ CloudFront CDN

단순히 서버 대수를 늘리는 것과 다름
→ 캐시를 사용자 가까이에 배치하는 구조
```
