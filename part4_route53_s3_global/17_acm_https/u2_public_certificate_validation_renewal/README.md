# u2. Public Certificate Validation & Renewal

ACM에서 Public Certificate를 요청하면 AWS는 "정말 이 도메인을 제어할 권한이 있는가"를 확인해야 한다. 이 과정을 Domain Validation이라고 생각하면 된다.

## 1. FQDN과 Wildcard

예:

```text
shop.example.com
api.example.com
```

처럼 완전한 도메인 이름을 FQDN(Fully Qualified Domain Name)이라고 한다.

Wildcard Certificate는 여러 하위 도메인을 한 번에 포함할 때 쓸 수 있다.

```text
*.example.com
```

이 인증서는 `shop.example.com`, `api.example.com` 같은 1단계 하위 도메인에 사용할 수 있다.

## 2. DNS Validation

DNS Validation은 DNS에 ACM이 요구하는 CNAME Record를 추가해 도메인 소유를 증명하는 방식이다.

```text
ACM
→ "이 CNAME을 DNS에 추가하세요"

Route 53
→ CNAME 추가

ACM
→ Record 확인
→ 인증서 발급
```

자동화하기 쉽기 때문에 강의에서는 DNS Validation을 선호하는 방식으로 설명한다.

## 3. Email Validation

도메인 관련 연락처로 검증 메일을 보내 승인을 받는 방식도 있다.

```text
ACM → Validation Email → 승인 → 인증서 발급
```

자동화 측면에서는 DNS Validation보다 불편할 수 있다.

## 4. Automatic Renewal

ACM이 직접 발급하고 관리하는 Public Certificate는 자동 갱신을 지원한다.

즉 사람이 매번 만료 직전에 새 인증서를 만들어 교체하는 부담을 줄일 수 있다.

DNS Validation을 사용하고 필요한 DNS Record가 유지되어 있으면 자동 갱신 운영에 특히 유리하다.

## 예시

`shop.example.com` 인증서를 만든다고 하자.

```text
1. ACM에서 shop.example.com 요청
2. DNS Validation 선택
3. Route 53에 ACM CNAME 추가
4. 검증 완료
5. ALB HTTPS Listener에 인증서 연결
6. 이후 ACM이 인증서 갱신 관리
```

## SAA 판단

```text
자동화하기 쉬운 Domain Validation
→ DNS Validation

DNS에 검증 Record 추가
→ CNAME

사람의 이메일 승인이 필요한 방식
→ Email Validation

ACM이 발급한 Public Certificate
→ Automatic Renewal 지원
```
