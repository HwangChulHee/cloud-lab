# Example 13 — Route 53 + ACM + HTTPS

지금까지 ALB DNS 이름으로 접속하던 서비스를 실제 보유 도메인과 HTTPS로 연결한다.

이 실습에서는 루트 도메인 `chulheehwang.com` 자체를 직접 건드리기보다 **실습용 서브도메인**을 사용한다.

```text
lab.chulheehwang.com
```

루트 도메인은 다른 서비스에 사용할 수 있으므로 장애 실험도 `lab.chulheehwang.com`에서만 수행한다.

## Recall Check
- ALB Listener와 Target Group의 관계는?
- ALB-SG와 EC2-SG는 어떻게 연결했나?
- DNS는 무엇을 해결하는가?
- Registrar와 DNS Service는 왜 같은 개념이 아닌가?

## 새로 배우는 것
- Hosted Zone
- A / CNAME / Alias
- ACM Certificate
- DNS Validation
- HTTPS Listener
- HTTP → HTTPS Redirect

## 반복하는 것
ALB, Target Group, Security Group, Health Check, Route 53 record 확인을 반복한다.

## 이번에는 도움 없이
ALB + Target Group + EC2/ASG 기본 구조는 요구사항만 보고 구성한다.

## 목표 구조
```text
User
 ↓
lab.chulheehwang.com
 ↓ DNS
Route 53
 ↓ A Alias
ALB :443
 ↓
EC2 / ASG

ACM
└─ lab.chulheehwang.com certificate
```

## 1. chulheehwang.com의 DNS 관리 위치 확인

먼저 `chulheehwang.com`을 어디에서 구매했는지와 별개로, 현재 authoritative DNS가 어디인지 확인한다.

Route 53 Hosted Zone을 사용할 경우:

```text
chulheehwang.com Hosted Zone
└─ NS record
```

Registrar가 AWS 외부라면 Registrar 측 nameserver가 Route 53 Hosted Zone의 NS를 가리키는지 확인한다.

이 단계의 목표는 다음 흐름을 설명하는 것이다.

```text
Registrar
  ↓ NS delegation
Route 53 Hosted Zone
  ↓ record lookup
lab.chulheehwang.com
```

## 2. 실습용 ACM 인증서 발급

ALB가 있는 **같은 AWS Region**에서 다음 이름으로 ACM public certificate를 요청한다.

```text
lab.chulheehwang.com
```

DNS Validation을 선택하고 Route 53에 validation record를 만든다.

확인할 것:
- Certificate status가 `Issued`가 되는가?
- Validation용 CNAME record가 Hosted Zone에 존재하는가?
- 왜 DNS Validation이 도메인 소유권 확인이 되는가?

## 3. ALB HTTPS Listener 추가

- HTTPS : 443
- ACM certificate: `lab.chulheehwang.com`
- Default action: 기존 Target Group forward

ALB-SG에도 443 inbound를 허용한다.

## 4. Route 53 Alias Record

Hosted Zone `chulheehwang.com`에 다음 record를 만든다.

```text
Name   : lab.chulheehwang.com
Type   : A
Alias  : Yes
Target : Example 13 ALB
```

확인:

```text
lab.chulheehwang.com
→ Route 53
→ ALB
→ Target Group
→ EC2
```

로컬에서도 확인한다.

```bash
dig lab.chulheehwang.com
curl -I https://lab.chulheehwang.com
```

## 5. HTTP → HTTPS Redirect

HTTP :80 Listener의 action을 HTTPS :443 redirect로 바꾼다.

```bash
curl -I http://lab.chulheehwang.com
```

응답의 `Location`이 HTTPS 주소를 가리키는지 확인하고 브라우저에서도 실제 접속한다.

```text
https://lab.chulheehwang.com
```

## 장애 실험 A — DNS Record 오류

**루트 도메인 `chulheehwang.com`은 변경하지 않는다.**

`lab.chulheehwang.com`의 Alias를 잘못된 대상으로 바꾸거나, 별도 테스트 이름을 사용한다.

예:

```text
broken.lab.chulheehwang.com
```

관찰할 것:
- DNS lookup 자체가 실패하는 경우
- DNS는 성공하지만 잘못된 endpoint로 가는 경우
- ALB/Target 문제와 DNS 문제의 차이

실험 후 record를 원래 상태로 복구한다.

## 장애 실험 B — HTTPS 계층 분리

다음을 각각 구분해서 관찰하거나 설명한다.

```text
DNS 정상 + 443 SG 차단
DNS 정상 + HTTPS Listener 없음
DNS 정상 + certificate hostname 불일치
DNS 정상 + Target unhealthy
```

중요한 것은 모두 "사이트가 안 된다"로 보이더라도 실패 계층이 다르다는 점이다.

## 관찰
- Alias와 CNAME의 차이는 무엇인가?
- `lab.chulheehwang.com`은 왜 A Alias로 ALB를 가리킬 수 있는가?
- HTTPS 암호화는 Client→ALB까지만 할 수도 있는가?
- ACM 인증서는 ALB의 어느 Listener와 연결되는가?
- DNS가 정상이라는 것과 애플리케이션이 정상이라는 것은 왜 다른가?

## 기억만으로 설명하기

브라우저에 `https://lab.chulheehwang.com`을 입력한 순간부터 EC2 응답까지 다음 순서로 설명한다.

```text
DNS
→ Route 53 Alias
→ ALB
→ TLS/ACM
→ HTTPS Listener
→ Target Group
→ EC2
```

## 완료 체크
- [ ] `chulheehwang.com`의 DNS 관리 위치와 NS 위임을 확인했다.
- [ ] `lab.chulheehwang.com` ACM Certificate를 발급했다.
- [ ] DNS Validation 과정을 확인했다.
- [ ] ALB에 443 Listener를 연결했다.
- [ ] Route 53 A Alias로 ALB를 연결했다.
- [ ] `https://lab.chulheehwang.com` 실제 접속에 성공했다.
- [ ] HTTP → HTTPS redirect를 확인했다.
- [ ] `dig`/`curl`로 DNS와 HTTPS를 각각 확인했다.
- [ ] DNS 문제와 ALB/backend 문제를 구분해 설명할 수 있다.

## 비용 정리

실습 종료 후 ALB/EC2 등 과금 리소스는 삭제한다.

`chulheehwang.com` Hosted Zone과 도메인은 실제 보유 자산일 수 있으므로 **무조건 삭제하지 않는다.** `lab.chulheehwang.com` 실습 record는 이후 Example 16에서 재사용하지 않는다면 삭제해도 된다.
