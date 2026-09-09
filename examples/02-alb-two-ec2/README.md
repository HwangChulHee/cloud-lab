# Example 02 — EC2 두 대를 ALB 뒤에 연결하기

이번에는 사용자가 EC2의 Public IP를 직접 호출하지 않고 Application Load Balancer(ALB)의 DNS 이름으로 접근하도록 만든다.

```text
                ┌→ EC2-A
User → ALB → Target Group
                └→ EC2-B
```

## 목표

- ALB의 역할을 실제 요청으로 확인한다.
- Target Group이 무엇인지 이해한다.
- Listener와 Target의 관계를 본다.
- 두 EC2가 서로 다른 응답을 하도록 만들어 분산 여부를 확인한다.
- EC2 Public IP가 아니라 ALB DNS 이름을 서비스 진입점으로 사용한다.

## 1. EC2 두 대 생성

두 인스턴스를 같은 VPC에 생성한다.

예시 이름:

```text
example-02-web-a
example-02-web-b
```

가능하면 서로 다른 Availability Zone에 위치하도록 서로 다른 Subnet을 선택한다.

각 인스턴스의 User Data에 간단한 웹 서버를 실행한다.

EC2-A:

```bash
#!/bin/bash
dnf install -y nginx
systemctl enable nginx
systemctl start nginx
cat <<EOF > /usr/share/nginx/html/index.html
<h1>EC2-A</h1>
<p>served by instance A</p>
EOF
```

EC2-B:

```bash
#!/bin/bash
dnf install -y nginx
systemctl enable nginx
systemctl start nginx
cat <<EOF > /usr/share/nginx/html/index.html
<h1>EC2-B</h1>
<p>served by instance B</p>
EOF
```

## 2. EC2용 Security Group 생성

일단 원리를 확인하기 위해 EC2 Security Group에서 HTTP 80을 허용한다.

```text
HTTP  TCP  80  0.0.0.0/0
```

이 설정은 다음 Example 04에서 더 안전하게 바꾼다.

## 3. Target Group 생성

EC2 → Target Groups → Create target group

설정 예시:

```text
Target type: Instances
Protocol: HTTP
Port: 80
VPC: EC2가 속한 VPC
Health check path: /
```

생성 후 EC2-A와 EC2-B를 등록한다.

Target 상태가 `healthy`가 될 때까지 기다린다.

## 4. ALB 생성

EC2 → Load Balancers → Create → Application Load Balancer

설정 예시:

```text
Scheme: Internet-facing
IP address type: IPv4
Listener: HTTP : 80
```

네트워크 매핑에서 EC2가 존재하는 두 AZ의 Subnet을 선택한다.

ALB용 Security Group:

```text
HTTP  TCP  80  0.0.0.0/0
```

Listener의 Default action은 앞에서 만든 Target Group으로 Forward한다.

## 5. ALB DNS 이름으로 접속

ALB 상세 화면에서 DNS name을 확인한다.

형태:

```text
xxxx.ap-northeast-2.elb.amazonaws.com
```

브라우저에서 접속한다.

```text
http://<ALB_DNS_NAME>
```

여러 번 새로고침한다.

응답 예:

```text
EC2-A
EC2-B
EC2-A
EC2-B
...
```

정확히 번갈아 나온다는 보장은 없지만 여러 요청이 서로 다른 Target으로 전달되는 것을 확인할 수 있다.

## 6. 요청 흐름 따라가기

이번 구조에서 클라이언트 요청은 다음 순서로 이동한다.

```text
1. Client가 ALB DNS 이름을 조회
2. ALB로 HTTP 요청
3. ALB Listener가 요청 수신
4. Listener Rule이 Target Group 선택
5. ALB가 healthy target 중 하나에 요청 전달
6. EC2의 nginx가 응답
7. ALB를 통해 Client에 응답 반환
```

직접 설명해본다.

```text
Listener란?
→

Target Group이란?
→

Health Check가 필요한 이유?
→
```

## 7. EC2 직접 접근과 ALB 접근 비교

다음을 각각 실행해본다.

```text
http://<EC2_A_PUBLIC_IP>
http://<EC2_B_PUBLIC_IP>
http://<ALB_DNS_NAME>
```

차이를 적는다.

```text
EC2 직접 접근:

ALB 접근:
```

핵심은 사용자가 개별 서버를 알 필요 없이 하나의 진입점만 사용하게 된다는 것이다.

## 8. 완료 체크

- [ ] EC2를 두 대 생성했다.
- [ ] 각 EC2가 서로 다른 내용을 반환한다.
- [ ] Target Group을 만들었다.
- [ ] 두 Target이 healthy인 것을 확인했다.
- [ ] ALB를 만들었다.
- [ ] ALB DNS 이름으로 접속했다.
- [ ] 여러 요청이 서로 다른 EC2에서 처리되는 것을 확인했다.
- [ ] Listener → Target Group → EC2 흐름을 설명할 수 있다.

## 9. 다음 질문

현재 EC2-A의 nginx를 끄면 어떻게 될까?

```text
A. ALB가 계속 A로 요청을 보낼까?
B. 어느 순간 A를 제외할까?
C. 바로 제외할까, 시간이 걸릴까?
```

다음 예제에서 Health Check를 직접 관찰한다.

## 10. 비용 정리

ALB는 실행 시간에 따라 비용이 발생할 수 있다.

실습을 이어서 Example 03/04를 할 예정이면 리소스를 유지해도 되고, 오늘 끝낼 경우 다음을 삭제한다.

- ALB
- Target Group
- EC2 두 대
- 불필요한 Security Group
