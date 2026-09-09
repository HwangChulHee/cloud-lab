# Example 04 — Security Group을 계층별로 나누기

Example 02~03의 구조를 그대로 사용한다.

이제 EC2의 HTTP 포트를 인터넷 전체에 열지 않고, **ALB를 통해 들어온 요청만 EC2가 받도록** 변경한다.

```text
Internet
   ↓
ALB
   ↓
EC2
```

Security Group 기준으로 보면 다음과 같다.

```text
Internet
   ↓ TCP 80 from 0.0.0.0/0
ALB-SG
   ↓ TCP 80, source = ALB-SG
EC2-SG
```

## 목표

- Security Group Reference를 실제로 사용한다.
- "IP를 허용"하는 방식과 "다른 Security Group을 허용"하는 방식의 차이를 이해한다.
- 사용자는 ALB에는 접근할 수 있지만 EC2에는 직접 접근할 수 없는 구조를 만든다.
- 계층별 접근 제어가 왜 필요한지 체감한다.

## 1. 현재 구조 확인

Example 02에서 EC2 Security Group을 다음처럼 만들었다면:

```text
HTTP TCP 80 0.0.0.0/0
```

인터넷의 누구든 EC2 Public IP를 알고 있다면 직접 요청할 수 있다.

확인한다.

```text
http://<EC2_A_PUBLIC_IP>
http://<EC2_B_PUBLIC_IP>
```

현재는 둘 다 접속될 가능성이 높다.

## 2. ALB Security Group 확인

ALB용 Security Group을 `example-alb-sg`라고 가정한다.

Inbound:

```text
HTTP TCP 80 0.0.0.0/0
```

의미:

> 인터넷 사용자는 ALB의 HTTP 80 포트에 접근할 수 있다.

## 3. EC2 Security Group 수정

EC2용 Security Group의 기존 HTTP rule을 삭제한다.

삭제:

```text
HTTP TCP 80 0.0.0.0/0
```

대신 다음 rule을 추가한다.

```text
HTTP TCP 80 Source: example-alb-sg
```

즉 source에 IP/CIDR이 아니라 **ALB의 Security Group**을 지정한다.

## 4. ALB를 통한 요청 확인

다시 ALB DNS 이름으로 접근한다.

```text
http://<ALB_DNS_NAME>
```

정상적으로 응답해야 한다.

요청 흐름:

```text
Client
  ↓
ALB-SG가 Client의 요청 허용
  ↓
ALB
  ↓
EC2-SG가 ALB-SG에서 온 트래픽 허용
  ↓
EC2
```

## 5. EC2 직접 접근 확인

이번에는 EC2 Public IP로 직접 접속한다.

```text
http://<EC2_A_PUBLIC_IP>
```

예상:

```text
접속 실패 또는 timeout
```

왜냐하면 이 요청은 ALB Security Group을 가진 네트워크 인터페이스에서 온 트래픽이 아니기 때문이다.

## 6. 핵심 비교

### 나쁜 예

```text
EC2-SG
Inbound: HTTP 80 from 0.0.0.0/0
```

구조:

```text
User ─────────→ EC2
  └→ ALB ─────→ EC2
```

ALB를 우회할 수 있다.

### 개선된 예

```text
ALB-SG
HTTP 80 from 0.0.0.0/0

EC2-SG
HTTP 80 from ALB-SG
```

구조:

```text
User → ALB → EC2
User ──X──→ EC2
```

## 7. 왜 IP가 아니라 Security Group Reference인가?

ALB 뒤에 있는 IP 주소를 직접 하나씩 등록하는 방식보다 Security Group을 참조하면 구조의 의미를 그대로 정책으로 표현할 수 있다.

```text
"10.0.1.15만 허용"
```

보다

```text
"ALB 계층에서 온 요청만 허용"
```

에 가깝다.

나중에 EC2가 추가되거나 교체되어도 같은 EC2 Security Group을 붙이면 동일한 정책을 적용할 수 있다.

## 8. SSH도 분리해보기

SSH가 필요한 경우 다음처럼 인터넷 전체에 열지 않는다.

나쁜 예:

```text
SSH TCP 22 0.0.0.0/0
```

실습용 예:

```text
SSH TCP 22 <MY_PUBLIC_IP>/32
```

운영 환경에서는 Bastion Host나 Systems Manager Session Manager 같은 방식도 고려할 수 있지만, 이 예제에서는 Security Group의 기본 원리를 이해하는 데 집중한다.

## 9. 장애 실험 — ALB SG 연결 끊기

EC2-SG의 다음 rule을 잠시 삭제한다.

```text
HTTP TCP 80 Source: ALB-SG
```

ALB DNS로 요청한다.

예상:

```text
Client → ALB   성공
ALB → EC2      차단
```

Target Group Health Check도 실패하면서 Target이 unhealthy로 바뀔 수 있다.

다시 rule을 복구하고 Target이 healthy로 돌아오는지 확인한다.

## 10. 직접 설명하기

```text
Q1. ALB-SG와 EC2-SG를 왜 따로 만드는가?
→

Q2. EC2-SG의 source를 ALB-SG로 지정한다는 것은 무슨 뜻인가?
→

Q3. EC2에 Public IP가 있어도 직접 접근이 막힐 수 있는 이유는?
→

Q4. 나중에 EC2를 Private Subnet으로 옮기면 이 구조에서 무엇이 더 달라질까?
→
```

## 11. 완료 체크

- [ ] ALB-SG와 EC2-SG를 구분했다.
- [ ] ALB는 인터넷에서 접근 가능하다.
- [ ] EC2의 HTTP source를 ALB-SG로 제한했다.
- [ ] ALB DNS를 통한 요청은 성공한다.
- [ ] EC2 Public IP 직접 요청은 실패한다.
- [ ] EC2-SG rule을 제거해 Health Check 실패를 관찰했다.
- [ ] Security Group Reference의 의미를 설명할 수 있다.

## 12. Example 단계에서 지금까지 만든 구조

```text
                 Internet
                    ↓
              [ ALB-SG :80 ]
                    ↓
                   ALB
                    ↓
              Target Group
                 ↙     ↘
           EC2-A         EC2-B
              [ EC2-SG :80 ]
            source = ALB-SG
```

여기까지 이해하면 `labs/01-high-availability-web`을 바로 푸는 것보다 훨씬 수월해진다.

다음 학습에서 Auto Scaling Group을 배운 뒤에는 EC2를 사람이 직접 두 대 만드는 구조를 자동화하는 Example을 추가한다.
