# u2. CloudFront Origins — S3 / VPC Origin / Custom Origin

`Origin`은 CloudFront가 원본 콘텐츠를 가져오는 실제 출처다.

```text
User
 ↓
CloudFront Edge
 ↓ cache miss
Origin
```

## 1. S3 Origin

S3 Bucket을 Origin으로 사용하면 파일을 Edge에 캐시해 배포할 수 있다.

```text
CloudFront → S3 Bucket
```

대표 사용 사례는 이미지, JS/CSS, 다운로드 파일 같은 정적 콘텐츠다.

## 2. VPC Origin

강의에서는 VPC private subnet에 있는 애플리케이션도 CloudFront Origin으로 연결할 수 있는 VPC Origin을 다룬다.

예:

```text
CloudFront
 ↓
Private ALB
 ↓
Private EC2
```

인터넷에 직접 공개하지 않은 ALB/NLB/EC2를 Origin으로 두고 싶을 때 연결된다.

## 3. Custom Origin

S3가 아닌 일반 HTTP 서버도 Origin으로 사용할 수 있다.

예:

```text
Public ALB
EC2 Web Server
외부 HTTP 서버
S3 Static Website Endpoint
```

S3 Static Website를 쓸 때는 일반 S3 Origin과 다르게 **Custom Origin**으로 취급한다는 점을 구분한다.

## Origin과 Cache의 관계

CloudFront가 모든 요청마다 Origin을 호출하는 것은 아니다.

```text
cache hit
→ Edge에서 응답

cache miss
→ Origin 호출 → 응답을 Cache
```

## SAA 판단

```text
S3 파일 CDN 배포
→ S3 Origin

Private subnet의 ALB/EC2를 CloudFront 뒤에 둠
→ VPC Origin

일반 Public HTTP Backend
→ Custom Origin

S3 Static Website Endpoint
→ Custom Origin
```
