# u3. Routing, Firewall과 Troubleshooting

## 지도 확인

네트워크 장애를 볼 때는 단순히 "인터넷이 안 된다"고 보지 않고 패킷이 목적지까지 가는 경로와 각 구간의 허용 여부를 나눠 본다.

```text
Source
  ↓
Route
  ↓
Firewall
  ↓
Destination
  ↓
Application
```

---

## 1. Routing

Routing은 목적지 IP로 가기 위해 다음에 어디로 보낼지 결정하는 과정이다.

Linux에서는:

```bash
ip route
```

로 현재 route를 볼 수 있다.

AWS에서는 뒤에서 Route Table을 별도의 리소스로 다룬다.

예:

```text
10.0.0.0/16 → local
0.0.0.0/0   → Internet Gateway
```

`0.0.0.0/0`은 모든 IPv4 목적지를 의미하는 default route로 자주 등장한다.

---

## 2. Firewall

Firewall은 네트워크 트래픽을 규칙에 따라 허용하거나 차단한다.

AWS에서 대표적으로:

```text
Security Group
Network ACL
```

을 만나게 된다.

지금은 세부 차이보다 다음 형태에 익숙해지면 된다.

```text
Source → Destination : Protocol / Port
```

예를 들어 DB를 안전하게 구성하려면:

```text
Internet → RDS:5432   X
App SG   → RDS:5432   O
```

처럼 **필요한 주체에게 필요한 포트만 허용**하는 식으로 생각한다.

---

## 3. Timeout과 Connection Refused

둘은 비슷해 보이지만 조사 방향이 다르다.

### timeout

응답 자체를 받지 못한 경우다.

```text
route 문제
firewall 차단
대상이 도달 불가능
```

등을 의심할 수 있다.

### connection refused

목적지까지는 도달했지만 해당 포트에서 연결을 받아주는 서비스가 없는 경우 흔히 나타난다.

```text
process가 죽음
잘못된 port
127.0.0.1에만 bind
```

등을 확인한다.

AWS SAA 강의의 Security Group 파트에서도 timeout과 connection refused를 장애 판단의 중요한 단서로 구분한다.

---

## 4. 계층별로 좁히기

웹 서비스가 안 된다고 하자.

```text
1. DNS가 올바른 주소를 반환하는가?
2. Route가 존재하는가?
3. Security Group/NACL이 허용하는가?
4. 서버가 port를 listen하는가?
5. application이 정상 응답하는가?
6. downstream DB/API는 정상인가?
```

한 번에 모든 설정을 바꾸지 않고 위에서 아래로 하나씩 확인한다.

---

## 5. 최소 도구

```bash
ip addr
ip route
ss -lntp
curl -v <url>
ping <host>
```

DNS 확인 도구도 뒤에서 사용한다.

```bash
nslookup <domain>
dig <domain>
```

중요한 것은 명령어 개수가 아니라 **각 명령으로 어느 계층을 확인하는지**다.

---

## Cloud Engineer 관점

앞으로 장애 실험은 대부분 이 방식으로 한다.

```text
정상 상태 확인
→ 하나의 설정을 의도적으로 깨기
→ 현상 예측
→ 로그/명령/메트릭으로 관측
→ 원인 특정
→ 복구
```

이 유닛은 이후 EC2 + Security Group 장애 실습에서 다시 사용하므로 지금은 별도 유제와 3문장 요약을 생략한다.
