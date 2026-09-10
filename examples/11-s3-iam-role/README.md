# Example 11 — IAM Role로 EC2에서 S3 접근하기

이번 단계에서는 Access Key를 서버에 저장하지 않고 IAM Role을 이용해 EC2가 S3에 접근하도록 만든다.

## Recall Check
- IAM User와 Role의 차이는?
- EC2가 다른 AWS 서비스에 접근할 때 왜 Role을 쓰는가?
- SG는 네트워크 권한이고 IAM은 무엇을 제어하는가?

## 새로 배우는 것
- EC2 IAM Role / Instance Profile
- S3 bucket
- `GetObject`, `PutObject`, `ListBucket`
- 최소 권한

## 반복하는 것
EC2 생성, IAM 정책 확인, 애플리케이션/CLI 테스트, AccessDenied 진단을 반복한다.

## 이번에는 도움 없이
EC2는 이전 예제 방식대로 생성한다. 가능하면 Private EC2 + SSM 구조를 재사용한다.

## 목표 구조
```text
EC2
 ↓ IAM Role
S3 Bucket
```

## 구축
1. 실습용 S3 Bucket을 만든다.
2. 테스트 파일 하나를 업로드한다.
3. EC2용 IAM Role을 만들고 S3에 필요한 최소 권한을 붙인다.
4. Role을 EC2에 연결한다.
5. EC2에서 AWS CLI로 `aws s3 ls`, 파일 다운로드/업로드를 시도한다.
6. `aws configure`로 Access Key를 입력하지 않았는지 확인한다.

## 최소 권한 생각하기
예를 들어 한 bucket만 접근해야 한다면 모든 S3 Resource `*`를 허용하지 않고 bucket ARN/object ARN 범위를 제한한다.

## 장애 실험 A — GetObject 제거
Role에서 `s3:GetObject`를 제거한 뒤 파일 다운로드를 시도한다.

```text
EC2 정상
네트워크 정상
S3 정상
→ AccessDenied
```

## 장애 실험 B — Resource 범위 오류
정책의 bucket ARN 또는 object ARN을 일부러 잘못 지정하고 동일 명령을 실행한다.

## 관찰
- AccessDenied가 나면 SG부터 볼 필요가 있는가?
- `ListBucket`과 `GetObject`는 같은 Resource ARN을 사용하는가?
- Role을 바꾼 뒤 자격 증명 파일을 서버에 배포해야 하는가?

## 기억만으로 설명하기
- Access Key보다 EC2 Role이 나은 이유는?
- IAM의 `Action`과 `Resource`는 각각 무엇인가?
- S3 AccessDenied 발생 시 어떤 순서로 확인할 것인가?

## 완료 체크
- [ ] S3 Bucket을 생성했다.
- [ ] EC2에 IAM Role을 연결했다.
- [ ] Access Key 없이 S3에 접근했다.
- [ ] 최소 권한으로 범위를 제한했다.
- [ ] AccessDenied를 재현하고 복구했다.
- [ ] 네트워크 오류와 IAM 권한 오류를 구분할 수 있다.

## 비용 정리
테스트 object와 bucket을 삭제하고 필요 없는 IAM policy/role을 정리한다.
