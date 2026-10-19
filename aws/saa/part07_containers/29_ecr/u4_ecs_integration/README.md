# u4. ECR과 ECS/EKS 연동

ECR의 대표 사용 흐름:

```text
Developer
   ↓
Docker Image
   ↓
ECR
   ↓
ECS Task Definition
   ↓
ECS Task
```

Task Definition의 container image 항목에 ECR Image URI가 들어간다.

EKS에서도 Pod가 ECR Image를 pull해 실행할 수 있다.

## 오류 추적

```text
Task 시작 실패
→ Image URI 확인
→ ECR repository/tag 존재 확인
→ IAM pull 권한 확인
→ network path 확인
```

Private subnet에서 Image를 pull해야 한다면 인터넷/NAT 또는 필요한 AWS private endpoint 경로 같은 네트워크 조건도 별도로 고려해야 한다.

## 기억할 문장

> ECR은 image registry이고, ECS/EKS가 그 image를 가져가 실제 container workload를 실행한다.
