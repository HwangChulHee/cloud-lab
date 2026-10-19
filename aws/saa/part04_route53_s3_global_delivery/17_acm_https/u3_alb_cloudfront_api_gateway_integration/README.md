# u3. ALB, CloudFront & API Gateway Integration

ACM에서 가장 시험에 자주 연결되는 부분은 **인증서를 어느 서비스와 어느 Region에서 사용하는가**다.

## 1. ALB + ACM

ALB에서 HTTPS를 사용하려면 HTTPS Listener에 인증서를 연결한다.

```text
Client
 ↓ HTTPS :443
ALB + ACM Certificate
 ↓
Target Group
```

필요하면 HTTP 요청을 HTTPS로 Redirect하도록 Rule을 구성할 수 있다.

```text
HTTP :80
→ Redirect
→ HTTPS :443
```

## 2. CloudFront + ACM

CloudFront Distribution에서 사용자에게 HTTPS를 제공하려면 Viewer Certificate를 설정한다.

CloudFront는 글로벌 서비스지만 ACM 인증서 Region 제약이 있다.

```text
CloudFront에서 사용할 ACM Certificate
→ us-east-1 (N. Virginia)
```

시험에서 매우 자주 헷갈리는 포인트다.

예:

```text
S3 Bucket: ap-northeast-2
CloudFront: Global
ACM Certificate: us-east-1
```

Origin이 서울 Region이어도 CloudFront Viewer Certificate는 us-east-1에 있어야 한다.

## 3. API Gateway

API Gateway는 Endpoint 유형에 따라 인증서 Region 판단이 달라진다.

### Edge-Optimized

글로벌 사용자가 CloudFront Edge를 거쳐 API Gateway로 접근하는 형태다.

```text
Certificate
→ us-east-1
```

### Regional

특정 Region의 API Gateway endpoint를 직접 사용한다.

```text
Certificate
→ API Gateway와 같은 Region
```

예:

```text
API Gateway: ap-northeast-2
→ ACM Certificate: ap-northeast-2
```

## 4. Route 53과 연결

Custom Domain을 만든 뒤 Route 53에서 DNS Record를 연결한다.

```text
api.example.com
 ↓ Route 53 Alias
API Gateway / ALB / CloudFront
```

## SAA 판단

```text
ALB HTTPS
→ ALB Region의 ACM Certificate

CloudFront HTTPS
→ ACM Certificate는 us-east-1

API Gateway Edge-Optimized
→ us-east-1

API Gateway Regional
→ API Gateway와 같은 Region

HTTP → HTTPS 강제
→ ALB Redirect Rule 가능
```
