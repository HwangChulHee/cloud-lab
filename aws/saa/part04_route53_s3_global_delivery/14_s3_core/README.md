# 14. Amazon S3 Core

Amazon S3(Simple Storage Service)는 AWS의 대표적인 **Object Storage** 서비스다.

이번 단원에서는 Bucket/Object 구조, Versioning, Replication, Storage Class, Lifecycle을 중심으로 본다. 보안, CORS, Presigned URL, Event Notification 같은 고급 내용은 다음 단원에서 다룬다.

## Units

- [x] u1. S3와 Object Storage 기본
- [x] u2. Bucket, Object, Key와 기본 동작
- [x] u3. Durability, Availability와 S3 Standard
- [x] u4. Versioning
- [x] u5. Replication — CRR / SRR
- [x] u6. Storage Classes
- [x] u7. Lifecycle Rules

## SAA 선택 지도

```text
파일/이미지/백업/로그 같은 객체 저장
→ S3

삭제/덮어쓰기 실수에서 이전 버전 복구
→ Versioning

다른 Region으로 복제
→ CRR

같은 Region의 다른 Bucket으로 복제
→ SRR

자주 접근
→ S3 Standard

덜 자주 접근하지만 즉시 필요
→ Standard-IA

재생성 가능한 단일 AZ 데이터
→ One Zone-IA

접근 패턴을 예측하기 어려움
→ Intelligent-Tiering

장기 보관
→ Glacier 계열

시간이 지나면 자동으로 저렴한 Class로 이동/삭제
→ Lifecycle Rule
```
