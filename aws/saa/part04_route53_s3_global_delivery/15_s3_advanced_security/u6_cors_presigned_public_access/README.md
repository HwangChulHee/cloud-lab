# u6. CORS, Presigned URL & Public Access

## 1. CORS란

CORS(Cross-Origin Resource Sharing)는 브라우저에서 **다른 Origin의 리소스에 접근할 수 있는지**를 제어하는 규칙이다.

Origin은 보통 다음 조합으로 생각하면 된다.

```text
scheme + host + port
```

예:

```text
https://shop.example.com
https://api.example.com
```

도메인이 다르므로 서로 다른 Origin이다.

프론트엔드가 S3에 직접 업로드한다고 해보자.

```text
Browser
https://shop.example.com
       ↓ upload
https://my-bucket.s3.amazonaws.com
```

브라우저 보안 정책 때문에 S3가 이 Origin을 허용하도록 CORS 설정이 필요할 수 있다.

CORS는 S3의 IAM 권한을 대신하지 않는다. 즉 CORS가 허용되어도 IAM/Bucket Policy에서 거부되면 접근할 수 없다.

## 2. Presigned URL

Presigned URL은 S3 객체에 대한 권한을 **URL에 제한된 시간 동안 위임**하는 방식이다.

예를 들어 사용자가 본인 주문 영수증 PDF를 10분 동안만 다운로드하게 하고 싶다고 하자.

```text
Backend
 ↓ 권한 확인
Presigned URL 생성 (10분)
 ↓
User
 ↓
S3에서 직접 다운로드
```

Bucket을 Public으로 만들 필요가 없다.

업로드 Presigned URL도 같은 방식으로 사용할 수 있다.

```text
Client → Backend에 업로드 요청
Backend → Presigned Upload URL 반환
Client → S3에 직접 업로드
```

이때 URL은 URL을 만든 IAM Principal의 권한을 기반으로 한다.

## 3. Block Public Access

S3에는 실수로 Bucket/Object를 외부에 공개하는 일을 막기 위한 Block Public Access 설정이 있다.

시험에서는 "공개가 필요 없는 데이터"라면 Public access를 막고, 필요한 사용자에게 IAM/Bucket Policy 또는 Presigned URL을 이용하는 방향을 우선 생각하면 된다.

## SAA 판단

```text
브라우저에서 다른 Origin의 S3 호출
→ CORS

Private Object를 특정 사용자에게 잠시 다운로드 허용
→ Presigned URL

클라이언트가 서버를 거치지 않고 S3에 직접 업로드
→ Presigned Upload URL

실수로 Public Bucket이 되는 것을 방지
→ Block Public Access
```
