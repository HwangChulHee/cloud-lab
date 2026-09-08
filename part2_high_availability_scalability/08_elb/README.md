# 08. Elastic Load Balancing

SAA 강의의 High Availability & Scalability 섹션에서 Elastic Load Balancing 부분을 정리한다.

시험 전에는 강의 흐름과 서비스 선택 기준을 중심으로 본다. 장애 실험과 Cloud Shop 적용은 SAA 취득 후 Core Lab 단계에서 다시 진행한다.

## Units

- [ ] u1. Elastic Load Balancing Overview & Health Checks
- [ ] u2. Application Load Balancer (ALB)
- [ ] u3. Network Load Balancer (NLB)
- [ ] u4. Gateway Load Balancer (GWLB)
- [ ] u5. Sticky Sessions & Cross-Zone Load Balancing
- [ ] u6. TLS, SNI & Connection Draining

## SAA 선택 지도

```text
HTTP/HTTPS + Path/Host routing
→ ALB

TCP/UDP + 매우 높은 성능 + 고정 IP
→ NLB

Firewall / IDS / IPS / 네트워크 appliance
→ GWLB

비정상 Target 제외
→ Health Check

같은 사용자를 같은 Target으로 유지
→ Sticky Session

AZ 전체 Target에 걸친 분산
→ Cross-Zone Load Balancing

여러 도메인의 TLS 인증서
→ SNI

Target 제거 중 기존 요청 완료
→ Deregistration Delay
```

다음 단원은 Auto Scaling Group으로 이어진다.
