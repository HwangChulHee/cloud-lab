# Example 13 — Route 53 + ACM + HTTPS

지금까지 ALB DNS 이름으로 접속하던 서비스를 실제 도메인과 HTTPS로 연결한다.

## Recall Check
- ALB Listener와 Target Group의 관계는?
- ALB-SG와 EC2-SG는 어떻게 연결했나?
- DNS는 무엇을 해결하는가?

## 새로 배우는 것
- Hosted Zone
- A / CNAME / Alias
- ACM Certificate
- HTTPS Listener
- HTTP → HTTPS Redirect

## 반복하는 것
ALB, Target Group, Security Group, Health Check, Route 53 record 확인을 반복한다.

## 이번에는 도움 없이
ALB + Target Group + EC2/ASG 기본 구조는 요구사항만 보고 구성한다.

## 목표 구조
```text
User
 ↓ DNS
Route 53
 ↓ Alias
ALB :443
 ↓
EC2 / ASG
```

## 1. 도메인과 Hosted Zone 확인
보유한 도메인을 Route 53 Hosted Zone에서 관리하거나, 다른 Registrar를 쓴다면 NS 위임 구조를 확인한다.

## 2. ACM 인증서 발급
서비스할 도메인 이름으로 public certificate를 요청하고 DNS Validation을 완료한다.

## 3. ALB HTTPS Listener 추가
- HTTPS : 443
- ACM certificate 연결
- Default action: 기존 Target Group forward

ALB-SG에도 443 inbound를 허용한다.

## 4. Route 53 Alias Record
도메인에 A Alias Record를 만들고 대상은 ALB로 지정한다.

확인:
```text
Domain → Route 53 → ALB → Target Group → EC2
```

## 5. HTTP → HTTPS Redirect
HTTP :80 Listener의 action을 HTTPS :443 redirect로 바꾼다.

브라우저에서 `http://`로 접근했을 때 `https://`로 전환되는지 확인한다.

## 장애 실험 A — 잘못된 Record
Alias 대상을 잠시 잘못 설정하거나 별도 테스트 record를 만들어 DNS 해석 실패/잘못된 대상 증상을 관찰한다.

## 장애 실험 B — Certificate 불일치 생각하기
인증서의 도메인 이름과 실제 접속 hostname이 다르면 왜 브라우저가 경고하는지 설명한다.

## 관찰
- Alias와 CNAME의 차이는 무엇인가?
- HTTPS 암호화는 Client→ALB까지만 할 수도 있는가?
- ACM 인증서는 ALB의 어느 Listener와 연결되는가?

## 기억만으로 설명하기
브라우저 주소 입력부터 EC2 응답까지 `DNS → TLS → Listener → Target Group → EC2` 순서로 설명한다.

## 완료 체크
- [ ] Hosted Zone/NS를 확인했다.
- [ ] ACM Certificate를 발급했다.
- [ ] ALB에 443 Listener를 연결했다.
- [ ] Route 53 Alias로 ALB를 연결했다.
- [ ] HTTP → HTTPS redirect를 확인했다.
- [ ] DNS 문제와 ALB 문제를 구분해 설명할 수 있다.

## 비용 정리
도메인/Hosted Zone은 유지 비용을 확인한다. 실습용 ALB/EC2는 필요 없으면 삭제한다.
