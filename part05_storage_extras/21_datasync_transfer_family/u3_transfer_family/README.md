# u3. AWS Transfer Family

AWS Transfer Family는 **FTP 계열 protocol을 사용해 Amazon S3 또는 EFS로 파일을 전송할 수 있게 하는 fully managed service**다.

## 지원 Protocol

강의에서 다음을 다룬다.

```text
FTP
FTPS
SFTP
```

## 구조

```text
External User / FTP Client
          ↓
   AWS Transfer Family
          ↓
      S3 or EFS
```

## 특징

```text
managed infrastructure
scalable
reliable
highly available
multi-AZ
```

강의에서는 provisioned endpoint 시간 + data transfer GB 기준의 비용 구조를 언급한다.

## Authentication Integration

```text
Microsoft Active Directory
LDAP
Okta
Amazon Cognito
Custom Authentication
```

## Use Cases

```text
file sharing
public datasets
CRM
ERP
```

## SAA 판단

```text
외부 partner/client가 SFTP로 S3에 파일 업로드
→ Transfer Family

기존 FTP workflow를 managed endpoint로 AWS에 연결
→ Transfer Family
```
