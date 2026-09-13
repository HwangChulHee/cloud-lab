# Example 06 — EC2를 Private Subnet에 배치하기

이제 웹 서버를 인터넷에 직접 노출하지 않고 ALB를 통해서만 접근하도록 바꾼다. 이번 예제의 핵심은 **Private Subnet의 inbound와 outbound를 분리해서 이해하는 것**이다.

## Recall Check

- Public Subnet의 조건은 무엇이었나?
- ALB-SG → EC2-SG Reference는 어떻게 구성했나?
- ALB Listener와 Target Group의 관계는?
- Route Table과 Security Group은 각각 무엇을 결정했나?

## 새로 배우는 것

- Private Subnet의 실제 의미
- Public ALB + Private EC2 구조
- Private EC2의 outbound 경로
- NAT Gateway
- Session Manager / IAM Role
- Private EC2 bootstrap 실패 원인

## 반복하는 것

- VPC / Subnet / Route Table
- ALB / Target Group
- EC2 / Security Group
- Health Check

## 이번에는 도움 없이

다음은 이전 README를 보지 않고 먼저 구성한다.

- ALB-SG: HTTP 80 from Internet
- EC2-SG: HTTP 80 from ALB-SG
- Target Group과 Listener 연결

모든 태그 가능 리소스에 다음 태그를 붙인다.

```text
Project=cloud-lab
Stage=examples
Example=06
```

## 목표 구조

```text
Internet
   ↓
Public Subnet
   ALB
   ↓ VPC local routing
Private Subnet
   EC2

Private EC2 outbound가 필요할 때:
EC2 → Private RT → NAT Gateway(public subnet) → IGW → Internet
```

## 1. 네트워크 준비

Example 05의 VPC를 재사용하거나 동일 구조를 다시 만든다.

- Public Subnet 2개
- Private Subnet 2개
- Public RT: Internet Gateway로 향하는 default route 보유
- Private RT: 처음에는 VPC 내부 local route만 유지

## 2. ALB 생성

Internet-facing ALB를 두 Public Subnet에 배치한다. Target Group은 HTTP 80을 사용한다.

## 3. Private EC2 생성 — 일부러 outbound 없는 상태부터 시작

EC2를 Private Subnet에 만들고 Public IPv4를 비활성화한다.

먼저 NAT Gateway 없이 시작한다. User Data가 외부 저장소에서 nginx를 설치하도록 구성한다면 package download 단계가 실패할 수 있다.

예:

```bash
#!/bin/bash
dnf install -y nginx
systemctl enable --now nginx
```

Target Group에서 unhealthy가 된다면 다음 후보를 구분해서 본다.

```text
SG 문제인가?
Health Check 문제인가?
애플리케이션이 설치/실행되지 않았는가?
User Data가 외부 인터넷 접근 실패로 중단됐는가?
```

가능하면 콘솔 로그나 접근 가능한 관리 경로에서 cloud-init 로그를 확인한다.

```bash
sudo tail -n 100 /var/log/cloud-init-output.log
```

## 4. NAT Gateway로 outbound 경로 추가

Public Subnet에 NAT Gateway를 생성하고 Elastic IP를 연결한다. Private Route Table의 인터넷 default route가 NAT Gateway를 가리키게 한다.

이후 **새 Private EC2를 다시 생성**해서 동일 User Data가 정상 실행되는지 확인한다. 기존 인스턴스에서 수동 재실행하는 것보다 bootstrap 성공/실패 비교가 쉽다.

```text
NAT 없음
→ private EC2 outbound 인터넷 불가
→ package download 실패 가능
→ app 시작 실패
→ target unhealthy

NAT 있음
→ package download 성공
→ app 실행
→ health check 성공
→ target healthy
```

## 5. ALB 요청 확인

ALB DNS 이름으로 접속한다.

```text
Client → ALB(public) → EC2(private)
```

EC2에 Public IP가 없어도 서비스가 가능한 이유를 VPC local routing과 Security Group 관점에서 설명한다.

## 6. 직접 접근 불가 확인

Private EC2에 Public IPv4가 없는지 확인한다. 인터넷에서 EC2로 직접 들어갈 주소가 없다는 점을 Example 04의 SG 차단 방식과 비교한다.

## 7. Session Manager로 관리 접근 — NAT가 있는 동안 확인

SSH 22를 인터넷에 열지 않는 방향을 실습한다.

가능하면 EC2에 `AmazonSSMManagedInstanceCore` 권한이 있는 IAM Role을 연결하고 Session Manager를 사용한다.

SSM 통신에는 다음 중 하나가 필요하다.

```text
A. NAT/인터넷 outbound
B. 필요한 Systems Manager용 VPC Interface Endpoint 구성
```

이번 순서에서는 **NAT가 아직 살아 있는 동안 먼저 Session Manager 접속을 확인**한다. `PingStatus=Online`과 실제 세션 연결을 확인한 뒤 다음 단계로 간다.

심화로 VPC Endpoint 방식을 선택한다면 NAT를 제거하기 전에 endpoint 구성을 완료하고 SSM이 계속 Online인지 검증한다.

## 8. NAT route를 제거해 inbound/outbound 차이 확인

Private Route Table의 NAT default route를 잠시 제거한다.

비교한다.

```text
사용자 → ALB → EC2
→ VPC 내부 경로이므로 계속 가능

EC2 → Internet
→ 불가

Session Manager
→ NAT에 의존하고 있었다면 Offline/접속 실패 가능
→ VPC Endpoint를 구성했다면 계속 가능
```

핵심은 **ALB에서 Private EC2로 가는 통신은 NAT를 사용하지 않는다**는 점이다.

실험 후 다음 Example을 이어갈 경우 필요한 outbound 전략에 맞게 route를 복구한다.

## 9. 기억만으로 설명하기

- Public ALB가 Private EC2에 요청을 전달할 수 있는 이유는?
- Private EC2가 인터넷 outbound를 하려면 무엇이 필요한가?
- NAT가 없으면 User Data의 어떤 작업이 실패할 수 있는가?
- SG와 NAT의 역할은 어떻게 다른가?
- Session Manager가 NAT에 의존하는 경우 NAT route를 제거하면 왜 영향을 받는가?
- VPC Endpoint를 쓰면 어떤 차이가 생기는가?

## 10. CLI 구축/장애 검증

[CLI Verification Guide](../CLI_VERIFICATION.md)의 Example 06 명령을 실행한다.

판단 포인트:

```text
Private EC2 PublicIP 없음
ALB active
Target healthy
NAT 사용 시 NAT가 public subnet에 존재
NAT가 있는 동안 SSM PingStatus=Online
NAT route 제거 전/후 outbound 차이
```

## 완료 체크

- [ ] ALB를 Public Subnet에 배치했다.
- [ ] EC2를 Private Subnet에 배치했다.
- [ ] EC2에 Public IP가 없음을 확인했다.
- [ ] NAT 없는 bootstrap 실패 가능성을 직접 관찰했다.
- [ ] NAT route 추가 후 새 인스턴스 bootstrap 성공을 확인했다.
- [ ] ALB를 통해 서비스가 정상 동작했다.
- [ ] NAT가 있는 상태에서 Session Manager 접속을 확인했다.
- [ ] NAT route 제거 후 inbound와 outbound의 차이를 관찰했다.
- [ ] Session Manager의 IAM/네트워크 요구사항을 설명할 수 있다.

## 비용 정리

특히 NAT Gateway와 Elastic IP를 즉시 정리한다. 다음 Example에서 재사용하지 않는다면 ALB, EC2, VPC 관련 리소스도 삭제한다.

삭제 후 [CLI Verification Guide](../CLI_VERIFICATION.md)의 Example 06 삭제 검증을 실행한다.
