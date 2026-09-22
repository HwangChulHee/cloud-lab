# u2. ECR IAM / Authentication

ECR 접근은 IAM 권한과 연결된다.

## Push/Pull 권한

개념적으로:

```text
Developer / CI Role
→ ECR push 권한

ECS execution 측 권한
→ ECR pull 권한
```

ECR 접근 오류가 발생하면 단순 네트워크 문제만 보지 않고 IAM Policy를 확인해야 한다.

강의에서도 ECR permission error는 IAM policy를 확인하는 흐름으로 설명한다.

## ECS와 연결

EC2 Launch Type에서는 ECS agent가 ECR에서 image를 pull하는 데 필요한 권한이 EC2 Instance Profile 쪽과 연결될 수 있다.

Fargate에서는 EC2 instance를 직접 관리하지 않지만 Task 실행 과정에서 필요한 AWS service 권한 구조를 구분해서 이해해야 한다.

## 핵심 구분

```text
ECS Task Role
→ application container가 S3/DynamoDB 등 AWS API 호출

Image pull / log 전송 등 task 실행 준비
→ execution/infrastructure 측 권한

둘을 같은 역할로 뭉뚱그리지 않는다.
```
