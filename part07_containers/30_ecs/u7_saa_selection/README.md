# u7. ECS SAA 선택 기준

## 전체 구조

```text
Image
→ ECR

Orchestration
→ ECS

Compute
→ EC2 or Fargate

Traffic
→ ALB/NLB

Shared File
→ EFS

Permissions
→ Task Role / EC2 Instance Profile

Scaling
→ ECS Service Auto Scaling
```

## 문제별 선택

```text
AWS-native container platform
→ ECS

EC2 관리 없이 container 실행
→ Fargate

container host까지 직접 제어
→ ECS EC2 Launch Type

HTTP microservice 여러 Task에 분산
→ ALB + ECS Service

Task application이 S3 접근
→ ECS Task Role

EC2 Launch Type의 ECS Agent 권한
→ EC2 Instance Profile

여러 AZ Task가 file 공유
→ EFS

Task CPU/Memory/ALB request 기준 확장
→ ECS Service Auto Scaling

S3 event 또는 schedule로 container batch 실행
→ EventBridge + ECS Task
```

## ECS vs EKS 미리보기

```text
ECS
→ AWS-native API
→ AWS에 최적화
→ Kubernetes 필요 없음

EKS
→ Kubernetes API
→ multi-cloud/on-prem Kubernetes 경험 재사용
```

## 면접용 설명

> ECS는 AWS-native container orchestration 서비스이고, Task Definition으로 실행 구성을 정의한 뒤 Task/Service로 workload를 운영합니다. Compute는 EC2 또는 Fargate를 선택하며, Service Auto Scaling은 Task 수를 조정하고 EC2 Auto Scaling은 underlying host 수를 조정한다는 점을 구분해야 합니다.
