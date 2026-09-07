# u3. 계층별 Security Group 접근 제어

## 지도 확인

Security Group은 개별 서버의 포트를 여는 기능으로만 보면 아쉽다.
실제 아키텍처에서는 **계층 사이에 누가 누구에게 접근할 수 있는지** 표현하는 데 사용한다.

강의의 Stateful Web App 예시에서도 다음과 같은 흐름이 등장한다.

```text
Internet
   ↓
Load Balancer
   ↓
EC2 Application
   ↓
RDS / ElastiCache
```

핵심은 각 계층을 인터넷 전체에 공개하지 않고, **바로 앞 계층에서 필요한 트래픽만 허용**하는 것이다.

---

## 1. 3-Tier 구조

가장 기본적인 형태를 보자.

```text
Internet
   │
   ▼
[ ALB ]
SG: sg-alb
   │
   ▼
[ Application ]
SG: sg-app
   │
   ▼
[ Database ]
SG: sg-db
```

접근 정책을 역할 기준으로 표현하면:

```text
sg-alb
80 / 443 ← Internet

sg-app
Application Port ← sg-alb

sg-db
DB Port ← sg-app
```

이렇게 된다.

---

## 2. ALB 계층

ALB는 사용자 요청을 받는 공개 진입점이다.

예:

```text
Inbound
TCP 80  ← 0.0.0.0/0
TCP 443 ← 0.0.0.0/0
```

반면 Application EC2까지 같은 방식으로 인터넷 전체에 열 필요는 없다.

```text
잘못된 방향
Internet
   ├── ALB
   └── EC2 직접 접근 가능
```

보다:

```text
Internet
   ↓
ALB
   ↓
EC2
```

처럼 진입 경로를 제한하는 것이 구조적으로 명확하다.

---

## 3. Application 계층

Application Security Group은 ALB Security Group을 Source로 받을 수 있다.

예:

```text
TCP 8080
Source: sg-alb
```

그러면 Application이 Auto Scaling으로 여러 대가 되더라도 각 인스턴스의 IP를 규칙에 직접 추가할 필요가 없다.

```text
             ALB SG
                │
        ┌───────┴───────┐
        ▼               ▼
      App 1           App 2
      sg-app          sg-app
```

---

## 4. Database 계층

RDS는 일반 사용자에게 직접 노출할 이유가 없다.

예를 들어 PostgreSQL이라면:

```text
TCP 5432
Source: sg-app
```

처럼 Application 계층에서 오는 연결만 허용할 수 있다.

```text
Internet ─X→ RDS
ALB      ─X→ RDS
APP      ──→ RDS
```

MySQL이라면 대표적으로 `3306`을 사용한다.

SAA 문제에서는 특정 DB 포트 숫자 자체보다 다음 설계 원칙이 더 중요하다.

> Database는 Application 계층에서 필요한 접근만 허용한다.

---

## 5. Cache 계층도 같은 원리

ElastiCache 같은 내부 데이터 계층도 같은 방식으로 생각할 수 있다.

강의 예시에서는 RDS와 ElastiCache 접근을 EC2 Security Group에서 오는 요청으로 제한하는 구조를 보여준다.

```text
ALB SG
   ↓
APP SG
   ├──→ DB SG
   └──→ Cache SG
```

즉 Security Group을 **서버 단위가 아니라 아키텍처 관계 단위**로 이해하는 것이 중요하다.

---

## 6. Least Privilege와 연결

IAM에서 배웠던 Least Privilege 사고방식은 네트워크에서도 그대로 적용할 수 있다.

```text
필요한 대상만
필요한 Port만
필요한 방향으로만
```

예:

```text
DB 5432 ← APP SG
```

이면 충분한데:

```text
DB 5432 ← 0.0.0.0/0
```

로 열어둘 이유는 없다.

IAM과 Security Group은 서로 다른 계층이지만, **필요 최소 권한/접근만 허용한다는 설계 원칙**은 같다.

---

## SAA 연결

```text
공개 웹 진입점
→ ALB SG에 80/443 인터넷 허용

Application을 ALB 뒤에 숨김
→ APP SG가 ALB SG만 허용

RDS 직접 노출 방지
→ DB SG가 APP SG만 허용

인스턴스가 Auto Scaling으로 교체됨
→ IP 목록보다 SG Reference 사용

다계층 아키텍처
→ 각 계층 간 필요한 Port만 연결
```

이번 유닛은 이후 ALB/RDS 파트에서 다시 반복해서 사용한다.
시험 전에는 구조와 선택 기준을 이해하는 수준으로 두고, 실제 장애 실험은 SAA 취득 후 Cloud Shop에서 진행한다.
