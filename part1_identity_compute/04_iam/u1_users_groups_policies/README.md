# u1. IAM Users, Groups, Policies

## 지도 확인

IAM(Identity and Access Management)은 AWS 리소스에 **누가 접근할 수 있고 무엇을 할 수 있는지**를 제어하는 서비스다.

강의에서는 IAM을 Global Service로 다루며, 가장 먼저 Root Account, User, Group, Policy의 관계를 설명한다.

```text
AWS Account
├── Root Account
├── IAM Users
│   ├── Alice
│   ├── Bob
│   └── Charles
├── IAM Groups
│   ├── Developers
│   └── Operations
└── IAM Policies
```

이번 유닛의 목표는 각 객체의 역할을 구분하는 것이다.

---

## 1. Root Account

AWS 계정을 만들면 Root Account가 생성된다.

Root Account는 계정 자체의 최상위 권한을 가지므로, 강의에서는 **초기 계정 설정 외에는 일상적인 작업에 사용하지 않는 것**을 권장한다.

```text
Root Account
→ 계정의 최상위 사용자
→ 평소 작업용 계정으로 사용하지 않음
```

이후 실제 AWS 작업은 IAM User나 IAM Role을 이용하게 된다.

---

## 2. IAM User

IAM User는 조직 안의 실제 사용자에게 대응되는 AWS 사용자다.

예:

```text
Alice
Bob
Charles
```

각 IAM User는 필요에 따라 AWS Console에 로그인하거나, 프로그램 방식으로 AWS API에 접근할 수 있다.

중요한 원칙은 다음이다.

```text
한 사람
→ 하나의 IAM User
```

여러 사람이 하나의 IAM User를 공유하는 방식은 피한다.

---

## 3. IAM Group

Group은 여러 IAM User를 묶는 단위다.

```text
Developers
├── Alice
├── Bob
└── Charles
```

강의에서 강조하는 특징은 다음과 같다.

- Group에는 User만 들어간다.
- Group 안에 다른 Group을 넣지 않는다.
- User는 Group에 반드시 속할 필요는 없다.
- 하나의 User가 여러 Group에 속할 수 있다.

예:

```text
Alice
├── Developers
└── Audit Team
```

Group을 사용하는 이유는 여러 사용자에게 같은 권한을 반복해서 설정하지 않기 위해서다.

```text
개별 User마다 권한 설정
        ↓
관리 어려움

Group에 권한 설정
        ↓
User를 Group에 추가
```

---

## 4. IAM Policy

Policy는 AWS에서 어떤 작업을 허용하거나 거부할지를 정의하는 JSON 문서다.

예를 들어 다음과 같은 의미의 Policy를 생각할 수 있다.

```text
EC2 정보 조회 허용
CloudWatch Metric 조회 허용
```

Policy는 User나 Group 등에 연결되어 권한을 결정한다.

```text
Policy
  ↓
Group: Developers
  ↓
Alice / Bob / Charles
```

---

## 5. Least Privilege

강의에서 IAM 권한의 핵심 원칙으로 **Least Privilege**를 제시한다.

```text
필요한 권한만 부여한다.
```

예를 들어 사용자가 EC2 목록 조회만 해야 한다면 처음부터 모든 AWS 서비스에 관리자 권한을 줄 이유가 없다.

```text
필요: EC2 조회

좋은 방향
→ EC2 조회 권한만 부여

나쁜 방향
→ 전체 관리자 권한 부여
```

이 원칙은 이후 Security Group, Linux Permission, Kubernetes RBAC 등에서도 반복되는 보안 사고방식과 연결된다.

---

## 6. 관계 정리

```text
User
→ 실제 사용자

Group
→ 여러 User를 묶음

Policy
→ 무엇을 할 수 있는지 정의
```

예:

```text
Policy: ReadOnlyEC2
        │
        ▼
Group: Developers
        │
   ┌────┴────┐
 Alice      Bob
```

---

## SAA 연결

시험에서는 이름 자체보다 관계를 구분하는 것이 중요하다.

```text
여러 개발자에게 같은 권한을 주고 싶다
→ Group에 Policy를 연결

사용자에게 필요한 권한만 주고 싶다
→ Least Privilege

Root Account를 일상적인 작업에 사용한다
→ 피해야 할 패턴
```

---

## 앞으로의 연결

다음 유닛에서는 Policy 내부 JSON 구조와 Policy가 User/Group에 어떻게 상속되는지 본다.

이번 유닛은 기본 구조를 이해하는 단계이므로 별도 유제와 3문장 요약은 생략한다.
