# u5. IAM Roles for Services

## 지도 확인

AWS 서비스 자체가 다른 AWS 서비스의 API를 호출해야 하는 경우가 있다.

예를 들어 EC2 위의 애플리케이션이 S3에서 파일을 읽는 상황이다.

```text
EC2
 ↓
S3 GetObject
```

이때 강의에서는 AWS 서비스에 권한을 부여하기 위해 **IAM Role**을 사용한다고 설명한다.

---

## 1. Role은 왜 필요한가

사람에게는 IAM User가 있을 수 있지만 EC2나 Lambda 같은 AWS 서비스는 사람이 아니다.

그러나 이런 서비스도 다른 AWS 리소스에 접근하려면 권한이 필요하다.

```text
EC2
→ S3 접근 필요

Lambda
→ DynamoDB 접근 필요

CloudFormation
→ 여러 AWS 리소스 생성 필요
```

이때 Role을 연결한다.

---

## 2. 기본 구조

```text
EC2 Instance
     │
     ▼
  IAM Role
     │
     ▼
 IAM Policy
     │
     ▼
     S3
```

Role에 Policy가 연결되고, 그 Role을 EC2 같은 서비스가 사용한다.

강의의 대표적인 Role 예시는 다음과 같다.

- EC2 Instance Role
- Lambda Function Role
- CloudFormation Role

---

## 3. User와 Role 구분

초기 학습 단계에서는 다음 정도로 구분하면 된다.

```text
IAM User
→ 사람을 표현

IAM Role
→ AWS 서비스 등이 필요한 권한을 사용하도록 연결
```

강의의 IAM Summary에서도 User는 physical user에 대응하고 Role은 EC2 instance나 AWS service에 연결되는 것으로 정리한다.

---

## 4. Access Key를 EC2에 넣는 방식과 비교

다음 구조를 생각해보자.

```text
EC2 application
 ↓
코드에 Access Key 저장
 ↓
S3
```

이 방식은 Credential을 직접 관리해야 한다.

반면 Role을 사용하면 개념적으로 다음처럼 바뀐다.

```text
EC2
 ↓
IAM Role
 ↓
S3
```

따라서 EC2가 AWS 서비스에 접근해야 할 때 강의에서 배운 Role을 먼저 떠올린다.

---

## 5. Least Privilege와 Role

Role이라고 해서 무조건 큰 권한을 주는 것은 아니다.

예를 들어 EC2가 특정 S3 Bucket에서 파일만 읽어야 한다면 필요한 작업에 맞게 Policy를 제한하는 방향으로 생각한다.

```text
EC2 Role
 ↓
필요한 S3 권한
```

즉 앞에서 배운 Least Privilege 원칙은 User와 Group뿐 아니라 Role에도 이어진다.

---

## 6. 이후 실습에서 확인할 것

EC2 파트에서 실제 인스턴스를 만들게 되면 다음 구조를 실습 대상으로 삼는다.

```text
EC2
 ↓ IAM Role
S3
```

목표는 애플리케이션 코드에 AWS Access Key를 직접 넣지 않고 EC2가 Role을 통해 권한을 사용하게 만드는 것이다.

이 실습은 S3를 배운 뒤 더 완전하게 진행한다.

---

## SAA 연결

문제에서 다음 패턴이 보이면 Role을 떠올린다.

```text
EC2가 AWS 서비스에 접근해야 한다
→ IAM Role

Lambda가 다른 AWS 서비스를 호출해야 한다
→ IAM Role

AWS 서비스에 권한을 부여한다
→ Role을 우선 검토
```

---

## 핵심 구분

```text
User
→ 사람

Group
→ User 묶음

Policy
→ 권한 정의

Role
→ AWS 서비스 등이 사용할 권한을 연결
```

IAM에서 가장 중요한 관계 중 하나이므로 이 네 가지는 바로 구분할 수 있어야 한다.
