# u3. Build / Run / Repository 흐름

강의의 Docker 기본 흐름은 다음과 같다.

```text
Dockerfile
   │
   │ build
   ▼
 Docker Image
   │
   ├─ run → Container
   │
   └─ push
        ↓
 Docker Repository
        ↓ pull
 ECS / EKS / Other Host
```

## 1. Build

Dockerfile에서 Image를 만든다.

```bash
docker build -t my-app .
```

개념적으로는:

```text
source + Dockerfile
→ immutable image artifact
```

## 2. Run

Image를 실제 Container로 실행한다.

```bash
docker run my-app
```

## 3. Repository

Image는 Registry/Repository에 저장해 다른 환경에서 pull할 수 있다.

대표:

```text
Docker Hub
→ public images 중심

Amazon ECR
→ AWS에서 private/public container image 저장
```

## 4. CI/CD와 연결

나중에 포트폴리오에서는 다음 흐름으로 이어진다.

```text
Git Push
→ CI Build
→ Docker Image
→ ECR Push
→ ECS Deployment
```

SAA 단계에서는 이 파이프라인을 구현하기보다 구조를 먼저 이해한다.
