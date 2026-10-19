# Example 01 — EC2 한 대에 웹 서버 띄우기

가장 단순한 AWS 웹 서비스 구조를 직접 만든다.

```text
Browser
   ↓ HTTP
EC2
   ↓
Simple Web Server
```

모든 태그 가능 리소스에는 가능한 한 다음 태그를 붙인다.

```text
Project=cloud-lab
Stage=examples
Example=01
```

Name은 `example-01-*` 형식을 사용한다.

## 리소스 이름표

이 예제에서 직접 만드는 리소스 이름은 아래처럼 고정한다. 콘솔에서 이름을 고민하지 말고 그대로 사용한다.

| 리소스 | 이름 |
| --- | --- |
| EC2 | `example-01-web` |
| Security Group | `example-01-web-sg` |

## 목표

이 예제를 끝내면 다음을 실제 리소스로 확인할 수 있어야 한다.

- EC2가 인터넷에서 어떻게 접근되는지
- Public IP와 Private IP의 차이
- Security Group이 왜 필요한지
- HTTP 80 포트를 열면 무엇이 달라지는지
- EC2 User Data가 인스턴스 생성 시 어떤 역할을 하는지
- EC2를 Stop/Start 했을 때 Public IP가 어떻게 되는지

## 1. EC2 생성

AWS Console → EC2 → Instances → Launch instances

권장 설정:

- Name: `example-01-web`
- AMI: Amazon Linux 계열
- Instance type: 실습용 소형 인스턴스
- Key pair: 필요하면 기존 키 사용
- Auto-assign public IP: Enabled

Security Group은 새로 만든다.

### Inbound

```text
HTTP  TCP  80  0.0.0.0/0
```

SSH가 필요하면 자신의 IP에만 22번 포트를 허용한다.

```text
SSH  TCP  22  <MY_IP>/32
```

## 2. User Data로 웹 서버 실행

Advanced details → User data에 아래 형태의 스크립트를 넣는다.

```bash
#!/bin/bash
dnf update -y
dnf install -y nginx
systemctl enable nginx
systemctl start nginx

HOSTNAME=$(hostname)
PRIVATE_IP=$(hostname -I | awk '{print $1}')

cat <<EOF > /usr/share/nginx/html/index.html
<h1>Hello from EC2</h1>
<p>hostname: $HOSTNAME</p>
<p>private ip: $PRIVATE_IP</p>
EOF
```

> AMI에 따라 패키지 관리 명령이 다를 수 있다. 핵심은 인스턴스 최초 생성 시 웹 서버 설치와 시작을 자동화하는 것이다.

## 3. 접속 확인

인스턴스가 `Running` 상태가 되면 Public IPv4 address를 확인한다.

```text
http://<PUBLIC_IP>
```

정상이라면 EC2가 응답한 HTML을 볼 수 있다.

## 4. 관찰 포인트

EC2 상세 화면에서 다음을 직접 확인한다.

```text
Public IPv4 address
Private IPv4 address
Subnet
Availability Zone
Security Group
```

생각해볼 것:

1. 브라우저는 어떤 IP로 접속했는가?
2. EC2 내부 웹 서버는 어떤 포트에서 요청을 받는가?
3. Security Group에서 80번 포트를 닫으면 어떤 현상이 생기는가?
4. 애플리케이션이 꺼진 경우와 Security Group이 막힌 경우 증상이 같은가?

## 5. 장애 실험 A — HTTP 포트 닫기

Security Group에서 HTTP 80 inbound rule을 잠시 삭제하고 다시 요청한다.

```text
Client
  X
Security Group
  X
EC2
```

확인 후 다시 80번 포트를 연다.

## 6. 장애 실험 B — 웹 서버 중지

SSH 또는 Session Manager를 사용할 수 있다면 nginx를 중지한다.

```bash
sudo systemctl stop nginx
```

Security Group은 열려 있지만 애플리케이션이 응답하지 않는 상태를 확인한 뒤 다시 시작한다.

```bash
sudo systemctl start nginx
```

## 7. Stop / Start 실험

현재 Public IP를 기록하고 EC2를 Stop한 뒤 다시 Start한다.

```text
Before: __________________
After:  __________________
```

Private IP와 Public IP가 각각 어떻게 되는지 확인하고, 왜 서비스 주소로 임시 Public IP에 의존하면 불편한지 설명한다.

## 8. CLI 구축 검증

이 예제부터 CLI는 단순 복붙이 아니라 **"무슨 리소스를 어떤 조건으로 조회하고, 출력의 어느 필드를 보는가"**까지 이해한다.

먼저 공통 변수다.

```bash
export AWS_REGION=ap-northeast-2
```

- `export`: 현재 셸에서 뒤 명령들이 재사용할 변수를 만든다.
- `AWS_REGION`: 아래 명령이 어느 AWS Region을 조회할지 명시한다.

### 1. EC2 상태와 네트워크 정보

```bash
aws ec2 describe-instances \
  --region $AWS_REGION \
  --filters \
    'Name=tag:Project,Values=cloud-lab' \
    'Name=tag:Stage,Values=examples' \
    'Name=tag:Example,Values=01' \
    'Name=instance-state-name,Values=pending,running,stopping,stopped' \
  --query 'Reservations[].Instances[].{Name:Tags[?Key==`Name`]|[0].Value,Id:InstanceId,State:State.Name,PublicIP:PublicIpAddress,PrivateIP:PrivateIpAddress,Subnet:SubnetId,Vpc:VpcId,SG:SecurityGroups[].GroupId}' \
  --output table
```

명령을 쪼개서 읽으면:

```text
aws ec2 describe-instances
→ EC2 인스턴스 정보를 조회한다.

--filters
→ 전체 계정의 EC2 중 이 실습 태그와 상태에 맞는 것만 좁힌다.

--query
→ 응답 JSON 전체가 아니라 Name/ID/상태/IP/Subnet/VPC/SG만 뽑는다.

--output table
→ 사람이 읽기 좋은 표로 출력한다.
```

출력에서 `PublicIP`와 `PrivateIP`를 비교하고, Stop/Start 전후에 같은 명령을 다시 실행한다.

### 2. Security Group의 실제 inbound rule

```bash
aws ec2 describe-security-groups \
  --region $AWS_REGION \
  --filters 'Name=tag:Example,Values=01' \
  --query 'SecurityGroups[].{Name:GroupName,Id:GroupId,Ingress:IpPermissions}'
```

- `describe-security-groups`: SG의 설정을 조회한다.
- `IpPermissions`: **Inbound rule**이다.
- HTTP 80을 열었을 때와 제거했을 때 같은 명령을 실행하면 rule 변화가 그대로 보인다.

### 3. 삭제 후 확인

```bash
aws ec2 describe-instances --region $AWS_REGION \
  --filters 'Name=tag:Example,Values=01' \
            'Name=instance-state-name,Values=pending,running,stopping,stopped' \
  --query 'Reservations[].Instances[].InstanceId'

aws ec2 describe-volumes --region $AWS_REGION \
  --filters 'Name=tag:Example,Values=01' \
  --query 'Volumes[].{Id:VolumeId,State:State}'
```

첫 명령은 아직 실행/정지 상태로 남은 EC2가 있는지, 두 번째는 **EC2를 삭제했는데 EBS Volume이 별도로 남아 있지 않은지** 확인한다. 의도적으로 남긴 리소스가 없다면 결과가 비어 있어야 한다.

## 9. 완료 체크

- [ ] EC2를 직접 생성했다.
- [ ] 공통 태그와 이름 규칙을 적용했다.
- [ ] User Data로 웹 서버를 자동 실행했다.
- [ ] Public IP로 접속했다.
- [ ] Public/Private IP를 확인했다.
- [ ] Security Group에서 HTTP를 차단해봤다.
- [ ] 웹 서버 프로세스를 중지해봤다.
- [ ] Stop/Start 후 Public IP 변화를 확인했다.
- [ ] CLI로 실제 구성을 검증했다.

## 10. 정리

이 단계의 구조에는 명확한 한계가 있다.

```text
User
 ↓
EC2 1대
```

EC2가 죽으면 서비스도 같이 죽는다. 다음 예제에서는 EC2를 두 대 만들고 그 앞에 Application Load Balancer를 둔다.

## 11. 비용 정리와 삭제 검증

실습 종료 후 필요 없다면 EC2, 불필요한 Security Group, 추가 EBS Volume 등을 삭제한다.

삭제 후 [CLI Verification Guide](../CLI_VERIFICATION.md)의 Example 01 삭제 검증을 실행한다. 실습 종료는 콘솔에서 삭제 버튼을 누른 시점이 아니라 **과금 가능한 리소스가 남지 않았음을 확인한 시점**으로 본다.

---
