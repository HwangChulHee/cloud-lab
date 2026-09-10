# Cloud / DevOps Interview

클라우드 엔지니어 및 DevOps 면접 대비 문제은행입니다.

단순 암기보다 `What → Why → When → Trade-off → Troubleshooting` 순서로 답변하는 것을 목표로 합니다.

## 구성

- [01 Linux](./01_linux.md)
- [02 Networking](./02_networking.md)
- [03 AWS](./03_aws.md)
- [04 Docker](./04_docker.md)
- [05 Kubernetes](./05_kubernetes.md)
- [06 Terraform](./06_terraform.md)
- [07 CI/CD](./07_cicd.md)
- [08 Monitoring](./08_monitoring.md)
- [09 Troubleshooting](./09_troubleshooting.md)

## 공부 방법

1. 질문을 보고 1~2분 동안 직접 말로 답한다.
2. 정의만 말하지 않고 실제 상황을 예로 든다.
3. 장애 문제는 `증상 → 범위 축소 → 확인 명령/지표 → 원인 → 조치` 순서로 답한다.
4. AWS 문제는 현재 SAA 학습 내용과 연결해서 복습한다.
5. Kubernetes/Terraform/CI-CD는 실습한 뒤 다시 답변을 갱신한다.

## 핵심 사고 흐름

```text
사용자
  ↓
DNS / Route 53
  ↓
Load Balancer
  ↓
Security Group / NACL / Route
  ↓
EC2 / Container / Pod
  ↓
Application
  ↓
RDS / Redis / Storage
```

면접에서 중요한 것은 도구 이름을 많이 아는 것이 아니라, 문제가 생겼을 때 어디부터 확인하고 어떻게 범위를 좁히는지 설명하는 것입니다.
