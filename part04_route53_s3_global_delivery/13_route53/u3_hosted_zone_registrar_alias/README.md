# u3. Hosted Zone, Registrar와 Alias

## 1. Hosted Zone

Hosted Zone은 Route 53에서 **특정 도메인의 DNS 레코드를 모아 관리하는 공간**이다.

예를 들어 `example.com`을 관리한다면:

```text
Hosted Zone: example.com
├── example.com
├── www.example.com
├── api.example.com
└── admin.example.com
```

각 이름에 A, AAAA, Alias 등의 레코드를 저장한다.

Hosted Zone은 크게 두 종류가 있다.

```text
Public Hosted Zone
→ 인터넷에서 조회하는 공개 DNS 레코드

Private Hosted Zone
→ 연결된 VPC 내부에서 사용하는 사설 DNS 레코드
```

예를 들어 내부 DB나 사내 서비스 이름을 인터넷에 공개하지 않고 VPC 내부에서만 해석하고 싶으면 Private Hosted Zone을 사용할 수 있다.

---

## 2. Domain Registrar와 DNS Service

Domain Registrar는 **도메인을 등록/구매하는 곳**이다.

DNS Service는 **그 도메인의 DNS 레코드를 실제 관리하는 곳**이다.

둘은 같을 필요가 없다.

예:

```text
가비아에서 example.com 구매
        ↓
Route 53에 example.com Public Hosted Zone 생성
        ↓
가비아에 Route 53 Name Server(NS) 등록
        ↓
DNS 레코드는 Route 53에서 관리
```

따라서 "도메인을 AWS에서 안 샀으니 Route 53을 못 쓴다"는 잘못된 생각이다.

---

## 3. Alias Record

Alias는 Route 53의 AWS 전용 기능으로, DNS 이름을 AWS 리소스에 연결할 때 자주 사용한다.

대표 대상 예:

```text
Application Load Balancer
CloudFront Distribution
S3 Website Endpoint
API Gateway
다른 Route 53 Record
```

### CNAME과 비슷한데 왜 Alias가 필요한가

예를 들어 루트 도메인:

```text
example.com
```

을 ALB에 연결하고 싶다고 하자.

일반 CNAME은 zone apex에서 쓸 수 없지만 Alias는 가능하다.

```text
example.com
→ Alias → ALB
```

또한 Alias 레코드는 AWS 리소스의 IP가 바뀌더라도 사용자가 직접 IP를 관리할 필요가 없게 해준다.

---

## 4. Alias와 TTL

Alias 레코드에서는 대상 AWS 리소스의 정보를 Route 53이 처리하므로 일반 레코드처럼 사용자가 TTL을 직접 설정하는 방식과 다르다.

시험에서는 세부 구현보다 다음 구분이 중요하다.

```text
AWS 리소스를 가리킴
zone apex에서도 사용
→ Alias

일반 DNS 이름을 다른 DNS 이름으로 매핑
→ CNAME
```

---

## 예시

쇼핑몰 구조:

```text
User
 ↓ shop.example.com
Route 53
 ↓ Alias
ALB
 ↓
EC2 / ECS
```

서버가 교체되거나 ALB 내부 IP가 바뀌더라도 사용자는 `shop.example.com`만 사용한다.

## SAA 포인트

```text
외부 공개 DNS
→ Public Hosted Zone

VPC 내부 DNS
→ Private Hosted Zone

다른 registrar에서 산 도메인을 Route 53 DNS로 사용
→ Hosted Zone 생성 + registrar의 NS 변경

루트 도메인을 ALB/CloudFront 같은 AWS 리소스에 연결
→ Alias
```
