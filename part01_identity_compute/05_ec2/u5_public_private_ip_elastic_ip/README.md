# u5. Public IP, Private IP와 Elastic IP

## 지도 확인

EC2를 외부에서 접근하려면 인스턴스가 어떤 IP를 가지고 있고 그 IP가 어디에서 사용되는지 구분해야 한다.

```text
Private IP
→ VPC 내부 통신

Public IP
→ 인터넷에서 접근 가능한 주소

Elastic IP
→ 고정된 Public IPv4
```

Security Group과 SSH를 먼저 본 뒤 이 주소 체계를 연결하면 EC2 접속 흐름이 더 명확해진다.

---

## 1. Private IP

EC2는 VPC 내부에서 통신하기 위한 Private IP를 가진다.

```text
EC2 A 10.x.x.x
   ↓
VPC 내부
   ↓
EC2 B 10.x.x.x
```

Private IP는 인터넷에서 직접 라우팅되는 주소가 아니다.

---

## 2. Public IP

인터넷에서 EC2에 직접 접근하려면 Public IPv4가 사용될 수 있다.

```text
Local PC
  ↓ Internet
EC2 Public IP
  ↓
EC2 Private IP / ENI
```

Public IP가 있다고 해서 무조건 접근되는 것은 아니다. Security Group, Route, 서버 프로세스 등 다른 조건도 함께 맞아야 한다.

---

## 3. Stop / Start와 Public IP

자동 할당된 Public IPv4는 일반적인 stop/start 과정에서 변경될 수 있다.

```text
Before stop
→ Public IP A

Stop → Start

After start
→ Public IP B
```

따라서 애플리케이션 설정에 일회성 Public IP를 영구 주소처럼 박아두는 것은 취약할 수 있다.

---

## 4. Elastic IP

고정 Public IPv4가 필요하면 Elastic IP를 사용할 수 있다.

```text
Elastic IP
→ 계정에 할당
→ EC2의 네트워크 인터페이스와 연결
```

하지만 고정 IP가 필요하지 않다면 DNS나 Load Balancer 같은 계층을 사용하는 설계가 더 자연스러울 수 있다.

즉:

```text
IP를 고정해야 한다
```

와

```text
사용자가 항상 같은 주소로 서비스에 접근해야 한다
```

는 같은 요구사항이 아닐 수 있다. 후자는 DNS로 해결할 수 있다.

---

## 장애 분석

SSH가 되지 않는다고 하자.

```text
1. EC2가 running인가?
2. 현재 Public IP가 맞는가?
3. Security Group에서 22를 허용하는가?
4. 네트워크 경로가 존재하는가?
5. username / key가 맞는가?
6. sshd가 실행 중인가?
```

이 순서처럼 IP, AWS 네트워크, OS, 프로세스를 분리해서 본다.

---

## SAA 연결

```text
VPC 내부 주소
→ Private IP

인터넷에서 직접 접근 가능한 동적 주소
→ Public IP

고정 Public IPv4
→ Elastic IP
```

Elastic IP는 유용하지만 무조건적인 기본 선택이 아니다. 이후 Route 53과 Load Balancer를 배울 때 다시 비교한다.

이번 유닛은 0부 네트워크와 겹치는 부분이 많으므로 별도 유제와 3문장 요약은 생략한다.
