# Example 04 — Security Group을 계층별로 나누기

Example 02~03의 구조를 그대로 사용한다. 이제 EC2의 HTTP 포트를 인터넷 전체에 열지 않고, **ALB를 통해 들어온 요청만 EC2가 받도록** 변경한다.

```text
Internet
   ↓ TCP 80 from 0.0.0.0/0
ALB-SG
   ↓ TCP 80, source = ALB-SG
EC2-SG
```

## 목표

- Security Group Reference를 실제로 사용한다.
- IP/CIDR 허용과 Security Group 참조의 차이를 이해한다.
- 사용자는 ALB에는 접근할 수 있지만 EC2에는 직접 접근할 수 없는 구조를 만든다.
- 계층별 접근 제어가 왜 필요한지 체감한다.

## 1. 현재 구조 확인

Example 02에서 EC2 Security Group이 다음과 같다면 인터넷의 누구든 EC2 Public IP를 알고 있을 때 직접 요청할 수 있다.

```text
HTTP TCP 80 0.0.0.0/0
```

확인한다.

```text
http://<EC2_A_PUBLIC_IP>
http://<EC2_B_PUBLIC_IP>
```

## 2. ALB Security Group

ALB-SG inbound는 다음처럼 둔다.

```text
HTTP TCP 80 0.0.0.0/0
```

즉 인터넷 사용자는 ALB의 HTTP 80 포트까지 접근할 수 있다.

## 3. EC2 Security Group 수정

EC2-SG의 기존 HTTP rule을 삭제한다.

```text
HTTP TCP 80 0.0.0.0/0
```

대신 source에 IP/CIDR이 아니라 ALB-SG를 지정한다.

```text
HTTP TCP 80 Source: ALB-SG
```

## 4. ALB를 통한 요청 확인

ALB DNS 이름으로 접근한다.

```text
Client
  ↓
ALB-SG가 Client 요청 허용
  ↓
ALB
  ↓
EC2-SG가 ALB-SG에서 온 트래픽 허용
  ↓
EC2
```

정상적으로 응답해야 한다.

## 5. EC2 직접 접근 확인

EC2 Public IP로 직접 접속한다.

```text
http://<EC2_A_PUBLIC_IP>
```

예상 결과는 접속 실패 또는 timeout이다. EC2에 Public IP가 있어도 HTTP source가 ALB-SG로 제한되어 있기 때문이다.

## 6. 구조 비교

나쁜 예:

```text
EC2-SG
HTTP 80 from 0.0.0.0/0

User ─────────→ EC2
  └→ ALB ─────→ EC2
```

개선된 예:

```text
ALB-SG
HTTP 80 from 0.0.0.0/0

EC2-SG
HTTP 80 from ALB-SG

User → ALB → EC2
User ──X──→ EC2
```

## 7. 왜 IP 대신 Security Group Reference인가?

특정 IP 하나를 허용하는 것보다 "ALB 계층에서 온 트래픽만 허용"한다는 의도를 정책에 직접 표현할 수 있다. 나중에 ALB의 내부 IP가 바뀌거나 EC2가 추가·교체되어도 동일한 SG 관계를 유지할 수 있다.

## 8. SSH도 분리하기

SSH가 필요하더라도 인터넷 전체에 열지 않는다.

```text
나쁜 예: SSH TCP 22 0.0.0.0/0
실습 예: SSH TCP 22 <MY_PUBLIC_IP>/32
```

운영 환경에서는 Bastion Host나 Systems Manager Session Manager 같은 방법도 고려할 수 있다. 여기서는 SG의 기본 원리에 집중한다.

## 9. 장애 실험 — ALB → EC2 허용 제거

EC2-SG의 다음 rule을 잠시 삭제한다.

```text
HTTP TCP 80 Source: ALB-SG
```

ALB DNS로 요청하고 다음 흐름을 관찰한다.

```text
Client → ALB   도달 가능
ALB → EC2      차단
```

Target Group Health Check도 실패하면서 Target이 unhealthy가 될 수 있다. 다시 rule을 복구하고 healthy로 돌아오는지 확인한다.

## 10. 직접 설명하기

```text
Q1. ALB-SG와 EC2-SG를 왜 따로 만드는가?
Q2. EC2-SG source를 ALB-SG로 지정한다는 것은 무슨 뜻인가?
Q3. EC2에 Public IP가 있어도 직접 접근이 막힐 수 있는 이유는?
Q4. EC2를 Private Subnet으로 옮기면 무엇이 더 달라지는가?
```

## 11. 완료 체크

- [ ] ALB-SG와 EC2-SG를 구분했다.
- [ ] ALB는 인터넷에서 접근 가능하다.
- [ ] EC2 HTTP source를 ALB-SG로 제한했다.
- [ ] ALB DNS를 통한 요청은 성공한다.
- [ ] EC2 Public IP 직접 요청은 실패한다.
- [ ] EC2-SG rule 제거로 Health Check 실패를 관찰했다.
- [ ] Security Group Reference의 의미를 설명할 수 있다.

## 12. 현재까지의 구조

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

여기까지 이해하면 다음 VPC/ASG 예제에서 같은 SG 계층 구조를 자연스럽게 반복할 수 있다. 다음 예제부터 VPC를 직접 만들고, 이후 Auto Scaling Group으로 수동 EC2 구조를 자동화한다.
