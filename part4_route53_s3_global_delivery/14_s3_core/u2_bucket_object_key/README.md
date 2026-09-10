# u2. Bucket, Object, Key와 기본 동작

## 1. Bucket

Bucket은 S3 Object를 담는 최상위 컨테이너다.

```text
my-shop-assets
├── products/1.jpg
├── products/2.jpg
└── logs/app.log
```

Bucket은 특정 AWS Region에 생성한다. 애플리케이션과 가까운 Region을 선택하면 latency와 데이터 전송 비용 측면에서 유리할 수 있다.

Bucket 이름은 AWS 전체에서 고유해야 한다.

---

## 2. Object

Object는 S3에 실제로 저장되는 데이터 단위다.

예:

```text
image.jpg
backup.zip
orders.csv
video.mp4
```

Object에는 실제 데이터뿐 아니라 Key, Metadata 같은 정보가 함께 존재한다.

---

## 3. Key

Key는 Bucket 내부에서 Object를 식별하는 이름이다.

예:

```text
products/2026/09/item-100.jpg
```

이 전체 문자열이 Key다.

S3 Console에서는 `/`를 기준으로 폴더처럼 보여주지만, 전통적인 파일 시스템의 실제 디렉터리 구조와 동일하다고 생각하면 안 된다.

```text
products/
  2026/
    09/
      item-100.jpg
```

처럼 보여도 실제 핵심 식별자는 전체 Key 문자열이다.

---

## 4. Prefix

Key의 앞부분을 Prefix라고 생각할 수 있다.

예:

```text
products/2026/09/item-100.jpg
```

여기서:

```text
products/
products/2026/
products/2026/09/
```

같은 앞부분을 Prefix로 사용할 수 있다.

이 개념은 나중에 Lifecycle Rule, Event Notification, Access Pattern 등을 이해할 때 다시 나온다.

---

## 5. 기본 작업 — PUT / GET / DELETE

S3에서 Object를 다룰 때 자주 보는 작업은 다음과 같다.

```text
PUT
→ Object 업로드

GET
→ Object 다운로드/조회

DELETE
→ Object 삭제

LIST
→ Bucket의 Object 목록 조회
```

### 예시

```text
Application
  ↓ PUT products/1.jpg
S3

Application
  ↓ GET products/1.jpg
S3
```

---

## 6. Object 크기

S3 Object는 매우 큰 파일도 저장할 수 있다. 큰 Object를 업로드할 때는 이후 단원에서 Multipart Upload 같은 방식을 다룬다.

이번 단원에서는 "S3는 파일 서버가 아니라 Object API 기반 저장소"라는 점을 우선 기억한다.

---

## 쇼핑몰 예시

```text
Bucket: cloud-shop-assets

products/1001/main.jpg
products/1001/thumb.jpg
products/1002/main.jpg
exports/orders-2026-09.csv
```

애플리케이션 DB에는 이미지 자체를 넣기보다 다음처럼 S3 Object 위치를 저장할 수 있다.

```text
Product
├── id: 1001
└── imageKey: products/1001/main.jpg
```

## SAA 포인트

```text
S3의 최상위 저장 공간
→ Bucket

실제 데이터 단위
→ Object

Bucket 안에서 Object를 식별하는 이름
→ Key

폴더처럼 보이는 구조
→ 실제로는 Key Prefix 기반
```
