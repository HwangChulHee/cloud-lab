# u2. Application Load Balancer (ALB)

## 지도 확인

Application Load Balancer는 HTTP/HTTPS 트래픽을 애플리케이션 수준에서 분산한다.

```text
Client
  ↓ HTTP/HTTPS
ALB
  ↓
Target Group
  ↓
EC2 / ECS / IP / Lambda
```

---

## 1. Layer 7 Load Balancer

ALB는 HTTP 요청의 내용을 보고 라우팅할 수 있다.

예:

```text
/api/*     → API Target Group
/images/*  → Image Target Group
```

또는 Host 기반으로:

```text
api.example.com → API Target Group
www.example.com → Web Target Group
```

즉 단순히 포트 단위로만 분산하는 것이 아니라 HTTP의 Host, Path 등 애플리케이션 정보를 활용한다.

---

## 2. Target Group

ALB는 직접 특정 서버 하나만 가리키기보다 Target Group을 통해 대상을 관리한다.

Target의 예:

```text
EC2 Instance
IP Address
Lambda
```

Listener Rule이 어떤 Target Group으로 보낼지 결정한다.

```text
Listener :80 / :443
  ↓ Rule
Target Group
  ↓
Targets
```

Health Check도 Target Group 단위로 설정한다.

---

## 3. Listener와 Routing Rule

Listener는 Load Balancer가 어떤 포트와 프로토콜로 요청을 받을지 정의한다.

예:

```text
HTTP  :80
HTTPS :443
```

Listener Rule을 이용하면 하나의 ALB가 여러 서비스로 트래픽을 분기할 수 있다.

```text
/path-a → TG-A
/path-b → TG-B
```

마이크로서비스나 컨테이너 환경에서 자주 연결되는 이유다.

---

## 4. Client IP

ALB가 클라이언트와 연결을 종료한 뒤 Target에 새 연결을 만든다.

따라서 애플리케이션 서버에서 직접 보는 Source IP는 Load Balancer 쪽 주소일 수 있다.

실제 클라이언트 정보는 다음과 같은 헤더로 전달된다.

```text
X-Forwarded-For
X-Forwarded-Port
X-Forwarded-Proto
```

---

## 5. ALB 특징 정리

```text
Layer 7
HTTP / HTTPS
Path-based routing
Host-based routing
여러 Target Group
고정 hostname 제공
```

ALB 자체에 고정 IP를 기대하는 문제와는 맞지 않는다.

---

## SAA 판단

```text
URL path에 따라 서로 다른 서비스로 분기
→ ALB

여러 도메인을 하나의 Load Balancer에서 처리
→ ALB + Host-based routing

HTTP/HTTPS 기반 마이크로서비스
→ ALB

실제 Client IP를 애플리케이션에서 확인
→ X-Forwarded-For
```
