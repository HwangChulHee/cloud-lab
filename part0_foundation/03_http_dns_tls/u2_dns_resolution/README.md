# u2. DNS Resolution

## 지도 확인

사용자는 보통 IP 주소가 아니라 도메인 이름으로 서비스에 접근한다.

```text
https://api.example.com
        ↓ DNS
IP 또는 AWS endpoint
        ↓
Server / Load Balancer / CDN
```

SAA 강의의 Route 53 파트에서도 DNS를 사람이 읽는 hostname을 IP 주소 등 네트워크 대상으로 연결하는 인터넷의 핵심 기반으로 설명한다.

---

## 1. DNS가 하는 일

DNS(Domain Name System)는 이름을 네트워크에서 사용할 수 있는 대상으로 해석한다.

```text
example.com
    ↓
203.0.113.10
```

실제로는 한 번에 하나의 서버에 묻는 구조가 아니라 resolver, root, TLD, authoritative name server 등이 계층적으로 참여한다.

---

## 2. 이름의 계층

```text
api.example.com
│   │       └─ TLD: .com
│   └───────── domain: example.com
└───────────── subdomain: api
```

AWS에서는 Route 53 Hosted Zone 안에 해당 도메인의 DNS record들을 관리하게 된다.

---

## 3. 기본 Record

SAA에서 특히 자주 보는 종류:

```text
A      hostname → IPv4
AAAA   hostname → IPv6
CNAME  hostname → 다른 hostname
NS     zone을 담당하는 name server
```

AWS에서는 뒤에서 **Alias record**도 중요하게 다룬다. Load Balancer, CloudFront 같은 AWS 리소스와 연결할 때 CNAME과 비교하게 된다.

---

## 4. TTL과 Cache

DNS 결과는 매 요청마다 authoritative server까지 다시 찾지 않고 일정 시간 cache된다.

TTL(Time To Live)은 그 cache를 얼마나 유지할지 정한다.

```text
TTL 큼
→ DNS 질의 감소
→ 변경 전파는 상대적으로 느림

TTL 작음
→ 변경 반영이 빠름
→ DNS 질의 증가
```

따라서 DNS record를 변경했다고 해서 모든 사용자가 즉시 새 값을 보는 것은 아닐 수 있다.

---

## 5. DNS 확인

```bash
nslookup example.com
dig example.com
```

문제가 있을 때 다음을 구분한다.

```text
도메인 해석 자체가 실패하는가?
DNS는 정상인데 HTTP 연결이 실패하는가?
예상한 주소가 아니라 오래된 주소가 반환되는가?
```

DNS 문제와 서버/네트워크 문제를 분리하는 것이 핵심이다.

---

## 6. AWS 연결

뒤에서 다음 구조를 직접 만든다.

```text
User
 ↓
Route 53
 ↓
Application Load Balancer
 ↓
Application
```

그리고 정적 콘텐츠에서는:

```text
User
 ↓
Route 53
 ↓
CloudFront
 ↓
S3 / Origin
```

형태도 만나게 된다.

## SAA 연결

Route 53에서는 이후 A/AAAA/CNAME/NS, Hosted Zone, Alias, TTL, health check, routing policy를 본격적으로 공부한다. 이번 유닛은 그 전제인 DNS resolution만 잡는다.

기초 개념이므로 별도 유제와 3문장 요약은 생략한다.
