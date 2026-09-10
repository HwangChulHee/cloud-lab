# 54. KMS

AWS KMS(Key Management Service)는 AWS 리소스와 애플리케이션 데이터의 **암호화 키를 생성하고 사용 권한을 통제하는 서비스**다.

S3, EBS, RDS 같은 서비스에서 "암호화됨"만 보는 것이 아니라, **어떤 키를 누가 사용할 수 있는가**까지 이해하는 것이 핵심이다.

## 핵심 질문

- SSE-S3와 SSE-KMS는 무엇이 다른가?
- KMS Key를 사용할 권한은 IAM Policy만 있으면 항상 충분한가?
- 왜 애플리케이션이 암호화 키 원문을 직접 관리하지 않는가?
- Encrypt/Decrypt 권한과 키 관리 권한은 왜 분리하는가?
- 다른 계정에서 KMS Key를 사용하려면 무엇을 고려해야 하는가?

## 반드시 이해할 개념

### KMS Key

KMS가 관리하는 논리적인 암호화 키다.

```text
Application / AWS Service
        ↓
      KMS Key
        ↓
 Encrypt / Decrypt 권한 통제
```

실제 운영에서는 애플리케이션이 장기 암호화 키를 코드나 환경변수에 직접 넣어두는 방식보다 KMS와 IAM을 이용해 접근을 통제한다.

### AWS owned key / AWS managed key / Customer managed key

큰 그림은 다음처럼 구분한다.

```text
AWS owned key
→ AWS가 소유/관리
→ 사용자가 직접 제어하지 않음

AWS managed key
→ 특정 AWS 서비스용으로 AWS가 생성/관리
→ aws/<service> 형태

Customer managed key
→ 사용자가 생성
→ Key Policy, rotation, alias 등 제어 가능
```

SAA에서는 "어느 정도의 제어가 필요한가"를 기준으로 구분한다.

### Key Policy와 IAM Policy

KMS는 일반 리소스보다 권한 모델을 조금 더 주의해서 봐야 한다.

```text
IAM Policy
+ KMS Key Policy
→ 실제 사용 가능 여부 결정
```

특히 Customer managed key에서는 Key Policy가 중요하다.

"IAM에서 kms:Decrypt를 줬으니 무조건 된다"고 단순하게 생각하지 않는다.

### Envelope Encryption

대용량 데이터를 KMS가 직접 전부 암복호화하는 구조로 이해하면 안 된다.

개념적으로는:

```text
KMS Key
   ↓
Data Key 보호
   ↓
Data Key가 실제 데이터 암호화
```

즉 KMS는 데이터 암호화에 사용할 키를 안전하게 보호하는 중심 역할을 한다.

## AWS 서비스와 연결

### S3

```text
SSE-S3
→ S3가 관리하는 키 사용

SSE-KMS
→ KMS Key 사용
→ KMS 권한/감사/제어 추가
```

`examples/12`에서 기본 SSE-S3를 확인한 뒤 SSE-KMS가 왜 더 강한 제어를 제공하는지 연결해서 이해한다.

### EBS / RDS

EBS Volume, Snapshot, RDS도 KMS 기반 암호화를 사용할 수 있다.

중요한 점은 "암호화 체크박스"보다:

```text
어떤 KMS Key인가?
누가 Decrypt 가능한가?
Snapshot/복제/공유 때 키 권한은 어떻게 되는가?
```

를 생각하는 것이다.

## 권한 장애 시나리오

예를 들어 애플리케이션이 SSE-KMS로 암호화된 S3 Object를 읽어야 하는데 `s3:GetObject`만 있고 `kms:Decrypt`가 없다면 객체 권한은 있어도 복호화 단계에서 실패할 수 있다.

```text
EC2 Role
 ├─ s3:GetObject        OK
 └─ kms:Decrypt         없음

→ AccessDenied 계열 오류 가능
```

이 사례는 "서비스 권한"과 "암호화 키 권한"이 별개라는 점을 체감하기 좋다.

## 최소 Hands-on

비용을 크게 늘리지 않는 범위에서 다음을 확인한다.

1. KMS Console에서 AWS managed key와 Customer managed key 차이를 본다.
2. Customer managed key 하나를 만들 경우 Alias와 Key Policy를 확인한다.
3. 가능하면 작은 S3 Object를 SSE-KMS로 업로드한다.
4. 어떤 KMS Key ARN이 사용됐는지 확인한다.
5. 실습 후 Customer managed key는 즉시 삭제되지 않고 삭제 예약 기간이 존재한다는 점을 확인한다.

Customer managed key는 비용이 발생할 수 있으므로 단순 확인만으로도 충분하다.

## 기억만으로 설명하기

```text
Q1. SSE-S3와 SSE-KMS 차이는?
Q2. Customer managed key를 쓰는 이유는?
Q3. Key Policy와 IAM Policy는 어떤 관계인가?
Q4. s3:GetObject가 있어도 SSE-KMS Object 읽기에 실패할 수 있는 이유는?
Q5. Envelope Encryption을 왜 사용하는가?
Q6. EBS/RDS/S3 암호화가 KMS와 어떻게 연결되는가?
```

## examples 연결

```text
examples/11 S3 + IAM Role
→ 서비스 권한과 IAM Role

examples/12 S3 Security & Recovery
→ SSE-S3 확인
→ SSE-KMS와 권한 모델 비교

examples/15 Troubleshooting
→ S3 권한 문제와 KMS 권한 문제 구분

examples/16 Final Architecture
→ 암호화와 최소 권한 설계 근거 설명
```

## 완료 기준

- [ ] KMS Key의 역할을 설명할 수 있다.
- [ ] AWS owned / AWS managed / Customer managed key를 구분할 수 있다.
- [ ] SSE-S3와 SSE-KMS의 차이를 설명할 수 있다.
- [ ] Key Policy와 IAM Policy가 함께 권한 판단에 관여한다는 것을 이해한다.
- [ ] Envelope Encryption의 큰 흐름을 설명할 수 있다.
- [ ] S3/EBS/RDS 암호화와 KMS를 연결해서 설명할 수 있다.
- [ ] `s3:GetObject`와 `kms:Decrypt`가 별도 권한이라는 것을 이해한다.
