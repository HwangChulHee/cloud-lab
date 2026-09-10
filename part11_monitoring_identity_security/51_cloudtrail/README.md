# 51. CloudTrail

CloudTrail은 **AWS 계정에서 누가, 언제, 어떤 API 작업을 수행했는지 추적하는 감사(Audit) 서비스**다.

CloudWatch가 "지금 시스템 상태가 어떤가?"를 보는 쪽이라면, CloudTrail은 "누가 이 설정을 바꿨지?"를 추적하는 데 가깝다.

## 핵심 질문

- 누가 이 리소스를 생성/삭제/변경했는가?
- Console에서 한 작업도 기록되는가?
- IAM User가 아니라 Role로 수행한 작업은 어떻게 보이는가?
- 특정 API 호출이 실패했다면 누가 어떤 권한으로 호출했는가?
- CloudWatch Logs와 CloudTrail Event의 역할 차이는 무엇인가?

## 반드시 이해할 개념

### Event History

최근 관리 이벤트를 빠르게 확인할 때 사용한다.

예:

```text
TerminateInstances
AuthorizeSecurityGroupIngress
DeleteBucket
PutRolePolicy
CreateLoadBalancer
```

장애가 갑자기 발생했을 때 "직전에 누가 설정을 바꿨는지" 확인하는 출발점으로 사용할 수 있다.

### Management Event vs Data Event

```text
Management Event
→ AWS 리소스의 제어면(Control Plane) 작업
→ EC2 생성, SG 수정, IAM 변경 등

Data Event
→ 실제 데이터 계층 작업
→ S3 Object 접근, Lambda Invoke 등
```

모든 데이터 이벤트가 기본적으로 동일하게 기록된다고 생각하면 안 된다. 데이터 이벤트는 양이 많을 수 있으므로 별도 설정과 비용을 의식한다.

### Trail

장기간 보관하거나 S3로 전달하려면 Trail을 구성한다.

```text
AWS API Activity
     ↓
CloudTrail
     ↓
S3
```

필요하면 CloudWatch Logs와 연결해 특정 API 호출에 대한 경보도 만들 수 있다.

## 운영 시나리오

### Security Group이 갑자기 열렸다

```text
증상
EC2-SG에 0.0.0.0/0 규칙이 생김

CloudTrail에서 확인
AuthorizeSecurityGroupIngress

확인할 것
userIdentity
sourceIPAddress
eventTime
requestParameters
```

CloudWatch가 "서비스가 이상하다"는 신호를 제공했다면 CloudTrail은 "누가 구성을 바꿨는가"를 추적하는 데 사용할 수 있다.

### EC2가 갑자기 종료됐다

```text
TerminateInstances 검색
→ 호출 주체 확인
→ IAM User / AssumedRole 확인
→ 대상 InstanceId 확인
```

## CloudWatch와 차이

```text
CloudWatch
→ Metrics / Logs / Alarms
→ CPU, 5xx, latency, application log
→ 시스템 상태 관측

CloudTrail
→ AWS API activity
→ 누가 어떤 AWS 설정을 변경했는가
→ 감사와 변경 추적
```

둘은 경쟁 관계가 아니라 함께 사용한다.

## 실습 전 최소 Hands-on

Console에서 다음 중 하나를 직접 수행한다.

```text
Security Group rule 추가
또는
EC2 Stop/Start
```

그 뒤 CloudTrail Event History에서 해당 API 이벤트를 찾아 다음을 확인한다.

- Event name
- Event time
- Username / assumed role
- AWS Region
- Source IP
- Resource

## 기억만으로 설명하기

```text
Q1. CloudWatch와 CloudTrail은 무엇이 다른가?
Q2. EC2가 삭제되었을 때 어떤 API 이름부터 찾을 것인가?
Q3. Management Event와 Data Event의 차이는?
Q4. Role을 Assume한 사용자의 활동도 추적할 수 있는가?
Q5. 장애 대응에서 CloudTrail은 어느 단계에 쓰이는가?
```

## examples 연결

직접적인 신규 서비스 구축보다는 15~16의 장애 분석을 보강한다.

```text
examples/15 Troubleshooting
→ 설정 변경 원인 추적

examples/16 Final Architecture
→ SG/IAM/EC2 설정 변경 이력 확인
```

## 완료 기준

- [ ] Event History에서 API 호출을 찾을 수 있다.
- [ ] Management Event와 Data Event를 구분할 수 있다.
- [ ] CloudWatch와 CloudTrail의 역할 차이를 설명할 수 있다.
- [ ] `userIdentity`, `eventName`, `requestParameters`를 보고 변경 주체와 내용을 추적할 수 있다.
- [ ] "누가 설정을 바꿨는가?"라는 질문에서 CloudTrail을 떠올릴 수 있다.
