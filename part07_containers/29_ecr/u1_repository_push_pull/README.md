# u1. ECR Repository / Push / Pull

## 1. Repository

ECR Repository는 Container Image를 저장하는 논리적 공간이다.

```text
ECR
├─ app-api
│  ├─ image:v1
│  └─ image:v2
└─ worker
   └─ image:latest
```

## 2. Push

개발자나 CI가 빌드한 Image를 ECR에 push한다.

```text
Dockerfile
→ Image
→ ECR Push
```

## 3. Pull

ECS/EKS runtime은 Task/Pod를 시작할 때 필요한 Image를 Registry에서 pull한다.

```text
ECS Task start
→ ECR에서 image pull
→ Container start
```

## 4. Public / Private

강의에서는 ECR이 private repository와 public repository(ECR Public Gallery)를 제공한다고 설명한다.

## 핵심

ECR은 애플리케이션을 실행하지 않는다.

```text
ECR = 저장
ECS/EKS = 실행/관리
```
