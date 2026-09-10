# 66. VPC Flow Logs / Networking Troubleshooting

이 챕터는 `examples/15-troubleshooting-web-stack`을 준비하기 위한 네트워크 진단 파트다.

## 1. VPC Flow Logs

VPC Flow Logs는 VPC 네트워크 인터페이스를 통과하는 IP 트래픽에 대한 메타데이터를 기록한다.

Flow Logs는 다음 수준에서 만들 수 있다.

```text
VPC
Subnet
Network Interface
```

패킷 내용(payload)을 캡처하는 도구가 아니라, 어떤 source/destination/port/protocol의 흐름이 허용 또는 거부되었는지 분석하는 데 사용한다.

## 2. 왜 필요한가?

예를 들어 애플리케이션에서 DB 연결이 timeout 난다고 하자.

원인은 다양하다.

```text
EC2-SG 문제
RDS-SG 문제
NACL 문제
Route Table 문제
DB 프로세스/포트 문제
DNS 문제
```

Flow Logs를 보면 네트워크 계층에서 트래픽이 전달/거부되는지 판단하는 데 도움을 받을 수 있다.

## 3. ACCEPT / REJECT

Flow Log record에서 중요한 신호 중 하나가 traffic action이다.

```text
ACCEPT
REJECT
```

`REJECT`가 보인다고 무조건 Security Group 하나만 원인이라고 단정하지 않는다. SG/NACL을 포함한 네트워크 접근 제어와 실제 경로를 함께 확인한다.

## 4. 계층별 장애 진단 순서

웹 요청이 실패할 때 요청 경로를 따라간다.

```text
Client
  ↓
DNS / Route 53
  ↓
ALB Listener
  ↓
Target Group / Health Check
  ↓
ALB-SG
  ↓
EC2-SG
  ↓
EC2 process
  ↓
RDS-SG
  ↓
RDS
```

중요한 원칙은 `AWS가 안 된다`라고 뭉뚱그리지 않고 계층을 좁히는 것이다.

## 5. 증상별 출발점

### Timeout

우선 네트워크 차단 가능성을 생각한다.

```text
Route Table
Security Group
NACL
대상 서비스가 실제 포트를 listen 중인지
```

### Connection refused

네트워크 경로는 도달했지만 대상 포트에서 프로세스가 듣고 있지 않을 가능성을 우선 점검한다.

### ALB 503

```text
Target Group에 healthy target이 있는가?
ASG instance가 등록됐는가?
Health Check가 성공하는가?
```

### Target unhealthy

```text
Health Check path / port
EC2 application process
EC2-SG가 ALB-SG를 허용하는지
애플리케이션이 기대한 status code를 반환하는지
```

### DB 연결 timeout

```text
DNS endpoint
EC2 → RDS route
RDS-SG source
NACL
DB port
```

### S3 AccessDenied

`AccessDenied`는 일반적으로 단순 네트워크 timeout과 다른 신호다.

```text
IAM Role
IAM Policy
Bucket Policy
Endpoint Policy
```

를 우선 확인한다.

## 6. Route Table 디버깅

패킷마다 질문한다.

```text
Source는 어디인가?
Destination은 어디인가?
어느 subnet에 있는가?
그 subnet의 route table은 무엇인가?
가장 구체적으로 일치하는 route는 무엇인가?
다음 hop은 무엇인가?
```

## 7. SG 디버깅

```text
Client → ALB
ALB → EC2
EC2 → RDS
```

각 화살표를 독립적으로 본다.

예:

```text
ALB-SG :443 from 0.0.0.0/0
EC2-SG :80 from ALB-SG
RDS-SG :5432 from EC2-SG
```

어느 한 계층의 source reference를 잘못 지정해도 전체 서비스가 실패할 수 있다.

## 8. NACL 디버깅

NACL은 stateless이므로 요청 방향뿐 아니라 응답 방향도 확인한다.

특히 임시 포트(ephemeral ports)와 rule number 순서를 놓치지 않는다.

## 9. Flow Logs가 해결하지 못하는 것

Flow Logs만 보고 다음을 직접 알 수 있는 것은 아니다.

- 애플리케이션 내부 exception
- SQL query 오류
- HTTP response body
- 프로세스 stack trace

따라서:

```text
Flow Logs → 네트워크 흐름 확인
CloudWatch/application logs → 애플리케이션 원인 확인
Metrics → 자원 상태와 시간적 변화 확인
```

처럼 도구를 조합한다.

## 10. 실습 전 Recall Check

- Timeout과 connection refused는 어떤 차이를 시사하는가?
- ALB 503이면 어디부터 확인할 것인가?
- Target unhealthy라면 네트워크와 애플리케이션 중 어떤 항목을 확인할 것인가?
- Flow Logs의 ACCEPT/REJECT는 무엇을 알려주는가?
- S3 AccessDenied를 Route Table부터 확인하는 것이 비효율적일 수 있는 이유는?

## 11. 완료 기준

- [ ] Client → ALB → EC2 → RDS 요청 경로를 순서대로 진단할 수 있다.
- [ ] Timeout / refused / 503 / unhealthy / AccessDenied를 구분해 첫 확인 지점을 고를 수 있다.
- [ ] Route Table / SG / NACL의 역할을 섞지 않는다.
- [ ] Flow Logs와 CloudWatch Logs의 차이를 설명할 수 있다.
- [ ] 장애 시 가설 → 관찰 → 원인 → 복구 순서로 접근할 수 있다.
