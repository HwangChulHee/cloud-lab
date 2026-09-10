# Example 12 — S3 보안과 삭제 복구

S3를 단순 파일 저장소가 아니라 권한, 공개 차단, 버전 관리, 복구 관점에서 다룬다.

## Recall Check
- EC2가 Access Key 없이 S3에 접근한 방식은?
- `AccessDenied`가 네트워크 장애와 다른 점은?
- IAM Policy에서 Action/Resource는 무엇이었나?
- `ListBucket`과 `GetObject`가 사용하는 Resource ARN은 어떻게 달랐나?

## 새로 배우는 것
- Block Public Access
- Bucket Policy
- Versioning
- Lifecycle
- S3 기본 암호화 상태 확인
- SSE-S3와 SSE-KMS 차이

## 반복하는 것
S3 Bucket, IAM Role, `GetObject`/`PutObject`, AccessDenied 진단을 다시 수행한다.

모든 태그 가능 리소스에는 `Project=cloud-lab`, `Stage=examples`, `Example=12`를 붙인다.

## 이번에는 도움 없이
새 bucket과 EC2 Role을 최소 권한으로 구성한다.

## 실험 A — Public Access 차단
1. Block Public Access 설정을 확인한다.
2. object URL을 인터넷 브라우저에서 직접 요청한다.
3. IAM Role을 가진 EC2에서는 object를 읽는다.

`인터넷 공개 여부`와 `인증된 IAM 접근`이 별개임을 확인한다.

## 실험 B — Bucket Policy
특정 Principal 또는 조건만 허용하는 간단한 Bucket Policy를 적용한다. IAM Policy와 Bucket Policy가 함께 권한 판단에 참여한다는 점을 관찰한다.

정책을 잘못 설정해 AccessDenied를 재현하고 다음 순서로 본다.

```text
Principal → Action → Resource → Explicit Deny/Allow
```

## 실험 C — Versioning과 삭제 복구
1. Versioning을 활성화한다.
2. 같은 key의 파일을 여러 번 덮어쓴다.
3. Version ID가 생기는지 확인한다.
4. object를 삭제하고 Delete Marker를 확인한다.
5. 이전 version을 이용해 복구한다.

CLI로도 확인한다.

```bash
aws s3api list-object-versions --bucket <bucket-name>
```

## 실험 D — Lifecycle
오래된 version이나 object를 다른 storage class로 전환/삭제하는 Lifecycle Rule 화면을 구성해본다. 실제 장기 대기는 하지 않고 규칙 의미를 설명한다.

## 실험 E — 기본 암호화 확인

현재 S3는 새로 업로드되는 객체에 서버 측 암호화를 기본 적용한다. 따라서 이 예제에서는 단순히 "암호화를 켠다"가 아니라 **현재 bucket/object에 어떤 암호화가 적용되는지 확인**한다.

```bash
aws s3api get-bucket-encryption --bucket <bucket-name>
aws s3api head-object --bucket <bucket-name> --key <object-key>
```

기본 SSE-S3와 SSE-KMS의 차이를 다음 관점에서 설명한다.

```text
키 관리 주체
KMS 권한 필요 여부
감사/키 제어 수준
비용/복잡도
```

SSE-KMS는 개념 비교가 목적이며 반드시 별도 KMS key를 만들어야 하는 것은 아니다.

## 관찰
- Versioning은 backup과 완전히 같은가?
- Delete Marker가 생겼을 때 데이터가 즉시 물리 삭제되는가?
- Bucket Policy와 IAM Policy가 충돌하면 무엇을 먼저 의심해야 하는가?
- 기본 암호화가 적용된다고 해서 bucket이 public/private인지가 결정되는가?

## CLI 구축 검증
[CLI Verification Guide](../CLI_VERIFICATION.md)의 Example 12 명령을 실행한다.

## 기억만으로 설명하기
- S3를 public website처럼 열어두는 것과 private application storage로 쓰는 차이는?
- 실수로 object를 삭제했을 때 Versioning이 어떻게 도움 되는가?
- Lifecycle은 성능 기능인가 비용/보존 정책 기능인가?
- SSE-S3와 SSE-KMS는 무엇이 다른가?

## 완료 체크
- [ ] Block Public Access를 확인했다.
- [ ] IAM 접근과 Public 접근을 비교했다.
- [ ] Bucket Policy로 AccessDenied를 재현했다.
- [ ] Versioning과 Delete Marker를 확인했다.
- [ ] 이전 version을 복구했다.
- [ ] Lifecycle의 목적을 설명할 수 있다.
- [ ] 현재 기본 암호화 상태를 CLI로 확인했다.

## 비용 정리

Versioning bucket은 현재 object 목록이 비어 보여도 old version과 delete marker가 남을 수 있다. bucket 삭제 전 반드시 확인한다.

```bash
aws s3api list-object-versions --bucket <bucket-name>
```

모든 version과 delete marker까지 삭제한 뒤 bucket을 삭제한다. 삭제 후 CLI 삭제 검증을 실행한다.
