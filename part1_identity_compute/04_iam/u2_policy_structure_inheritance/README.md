# u2. IAM Policy Structure와 Inheritance

## 지도 확인

IAM Policy는 권한을 설명하는 JSON 문서다.

이번 유닛에서는 강의의 두 내용을 연결해서 본다.

1. Policy가 User와 Group을 통해 어떻게 적용되는가
2. Policy JSON이 어떤 구조를 가지는가

---

## 1. Policy Inheritance

User가 Group에 속하면 그 Group에 연결된 Policy의 권한을 받는다.

```text
Developers Group
└── EC2 Read Policy

Alice ∈ Developers
        ↓
Alice도 EC2 Read 권한을 가짐
```

한 User가 여러 Group에 속할 수도 있으므로 여러 Group의 권한이 함께 적용될 수 있다.

```text
Alice
├── Developers
│   └── EC2 관련 권한
└── Audit Team
    └── 감사 관련 권한
```

또 User에게 직접 Policy를 연결할 수도 있다.

```text
User
├── Group에서 받은 권한
└── 직접 연결된 권한
```

강의의 핵심은 **권한이 어디에서 왔는지 추적할 수 있어야 한다**는 것이다.

---

## 2. Policy 기본 구조

강의에서는 IAM Policy를 다음 요소로 설명한다.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:Describe*",
      "Resource": "*"
    }
  ]
}
```

이 예제는 구조를 이해하기 위한 최소 형태다.

---

## 3. Version

```json
"Version": "2012-10-17"
```

Policy language의 버전을 나타낸다.

강의에서는 `2012-10-17`을 포함하는 형태를 기본으로 설명한다.

---

## 4. Statement

실제 권한 규칙이 들어가는 부분이다.

```json
"Statement": [ ... ]
```

하나 이상의 Statement를 둘 수 있다.

각 Statement에는 다음 요소가 등장할 수 있다.

```text
Sid
Effect
Principal
Action
Resource
Condition
```

---

## 5. Effect

```json
"Effect": "Allow"
```

또는:

```json
"Effect": "Deny"
```

해당 규칙이 접근을 허용하는지 거부하는지 나타낸다.

---

## 6. Action

어떤 AWS API 동작을 허용하거나 거부할지 나타낸다.

```json
"Action": "ec2:Describe*"
```

의미:

```text
EC2의 Describe 계열 동작
```

여러 Action을 지정할 수도 있다.

```json
"Action": [
  "cloudwatch:ListMetrics",
  "cloudwatch:GetMetricStatistics"
]
```

AWS Console의 버튼을 누르는 행위도 결국 뒤에서는 AWS API 동작과 연결된다고 생각하면 이해하기 쉽다.

---

## 7. Resource

Action이 어떤 리소스에 적용되는지를 나타낸다.

```json
"Resource": "*"
```

`*`는 해당 Statement에서 모든 대상 리소스를 의미한다.

이후 S3나 IAM을 공부하면 특정 ARN을 Resource로 제한하는 예제를 보게 된다.

---

## 8. Principal

강의에서는 Principal을 Policy가 적용되는 account/user/role을 표현하는 요소로 소개한다.

Principal은 이후 Role의 Trust Policy나 S3 Bucket Policy 같은 내용을 공부할 때 더 중요하게 다시 등장한다.

지금은:

```text
Principal
→ 누가 이 규칙의 주체인가
```

정도로 기억한다.

---

## 9. Condition

Policy가 적용되는 추가 조건을 지정할 수 있다.

```text
특정 조건일 때만 허용/거부
```

강의 초반 IAM 섹션에서는 구조를 이해하는 정도로 보고, 구체적인 Condition 예시는 뒤의 Advanced Identity에서 다시 나온다.

---

## 10. Policy를 읽는 순서

처음부터 JSON 전체를 외우지 말고 다음 순서로 읽으면 된다.

```text
1. Effect
   → 허용인가 거부인가?

2. Action
   → 무엇을 할 수 있는가?

3. Resource
   → 어디에 할 수 있는가?

4. Principal / Condition
   → 누구에게, 어떤 조건에서 적용되는가?
```

예:

```json
{
  "Effect": "Allow",
  "Action": "ec2:Describe*",
  "Resource": "*"
}
```

읽기:

```text
Allow
→ 허용한다

ec2:Describe*
→ EC2 Describe 계열 동작을

Resource: *
→ 대상 리소스 범위에 대해
```

---

## SAA 연결

IAM 문제를 만나면 JSON 자체를 암기하기보다 다음을 구분한다.

```text
누가?
→ Principal / User / Group / Role

무엇을?
→ Action

어디에?
→ Resource

허용인가 거부인가?
→ Effect
```

또 User의 권한은 직접 연결된 Policy뿐 아니라 속한 Group의 Policy에서도 올 수 있다는 점을 기억한다.

---

## 작은 확인 문제

다음 Policy의 의미를 읽어본다.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:Describe*",
      "Resource": "*"
    }
  ]
}
```

스스로 다음 세 질문에 답할 수 있으면 충분하다.

1. Allow인가 Deny인가?
2. 어떤 서비스의 어떤 계열 Action인가?
3. Resource 범위는 어디까지인가?

별도 답안 파일은 만들지 않는다.
