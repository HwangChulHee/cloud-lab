# u5. CloudFront Architecture Examples

CloudFront는 단순히 S3 앞에만 두는 서비스가 아니다. Origin 조합에 따라 여러 아키텍처를 만들 수 있다.

## 1. S3 정적 콘텐츠

```text
User
 ↓
CloudFront
 ↓
Private S3 Bucket
```

상품 이미지, JS/CSS, 다운로드 파일처럼 반복 조회가 많은 정적 콘텐츠에 적합하다.

## 2. 동적 애플리케이션 + ALB

```text
User
 ↓
CloudFront
 ↓
ALB
 ↓
EC2 / ECS
```

CloudFront는 정적 파일뿐 아니라 HTTP 기반 동적 애플리케이션 앞에도 둘 수 있다.

Cache 가능한 경로와 그렇지 않은 경로를 분리할 수 있다.

예:

```text
/static/*
→ 길게 캐시

/api/*
→ 짧게 캐시하거나 캐시하지 않음
```

## 3. 여러 Origin 사용

하나의 Distribution에서 Path별로 서로 다른 Origin으로 보낼 수 있다.

```text
/images/* → S3
/api/*    → ALB
```

쇼핑몰이라면:

```text
Client
 ↓
CloudFront
 ├── /images/* → S3
 └── /api/*    → ALB → App
```

처럼 구성할 수 있다.

## 4. Upload와 Download 경로

강의에서는 CloudFront를 통해 S3에 파일을 업로드하는 구성도 다룬다.

```text
Client
 ↓
CloudFront
 ↓
S3
```

즉 CloudFront를 반드시 "읽기 전용 CDN"으로만 기억하지 않는다.

## SAA 판단

```text
정적 파일 글로벌 배포
→ CloudFront + S3

웹 애플리케이션 글로벌 진입점 + HTTP Origin
→ CloudFront + ALB

정적/동적 경로별 Origin 분리
→ Cache Behavior + Multiple Origins
```
