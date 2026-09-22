# u3. Amazon Macie

Amazon Macie는 **Machine Learning과 pattern matching으로 AWS의 sensitive data를 발견하고 보호하는 fully managed data security/privacy service**다.

강의에서 핵심 대상은 **Amazon S3**다.

## 구조

```text
S3 Buckets
    ↓
Amazon Macie
    ↓
Sensitive Data Discovery
    ↓
PII Finding
    ↓
EventBridge / Integration
```

## 대표 탐지 대상

강의에서는 다음을 대표적으로 강조한다.

```text
Personally Identifiable Information (PII)
민감 데이터
```

## 다른 서비스와 구분

```text
S3 bucket이 public인가?
→ AWS Config / S3 security 설정

S3 안에 PII가 들어 있는가?
→ Macie

S3 API 사용이 수상한가?
→ GuardDuty
```

## 기억할 문장

> Macie는 S3 object 안의 민감정보/PII를 찾아내는 data privacy 서비스다.
