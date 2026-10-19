# u1. Container / Image / Dockerfile

## 1. Container

Container는 애플리케이션 프로세스와 필요한 라이브러리/환경을 묶어 실행하는 단위다.

```text
Application
+ Runtime
+ Libraries
+ Configuration
   ↓
Container
```

## 2. Image

Image는 Container를 만들기 위한 읽기 전용 템플릿이다.

```text
Image
→ run
→ Container
```

같은 Image로 여러 Container를 실행할 수 있다.

## 3. Dockerfile

Dockerfile은 Image를 어떻게 만들지 정의하는 파일이다.

개념적으로:

```dockerfile
FROM base-image
COPY application
RUN install-dependencies
CMD start-application
```

실제 syntax 자체보다 다음 흐름을 이해한다.

```text
Dockerfile
→ docker build
→ Image
→ docker run
→ Container
```

## 4. 왜 Container인가?

강의에서 강조하는 장점:

```text
어디서 실행해도 동일한 환경
compatibility 문제 감소
배포 예측 가능성 향상
microservices에 적합
on-premises → AWS lift-and-shift에도 활용
```

## 기억할 문장

> Image는 실행 템플릿이고, Container는 그 Image로 실제 실행된 프로세스 환경이다.
