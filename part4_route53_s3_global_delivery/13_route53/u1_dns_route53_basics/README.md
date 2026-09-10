# u1. DNS와 Route 53 기본

## 1. DNS가 왜 필요한가

컴퓨터는 서버를 IP 주소로 찾지만 사람은 `example.com` 같은 이름을 기억하는 편이 쉽다.

```text
사용자: example.com 접속
        ↓
DNS: example.com의 주소는?
        ↓
203.0.113.10 반환
        ↓
브라우저가 서버에 접속
```

DNS(Domain Name System)는 이런 **이름 → 주소 정보 조회 시스템**이다.

중요한 점은 DNS가 웹 요청 자체를 대신 전달하는 Load Balancer가 아니라는 것이다. DNS는 우선 "어디로 갈지"를 알려준다.

---

## 2. Route 53란

Amazon Route 53는 AWS의 관리형 DNS 서비스다.

대표 역할은 다음과 같다.

```text
Domain Registration
DNS Routing
Health Checking
```

즉 도메인을 등록할 수도 있고, DNS 레코드를 관리할 수도 있고, 리소스 상태를 확인해 DNS 응답을 바꿀 수도 있다.

Route 53는 Authoritative DNS다. 쉽게 말하면 특정 도메인에 대해 **최종적으로 정답을 가지고 있는 DNS 서버** 역할을 할 수 있다는 뜻이다.

예:

```text
shop.example.com의 IP가 뭐야?
→ Route 53 Hosted Zone에 저장된 레코드를 기준으로 답변
```

---

## 3. Resolver와 Authoritative DNS 차이

사용자가 브라우저에 도메인을 입력했다고 바로 Route 53에 직접 묻는 것은 아니다.

대략적인 흐름은 다음과 같다.

```text
Browser
  ↓
DNS Resolver
  ↓ 필요하면 여러 DNS 서버 탐색
Authoritative DNS(Route 53 등)
  ↓
정답 반환
```

Resolver는 사용자를 대신해 답을 찾아오는 역할이고, Authoritative DNS는 해당 도메인의 공식 레코드를 보유한 역할이다.

### 비유

```text
Resolver
→ 도서관 사서: 필요한 책 정보를 찾아줌

Authoritative DNS
→ 원본 장부: 실제 정답이 적혀 있음
```

---

## 4. Route 53이라는 이름

DNS는 일반적으로 UDP/TCP 53번 포트를 사용한다. Route 53의 이름도 여기에서 왔다고 이해하면 된다.

---

## 예시

쇼핑몰이 있다고 하자.

```text
shop.example.com
```

Route 53에 다음과 같은 정보를 넣을 수 있다.

```text
shop.example.com
→ ALB
```

사용자는 서버의 긴 AWS DNS 이름이나 IP를 외울 필요 없이 도메인으로 접근한다.

```text
User
 ↓ shop.example.com
Route 53
 ↓ ALB 주소 반환
ALB
 ↓
Application
```

## SAA 포인트

```text
도메인 이름을 AWS 리소스에 연결
→ Route 53

DNS 기반 트래픽 분배 / 장애조치
→ Route 53 Routing Policy + Health Check

HTTP Path를 보고 요청 분기
→ Route 53가 아니라 ALB
```
