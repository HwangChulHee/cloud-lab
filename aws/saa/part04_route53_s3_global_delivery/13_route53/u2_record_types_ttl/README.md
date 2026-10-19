# u2. DNS Record Types와 TTL

DNS에는 여러 종류의 레코드가 있다. 레코드는 쉽게 말하면 **도메인 이름에 대해 어떤 정보를 반환할지 적어둔 항목**이다.

## 1. A Record

도메인을 IPv4 주소에 연결한다.

```text
example.com
→ 203.0.113.10
```

시험에서 가장 기본적인 레코드다.

---

## 2. AAAA Record

도메인을 IPv6 주소에 연결한다.

```text
example.com
→ 2001:db8::1
```

A는 IPv4, AAAA는 IPv6라고 기억하면 된다.

---

## 3. CNAME Record

한 도메인 이름을 다른 도메인 이름에 연결한다.

```text
www.example.com
→ app.example.net
```

즉 CNAME은 "IP가 여기다"가 아니라 "이 이름의 정답은 저 이름을 다시 따라가라"에 가깝다.

### 중요한 제한

Zone Apex, 즉 루트 도메인 자체에는 일반적인 CNAME을 사용할 수 없다.

```text
example.com      ← zone apex
www.example.com  ← 하위 도메인
```

그래서 AWS 리소스를 루트 도메인에 연결할 때 Route 53 Alias Record가 중요해진다.

---

## 4. NS Record

NS(Name Server) 레코드는 **이 도메인의 DNS 정보를 어떤 Name Server가 관리하는지** 알려준다.

예를 들어 다른 업체에서 도메인을 구매했더라도 Route 53을 DNS 서비스로 쓸 수 있다.

```text
도메인 구매: 가비아
DNS 관리: Route 53
```

이 경우 Route 53 Hosted Zone을 만든 뒤, 가비아 쪽에 Route 53이 제공한 Name Server들을 NS로 등록한다.

즉:

```text
Domain Registrar != DNS Service
```

이다.

---

## 5. TTL

TTL(Time To Live)은 DNS 응답을 **얼마 동안 캐시해도 되는지** 나타내는 시간이다.

예:

```text
TTL = 300초
```

Resolver가 `example.com → 1.2.3.4`를 한 번 조회하면 300초 동안 그 결과를 재사용할 수 있다.

### TTL이 길면

```text
DNS 조회 감소
비용/부하 감소
하지만 변경 반영이 느림
```

### TTL이 짧으면

```text
변경이 빨리 반영됨
하지만 DNS 조회 증가
```

예를 들어 서버 이전 직전에 DNS를 곧 바꿀 계획이면 TTL을 미리 낮추는 전략을 생각할 수 있다.

---

## 예시

```text
A
api.example.com → 203.0.113.10

AAAA
api.example.com → 2001:db8::10

CNAME
www.example.com → shop.example.com

NS
example.com → Route 53 Name Servers
```

## SAA 포인트

```text
IPv4
→ A

IPv6
→ AAAA

다른 hostname을 가리킴
→ CNAME

도메인의 authoritative name server 지정
→ NS

DNS 응답 캐시 시간
→ TTL
```
