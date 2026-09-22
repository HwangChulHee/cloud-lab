# u4. IAM Identity Center / Permission Sets

AWS IAM Identity Center는 과거 AWS Single Sign-On의 후속 서비스다.

## 목적

한 번 로그인해서 다음에 접근할 수 있게 한다.

```text
AWS Organizations의 여러 AWS Account
Business Cloud Applications
SAML 2.0 Applications
EC2 Windows Instances
```

## Identity Source

강의에서는 다음을 설명한다.

```text
IAM Identity Center Built-in Identity Store
Active Directory
OneLogin
Okta
기타 identity provider
```

## Permission Sets

여러 IAM Policy의 묶음을 User/Group에 할당해 특정 AWS Account 접근 권한을 정의한다.

```text
Developers Group
      ↓
Permission Set: ReadOnlyAccess
      ↓
Dev Account

DB Admins
      ↓
Permission Set: DB Admin
      ↓
Prod Account
```

## ABAC

Identity Center에 저장된 사용자 attribute를 이용해 Attribute-Based Access Control을 할 수 있다.

강의 예:

```text
cost center
title
locale
```

## 기억할 문장

> IAM Identity Center는 여러 AWS Account와 애플리케이션의 SSO를 중앙 관리하고, Permission Set으로 계정별 권한을 할당한다.
