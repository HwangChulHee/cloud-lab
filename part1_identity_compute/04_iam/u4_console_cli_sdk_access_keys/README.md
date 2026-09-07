# u4. Console, CLI, SDK와 Access Keys

## 지도 확인

강의에서는 AWS에 접근하는 방법을 세 가지로 나눈다.

```text
1. AWS Management Console
2. AWS CLI
3. AWS SDK
```

각 방식은 인증 방법이 조금 다르다.

---

## 1. AWS Management Console

웹 브라우저로 AWS Console에 로그인해서 리소스를 관리하는 방식이다.

```text
Browser
  ↓
AWS Management Console
```

강의에서는 Console 접근을 다음과 연결한다.

```text
Password
+
MFA
```

사람이 화면을 보고 직접 작업할 때 가장 익숙한 방식이다.

---

## 2. AWS CLI

CLI(Command Line Interface)는 터미널에서 명령어로 AWS 서비스의 API를 호출하는 도구다.

예:

```bash
aws sts get-caller-identity
```

또는 이후에 다음과 같은 형태를 만나게 된다.

```bash
aws s3 ls
aws ec2 describe-instances
```

강의에서는 CLI를 AWS Public API에 직접 접근할 수 있는 도구이자 자동화 스크립트를 만들 수 있는 수단으로 소개한다.

```text
Shell
 ↓
AWS CLI
 ↓
AWS API
```

Console에서 반복해서 클릭하는 작업을 CLI 명령이나 스크립트로 자동화할 수 있다.

---

## 3. AWS SDK

SDK(Software Development Kit)는 애플리케이션 코드에서 AWS 서비스를 호출할 수 있게 해주는 라이브러리다.

```text
Application
   ↓
AWS SDK
   ↓
AWS API
```

강의에서는 JavaScript, Python, Java, Go, .NET 등 여러 언어용 SDK가 제공된다고 설명한다.

Python에서는 이후 `boto3`를 접하게 된다.

예를 들어 애플리케이션에서 S3 파일을 조회하거나 업로드하는 동작이 SDK를 통해 이루어질 수 있다.

---

## 4. Access Keys

강의에서는 CLI와 SDK의 프로그램 방식 접근에 Access Key를 연결한다.

Access Key는 다음 두 값으로 구성된다.

```text
Access Key ID
Secret Access Key
```

강의의 비유로 보면:

```text
Access Key ID
≈ username

Secret Access Key
≈ password
```

따라서 Secret Access Key는 외부에 노출하면 안 되는 민감한 정보다.

```text
GitHub commit
README
Slack
블로그

→ Secret Access Key를 올리면 안 됨
```

---

## 5. Access Key는 공유하지 않는다

강의에서는 Access Key를 비밀번호처럼 취급하고 공유하지 말라고 강조한다.

특히 다음 방식은 피해야 한다.

```python
ACCESS_KEY = "..."
SECRET_KEY = "..."
```

코드에 직접 Credential을 하드코딩하면 저장소 유출이나 로그 노출 등으로 이어질 수 있다.

뒤에서 EC2를 공부하면 **IAM Role을 사용해 EC2에 권한을 주는 방식**을 배우게 된다.

이 구조가 중요한 이유는 다음과 같다.

```text
EC2
 ↓
IAM Role
 ↓
AWS Service
```

애플리케이션 코드 안에 장기 Access Key를 직접 넣지 않아도 되는 방향으로 이어진다.

---

## 6. 세 방식 비교

| 방식 | 주 사용 대상 | 강의에서 연결되는 인증 |
|---|---|---|
| Management Console | 사람의 웹 조작 | Password + MFA |
| CLI | 터미널, 스크립트 | Access Keys |
| SDK | 애플리케이션 코드 | Access Keys |

지금은 강의 흐름에 맞춰 이 구조로 기억한다.

---

## 7. CLI를 왜 배워야 하는가

Cloud Engineer 관점에서는 Console만 사용할 수 있는 것보다 CLI 사용에 익숙한 것이 중요하다.

```text
Console
→ 사람이 직접 조작

CLI
→ 명령 반복 가능
→ 스크립트 가능
→ 자동화 가능
```

나중에는 Terraform이나 CI/CD가 더 높은 수준에서 인프라와 배포를 자동화하지만, AWS CLI는 리소스 상태 확인과 간단한 운영 작업에서도 계속 사용된다.

---

## 최소 실습

AWS CLI를 설치하고 Credential 설정까지 완료한 상태라면 다음 명령으로 현재 호출 주체를 확인한다.

```bash
aws sts get-caller-identity
```

출력에서 다음 세 가지를 확인한다.

```text
Account
UserId
Arn
```

그리고 스스로 질문한다.

```text
지금 이 CLI 명령은 어떤 IAM Identity의 권한으로 실행되고 있는가?
```

이 질문이 IAM과 CLI를 연결하는 핵심이다.

---

## SAA 연결

```text
브라우저에서 AWS 사용
→ Management Console

터미널/스크립트로 AWS API 사용
→ CLI

프로그램 내부에서 AWS 사용
→ SDK

CLI / SDK 프로그램 방식 접근
→ Access Keys

Access Key 공유
→ 하지 않는다
```

이번 유닛은 실제 CLI 사용과 연결되므로 `aws sts get-caller-identity` 정도는 직접 실행해보는 것을 권장한다.
