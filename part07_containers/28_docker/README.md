# 28. Docker

SAA 강의의 Containers on AWS 첫 단원이다.

Docker는 애플리케이션과 실행에 필요한 환경을 **Container Image**로 패키징하고, 어디서 실행하더라도 일관된 동작을 기대할 수 있게 해주는 컨테이너 플랫폼이다.

## Units

- [ ] [u1. Container / Image / Dockerfile](./u1_container_image_dockerfile/README.md)
- [ ] [u2. Docker vs Virtual Machine](./u2_docker_vs_vm/README.md)
- [ ] [u3. Build / Run / Repository 흐름](./u3_build_run_repository/README.md)
- [ ] [u4. AWS에서 Container를 어디서 실행하는가](./u4_aws_container_map/README.md)

## 전체 흐름

```text
Dockerfile
   ↓ build
Docker Image
   ↓ run
Container

Docker Image
   ↓ push
Docker Repository
   ↓ pull
ECS / EKS / Local
```

## SAA에서 알아둘 것

```text
Docker
→ application packaging

ECR
→ image 저장소

ECS
→ AWS-native container orchestration

EKS
→ managed Kubernetes

Fargate
→ EC2를 직접 관리하지 않는 serverless container compute
```

Docker 자체의 깊은 명령어 학습보다 **Image → Registry → Container Runtime/Orchestrator** 흐름을 이해하는 것이 우선이다.
