# Example 01 — EC2 한 대에 웹 서버 띄우기

가장 단순한 AWS 웹 서비스 구조를 직접 만든다.

```text
Browser
   ↓ HTTP
EC2
   ↓
Simple Web Server
```

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

브라우저에서:

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

Security Group에서 HTTP 80 inbound rule을 잠시 삭제한다.

다시 브라우저에서 요청한다.

예상:

```text
Client
  X
Security Group
  X
EC2
```

EC2까지 요청이 들어오지 못한다.

확인 후 다시 80번 포트를 연다.

## 6. 장애 실험 B — 웹 서버 중지

SSH 또는 Session Manager를 사용할 수 있다면 nginx를 중지한다.

```bash
sudo systemctl stop nginx
```

이후 다시 요청해본다.

Security Group은 열려 있지만 애플리케이션이 응답하지 않는 상태다.

다시 시작한다.

```bash
sudo systemctl start nginx
```

## 7. Stop / Start 실험

현재 Public IP를 기록한다.

```text
Before: __________________
```

EC2를 Stop한 뒤 다시 Start한다.

새 Public IP를 기록한다.

```text
After: __________________
```

확인할 것:

- Private IP는 어떻게 되었는가?
- Public IP는 어떻게 되었는가?
- 왜 애플리케이션 주소로 EC2의 임시 Public IP에 의존하면 불편한가?

## 8. 완료 체크

- [ ] EC2를 직접 생성했다.
- [ ] User Data로 웹 서버를 자동 실행했다.
- [ ] Public IP로 접속했다.
- [ ] Public/Private IP를 확인했다.
- [ ] Security Group에서 HTTP를 차단해봤다.
- [ ] 웹 서버 프로세스를 중지해봤다.
- [ ] Stop/Start 후 Public IP 변화를 확인했다.

## 9. 정리

이 단계의 구조에는 명확한 한계가 있다.

```text
User
 ↓
EC2 1대
```

EC2가 죽으면 서비스도 같이 죽는다.

다음 예제에서는 EC2를 두 대 만들고 그 앞에 Application Load Balancer를 둔다.

## 10. 비용 정리

실습 종료 후 필요 없다면 다음 리소스를 삭제한다.

- EC2 Instance
- 필요 없는 Security Group
- 추가 생성한 EBS Volume 등

리소스 삭제까지 예제의 일부다.
