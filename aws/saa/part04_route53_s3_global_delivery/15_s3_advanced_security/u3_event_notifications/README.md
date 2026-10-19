# u3. S3 Event Notifications

S3 Event Notification은 Bucket에서 특정 이벤트가 발생했을 때 다른 AWS 서비스로 알림을 보내 후속 작업을 시작하는 기능이다.

대표 이벤트:

```text
ObjectCreated
ObjectRemoved
ObjectRestore
Replication event 등
```

예를 들어 사용자가 상품 이미지를 업로드하면:

```text
User
 ↓ upload
S3
 ↓ ObjectCreated
Lambda
 ↓
썸네일 생성
```

또는 이벤트를 SQS/SNS/EventBridge로 전달해 비동기 처리할 수 있다.

```text
S3 → SQS → Worker
S3 → SNS → 여러 Subscriber
S3 → EventBridge → 다양한 Rule/Target
```

## Prefix / Suffix Filter

모든 파일이 아니라 특정 Key 패턴에만 반응하도록 필터링할 수 있다.

```text
prefix: images/
suffix: .jpg
```

이면 `images/product.jpg`에는 반응하지만 `logs/app.txt`에는 반응하지 않는 식이다.

## 주의할 점

S3 이벤트를 받은 Lambda가 다시 같은 Bucket에 파일을 생성하고, 그 생성 이벤트가 다시 Lambda를 부르면 반복 호출이 생길 수 있다.

예:

```text
upload/original.jpg
→ Lambda
→ processed/thumb.jpg
```

처럼 입력/출력 prefix를 분리하면 이런 구조를 피하기 쉽다.

## SAA 판단

```text
S3 객체 업로드 직후 Lambda 실행
→ S3 Event Notification

이벤트를 Queue에 넣어 Worker가 처리
→ S3 → SQS

복잡한 이벤트 라우팅
→ EventBridge 연계
```
