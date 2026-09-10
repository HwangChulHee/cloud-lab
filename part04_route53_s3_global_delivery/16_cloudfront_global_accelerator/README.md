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

- [ ] u1. CloudFront, CDN, Edge Location & Cache
- [ ] u2. Origins — S3 / VPC Origin / Custom Origin
- [ ] u3. Cache Key, TTL, Cache Policy & Invalidation
- [ ] u4. OAC, Signed URL / Cookie & Geo Restriction
- [ ] u5. CloudFront Architecture Examples
- [ ] u6. Global Accelerator & CloudFront Comparison

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
