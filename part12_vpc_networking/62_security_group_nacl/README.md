# 62. Security Group과 NACL

## 1. 둘 다 네트워크 접근 제어지만 위치와 동작이 다르다

```text
Internet
   ↓
NACL          ← Subnet 경계
   ↓
Security Group ← ENI / EC2 등 리소스 경계
   ↓
EC2
```

## 2. Security Group

Security Group은 리소스의 ENI에 적용되는 stateful 방화벽이다.

특징:

- Allow rule만 사용한다.
- Inbound / Outbound를 구분한다.
- 응답 트래픽은 stateful 특성상 자동으로 허용된다.
- 다른 Security Group을 source/destination으로 참조할 수 있다.

실습 핵심 구조:

```text
ALB-SG
Inbound :80/:443 from Internet

EC2-SG
Inbound :80 from ALB-SG

RDS-SG
Inbound :5432 or :3306 from EC2-SG
```

이렇게 하면 정책 자체가 계층 관계를 표현한다.

## 3. NACL

Network ACL은 subnet 수준에서 적용되는 stateless 접근 제어다.

특징:

- Allow와 Deny rule을 모두 지원한다.
- rule number 순서대로 평가한다.
- stateless이므로 요청과 응답 방향을 각각 고려해야 한다.
- subnet에 연결된다.

## 4. SG와 NACL 비교

```text
Security Group
- ENI/리소스 수준
- Stateful
- Allow만
- 모든 rule을 종합
- SG reference 가능

NACL
- Subnet 수준
- Stateless
- Allow + Deny
- 낮은 rule number부터 평가
- CIDR 기반 제어
```

## 5. 장애 증상과 진단

### ALB는 접속되는데 Target이 unhealthy

```text
ALB-SG 정상?
→ EC2-SG가 ALB-SG를 허용하는가?
→ health check port/path 확인
→ NACL이 양방향 트래픽을 막는가?
```

### EC2 Public IP 직접 접속이 timeout

의도적으로 EC2-SG를 ALB-SG source만 허용했다면 정상적인 보안 결과일 수 있다.

## 6. Ephemeral Port 관점

NACL은 stateless이므로 TCP 응답 트래픽의 임시 포트 범위를 고려해야 할 수 있다. SG는 stateful이라 정상 요청에 대한 응답을 별도 inbound/outbound rule로 다시 허용하는 방식이 아니다.

실무 장애 진단에서 `SG는 열었는데 NACL 때문에 안 되는 상황`을 구분할 수 있어야 한다.

## 7. Recall Check

- SG가 stateful이라는 말은 무엇인가?
- NACL에서 Deny가 가능한 이유는?
- ALB-SG를 EC2-SG의 source로 쓰는 장점은?
- SG와 NACL 중 subnet 전체를 차단하려면 어느 쪽이 더 직접적인가?

## 8. 완료 기준

- [ ] SG/NACL 차이를 표 없이 설명할 수 있다.
- [ ] ALB → EC2 → RDS SG chain을 설계할 수 있다.
- [ ] SG reference의 의미를 설명할 수 있다.
- [ ] NACL의 stateless 특성과 rule order를 설명할 수 있다.
- [ ] timeout이 발생했을 때 SG/NACL을 어느 순서로 확인할지 말할 수 있다.
