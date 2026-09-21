# A01 — AWS PrivateLink로 특정 서비스만 VPC 간 private하게 노출하기

이 실습은 `examples/01~16`의 필수 흐름과 분리된 **Optional / Advanced Example**이다.

목표는 VPC Peering처럼 두 VPC의 네트워크를 서로 연결하지 않고, Provider VPC의 **특정 HTTP 서비스 하나만** Consumer VPC에서 private하게 호출하는 구조를 직접 만드는 것이다.

> 핵심 문장: **VPC Peering은 VPC ↔ VPC 네트워크 연결이고, PrivateLink는 Consumer가 Provider의 특정 서비스 endpoint에 접근하게 하는 방식이다.**

## 시작 전 Recall Check

README를 더 읽기 전에 먼저 답해본다.

- VPC Peering을 만들면 Route Table에는 무엇을 추가해야 하는가?
- Interface Endpoint는 VPC 안에 무엇을 생성하는가?
- ENI는 무엇인가?
- NLB와 ALB의 가장 큰 계층 차이는 무엇인가?
- Security Group과 Route Table은 각각 무엇을 통제하는가?

## 처음 나오는 용어

- **NLB(Network Load Balancer)**: TCP/UDP/TLS 같은 L4 트래픽을 Target으로 전달하는 AWS Load Balancer다.
- **Endpoint Service**: Provider가 NLB/GWLB 뒤의 서비스를 AWS PrivateLink 소비자에게 제공하기 위해 만드는 서비스 게시 지점이다.
- **PrivateLink**: VPC 전체 routing을 연결하지 않고 Interface Endpoint를 통해 특정 서비스에 사설 접근하게 하는 AWS 네트워크 기능이다.
- **Interface Endpoint**: Consumer VPC의 Subnet에 private IP를 가진 ENI를 만들어 PrivateLink 서비스로 들어가는 진입점을 제공한다.
- **ENI(Elastic Network Interface)**: VPC 안에서 private IP와 Security Group 등을 가지는 가상 네트워크 인터페이스다.

## 이번 실습에서 일부러 하지 않는 것

```text
VPC Peering         만들지 않음
Transit Gateway     만들지 않음
VPN / Direct Connect 만들지 않음
Terraform           사용하지 않음
Multi-AZ HA          필수 아님
```

PrivateLink의 본질만 보기 위해 한 AZ의 최소 구성으로 시작한다. 고가용성 자체는 이 실습의 목적이 아니다.

## 전체 아키텍처

```text
Provider VPC: 10.1.0.0/16

  provider-service EC2
  10.1.x.x :80
          ↑
          │ TCP 80
          │
      Internal NLB
          ↑
          │
   Endpoint Service
          ↑
          │
========== AWS PrivateLink ==========
          │
          ↓
   Interface Endpoint
   ENI private IP: 10.2.x.x
   + Endpoint-SG
          ↑
          │ TCP 80
          │
    Consumer EC2

Consumer VPC: 10.2.0.0/16

중요:
Provider VPC ↔ Consumer VPC 사이 VPC Peering 없음
Provider CIDR 10.1.0.0/16로 향하는 route도 없음
```

## 실제 packet / network path

Consumer가 Provider EC2의 private IP로 직접 가는 것이 아니다.

```text
curl <interface-endpoint-dns>:80

Consumer EC2
10.2.x.x
   │
   │ DNS resolution
   ↓
vpce-....vpce.amazonaws.com
   │
   │ resolves to
   ↓
Interface Endpoint ENI
10.2.x.x
   │
   │ Endpoint Security Group 검사
   ↓
AWS PrivateLink managed network
   │
   ↓
Provider Endpoint Service
   │
   ↓
Internal NLB :80
   │
   ↓
Target Group
   │
   ↓
Provider Service EC2 :80
10.1.x.x
```

Consumer의 Route Table에 `10.1.0.0/16 → ...` 같은 route가 없어도 된다. Consumer가 보는 목적지는 자기 VPC 안의 **Interface Endpoint ENI private IP**이기 때문이다.

## 리소스 이름 / 태그

가능한 리소스에는 다음 태그를 붙인다.

```text
Project = cloud-lab
Stage   = examples-advanced
Example = A01
```

이름은 다음 형식을 권장한다.

```text
advanced-a01-provider-vpc
advanced-a01-consumer-vpc
advanced-a01-provider-service
advanced-a01-nlb
advanced-a01-tg
advanced-a01-endpoint-sg
advanced-a01-consumer
```

---

# 1. Provider VPC 만들기

다음 최소 구조를 만든다.

```text
VPC: 10.1.0.0/16
Subnet: 10.1.1.0/24
```

Provider 서비스는 외부 인터넷에서 접근할 필요가 없으므로 Provider VPC에는 이 실습만을 위해 IGW나 NAT Gateway를 만들 필요가 없다.

## 2. Provider HTTP Service EC2 만들기

Provider Subnet에 EC2 한 대를 생성한다.

조건:

```text
Public IPv4: 없음
Service Port: TCP 80
```

인터넷 package download에 의존하지 않도록, 가능하면 Python이 포함된 Amazon Linux 계열 AMI에서 간단한 HTTP 서버를 실행한다.

예시 User Data:

```bash
#!/bin/bash
mkdir -p /opt/privatelink-demo
cat <<'EOF' > /opt/privatelink-demo/index.html
<h1>Hello through AWS PrivateLink</h1>
<p>provider-vpc: 10.1.0.0/16</p>
EOF

cd /opt/privatelink-demo
nohup python3 -m http.server 80 --bind 0.0.0.0 \
  >/var/log/privatelink-demo.log 2>&1 &
```

> 사용하는 AMI에 `python3`가 없다면 이 실습 전에 Python이 포함된 AMI를 선택하거나 다른 이미 설치된 HTTP 서버를 사용한다. Provider에 NAT를 추가해서 package install 문제까지 섞지 않는 것이 좋다.

Provider Service Security Group은 TCP 80만 허용한다.

이 최소 실습에서는 NLB node/health-check가 Provider VPC 내부에서 Target에 접근할 수 있도록 Provider VPC CIDR 범위에서 80을 허용해도 된다.

```text
Inbound TCP 80
Source: 10.1.0.0/16
```

더 엄격하게 구성하고 싶다면 NLB에 Security Group을 연결하고 Target EC2 SG가 NLB SG를 source로 허용하는 구조를 별도로 실험할 수 있다. 하지만 NLB Security Group의 PrivateLink traffic enforcement 설정까지 섞이면 핵심이 흐려질 수 있으므로 A01에서는 필수로 하지 않는다.

## 3. NLB 만들기

Provider VPC에 **Internal Network Load Balancer**를 만든다.

```text
Scheme   : Internal
Listener : TCP 80
Subnet   : Provider Subnet
```

Target Group:

```text
Target type : Instances
Protocol    : TCP
Port        : 80
Target      : provider-service EC2
Health Check: TCP 80
```

Target이 `healthy`가 되는지 확인한다.

여기서 NLB는 Provider VPC의 여러 자원을 공개하는 장치가 아니라 **Endpoint Service가 제공할 정확한 서비스 진입점**이다.

## 4. Endpoint Service 만들기

VPC Console의 Endpoint Services에서 NLB를 기반으로 Endpoint Service를 만든다.

권장:

```text
Load Balancer       : advanced-a01-nlb
Acceptance required : Yes
```

Acceptance를 켜는 이유는 Provider가 어떤 Consumer endpoint 연결을 받을지 승인하는 흐름까지 보기 위해서다.

생성 후 service name을 기록한다.

형태:

```text
com.amazonaws.vpce.ap-northeast-2.vpce-svc-xxxxxxxx
```

### Allowed Principal

Consumer가 이 Endpoint Service를 발견하고 연결할 수 있도록 허용할 principal을 추가한다.

같은 AWS Account 안에서 실습한다면 account root principal을 사용할 수 있다.

```text
arn:aws:iam::<ACCOUNT_ID>:root
```

의미는 "이 principal이 endpoint 연결을 요청할 수 있다"이지, Provider VPC 전체에 접근 권한을 준다는 뜻이 아니다.

---

# 5. Consumer VPC 만들기

```text
VPC: 10.2.0.0/16
Subnet: 10.2.1.0/24
```

Consumer EC2에 접속하기 위한 관리 경로는 실습 편의상 자유롭게 선택한다.

가장 단순한 방법은 Consumer Subnet을 public subnet으로 만들고, Consumer EC2에 Public IPv4를 주며 SSH는 **내 IP/32**만 허용하는 것이다.

중요한 점은 Consumer EC2에 Public IP가 있더라도 **Provider 서비스 호출 자체는 Interface Endpoint의 private IP로 흐른다**는 것이다.

Private Consumer EC2 + SSM/VPC Endpoint까지 구성해도 되지만 A01의 필수 범위는 아니다.

## 6. Consumer EC2 만들기

Consumer VPC에 EC2 한 대를 생성한다.

Consumer EC2 Security Group은 관리 접근 외에 특별한 inbound가 필요하지 않다. HTTP 요청은 Consumer EC2가 밖으로 시작하는 outbound 연결이다.

가능하면 기본 outbound를 그대로 사용하고, 실습이 익숙해지면 Endpoint-SG를 대상으로 TCP 80만 허용하는 방식으로 줄여본다.

---

# 7. Interface Endpoint Security Group 만들기

Consumer VPC에서 Endpoint 전용 Security Group을 만든다.

```text
Name: advanced-a01-endpoint-sg

Inbound:
TCP 80
Source: Consumer EC2 Security Group
```

이 Security Group은 **Consumer가 Interface Endpoint ENI에 들어오는 지점**을 통제한다.

```text
Consumer EC2 SG
      │
      │ TCP 80
      ↓
Endpoint-SG
      │
Interface Endpoint ENI
```

Provider EC2의 SG와 역할이 다르다.

```text
Endpoint-SG
= Consumer VPC 안에서 누가 endpoint를 사용할 수 있는가

Provider Service SG
= NLB 뒤의 실제 서비스가 어떤 Provider-side traffic을 받을 수 있는가
```

## 8. Interface Endpoint 만들기

Consumer VPC에서 Interface Endpoint를 생성한다.

```text
Service name : 앞에서 기록한 vpce-svc service name
VPC          : Consumer VPC
Subnet       : Consumer Subnet
Security Group: advanced-a01-endpoint-sg
```

생성 직후 상태가 `Pending acceptance`라면 정상이다.

Provider 쪽 Endpoint Service에서 connection request를 확인하고 **Accept**한다.

Consumer 쪽 Endpoint 상태가 `Available`이 될 때까지 기다린다.

## 9. ENI를 직접 확인하기

Interface Endpoint를 생성하면 Consumer Subnet에 ENI가 생긴다.

확인할 것:

```text
Interface Endpoint
  └─ ENI
      ├─ Consumer Subnet
      ├─ private IP: 10.2.x.x
      └─ Endpoint-SG
```

이 private IP가 Consumer가 PrivateLink로 들어가는 실제 네트워크 진입점이다.

---

# 10. DNS가 어디로 해석되는지 확인하기

이번 A01에서는 Provider의 **custom private DNS name**까지 만들지 않는다. 대신 Interface Endpoint에 AWS가 자동으로 제공하는 endpoint DNS name을 사용한다.

예:

```text
vpce-xxxxxxxx-yyyyyyyy.vpce.amazonaws.com
```

Consumer EC2에서 확인한다.

```bash
getent hosts <interface-endpoint-dns>
```

또는:

```bash
nslookup <interface-endpoint-dns>
```

결과가 Consumer VPC의 `10.2.x.x` private IP를 가리키는지 확인한다.

즉 DNS 흐름은 다음과 같다.

```text
Endpoint DNS name
      ↓ DNS resolve
Interface Endpoint ENI private IP (10.2.x.x)
      ↓
AWS PrivateLink
      ↓
Provider Endpoint Service / NLB
```

> 별도의 `api.example.com` 같은 custom private DNS를 Endpoint Service에 붙일 수도 있지만 domain ownership verification 등 추가 단계가 필요하다. PrivateLink의 핵심 이해에는 필요하지 않으므로 이 실습에서는 선택 심화로 남긴다.

# 11. Consumer에서 Provider 서비스 호출하기

Consumer EC2에서 Interface Endpoint DNS로 요청한다.

```bash
curl -v http://<interface-endpoint-dns>/
```

예상 응답:

```text
Hello through AWS PrivateLink
provider-vpc: 10.1.0.0/16
```

중요한 것은 호출 대상이 Provider EC2 private IP가 아니라 **Interface Endpoint DNS / private IP**라는 점이다.

가능하면 DNS로 얻은 Endpoint ENI private IP에도 직접 요청해본다.

```bash
curl -v http://<endpoint-eni-private-ip>/
```

HTTP Host 기반 routing을 쓰지 않는 단순 서비스이므로 동일한 응답을 확인할 수 있다.

---

# 12. Peering이 정말 없는지 검증하기

두 VPC 사이에 VPC Peering Connection을 만들지 않는다.

CLI로도 확인한다.

```bash
aws ec2 describe-vpc-peering-connections \
  --region $AWS_REGION \
  --filters \
    "Name=requester-vpc-info.vpc-id,Values=<provider-vpc-id>" \
    "Name=accepter-vpc-info.vpc-id,Values=<consumer-vpc-id>"
```

반대 방향도 필요하면 확인한다.

또한 Consumer Route Table에 Provider CIDR로 향하는 route가 없는지 확인한다.

```text
Consumer Route Table
10.2.0.0/16 → local
...

없어야 함:
10.1.0.0/16 → peering/tgw/vpn/...
```

# 13. Provider EC2 private IP 직접 접근 실패 확인

Provider Service EC2의 private IP를 기록한다.

```text
10.1.x.x
```

Consumer EC2에서 직접 호출해본다.

```bash
curl --connect-timeout 3 http://10.1.x.x/
```

직접 접근은 성공하면 안 된다.

```text
Consumer EC2
   │
   │ destination = 10.1.x.x
   ↓
Consumer Route Table
   │
   X 10.1.0.0/16 route 없음
```

반면:

```bash
curl http://<interface-endpoint-dns>/
```

는 성공한다.

이 비교가 PrivateLink의 핵심이다.

```text
Provider VPC 전체 private network
→ 연결되지 않음

Provider가 Endpoint Service로 게시한 TCP 80 서비스
→ 접근 가능
```

Provider VPC에 다른 EC2/RDS 등이 있어도 Consumer가 그 private IP로 갈 route가 생기는 것이 아니다.

---

# 14. 장애 실험 A — Endpoint Security Group 차단

Endpoint-SG의 TCP 80 inbound rule을 잠시 제거한다.

Consumer에서 다시 요청한다.

```bash
curl --connect-timeout 3 http://<interface-endpoint-dns>/
```

관찰:

```text
DNS resolution      정상
Endpoint 상태        Available
Provider NLB/Target  정상
HTTP 요청            실패/timeout
```

즉 Endpoint ENI까지의 Security Group 계층 문제다.

rule을 복구하고 다시 성공하는지 확인한다.

# 15. 장애 실험 B — Provider Target 중지

Provider HTTP 서비스를 중지하거나 EC2를 stop하여 NLB Target을 unhealthy로 만든다.

확인:

```text
Interface Endpoint = Available
DNS = 정상
NLB Target = unhealthy
서비스 호출 = 실패
```

여기서 "Endpoint가 Available"과 "Provider application이 healthy"가 별개의 상태라는 점을 설명한다.

복구 후 Target이 healthy가 되고 다시 호출되는지 확인한다.

# 16. 장애 실험 C — Endpoint Connection Reject/삭제 생각하기

실습 종료 단계에서 Consumer Interface Endpoint를 삭제한다.

이후 Consumer에는 Endpoint ENI 자체가 사라진다.

```text
Consumer EC2
  ↓
Interface Endpoint ENI 없음
  ↓
PrivateLink 진입점 없음
```

이는 Provider 서비스 프로세스 장애와는 다른 계층의 실패다.

---

# VPC Peering과 PrivateLink를 실제 구조로 비교

## VPC Peering

```text
Consumer VPC 10.2.0.0/16
       ↕ route
   VPC Peering
       ↕ route
Provider VPC 10.1.0.0/16

목적:
VPC 간 IP network reachability 제공

보통 필요한 것:
- Peering Connection
- 양쪽 Route Table
- SG/NACL 허용
```

## PrivateLink

```text
Consumer EC2
   ↓
Interface Endpoint ENI
   ↓
PrivateLink
   ↓
Endpoint Service
   ↓
NLB
   ↓
특정 Provider Service
```

```text
Provider CIDR route 필요 없음
Provider VPC 전체 연결 없음
Consumer → 게시된 특정 서비스 접근
```

## 면접용 한 문장

> "VPC Peering은 두 VPC 사이에 IP routing을 열어 네트워크 reachability를 제공하지만, PrivateLink는 Provider가 NLB 뒤의 특정 서비스를 Endpoint Service로 게시하고 Consumer가 자기 VPC의 Interface Endpoint ENI를 통해 그 서비스만 private하게 소비하는 구조입니다. 그래서 Consumer Route Table에 Provider CIDR route를 추가하지 않아도 되고 Provider의 다른 리소스까지 연결되는 것도 아닙니다."

---

# CLI 구축 검증

[Advanced CLI Verification](../CLI_VERIFICATION.md)의 A01 명령을 실행한다.

반드시 확인할 것:

```text
Provider VPC CIDR = 10.1.0.0/16
Consumer VPC CIDR = 10.2.0.0/16
VPC Peering 없음
NLB internal / target healthy
Endpoint Service 존재
Endpoint Connection accepted
Interface Endpoint = available
Endpoint ENI private IP = Consumer VPC 10.2.x.x
Endpoint-SG TCP 80 source = Consumer EC2 SG
Consumer route table에 10.1.0.0/16 route 없음
Endpoint DNS 호출 성공
Provider EC2 private IP 직접 호출 실패
```

# 기억만으로 설명하기

README를 닫고 다음 질문에 답한다.

- PrivateLink에서 Provider가 NLB를 사용하는 이유는?
- Endpoint Service와 Interface Endpoint는 각각 어느 쪽에 존재하는가?
- Interface Endpoint가 생성될 때 ENI는 어느 VPC에 생기는가?
- Consumer가 Provider CIDR route 없이도 호출할 수 있는 이유는?
- Endpoint DNS는 어떤 IP로 해석되는가?
- Endpoint Security Group은 어느 구간을 통제하는가?
- Provider Target의 SG는 어느 구간을 통제하는가?
- Interface Endpoint가 `Available`인데도 서비스가 실패할 수 있는 이유는?
- VPC Peering이었다면 어떤 route가 추가로 필요했을까?
- 왜 PrivateLink를 "VPC 연결"보다 "서비스 노출"이라고 설명하는 편이 정확한가?

# 완료 체크

- [ ] Provider VPC `10.1.0.0/16`을 만들었다.
- [ ] Consumer VPC `10.2.0.0/16`을 만들었다.
- [ ] 두 VPC 사이에 Peering을 만들지 않았다.
- [ ] Provider HTTP Service를 NLB Target으로 등록했다.
- [ ] NLB Target이 healthy임을 확인했다.
- [ ] NLB 기반 Endpoint Service를 만들었다.
- [ ] Consumer principal을 허용했다.
- [ ] Consumer Interface Endpoint를 만들었다.
- [ ] Provider에서 Endpoint Connection을 Accept했다.
- [ ] Interface Endpoint ENI와 private IP를 확인했다.
- [ ] Endpoint DNS가 Consumer VPC private IP로 해석되는 것을 확인했다.
- [ ] Consumer EC2에서 Endpoint DNS를 통한 HTTP 호출에 성공했다.
- [ ] Provider EC2 private IP 직접 호출은 실패함을 확인했다.
- [ ] Endpoint-SG 차단 장애를 만들고 복구했다.
- [ ] Provider Target 장애와 Endpoint 장애를 구분할 수 있다.
- [ ] VPC Peering과 PrivateLink 차이를 1분 안에 설명할 수 있다.

# 비용 주의

이 실습은 짧게 끝내는 것이 좋다. 무료로 가정하지 않는다.

특히 비용이 발생할 수 있는 항목:

```text
Network Load Balancer
Interface VPC Endpoint
- endpoint가 존재하는 AZ/시간
- 처리 데이터
EC2 / EBS
Consumer EC2 Public IPv4를 사용했다면 Public IPv4
데이터 처리량
```

정확한 금액은 Region과 시점에 따라 달라질 수 있으므로 실습 시작 전 AWS Pricing/Console에서 현재 가격을 확인한다.

NLB와 Interface Endpoint는 트래픽을 거의 보내지 않아도 시간 기반 비용이 생길 수 있으므로 **다음 날까지 방치하지 않는다.**

# 삭제 순서

의존성 때문에 다음 순서를 권장한다.

```text
1. Consumer Interface Endpoint 삭제
   → Endpoint ENI가 사라지는지 확인

2. Provider Endpoint Service의 Endpoint Connection이 없어졌는지 확인

3. Provider Endpoint Service 삭제
   → NLB와의 service association 해제

4. Provider NLB 삭제

5. Provider Target Group 삭제

6. Provider / Consumer EC2 종료

7. 사용하지 않는 Security Group 삭제

8. Consumer 관리용 IGW / Route Table association 등 정리

9. Provider / Consumer Subnet 삭제

10. IGW가 있다면 detach/delete

11. Provider / Consumer VPC 삭제
```

삭제 후 [Advanced CLI Verification](../CLI_VERIFICATION.md)의 잔존 리소스 검사를 실행한다.

특히 다음이 남지 않았는지 본다.

```text
Interface Endpoint
Endpoint ENI
Endpoint Service
NLB
Target Group
EC2 / EBS
Public IPv4 관련 리소스
두 실습 VPC
```

# 이 실습의 종료 기준

단순히 `curl`이 성공했다고 끝내지 않는다.

```text
Endpoint DNS → Consumer ENI private IP를 설명할 수 있다
+
Provider CIDR route 없이 요청이 성공하는 이유를 설명할 수 있다
+
Provider private IP 직접 접근이 실패함을 확인했다
+
Peering과 PrivateLink를 network reachability vs service exposure로 비교할 수 있다
+
보안 제어 지점을 Consumer Endpoint-SG / Provider Service SG로 나눠 설명할 수 있다
+
삭제 후 과금 리소스가 남지 않았음을 CLI로 확인했다
```

---

## 로컬 CLI 검증 가이드

### A01 CLI — PrivateLink의 network path를 출력으로 증명하기

이 실습은 CLI가 특히 중요하다. Console에서 연결되어 보이는 것보다 **"Peering/Provider route는 없는데 Interface Endpoint ENI를 통해 서비스가 된다"**는 사실을 출력으로 증명해야 한다.

### 1. Provider / Consumer VPC

\`\`\`bash
aws ec2 describe-vpcs --region $AWS_REGION \
  --filters 'Name=tag:Stage,Values=examples-advanced' 'Name=tag:Example,Values=A01' \
  --query 'Vpcs[].{Name:Tags[?Key==\`Name\`]|[0].Value,Id:VpcId,CIDR:CidrBlock}' \
  --output table
\`\`\`

Provider=\`10.1.0.0/16\`, Consumer=\`10.2.0.0/16\`인지 확인한다.

### 2. Peering 부재 / Consumer Route

\`\`\`bash
aws ec2 describe-vpc-peering-connections --region $AWS_REGION \
  --filters "Name=requester-vpc-info.vpc-id,Values=$PROVIDER_VPC_ID"

aws ec2 describe-route-tables --region $AWS_REGION \
  --filters "Name=vpc-id,Values=$CONSUMER_VPC_ID" \
  --query 'RouteTables[].Routes'
\`\`\`

두 VPC를 직접 연결하는 Peering이 없고 Consumer Route Table에 Provider CIDR(\`10.1.0.0/16\`) route가 없는 것을 확인한다.

### 3. Provider NLB와 Target

\`\`\`bash
aws elbv2 describe-load-balancers --region $AWS_REGION \
  --names advanced-a01-nlb \
  --query 'LoadBalancers[].{Scheme:Scheme,Type:Type,State:State.Code,Vpc:VpcId,DNS:DNSName}'

export TG_ARN=$(aws elbv2 describe-target-groups --region $AWS_REGION \
  --names advanced-a01-tg \
  --query 'TargetGroups[0].TargetGroupArn' --output text)

aws elbv2 describe-target-health --region $AWS_REGION \
  --target-group-arn $TG_ARN \
  --query 'TargetHealthDescriptions[].{Target:Target.Id,State:TargetHealth.State,Reason:TargetHealth.Reason}'
\`\`\`

\`Scheme=internal\`, \`Type=network\`, Target=\`healthy\`를 확인한다.

### 4. Endpoint Service

\`\`\`bash
aws ec2 describe-vpc-endpoint-service-configurations --region $AWS_REGION \
  --query 'ServiceConfigurations[].{Id:ServiceId,Name:ServiceName,State:ServiceState,Acceptance:AcceptanceRequired,NLBs:NetworkLoadBalancerArns}'
\`\`\`

이 출력은 **Provider가 어느 NLB를 PrivateLink 서비스로 게시했는지** 보여준다.

### 5. Consumer Interface Endpoint / ENI

\`\`\`bash
aws ec2 describe-vpc-endpoints --region $AWS_REGION \
  --vpc-endpoint-ids $ENDPOINT_ID \
  --query 'VpcEndpoints[0].{Type:VpcEndpointType,State:State,Vpc:VpcId,Subnets:SubnetIds,ENIs:NetworkInterfaceIds,DNS:DnsEntries[].DnsName,SGs:Groups[].GroupId}'

export ENDPOINT_ENIS=$(aws ec2 describe-vpc-endpoints --region $AWS_REGION \
  --vpc-endpoint-ids $ENDPOINT_ID \
  --query 'VpcEndpoints[0].NetworkInterfaceIds' --output text)

aws ec2 describe-network-interfaces --region $AWS_REGION \
  --network-interface-ids $ENDPOINT_ENIS \
  --query 'NetworkInterfaces[].{Id:NetworkInterfaceId,Vpc:VpcId,Subnet:SubnetId,PrivateIP:PrivateIpAddress,SGs:Groups[].GroupId}' \
  --output table
\`\`\`

핵심은 ENI의 \`PrivateIP\`가 **Consumer VPC의 10.2.x.x**라는 점이다.

### 6. DNS가 ENI private IP로 해석되는지

Consumer EC2에서:

\`\`\`bash
getent hosts <interface-endpoint-dns>
curl -v http://<interface-endpoint-dns>/
curl --connect-timeout 3 http://<provider-ec2-private-ip>/
\`\`\`

\`getent hosts\` 결과는 Endpoint ENI private IP를 보여야 한다. Endpoint DNS 호출은 성공하고 Provider EC2 private IP 직접 호출은 실패해야 한다.

이 차이가 곧:

\`\`\`text
VPC Peering
= VPC ↔ VPC reachability

PrivateLink
= Consumer → 게시된 특정 서비스
\`\`\`

다.
