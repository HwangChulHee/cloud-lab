# u1. AWS Config — Configuration Recording / Timeline

AWS Config의 첫 번째 역할은 **리소스 설정 상태와 변화 기록**이다.

## Configuration History

예를 들어 ALB의 설정이 바뀌었다면:

```text
09:00
ALB + SG-A

11:00
ALB + SG-B

14:00
HTTPS Listener 추가
```

처럼 resource configuration이 시간에 따라 어떻게 바뀌었는지 추적할 수 있다.

## Resource Timeline

강의에서는 한 resource에 대해 다음을 함께 볼 수 있다고 설명한다.

```text
Compliance over time
Configuration over time
CloudTrail API calls over time
```

즉 "현재 설정"뿐 아니라 과거 상태까지 추적할 수 있다.

## Region / Account

AWS Config는 **per-Region service**다.

필요하면 여러 Region과 여러 Account의 정보를 aggregate할 수 있다.

## S3 연동

Configuration data를 S3에 저장하고 Athena로 분석하는 패턴도 강의에서 다룬다.

## 기억할 문장

> AWS Config는 리소스의 설정이 어떻게 바뀌었는지 시간축으로 기록하고 추적한다.
