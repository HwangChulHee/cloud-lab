# u1. S3와 Object Storage 기본

## 1. S3는 무엇인가

Amazon S3(Simple Storage Service)는 파일을 **Object** 형태로 저장하는 관리형 스토리지 서비스다.

예:

```text
상품 이미지
동영상
백업 파일
로그
정적 웹 파일
데이터 분석용 원본 파일
```

이런 데이터를 저장하는 데 적합하다.

---

## 2. Object Storage란

일반 파일 시스템에서는 보통 다음과 같은 디렉터리 구조를 생각한다.

```text
/home/user/images/a.jpg
```

S3는 내부적으로 전통적인 디렉터리/파일 시스템처럼 다루기보다, Bucket 안에 **Key를 가진 Object**를 저장한다고 이해하는 것이 좋다.

```text
Bucket
└── Object
    ├── Key
    ├── Data
    └── Metadata
```

Object는 쉽게 말하면:

```text
실제 데이터
+ 이름(Key)
+ 부가 정보(Metadata)
```

의 묶음이다.

---

## 3. S3와 EBS/EFS 차이

S3는 Object Storage이고, EBS는 Block Storage, EFS는 File Storage다.

```text
S3
→ 객체 단위 저장
→ 이미지, 파일, 백업, 로그

EBS
→ EC2 디스크처럼 block 단위 저장
→ OS disk, DB disk

EFS
→ 여러 서버가 mount해서 공유하는 file system
```

### 예시

쇼핑몰 상품 이미지는 S3에 두기 좋다.

```text
product-1.jpg
product-2.jpg
```

반면 PostgreSQL의 데이터 파일을 S3 bucket에 직접 mount해서 일반 디스크처럼 사용하는 개념은 아니다.

---

## 4. Serverless Storage라는 의미

S3를 쓰기 위해 EC2처럼 저장 서버를 직접 만들고 운영할 필요가 없다.

```text
디스크 서버 생성
RAID 구성
스토리지 서버 확장
서버 장애 교체
```

같은 인프라 운영을 사용자가 직접 하지 않는다.

애플리케이션은 API를 통해 S3에 Object를 PUT/GET하는 방식으로 사용한다.

---

## 5. 큰 그림

```text
Application
   ↓ PUT
Amazon S3 Bucket
   ↓ GET
User / Application
```

예를 들어 사용자가 상품 이미지를 업로드하면:

```text
POST /products/image
       ↓
Application
       ↓
S3에 image.jpg 저장
```

이후 이미지 조회 시 S3에 저장된 Object를 사용한다.

## SAA 포인트

```text
대규모 파일/객체 저장
→ S3

EC2의 OS disk
→ EBS

여러 EC2가 동시에 mount하는 공유 파일 시스템
→ EFS

Object Storage
→ Bucket + Object + Key 구조
```
