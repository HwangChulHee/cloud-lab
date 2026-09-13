# 16. CloudFront & Global Accelerator

이 단원은 강의의 **CloudFront & Global Accelerator** 범위를 정리한다.

둘 다 글로벌 사용자 성능 개선에 쓰이지만 해결하는 문제가 다르다.

```text
CloudFront
→ Edge Location에 콘텐츠를 캐시하는 CDN

Global Accelerator
→ AWS 글로벌 네트워크를 이용해 애플리케이션 endpoint까지 빠르고 안정적으로 라우팅
```

## Units

- [x] u1. CloudFront, CDN, Edge Location & Cache
- [x] u2. Origins — S3 / VPC Origin / Custom Origin
- [x] u3. Cache Key, TTL, Cache Policy & Invalidation
- [x] u4. OAC, Signed URL / Cookie & Geo Restriction
- [x] u5. CloudFront Architecture Examples
- [x] u6. Global Accelerator & CloudFront Comparison

## SAA 선택 지도

```text
정적/동적 콘텐츠를 전 세계 Edge에서 제공
→ CloudFront

S3를 직접 Public으로 열지 않고 CloudFront만 접근
→ OAC

유료 콘텐츠를 특정 사용자에게 제한
→ Signed URL / Signed Cookie

캐시된 파일을 즉시 새 버전으로 바꾸고 싶음
→ Cache Invalidation 또는 versioned filename

TCP/UDP 애플리케이션의 글로벌 성능, 고정 Anycast IP, 빠른 장애 전환
→ Global Accelerator

콘텐츠 캐싱이 핵심
→ CloudFront

네트워크 경로 최적화가 핵심
→ Global Accelerator
```

## 실제 도메인을 이용한 선택 실습

보유 도메인 `chulheehwang.com`을 활용할 수 있으므로 이 단원에서는 개념만 보는 것으로 끝내지 않고, 여유가 있으면 아래 작은 실습을 추가한다.

루트 도메인은 건드리지 않고 다음 서브도메인을 사용한다.

```text
cdn.chulheehwang.com
```

목표 구조:

```text
User
 ↓
cdn.chulheehwang.com
 ↓ Route 53 Alias
CloudFront
 ↓ OAC
S3 private bucket
```

핵심 확인 항목:

1. S3 Bucket은 Public Access Block을 유지한다.
2. CloudFront Distribution의 Origin을 S3로 지정한다.
3. OAC를 사용해 CloudFront만 S3 object에 접근하도록 한다.
4. CloudFront용 ACM certificate는 `us-east-1`에서 `cdn.chulheehwang.com` 이름으로 준비한다.
5. Route 53에 `cdn.chulheehwang.com` A/AAAA Alias를 만들어 CloudFront Distribution으로 연결한다.
6. 실제 브라우저와 `curl`로 HTTPS 응답을 확인한다.
7. S3 object를 수정한 뒤 캐시 때문에 즉시 바뀌지 않는 상황을 관찰한다.
8. Invalidation 또는 versioned filename으로 갱신 동작을 확인한다.

이 실습에서 반드시 설명할 수 있어야 하는 흐름:

```text
DNS
→ CloudFront Edge
→ cache hit / miss
→ Origin 요청
→ OAC
→ private S3
```

### 장애/비교 포인트

```text
Route 53 record 오류
→ DNS 계층 문제

CloudFront alternate domain name 미설정
→ custom domain 연결 문제

ACM certificate Region 오류
→ CloudFront용 인증서는 us-east-1 요구

OAC/Bucket Policy 오류
→ CloudFront는 도달하지만 S3 origin 접근 실패

S3 object 변경 후 예전 내용 표시
→ DNS 문제가 아니라 cache 문제
```

이 실습은 `examples/13`의 ALB 기반 실제 도메인/HTTPS 경험과 비교한다.

```text
lab.chulheehwang.com
→ Route 53 → ALB → EC2/ASG

cdn.chulheehwang.com
→ Route 53 → CloudFront → S3
```

둘 다 Route 53과 HTTPS를 사용하지만 **최종 endpoint와 트래픽 처리 방식이 완전히 다르다**는 점을 체감하는 것이 목적이다.
