# u1. Amazon GuardDuty

Amazon GuardDuty는 **AWS Account의 위협 행위를 탐지하는 intelligent threat detection 서비스**다.

강의에서는 Machine Learning, anomaly detection, third-party data를 사용한다고 설명한다.

## 주요 입력

```text
CloudTrail Management Events
CloudTrail S3 Data Events
VPC Flow Logs
DNS Logs
```

강의에서 optional feature로 다음도 언급한다.

```text
EKS Audit Logs / Runtime Monitoring
RDS / Aurora login activity
EBS
Lambda network activity
S3 Data Events
```

## 예시

```text
unusual API calls
unauthorized deployment
unusual internal traffic
suspicious IP
DNS query를 통한 data exfiltration 징후
cryptocurrency-related finding
```

## Finding 이후

```text
GuardDuty Finding
      ↓
EventBridge
   ├→ SNS
   └→ Lambda
```

## 특징

강의는 별도 software 설치 없이 enable할 수 있다고 설명한다.

## 기억할 문장

> GuardDuty는 CloudTrail/VPC Flow Logs/DNS 등 activity signal을 분석해 AWS 환경의 수상한 행동을 탐지한다.
