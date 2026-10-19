# u4. OAC, Signed URL / Cookie & Geo Restriction

## 1. OAC — Origin Access Control

S3를 CloudFront Origin으로 사용할 때 Bucket을 Public으로 열어둘 필요는 없다.

OAC(Origin Access Control)는 **CloudFront가 S3에 접근하도록 허용하고 사용자는 S3에 직접 접근하지 못하게** 만드는 구조에 사용한다.

```text
User
 ↓
CloudFront
 ↓ OAC로 허용
Private S3 Bucket
```

즉 사용자는 CloudFront URL로만 파일을 받고 S3 원본 URL을 직접 열면 거부되도록 만들 수 있다.

OAI(Origin Access Identity)는 이전 방식이고, 강의에서는 OAC를 최신 권장 방식으로 본다.

## 2. Signed URL

CloudFront Signed URL은 특정 파일 URL에 제한된 시간 동안 접근 권한을 부여하는 방식이다.

예:

```text
유료 강의 video.mp4
→ 로그인/결제 확인
→ 10분짜리 Signed URL 발급
→ 사용자 다운로드/재생
```

한두 개 개별 파일 접근에 잘 맞는다.

## 3. Signed Cookie

Signed Cookie는 URL 자체를 바꾸지 않고 Cookie로 접근 권한을 증명한다.

여러 파일에 대한 접근을 한꺼번에 허용하고 싶을 때 유용하다.

예:

```text
/private-course/*
```

아래 여러 영상/이미지에 접근해야 하는 사용자라면 Signed Cookie가 더 자연스러울 수 있다.

```text
Signed URL
→ 개별 파일 URL 중심

Signed Cookie
→ 여러 제한 콘텐츠에 접근하는 세션 중심
```

## 4. Geo Restriction

CloudFront는 국가 단위로 콘텐츠 접근을 허용하거나 차단할 수 있다.

예:

```text
한국/일본만 서비스 허용
또는
특정 국가 차단
```

저작권/라이선스나 지역별 서비스 정책 문제에서 연결된다.

## SAA 판단

```text
S3를 Private으로 두고 CloudFront만 접근
→ OAC

특정 파일을 제한 시간 동안 허용
→ Signed URL

여러 Private 파일에 사용자 세션 단위 접근
→ Signed Cookie

국가별 콘텐츠 허용/차단
→ Geo Restriction
```
