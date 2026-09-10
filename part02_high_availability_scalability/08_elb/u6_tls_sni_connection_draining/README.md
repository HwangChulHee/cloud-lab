# u6. TLS, SNI & Connection Draining

## 1. TLS 종료 지점

Load Balancer는 HTTPS 요청의 TLS 연결을 종료할 수 있다.

```text
Client
  ↓ HTTPS
Load Balancer
  ↓ HTTP 또는 HTTPS
Target
```

이 구조에서 외부 구간은 암호화하고, 내부 구간은 설계에 따라 HTTP 또는 HTTPS를 사용할 수 있다.

---

## 2. Certificate와 ACM

HTTPS Listener를 사용하려면 인증서가 필요하다.

AWS에서는 ACM(AWS Certificate Manager)으로 인증서를 관리할 수 있다.

Load Balancer의 HTTPS Listener에는 기본 인증서를 지정하고, 여러 도메인을 처리해야 한다면 추가 인증서를 연결할 수 있다.

---

## 3. SNI(Server Name Indication)

SNI는 클라이언트가 TLS handshake 과정에서 접속하려는 hostname을 알려주는 방식이다.

이를 통해 하나의 Load Balancer가 여러 도메인의 인증서를 구분해 사용할 수 있다.

```text
www.example.com
api.example.com

        ↓
      ALB/NLB
   ↙         ↘
Cert A      Cert B
```

강의에서는 ALB와 NLB가 여러 SSL/TLS 인증서를 SNI로 지원한다고 설명한다.

---

## 4. Connection Draining / Deregistration Delay

인스턴스를 Target Group에서 제거하거나 unhealthy 상태가 되었을 때, 진행 중인 요청까지 즉시 끊으면 문제가 생길 수 있다.

ALB/NLB에서는 이를 Deregistration Delay라고 부른다.

```text
기존 요청
→ 완료할 시간 제공

새 요청
→ 다른 healthy Target으로 전송
```

강의 기준 기본값은 300초이며, 1~3600초 범위에서 설정할 수 있고 0으로 비활성화할 수도 있다.

짧은 요청만 있는 서비스는 더 낮은 값을 고려할 수 있다.

---

## SAA 판단

```text
HTTPS를 Load Balancer에서 종료
→ HTTPS Listener + Certificate

여러 도메인에 서로 다른 인증서
→ SNI

Target 제거 중 진행 중 요청 보호
→ Deregistration Delay
```

TLS 자체의 상세 암호학보다 시험에서는 인증서, Listener, SNI, 종료 지점을 구분하는 것이 중요하다.
