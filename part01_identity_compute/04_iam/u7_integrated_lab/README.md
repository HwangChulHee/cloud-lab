# u7. IAM Integrated Lab

## 목표

지금까지 배운 IAM 개념을 실제 AWS 계정 안에서 한 번 연결한다.

이번 유닛은 단순 암기가 아니라 다음 흐름을 직접 확인하는 데 목적이 있다.

```text
User
→ Group
→ Policy
→ CLI
→ Role
→ Audit
```

IAM은 이후 모든 AWS 서비스의 권한 문제와 연결되므로 여기서는 유제와 3문장 요약을 진행한다.

---

## 1. 실습 전 원칙

실습하면서 다음은 지킨다.

- Root Account를 일상 작업용으로 사용하지 않는다.
- Secret Access Key를 코드나 GitHub에 올리지 않는다.
- 실습용 User와 Policy에는 필요한 권한만 준다.
- 실습이 끝난 뒤 불필요한 Credential과 리소스를 정리한다.

---

## 2. 예제: User → Group → Policy

AWS Console에서 다음 구조를 만든다.

```text
Group: cloud-lab-readonly
        │
        └── ReadOnly 성격의 Policy

User: cloud-lab-user
        │
        └── cloud-lab-readonly Group
```

강의 화면을 따라 IAM User와 Group을 생성하고 Group에 Policy를 연결한다.

그 다음 해당 User의 권한이 어디에서 왔는지 Console에서 확인한다.

확인할 질문:

```text
이 User에게 직접 Policy가 붙어 있는가?
Group을 통해 Policy가 적용되는가?
```

---

## 3. 예제: CLI 호출 주체 확인

강의의 CLI 실습을 진행한 뒤 다음 명령으로 현재 호출 주체를 확인한다.

```bash
aws sts get-caller-identity
```

확인:

```text
Account
UserId
Arn
```

중요한 것은 명령 실행 자체보다 다음 질문이다.

> 지금 이 AWS API 요청은 누구의 권한으로 실행되고 있는가?

---

## 4. 예제: 허용된 작업과 거부된 작업

실습 User에 제한된 권한만 주고 AWS CLI나 Console에서 허용된 작업과 허용되지 않은 작업을 비교한다.

예를 들어 읽기 성격의 권한만 가진 User라면:

```text
조회
→ 성공

리소스 변경/삭제
→ 권한에 따라 거부
```

실제 결과는 연결한 Policy에 따라 달라진다.

목표는 `AccessDenied`를 만나면 단순 오류가 아니라 다음 관점으로 보는 것이다.

```text
누구의 요청인가?
어떤 Action인가?
어떤 Policy가 적용되는가?
```

---

## 5. Role은 EC2 파트에서 완성한다

IAM Role은 지금 Console에서 위치와 개념을 확인하되, 핵심 실습은 EC2와 S3를 배운 뒤 진행한다.

최종적으로 만들 구조:

```text
EC2
 ↓ IAM Role
S3
```

목표:

```text
코드에 Access Key를 직접 저장하지 않고
EC2가 Role을 이용해 S3에 접근
```

따라서 이 항목은 지금 당장 완성하지 않아도 된다.

---

## 6. Audit 확인

IAM Console에서 다음 두 도구의 위치를 찾아본다.

```text
Credentials Report
Access Advisor
```

그리고 역할을 다시 구분한다.

```text
Credentials Report
→ Account-level

Access Advisor
→ User-level
```

---

# 유제

## 유제 1. 권한의 출처 추적

다음 구조가 있다.

```text
Alice
├── Developers Group
│   └── EC2 Read Policy
└── Audit Group
    └── CloudWatch Read Policy
```

질문:

1. Alice는 어떤 경로를 통해 EC2 권한을 얻는가?
2. CloudWatch 권한은 어디에서 오는가?
3. Alice에게 직접 연결된 Policy가 없어도 권한을 가질 수 있는가?

답을 README 아래에 자신의 말로 작성한다.

---

## 유제 2. Policy 읽기

다음 Policy를 읽어본다.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeSecurityGroups"
      ],
      "Resource": "*"
    }
  ]
}
```

다음 형식으로 설명한다.

```text
Effect:
Action:
Resource:
전체 의미:
```

---

## 유제 3. 어떤 IAM 객체를 사용할까?

각 상황에서 가장 먼저 떠올릴 IAM 개념을 적는다.

### 상황 A

개발자 10명에게 동일한 AWS 권한을 부여해야 한다.

### 상황 B

EC2가 다른 AWS 서비스의 API를 호출해야 한다.

### 상황 C

IAM User의 비밀번호가 유출되어도 추가 인증을 요구하고 싶다.

### 상황 D

특정 IAM User에게 부여된 서비스 권한과 최근 사용 여부를 확인하고 싶다.

### 상황 E

계정 전체 IAM User의 Credential 상태를 점검하고 싶다.

---

## 유제 4. 장애 분석

CLI에서 다음 결과가 발생했다.

```text
AccessDenied
```

무작정 관리자 권한을 부여하기 전에 어떤 순서로 확인할지 적는다.

힌트:

```text
Identity
Action
Policy
Resource
```

---

# 3문장 요약

아래 세 문장을 직접 채운다.

```text
1.

2.

3.
```

가능하면 다음 세 주제를 각각 한 문장에 담는다.

```text
Identity
Permission
Security / Audit
```

작성한 뒤 나에게 보여주면 유제 답과 3문장 요약을 같이 확인한다.

---

## IAM Section 완료 기준

다음 질문에 바로 답할 수 있으면 초기 IAM 섹션은 넘어가도 된다.

```text
User / Group / Policy / Role의 차이는?
Least Privilege란?
Policy의 Effect / Action / Resource는?
Console / CLI / SDK는 어떻게 다른가?
Access Key를 왜 보호해야 하는가?
MFA는 무엇을 해결하는가?
Credentials Report와 Access Advisor의 차이는?
EC2가 AWS 서비스에 접근할 때 무엇을 사용하는가?
```

여기까지 되면 다음은 EC2로 넘어간다.
