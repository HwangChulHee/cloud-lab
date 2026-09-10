# u6. RDS Security, Encryption & Authentication

## 지도 확인

RDS 보안은 크게 세 층으로 나눠서 보면 쉽다.

```text
1. 누가 DB에 접근할 수 있는가
→ Security Group / Network

2. DB에 접속할 때 누구인지 어떻게 증명하는가
→ DB 계정 / IAM Authentication / Secrets Manager

3. 데이터가 저장되거나 전송될 때 어떻게 보호하는가
→ KMS Encryption / SSL(TLS)
```

---

## 1. Security Group

RDS도 Security Group을 사용한다.

예를 들어 쇼핑몰 구조가:

```text
Internet
   ↓
ALB
   ↓
Spring App EC2
   ↓
RDS PostgreSQL
```

이라면 RDS를 인터넷 전체에 열 필요가 없다.

DB Security Group을:

```text
Inbound
TCP 5432
Source: Application Security Group
```

처럼 만들 수 있다.

뜻은:

> "5432번 PostgreSQL 포트로 들어오는 요청 중 Application SG가 붙은 자원에서 오는 요청만 허용"

이다.

```text
Internet ─X→ RDS
App EC2  ───→ RDS
```

이 패턴은 이전 Security Group 단원에서 본 **SG Reference**를 DB에 적용한 예다.

---

## 2. RDS를 Public으로 열면 안 되나

기술적으로 Public Access 설정이 가능한 경우가 있지만, 일반적인 운영 구조에서는 DB를 외부 인터넷에 직접 노출하지 않는 쪽이 안전하다.

예:

```text
Public Subnet
ALB

Private Subnet
App

Private/Data Subnet
RDS
```

핵심은:

```text
사용자
→ Application에 요청
→ Application이 DB 접근
```

이지:

```text
사용자
→ RDS 직접 접근
```

이 아니다.

SAA에서는 보통 **DB를 Private하게 두고 Application SG만 허용**하는 구조를 좋은 선택으로 본다.

---

## 3. Encryption at Rest

`At Rest`는 데이터가 저장되어 있는 상태를 말한다.

예:

```text
RDS Storage에 저장된 테이블 데이터
Snapshot
Backup
```

이런 데이터를 암호화할 때 KMS를 사용할 수 있다.

```text
Plain Data
   ↓ KMS Encryption
Encrypted Storage
```

KMS는 Key Management Service로, 암호화에 사용하는 키를 관리하는 AWS 서비스다.

시험에서는:

```text
RDS 데이터 저장 시 암호화
→ KMS
```

정도로 연결하면 된다.

---

## 4. Encryption in Transit

`In Transit`은 데이터가 네트워크를 통해 이동 중인 상태다.

```text
Application
   │ SQL query / result
   ▼
RDS
```

이 구간에서 데이터가 평문으로 오가면 중간에서 탈취될 위험이 있다.

그래서 SSL/TLS를 사용해 전송 구간을 암호화할 수 있다.

```text
Application
   │ TLS encrypted connection
   ▼
RDS
```

즉:

```text
At Rest
→ 저장된 데이터 암호화

In Transit
→ 이동 중 데이터 암호화
```

로 구분한다.

---

## 5. Database Username / Password

가장 일반적인 방식은 DB 계정과 비밀번호를 사용하는 것이다.

예:

```text
username = app_user
password = ********
```

문제는 이 비밀번호를 코드에 직접 넣으면 안 된다는 것이다.

나쁜 예:

```java
String password = "my-secret-password";
```

GitHub에 올라가면 큰 사고가 날 수 있다.

그래서 비밀값을 코드와 분리해야 한다.

---

## 6. Secrets Manager

AWS Secrets Manager는 비밀번호, API Key 같은 **Secret**을 저장하고 관리하는 서비스다.

예:

```text
Spring App
   │
   ├── Secrets Manager에서 DB password 조회
   │
   ▼
RDS
```

코드에는 비밀번호 자체를 넣지 않고, 필요한 시점에 권한을 가진 애플리케이션이 Secret을 가져오는 구조를 만들 수 있다.

개념적으로:

```text
Code
→ "DB 비밀번호는 Secrets Manager에서 가져와"

Secrets Manager
→ 실제 비밀번호 보관
```

이다.

RDS와 Secrets Manager를 연동해 credential 관리에 활용할 수 있다.

---

## 7. IAM Database Authentication

일부 RDS 엔진에서는 일반 비밀번호 대신 IAM 기반 인증을 사용할 수 있다.

쉽게 말하면:

> AWS IAM 권한을 이용해 DB 접속 인증을 처리하는 방식

이다.

일반 방식:

```text
Application
→ DB username/password
→ RDS
```

IAM Authentication:

```text
Application
→ IAM 권한 기반 임시 인증 정보
→ RDS
```

장점은 장기간 고정된 비밀번호를 애플리케이션에 들고 있는 부담을 줄일 수 있다는 점이다.

다만:

```text
IAM Authentication을 켰다
= Security Group이 필요 없어짐
```

은 아니다.

네트워크 접근 허용과 인증은 별개다.

```text
Security Group
→ 네트워크로 들어올 수 있는가

Authentication
→ 들어온 사용자가 누구인가
```

둘 다 만족해야 한다.

---

## 8. 예시 — Spring App → RDS

안전한 구조를 단순화하면:

```text
Spring App EC2
├── IAM Role
│    └── Secrets Manager 읽기 권한
│
└── SG: sg-app

RDS PostgreSQL
└── SG: sg-db
     inbound TCP 5432
     source: sg-app
```

애플리케이션은:

```text
1. Secrets Manager에서 DB credential 조회
2. TLS 연결 사용
3. RDS에 접속
```

하도록 만들 수 있다.

---

## SAA 판단

```text
RDS 접근을 Application Server로 제한
→ DB Security Group의 Source를 Application SG로 설정

저장된 RDS 데이터 암호화
→ KMS

Application ↔ RDS 전송 암호화
→ SSL/TLS

DB password 같은 Secret 관리
→ Secrets Manager

IAM을 이용한 DB 접속 인증
→ IAM Database Authentication
```

핵심은 **Network / Authentication / Encryption을 서로 다른 문제로 구분하는 것**이다.
