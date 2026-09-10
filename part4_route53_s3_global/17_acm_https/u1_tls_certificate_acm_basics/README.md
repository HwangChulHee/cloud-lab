# u1. TLS Certificate & ACM Basics

## 1. HTTPS와 TLS

HTTPS는 HTTP 통신을 TLS로 암호화한 형태다.

```text
HTTP
→ 평문 전송 가능

HTTPS
→ TLS를 사용해 전송 중 암호화
```

TLS Certificate는 브라우저나 클라이언트가 접속한 서버의 도메인과 인증서를 확인하고 암호화 통신을 시작하는 데 사용된다.

## 2. ACM이 하는 일

ACM(AWS Certificate Manager)은 AWS에서 TLS 인증서를 발급하고 관리하는 서비스다.

강의에서는 다음 특징을 다룬다.

```text
Public Certificate 지원
Private Certificate 지원
Public Certificate 발급 비용 없음
ACM이 발급한 인증서 자동 갱신
AWS 서비스와 직접 통합
```

대표 통합 대상:

```text
Elastic Load Balancer
CloudFront
API Gateway
```

중요한 점은 ACM 인증서를 EC2의 파일 시스템에 내려받아 웹 서버에 직접 설치하는 식으로 생각하는 것이 아니라, ACM과 통합되는 AWS 서비스에 연결해 사용하는 흐름을 먼저 이해하는 것이다.

## 3. TLS Termination

ALB가 HTTPS 요청을 받아 TLS 처리를 끝내고 뒤의 애플리케이션으로 HTTP를 보낼 수 있다.

```text
Client
 ↓ HTTPS
ALB + ACM Certificate
 ↓ HTTP 또는 HTTPS
EC2 / ECS
```

이때 ALB가 TLS 연결의 종료 지점이다.

## 예시

쇼핑몰에 `shop.example.com`을 연결한다고 하자.

```text
Route 53
shop.example.com
 ↓
ALB
 ↓
Spring App
```

ALB의 HTTPS Listener에 ACM 인증서를 연결하면 사용자는 `https://shop.example.com`으로 접속할 수 있다.

## SAA 판단

```text
AWS 서비스에서 HTTPS 인증서 쉽게 관리
→ ACM

ALB에서 HTTPS 처리
→ ACM Certificate + HTTPS Listener

전송 중 암호화
→ TLS / HTTPS
```
