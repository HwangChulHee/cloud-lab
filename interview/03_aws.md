# 03. AWS

## Compute / Storage

1. EC2란 무엇인가요?
2. EC2 Instance Type은 어떤 기준으로 선택하나요?
3. EC2 Stop/Start 후 public IP가 바뀌는 이유는 무엇인가요?
4. Elastic IP를 항상 사용하지 않는 이유는 무엇인가요?
5. EBS와 Instance Store의 차이는 무엇인가요?
6. EBS와 EFS의 차이는 무엇인가요?
7. gp3와 io2는 어떤 상황에서 선택하나요?

## Network / Security

8. Security Group이란 무엇인가요?
9. Security Group과 NACL의 차이는 무엇인가요?
10. VPC란 무엇인가요?
11. Internet Gateway의 역할은 무엇인가요?
12. NAT Gateway의 역할은 무엇인가요?
13. Route Table이 하는 일은 무엇인가요?
14. Private subnet의 EC2가 인터넷에 접속하려면 어떻게 구성하나요?
15. ALB와 NLB의 차이는 무엇인가요?
16. Target Group이란 무엇인가요?
17. Load Balancer Health Check가 실패하면 어떻게 되나요?

## Scaling / Availability

18. Auto Scaling Group의 min / desired / max를 설명하세요.
19. Auto Scaling은 어떤 metric으로 구성할 수 있나요?
20. CPU가 높다고 무조건 scale-out 해야 하나요?
21. Multi-AZ란 무엇인가요?
22. Availability Zone과 Region의 차이는 무엇인가요?

## Database / Cache

23. RDS를 EC2에 DB를 직접 설치하는 것과 비교해보세요.
24. RDS Multi-AZ와 Read Replica의 차이는 무엇인가요?
25. RDS의 읽기 부하가 증가하면 어떻게 대응하나요?
26. RDS CPU가 90%입니다. 어떻게 진단하겠습니까?
27. RDS Proxy는 왜 사용하나요?
28. ElastiCache를 왜 사용하나요?

## DNS / IAM / S3

29. Route 53의 역할은 무엇인가요?
30. A Record와 CNAME의 차이는 무엇인가요?
31. DNS TTL을 너무 크게 잡으면 어떤 문제가 있나요?
32. IAM User와 IAM Role의 차이는 무엇인가요?
33. EC2에서 S3에 접근할 때 access key 대신 무엇을 사용하겠습니까?
34. Least Privilege 원칙을 설명하세요.
35. S3 Bucket이 외부에 노출되었습니다. 어떤 항목을 점검하겠습니까?

## 대표 꼬리질문

### RDS Multi-AZ와 Read Replica는 왜 다른가요?

```text
Multi-AZ
- 목적: 고가용성 / 장애조치
- Standby 복제본
- 장애 발생 시 failover

Read Replica
- 목적: 읽기 확장
- SELECT 부하 분산
- 비동기 복제
```

### ALB 뒤 EC2의 포트를 인터넷에 열어야 하나요?

일반적으로 EC2의 application port source를 `0.0.0.0/0`로 열 필요가 없습니다.
ALB의 Security Group을 source로 지정해 ALB를 통해 들어오는 traffic만 허용하는 구성이 더 적절합니다.

### EC2 CPU 90%면 어떻게 하겠습니까?

```text
CloudWatch metric 확인
 ↓
일시 spike / 지속 부하 구분
 ↓
프로세스 확인
 ↓
트래픽 증가 / 애플리케이션 문제 구분
 ↓
scale-up / scale-out / 코드 개선 판단
```
