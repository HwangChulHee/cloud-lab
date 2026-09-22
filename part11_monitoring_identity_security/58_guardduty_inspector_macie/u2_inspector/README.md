# u2. Amazon Inspector

Amazon Inspector는 **workload의 software vulnerability와 network exposure를 자동 평가**하는 서비스다.

## 대상

강의에서는 세 대상을 명확히 구분한다.

```text
EC2 Instances
ECR Container Images
Lambda Functions
```

## EC2

EC2에서는 SSM Agent를 활용한다.

평가:

```text
known OS/package vulnerabilities
unintended network accessibility
```

## ECR

```text
Container Image push
→ Inspector assessment
→ package vulnerability 탐지
```

## Lambda

```text
Function deployment
→ code / package dependency vulnerability 탐지
```

## 무엇을 평가하나?

강의 핵심:

```text
Package Vulnerabilities (CVE)
→ EC2 / ECR / Lambda

Network Reachability
→ EC2
```

각 vulnerability에는 risk score가 연결되어 우선순위를 정하는 데 사용된다.

## Integration

```text
Inspector
→ EventBridge
→ Security Hub
```

## 기억할 문장

> Inspector는 EC2/ECR/Lambda의 known vulnerability를 지속 평가하는 workload vulnerability scanner다.
