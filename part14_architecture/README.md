# 14부 — CloudFormation & Architecture Coverage

SAA 강의의 **CloudFormation / Classic Solutions Architecture / More Solutions Architecture / White Papers & Architectures** 영역을 정리한다.

이 파트는 개별 AWS 서비스 암기보다 **여러 요구사항을 동시에 보고 어떤 architecture pattern을 조합할지** 판단하는 마무리 Coverage 파트다.

## Chapters

- [ ] [74. CloudFormation](./74_cloudformation/README.md)
- [ ] [75. Classic Solutions Architecture](./75_classic_solutions_architecture/README.md)
- [ ] [76. High Availability / Scalability Patterns](./76_high_availability_scalability_patterns/README.md)
- [ ] [77. Serverless / Global Architecture Patterns](./77_serverless_global_architecture_patterns/README.md)
- [ ] [78. 비용 최적화 개념](./78_cost_optimization/README.md)
- [ ] [79. AWS Well-Architected Framework](./79_well_architected_framework/README.md)
- [ ] [80. More Solutions Architecture / White Papers Coverage](./80_more_solutions_whitepapers/README.md)

## 전체 흐름

```text
CloudFormation
→ Infrastructure as Code
→ 같은 infrastructure를 재현

Classic Architecture
→ Route 53 / ELB / ASG / EC2
→ RDS / ElastiCache / EFS

HA / Scalability
→ Multi-AZ
→ Health Check
→ Horizontal Scaling
→ Caching / Decoupling

Serverless / Global
→ CloudFront / S3
→ API Gateway / Lambda
→ DynamoDB
→ Streams / Event-driven

Cost Optimization
→ Purchasing Model
→ Auto Scaling
→ Cache / Offloading
→ Storage Lifecycle

Well-Architected
→ 6 Pillars로 architecture review

More Architecture / White Papers
→ service 조합 복습
→ Trusted Advisor
→ reference architectures / white papers
```

## Classic Architecture 판단

강의의 대표 3-tier 흐름:

```text
Route 53
   ↓
ELB
   ↓
Auto Scaling EC2
   ├→ ElastiCache
   ├→ RDS
   └→ EFS
```

여기서 다음을 구분한다.

```text
Web tier scale
→ ELB + ASG

Session 분리
→ ElastiCache / DynamoDB

DB Read Scale
→ Read Replica

DB HA
→ Multi-AZ

Shared Linux File
→ EFS

계층별 접근 제한
→ Security Group reference
```

## Serverless / Global 판단

```text
Users
  ↓
CloudFront
  ├→ S3 Static Content
  └→ API Gateway
        ↓
      Lambda
        ↓
     DynamoDB
```

추가 event processing:

```text
DynamoDB Streams → Lambda → SES
S3 Event → Lambda / SQS / SNS
SNS → multiple SQS
```

## 시험에서 특히 중요한 비교

```text
RDS Multi-AZ
vs Read Replica
→ HA vs Read Scaling

Sticky Session
vs External Session Store
→ instance affinity vs stateless scale-out

CloudFront
vs 더 큰 EC2/ASG
→ static content offloading vs origin compute 확장

Synchronous
vs Asynchronous
→ immediate response vs decoupled buffering

On-Demand / Reserved / Savings Plans / Spot
→ workload 성격에 맞는 구매 옵션

Well-Architected Tool
vs Trusted Advisor
→ workload architecture review vs account/resource recommendation
```

## Well-Architected 6 Pillars

```text
1. Operational Excellence
2. Security
3. Reliability
4. Performance Efficiency
5. Cost Optimization
6. Sustainability
```

강의에서는 이들을 하나씩 trade-off하는 항목보다 함께 개선하는 **synergy**로 설명한다.

## 학습 순서

```text
74 CloudFormation
      ↓
75 Classic Architecture
      ↓
76 HA / Scalability Patterns
      ↓
77 Serverless / Global Patterns
      ↓
78 Cost Optimization
      ↓
79 Well-Architected
      ↓
80 More Architecture / White Papers
```

## 학습 깊이

14부는 **Coverage 중심**이다.

시험 전에 다음을 설명할 수 있으면 우선 충분하다.

```text
왜 이 architecture가 stateless한가?
어디에서 scale-out하는가?
어디에 state가 남아 있는가?
HA와 read scaling은 어떻게 다른가?
동기/비동기 communication 중 무엇을 선택하는가?
static content를 왜 CloudFront로 offload하는가?
비용 최적화는 구매 옵션 외에 어떤 설계로 가능한가?
6 Pillar 관점에서 어떤 risk가 있는가?
```

시험 이후에는 이 내용을 `examples/`와 `portfolio/`에서 **서비스 선택 근거, HA/보안/비용 trade-off 설명**으로 재사용한다.
