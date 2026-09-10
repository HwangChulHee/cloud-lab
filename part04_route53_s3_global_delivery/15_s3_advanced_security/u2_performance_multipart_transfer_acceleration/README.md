# u2. S3 Performance, Multipart Upload & Transfer Acceleration

## 1. Multipart Upload

큰 파일 하나를 통째로 업로드하면 중간에 실패했을 때 처음부터 다시 보내야 할 수 있다.

Multipart Upload는 큰 객체를 여러 조각으로 나누어 병렬 업로드한 뒤 S3에서 다시 합치는 방식이다.

```text
10 GB 파일
├── Part 1
├── Part 2
├── Part 3
└── ...
       ↓ 병렬 업로드
      S3
       ↓
   하나의 Object
```

강의에서는 **5GB를 초과하는 객체는 Multipart Upload가 필수**라는 점을 강조한다. 큰 파일에서는 그보다 작은 크기부터도 성능과 재시도 측면에서 사용할 수 있다.

예를 들어 8GB 영상 업로드 중 7GB 지점에서 실패했다고 해보자. 단일 업로드라면 전체를 다시 보낼 수 있지만 Multipart라면 실패한 Part만 재전송할 수 있다.

## 2. Byte-Range Fetch

객체 전체가 아니라 필요한 바이트 범위만 나누어 다운로드할 수 있다.

```text
큰 파일
├── bytes 0~999
├── bytes 1000~1999
└── ...
```

병렬 요청으로 다운로드 성능을 높이거나, 파일의 일부만 필요한 경우에 유용하다.

## 3. Transfer Acceleration

세계 여러 지역의 사용자가 한 Region의 S3 Bucket으로 대용량 파일을 업로드한다고 해보자.

```text
한국 사용자 ───────────────→ 미국 Region S3
브라질 사용자 ─────────────→ 미국 Region S3
```

긴 인터넷 경로를 그대로 타면 지연과 품질 편차가 커질 수 있다.

S3 Transfer Acceleration은 사용자가 가까운 AWS Edge Location으로 먼저 데이터를 보내고, 이후 AWS 글로벌 네트워크를 활용해 대상 Bucket까지 전달한다.

```text
User
 ↓ 가까운 Edge Location
AWS Global Network
 ↓
S3 Bucket
```

즉 CloudFront처럼 다운로드 캐시를 제공하는 기능이 아니라 **S3로 데이터를 빠르게 전송하기 위한 기능**으로 구분한다.

## SAA 판단

```text
5GB 초과 Object 업로드
→ Multipart Upload 필수

큰 파일 업로드 실패 시 일부만 재시도 / 병렬 전송
→ Multipart Upload

큰 객체 일부만 읽기 / 병렬 다운로드
→ Byte-Range Fetch

전 세계 사용자가 멀리 있는 S3 Bucket에 빠르게 업로드
→ S3 Transfer Acceleration
```
