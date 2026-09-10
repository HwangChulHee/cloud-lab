# u1. HTTP Request와 Response

## 지도 확인

웹 기반 AWS 서비스를 이해하려면 HTTP 요청이 어디로 들어오고 어떤 응답으로 돌아오는지 읽을 수 있어야 한다.

```text
Client
  ↓ HTTP Request
ALB / API Gateway / Web Server
  ↓
Application
  ↑ HTTP Response
Client
```

---

## 1. HTTP

HTTP는 클라이언트와 서버가 요청과 응답을 주고받기 위한 애플리케이션 계층 프로토콜이다.

예:

```http
GET /users/1 HTTP/1.1
Host: example.com
```

서버는 상태 코드, 헤더, body를 포함한 응답을 돌려준다.

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"id":1}
```

---

## 2. Method

자주 보는 method는 다음 정도다.

```text
GET     조회
POST    생성/처리 요청
PUT     전체 갱신 성격
PATCH   일부 갱신 성격
DELETE  삭제
```

클라우드 엔지니어 입장에서는 API 설계 자체보다 **어떤 요청이 어느 endpoint로 들어오는지** 로그와 health check에서 읽을 수 있으면 된다.

---

## 3. Status Code

범주를 먼저 기억한다.

```text
2xx → 성공
3xx → 리다이렉션
4xx → 클라이언트 요청 문제
5xx → 서버 측 처리 실패
```

대표적으로:

```text
200 OK
301/302 Redirect
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
500 Internal Server Error
502 Bad Gateway
503 Service Unavailable
```

ALB와 reverse proxy를 다룰 때 502/503은 특히 자주 보게 된다.

---

## 4. Header

HTTP header에는 요청/응답에 대한 부가 정보가 담긴다.

자주 보게 될 것:

```text
Host
Content-Type
Authorization
Cookie
User-Agent
X-Forwarded-For
X-Forwarded-Proto
```

뒤에서 ALB를 사용할 때 원래 client 정보가 `X-Forwarded-*` 계열 header를 통해 전달되는 이유를 다시 다룬다.

---

## 5. Health Check

Load Balancer는 애플리케이션이 정상인지 HTTP 요청으로 확인할 수 있다.

```text
GET /health
      ↓
200 OK
→ healthy
```

health check path가 잘못되거나 애플리케이션이 200을 반환하지 않으면 실제 프로세스가 살아 있어도 target은 unhealthy가 될 수 있다.

---

## 6. curl로 HTTP 관측

```bash
curl http://localhost:8000
curl -i http://localhost:8000
curl -v https://example.com
```

`-i`는 response header를 함께 보고, `-v`는 연결과 요청 과정을 더 자세히 관측할 때 유용하다.

---

## 앞으로의 연결

```text
ALB → HTTP listener, routing, health check
CloudFront → HTTP caching
API Gateway → HTTP API entry point
Nginx → reverse proxy
CloudWatch → HTTP error와 application log
```

웹 개발 경험이 있다면 대부분 익숙한 내용이므로 별도 유제와 3문장 요약은 생략한다.
