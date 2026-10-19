# u4. CloudWatch vs CloudTrail vs AWS Config

이 세 서비스는 시험에서 같이 비교된다.

## CloudWatch

```text
현재 성능/상태
Metric
Log
Alarm
Dashboard
```

예:

```text
ALB request 수?
HTTP 5xx 비율?
EC2 CPU?
```

## CloudTrail

```text
누가 무엇을 했나?
API Call
Audit
User / Role
변경 행위 추적
```

예:

```text
누가 Security Group rule을 변경했나?
```

## AWS Config

```text
리소스 설정이 어떻게 바뀌었나?
Compliance를 만족하는가?
Configuration Timeline
```

예:

```text
ALB에 HTTPS certificate가 항상 연결되어 있는가?
```

## ALB 하나로 비교

```text
CloudWatch
→ incoming connections / error metrics

Config
→ SG rule / Listener / certificate 설정과 compliance

CloudTrail
→ 누가 ALB 설정을 변경했는지 API call 추적
```

## 기억할 문장

> CloudWatch는 상태, CloudTrail은 행위, Config는 설정과 Compliance다.
