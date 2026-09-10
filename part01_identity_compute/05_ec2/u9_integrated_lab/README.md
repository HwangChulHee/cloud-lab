# u9. EC2 Integrated Lab

## 목표

EC2 강의를 끝낸 뒤 핵심 개념을 실제 한 번에 연결한다.

이번 유닛에서는 다음 흐름을 직접 확인한다.

```text
Launch
→ User Data
→ Security Group
→ SSH / EC2 Instance Connect
→ Purchasing Option 판단
→ Public / Private IP
→ Stop / Start
→ 상태 관측
```

EC2는 이후 EBS, Load Balancer, Auto Scaling의 기반이므로 여기서는 유제와 3문장 요약을 진행한다.

---

## 1. 구축

강의 Hands-on을 따라 Linux EC2 한 대를 생성한다.

조건:

```text
Region: 학습용 Region 하나 고정
AMI: Linux
Instance Type: 학습용 소형 General Purpose
User Data: 간단한 웹 서버 설치/시작
Security Group: SSH와 HTTP를 필요한 범위에서 허용
```

인스턴스가 실행되면 Console에서 다음을 확인한다.

```text
Instance ID
Instance Type
Availability Zone
Private IPv4
Public IPv4
Security Group
Instance State
```

---

## 2. 관측

브라우저 또는 curl로 User Data가 만든 웹 서버가 응답하는지 확인한다.

```bash
curl http://<PUBLIC_IP>
```

그 다음 SSH 또는 EC2 Instance Connect로 서버 내부에 들어가 다음을 확인한다.

```bash
hostname
ip addr
ps aux
ss -lntp
```

0부에서 배운 Linux와 EC2 Console의 정보를 연결해서 본다.

---

## 3. Security Group 관측

정상 동작을 먼저 확인한 뒤 HTTP inbound rule을 잠시 제거하거나 제한한다.

예상:

```text
EC2 State: running
웹 서버 process: running
localhost curl: success
외부 HTTP: timeout
```

다시 rule을 복구하고 외부 접근이 돌아오는지 확인한다.

목표는 다음을 직접 구분하는 것이다.

```text
EC2가 살아 있음
!=
외부에서 EC2에 접근 가능함
```

---

## 4. Stop / Start 관측

현재 Public IP를 기록한다.

```text
Before stop: ______
```

EC2를 stop 후 다시 start한다.

다시 Public IP를 기록한다.

```text
After start: ______
```

그리고 다음을 설명한다.

```text
왜 Public IP가 달라질 수 있는가?
Private IP와 Public IP의 역할은 어떻게 다른가?
고정 Public IPv4가 정말 필요하다면 무엇을 고려할 수 있는가?
```

---

## 5. 판단 유제

### 유제 1 — Instance Type

다음 workload에 어떤 계열을 먼저 검토할지 이유까지 적는다.

1. 일반적인 API 서버
2. CPU 집약적 영상 변환
3. 대규모 in-memory cache
4. 높은 local storage I/O가 중요한 시스템

### 유제 2 — Purchasing Option

다음 요구사항에 가장 먼저 떠올릴 구매 옵션과 이유를 적는다.

1. 사용 패턴을 아직 모르는 신규 서비스
2. 3년 동안 거의 항상 실행되는 안정적 workload
3. 중간에 종료되어도 다시 실행 가능한 batch job
4. 기존 서버 단위 라이선스를 가져와야 하는 시스템
5. 특정 AZ에 반드시 capacity가 확보되어야 하는 시스템

### 유제 3 — Placement Group

다음 상황에서 Cluster / Spread / Partition 중 하나를 선택하고 이유를 적는다.

1. 초저지연 네트워크가 최우선인 HPC 작업
2. 소수의 중요 서버를 서로 다른 물리 하드웨어에 분리
3. 수백 대 규모 Kafka/Hadoop 계열 분산 시스템

### 유제 4 — 장애 분석

아래 상태에서 가장 먼저 어디를 확인할지 적는다.

```text
EC2 State: running
웹 요청: timeout
SSH: timeout
```

그리고 다음 상태와 비교한다.

```text
EC2 State: running
SSH: success
curl localhost: success
외부 웹 요청: timeout
```

두 상황에서 문제를 좁혀가는 순서를 설명한다.

---

## 6. 운영 질문

다음 질문에 자신의 말로 답한다.

1. EC2가 `running`이라는 것과 애플리케이션이 정상이라는 것은 왜 다른가?
2. User Data는 어떤 문제를 해결하는가?
3. Spot Instance가 저렴함에도 모든 서버를 Spot으로 만들지 않는 이유는 무엇인가?
4. Elastic IP 대신 Load Balancer나 DNS를 선호할 수 있는 이유는 무엇인가?
5. Security Group에서 차단된 요청과 애플리케이션이 거절한 요청은 관측상 어떻게 달라질 수 있는가?
6. ENI를 독립적인 네트워크 카드로 이해하면 어떤 점이 편해지는가?

---

## 포트폴리오 반영

이 실습 자체를 포트폴리오라고 생각하지 않는다.

이후 Stage 1에서 실제 애플리케이션을 EC2에 배포하면서 다음을 기록한다.

```text
왜 이 instance type을 선택했는가?
어떤 초기화 작업을 자동화했는가?
어떤 Security Group rule을 왜 열었는가?
서버 상태와 application 상태를 어떻게 구분했는가?
외부 접근 장애가 났을 때 어떤 순서로 확인했는가?
```

EBS와 Security Group 심화를 배운 뒤 이 EC2를 다시 확장한다.

---

## 3문장 요약

1.
2.
3.

작성한 유제와 3문장 요약은 ChatGPT에게 보여주고 피드백을 받는다.
