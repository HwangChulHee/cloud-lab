# u4. IAM Policy, Bucket Policy & ACL

## 1. S3 권한은 어디에 붙는가

S3 접근 제어는 크게 **사용자 쪽 정책**과 **리소스 쪽 정책**을 구분하면 이해하기 쉽다.

```text
IAM Policy
→ 사용자 / Role에 붙는 정책

Bucket Policy
→ S3 Bucket 자체에 붙는 정책
```

예를 들어 개발자 Alice에게 `my-bucket` 읽기 권한을 주는 방법은 둘 다 가능하다.

```text
Alice IAM Policy에서 허용
또는
my-bucket Bucket Policy에서 Alice를 허용
```

단, 어디선가 Explicit Deny가 있으면 Allow보다 Deny가 우선한다.

## 2. Bucket Policy가 중요한 이유

Bucket Policy는 Bucket 전체 수준에서 규칙을 표현하기 좋고 특히 다음 상황에서 자주 사용한다.

```text
Public access 제어
Cross-account access
특정 조건에서만 업로드 허용
특정 Principal만 접근 허용
```

`Principal`은 "누구에게 적용할 것인가"를 뜻한다.

예:

```text
Account A의 S3 Bucket
↑
Account B의 Role 허용
```

이처럼 다른 AWS 계정에 접근을 허용하는 문제에서 Bucket Policy가 자주 등장한다.

## 3. Bucket과 Object ARN 차이

Bucket 자체와 Bucket 안의 Object는 Resource ARN이 다르다.

```text
Bucket
arn:aws:s3:::my-bucket

Objects
arn:aws:s3:::my-bucket/*
```

예를 들어 `ListBucket`은 Bucket 리소스에, `GetObject`는 Object 리소스에 권한을 주는 식으로 생각한다.

## 4. ACL

ACL(Access Control List)은 오래된 접근 제어 방식이다.

```text
Bucket ACL
Object ACL
```

강의에서는 존재와 구분은 알아두되, 현대적인 설계에서는 IAM Policy와 Bucket Policy를 우선하고 ACL은 비활성화할 수도 있다는 흐름으로 이해하면 된다.

## SAA 판단

```text
IAM User/Role 자체에 S3 API 권한 부여
→ IAM Policy

Bucket 전체 규칙 / Cross-account
→ Bucket Policy

명시적 Deny 존재
→ Allow가 있어도 Deny 우선

Object 개별 ACL 기반 권한
→ ACL
```
