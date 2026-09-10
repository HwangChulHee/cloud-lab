# 15. S3 Advanced & Security

이 단원은 강의의 **Amazon S3 – Advanced**와 **Amazon S3 – Security**를 묶어 정리한다.

시험 전에는 Lifecycle, 성능, 이벤트, 암호화, Bucket Policy, CORS, Object Lock, Access Point처럼 문제에서 직접 선택 기준이 되는 개념을 중심으로 본다.

## Units

- [ ] u1. Lifecycle Rules & Storage Class Transition
- [ ] u2. S3 Performance, Multipart Upload & Transfer Acceleration
- [ ] u3. Event Notifications
- [ ] u4. IAM Policy, Bucket Policy & ACL
- [ ] u5. S3 Encryption — SSE-S3 / SSE-KMS / SSE-C / Client-Side
- [ ] u6. CORS, Presigned URL & Public Access
- [ ] u7. MFA Delete, Object Lock & Glacier Vault Lock
- [ ] u8. S3 Access Points & Object Lambda

## SAA 선택 지도

```text
오래된 객체를 자동으로 저렴한 Storage Class로 이동
→ Lifecycle Rule / Transition

대용량 업로드
→ Multipart Upload

전 세계 사용자 업로드 속도 개선
→ S3 Transfer Acceleration

객체 생성/삭제를 계기로 후속 처리
→ S3 Event Notification

사용자 자체 권한
→ IAM Policy

Bucket 전체 / Cross-account 접근
→ Bucket Policy

AWS가 키까지 관리
→ SSE-S3

KMS의 감사/키 제어 필요
→ SSE-KMS

고객이 직접 키 제공
→ SSE-C

브라우저가 다른 Origin의 S3 리소스 호출
→ CORS

임시 다운로드/업로드 권한
→ Presigned URL

삭제 불가능한 WORM 보존
→ Object Lock / Glacier Vault Lock

복잡한 Bucket Policy를 팀/앱별 접근점으로 단순화
→ S3 Access Point
```

다음 단원은 CloudFront와 Global Accelerator로 이어진다.
