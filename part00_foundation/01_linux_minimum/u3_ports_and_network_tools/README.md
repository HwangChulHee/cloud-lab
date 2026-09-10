# u3. Port와 Linux 네트워크 확인

## 지도 확인

서버 장애를 볼 때는 **프로세스가 실행 중인지**와 **네트워크 요청을 받을 준비가 되어 있는지**를 분리해서 확인해야 한다.

```text
EC2 running
  ↓
process running
  ↓
port listening
  ↓
localhost access
  ↓
external access
```

이번 유닛에서는 Linux에서 이 흐름을 확인하는 최소 도구만 익힌다.

---

## 1. Port와 Listen

하나의 서버에서는 여러 프로그램이 동시에 네트워크를 사용할 수 있다. 어떤 프로그램으로 요청을 전달할지 구분하기 위해 포트를 사용한다.

```text
22   SSH
80   HTTP
443  HTTPS
8000 FastAPI 예시
```

FastAPI를 `0.0.0.0:8000`에서 실행했다면 프로세스가 8000번 포트에서 연결을 기다리는 상태, 즉 **listen** 중이라고 표현한다.

---

## 2. ss

현재 어떤 포트가 listen 중인지 확인할 때 다음을 사용할 수 있다.

```bash
ss -lntp
```

주요 의미는 다음 정도만 알면 된다.

```text
-l  listening
-n  주소와 포트를 숫자로 표시
-t  TCP
-p  관련 프로세스 표시
```

특정 포트만 확인한다면:

```bash
ss -lntp | grep 8000
```

애플리케이션 프로세스가 떠 있어도 원하는 포트를 listen하지 않고 있다면 외부 요청을 받을 수 없다.

---

## 3. localhost와 bind address

다음 둘은 의미가 다르다.

```text
127.0.0.1:8000
0.0.0.0:8000
```

`127.0.0.1`에만 bind하면 같은 서버 내부에서만 접근 가능하다.

`0.0.0.0`은 서버가 가진 모든 IPv4 인터페이스에서 해당 포트를 받겠다는 의미다.

따라서:

```text
curl localhost:8000 성공
외부에서는 접속 실패
```

라면 Security Group만 볼 것이 아니라 애플리케이션이 어느 주소에 bind되어 있는지도 확인해야 한다.

---

## 4. curl

HTTP 애플리케이션을 확인할 때 가장 유용한 도구 중 하나가 `curl`이다.

```bash
curl http://localhost:8000
```

헤더까지 확인하려면:

```bash
curl -i http://localhost:8000
```

서버 내부에서 localhost 요청이 성공한다면 최소한 다음은 정상일 가능성이 높다.

```text
process
application
local port
```

그런데 외부에서만 실패한다면 네트워크 계층으로 조사 범위를 좁힐 수 있다.

---

## 5. ip

서버의 네트워크 인터페이스와 주소를 확인할 때:

```bash
ip addr
```

라우팅 정보를 간단히 확인할 때:

```bash
ip route
```

AWS에서는 이후 EC2의 private IP, subnet, route table과 연결해서 다시 본다.

---

## 6. ping은 무엇을 확인하는가

```bash
ping <host>
```

`ping`은 ICMP를 이용해 네트워크 도달 가능성을 확인하는 도구다.

하지만 ping 실패가 곧 서비스 장애를 뜻하지는 않는다. ICMP가 차단되어 있어도 HTTP/HTTPS는 정상일 수 있다.

따라서 운영에서:

```text
ping 실패
→ 서버가 죽었다
```

라고 바로 결론 내리지 않는다.

---

## 7. 장애를 좁혀가는 순서

예를 들어 외부에서 FastAPI에 접근할 수 없다고 하자.

```bash
systemctl status myapp
ss -lntp | grep 8000
curl http://localhost:8000
ip addr
ip route
```

생각의 순서는 다음과 같다.

```text
프로세스가 죽었나?
  ↓ 아니오
포트를 listen하고 있나?
  ↓ 예
localhost 요청은 되나?
  ↓ 예
외부에서만 안 되나?
  ↓ 예
Security Group / NACL / Route / bind address 조사
```

이런 식으로 **문제의 계층을 하나씩 제거하는 것**이 중요하다.

---

## 최소 명령어

```bash
ss -lntp
curl <url>
ip addr
ip route
ping <host>
```

지금은 옵션을 외우기보다 각각이 무엇을 확인하는지 기억하면 충분하다.

## 앞으로의 연결

```text
EC2 → private/public IP
Security Group → 어떤 포트를 허용할 것인가
ALB → 어떤 target port로 전달할 것인가
VPC → subnet과 route
CloudWatch → 외부 관측과 로그
```

기초 확인용 유닛이므로 별도 유제와 3문장 요약은 생략한다.
