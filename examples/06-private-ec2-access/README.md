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

## 리소스 이름표

Example 05를 재사용해도 되고 처음부터 다시 만들어도 된다. 다시 만든다면 아래 이름을 사용한다.

| 리소스 | 이름 |
| --- | --- |
| VPC | `example-06-vpc` |
| Public Subnet A/B | `example-06-public-a`, `example-06-public-b` |
| Private Subnet A/B | `example-06-private-a`, `example-06-private-b` |
| Internet Gateway | `example-06-igw` |
| Public Route Table | `example-06-public-rt` |
| Private Route Table | `example-06-private-rt` |
| ALB | `example-06-alb` |
| ALB Security Group | `example-06-alb-sg` |
| Target Group | `example-06-tg` |
| Private EC2 | `example-06-web` |
| EC2 Security Group | `example-06-web-sg` |
| NAT Gateway | `example-06-nat` |
| Elastic IP Name tag | `example-06-nat-eip` |
| SSM IAM Role | `example-06-ssm-role` |

VPC Interface Endpoint 심화까지 진행한다면 Name tag는 `example-06-ssm-vpce`, `example-06-ssmmessages-vpce`, `example-06-ec2messages-vpce`를 사용한다.

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

### 1. Private EC2에 Public IP가 없는지 확인

```bash
aws ec2 describe-instances --region $AWS_REGION \
  --filters 'Name=tag:Example,Values=06' 'Name=instance-state-name,Values=running' \
  --query 'Reservations[].Instances[].{Name:Tags[?Key==`Name`]|[0].Value,Id:InstanceId,PublicIP:PublicIpAddress,PrivateIP:PrivateIpAddress,Subnet:SubnetId,IamProfile:IamInstanceProfile.Arn}' \
  --output table
```

`PublicIP=null`이어도 ALB를 통한 서비스는 가능해야 한다. `IamProfile`은 Session Manager에 필요한 EC2 Role이 붙었는지 확인하는 힌트다.

### 2. NAT Gateway

```bash
aws ec2 describe-nat-gateways --region $AWS_REGION \
  --filter 'Name=tag:Example,Values=06' 'Name=state,Values=available,pending' \
  --query 'NatGateways[].{Id:NatGatewayId,Subnet:SubnetId,State:State,NatAddresses:NatGatewayAddresses[].PublicIp}' \
  --output table
```

- NAT가 `available`인지 확인한다.
- `Subnet`이 **public subnet**인지 별도로 Route Table과 대조한다.
- `NatAddresses`에서 NAT에 연결된 public IP를 볼 수 있다.

### 3. Session Manager가 EC2를 관리 대상으로 보는지 확인

```bash
aws ssm describe-instance-information --region $AWS_REGION \
  --query 'InstanceInformationList[].{Instance:InstanceId,Ping:PingStatus,Agent:AgentVersion}' \
  --output table
```

`PingStatus=Online`은 SSM Agent가 Systems Manager endpoint와 통신 가능한 상태라는 뜻이다. NAT route를 제거한 뒤 Offline이 된다면 **관리 경로가 NAT outbound에 의존했다**는 증거가 된다.

### 4. ALB 상태

```bash
aws elbv2 describe-load-balancers --region $AWS_REGION \
  --query "LoadBalancers[?contains(LoadBalancerName, 'example-06')].[LoadBalancerName,Scheme,State.Code,DNSName]"
```

NAT route를 제거해도 ALB → private EC2 요청은 VPC 내부 경로이므로 계속 가능한지 확인한다. 즉 **NAT는 inbound용이 아니라 private resource의 outbound용**이라는 점을 상태 변화로 구분한다.

### 5. 삭제 후 NAT와 EIP 확인

```bash
aws ec2 describe-nat-gateways --region $AWS_REGION \
  --filter 'Name=tag:Example,Values=06' 'Name=state,Values=pending,available,deleting,failed' \
  --query 'NatGateways[].{Id:NatGatewayId,State:State}'

aws ec2 describe-addresses --region $AWS_REGION \
  --query "Addresses[?Tags[?Key=='Example' && Value=='06']].{AllocationId:AllocationId,PublicIp:PublicIp,AssociationId:AssociationId}"
```

NAT Gateway 삭제와 **Elastic IP 해제는 별개**로 확인한다. 비용 정리에서 중요한 명령이다.

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

---
