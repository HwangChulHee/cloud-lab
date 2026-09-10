# u3. TLS와 HTTPS

## 지도 확인

HTTP 요청을 인터넷에 그대로 보내면 중간에서 내용을 볼 수 있거나 변조될 위험이 있다. HTTPS는 HTTP 통신을 TLS로 보호한다.

```text
HTTP + TLS = HTTPS
```

AWS에서는 이후 ACM, ALB, CloudFront에서 인증서와 HTTPS를 직접 다룬다.

---

## 1. TLS가 제공하는 것

TLS의 핵심 목적은 세 가지 관점으로 볼 수 있다.

### Confidentiality

통신 내용을 암호화해 제3자가 쉽게 읽지 못하게 한다.

### Integrity

전송 중 데이터가 변조되지 않았는지 확인한다.

### Authentication

클라이언트가 접속한 서버가 의도한 서버인지 인증서를 통해 확인한다.

---

## 2. Certificate

HTTPS 서버는 자신의 신원을 증명하기 위해 인증서를 제공한다.

인증서에는 도메인과 공개키를 비롯한 정보가 들어가며, 일반적으로 신뢰할 수 있는 CA(Certificate Authority)의 서명을 통해 검증된다.

```text
Client
  ↓ HTTPS
Server
  └─ certificate: example.com
```

브라우저는 접속한 hostname과 인증서가 일치하는지, 인증서가 신뢰 가능한 체인을 가지는지, 유효기간이 지나지 않았는지 등을 확인한다.

---

## 3. 아주 단순화한 TLS 연결

```text
1. Client가 서버에 연결
2. Server가 인증서 제공
3. Client가 인증서를 검증
4. 암호화 통신에 사용할 키를 안전하게 합의
5. 이후 HTTP 요청/응답을 암호화해서 교환
```

세부 암호 알고리즘과 handshake 패킷을 지금 깊게 파지는 않는다. 클라우드 엔지니어 입장에서는 **인증서가 어디에 설치되고 어디에서 TLS가 종료되는지**가 우선 중요하다.

---

## 4. TLS Termination

다음 구조를 생각해보자.

```text
User
  ↓ HTTPS :443
ALB
  ↓ HTTP :8000
EC2
```

이 경우 외부의 TLS 연결은 ALB에서 종료될 수 있다. 이를 TLS/SSL termination이라고 한다.

즉 인증서를 각 애플리케이션 서버가 직접 관리하지 않고 Load Balancer가 처리하도록 설계할 수 있다.

AWS SAA 강의에서도 Elastic Load Balancer가 HTTPS와 인증서를 처리할 수 있고, AWS Certificate Manager(ACM)를 이용해 인증서를 관리하는 구조를 다룬다.

---

## 5. 80과 443

대표적인 포트:

```text
HTTP  : 80
HTTPS : 443
```

일반적인 웹 구성에서는 HTTP 요청을 HTTPS로 redirect하기도 한다.

```text
http://example.com
       ↓ redirect
https://example.com
```

뒤에서 ALB listener rule과 인증서를 구성하며 직접 확인한다.

---

## 6. 어디에서 문제가 났는지 구분하기

HTTPS 접속 실패는 여러 원인이 있을 수 있다.

```text
DNS가 잘못됨
443 port 접근 불가
인증서 hostname 불일치
인증서 만료
TLS 설정 문제
ALB 뒤 target 자체가 unhealthy
```

따라서 `HTTPS가 안 된다`를 하나의 문제로 보지 않는다.

```text
DNS
 ↓
TCP connection
 ↓
TLS handshake
 ↓
HTTP request
 ↓
Application
```

각 단계로 분리해서 조사한다.

`curl -v`는 연결/TLS/HTTP 흐름을 확인할 때 유용하다.

```bash
curl -v https://example.com
```

---

## 7. AWS에서 다시 만날 곳

```text
ACM
→ TLS 인증서 발급/관리

ALB
→ HTTPS listener와 TLS termination

CloudFront
→ 사용자와 Edge 사이 HTTPS

Route 53
→ 인증서가 사용하는 domain으로 트래픽 연결
```

여기까지 이해하면 0부에서 필요한 HTTP / DNS / TLS의 최소 기반은 충분하다. 실제 인증서 발급과 HTTPS 구성은 이후 AWS 실습에서 진행한다.

기초 개념이므로 별도 유제와 3문장 요약은 생략한다.
