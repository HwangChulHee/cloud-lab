# u6. IAM Security Tools와 Best Practices

## 지도 확인

강의의 IAM 마지막 부분에서는 권한을 부여하는 방법보다 **현재 계정의 IAM 상태를 점검하고 권한을 정리하는 방법**을 다룬다.

핵심 도구는 두 가지다.

```text
IAM Credentials Report
IAM Access Advisor
```

그리고 마지막에 IAM Best Practices를 정리한다.

---

## 1. IAM Credentials Report

Credentials Report는 **Account-level** 도구다.

강의에서는 AWS 계정 안의 IAM User들과 각 사용자의 Credential 상태를 확인할 수 있는 보고서로 설명한다.

개념적으로는 다음 질문에 답하기 위한 도구다.

```text
이 계정에는 어떤 IAM User가 있는가?
각 User의 Credential 상태는 어떤가?
```

여러 사용자의 보안 상태를 한 번에 점검할 때 사용하는 관점으로 이해한다.

---

## 2. IAM Access Advisor

Access Advisor는 **User-level** 도구다.

강의에서는 해당 User에게 어떤 서비스 권한이 부여되어 있는지와, 그 서비스가 언제 마지막으로 사용되었는지를 확인하는 데 사용할 수 있다고 설명한다.

이 정보를 이용해 오래 사용하지 않은 권한을 정리할 수 있다.

```text
권한 부여
 ↓
실제 사용 여부 확인
 ↓
불필요한 권한 제거
```

이 흐름은 Least Privilege를 유지하는 데 중요하다.

---

## 3. Credentials Report vs Access Advisor

```text
Credentials Report
→ Account-level
→ 여러 IAM User의 Credential 상태 확인

Access Advisor
→ User-level
→ User의 서비스 권한과 최근 사용 여부 확인
```

시험에서는 두 도구의 범위를 바꿔 묻는 식으로 구분 문제가 나올 수 있으므로 이름과 역할을 연결한다.

---

## 4. IAM Best Practices

강의에서 정리하는 IAM Best Practices를 현재까지 배운 개념과 연결하면 다음과 같다.

### Root Account

```text
Root Account
→ 초기 계정 설정 외에는 사용하지 않음
```

### User

```text
한 사람
→ 하나의 IAM User
```

IAM User를 여러 사람이 공유하지 않는다.

### Group

```text
User
→ Group에 배치
→ Group에 권한 부여
```

여러 사용자에게 공통 권한을 관리할 때 Group을 활용한다.

### Password

```text
Strong Password Policy
```

비밀번호 정책으로 계정 보안을 강화한다.

### MFA

```text
Root / IAM User
→ MFA 사용
```

### Role

```text
AWS Service
→ IAM Role 사용
```

서비스에 필요한 권한을 Role로 제공한다.

### Programmatic Access

```text
CLI / SDK
→ Access Keys
```

그리고 Access Key는 공유하지 않는다.

### Audit

```text
Credentials Report
Access Advisor
→ IAM 권한과 Credential 점검
```

---

## 5. IAM 전체 구조 다시 보기

```text
AWS Account
│
├── Root Account
│
├── IAM Users
│   └── Groups
│       └── Policies
│
├── IAM Roles
│   └── Policies
│
├── Password Policy / MFA
│
├── Access
│   ├── Console
│   ├── CLI
│   └── SDK
│
└── Audit
    ├── Credentials Report
    └── Access Advisor
```

이 그림이 초기 IAM 섹션 전체 지도다.

---

## SAA 연결

다음 표현을 바로 연결할 수 있으면 된다.

```text
계정 전체 IAM User Credential 상태
→ Credentials Report

특정 User가 어떤 서비스를 언제 마지막으로 사용했는지
→ Access Advisor

AWS 서비스에 권한 제공
→ IAM Role

최소한의 권한만 부여
→ Least Privilege

Root Account 일상 사용
→ 피해야 함
```

---

## 다음 단계

IAM 개념 학습은 여기까지가 강의 초반 IAM 섹션의 핵심이다.

다음 유닛에서는 지금까지의 내용을 실제 AWS 계정에서 한 번 연결해본다.
