# Example 09 — RDS를 Private Subnet에 배치하기

웹 계층 뒤에 관리형 DB를 붙이고, 인터넷이 아니라 애플리케이션 계층에서만 접근하도록 만든다.

## Recall Check
- Private Subnet의 의미는?
- SG Reference는 왜 IP 허용보다 구조를 잘 표현했나?
- ALB-SG → EC2-SG 흐름은?
- Private EC2가 외부 패키지를 내려받아야 한다면 어떤 outbound 경로가 필요한가?

## 새로 배우는 것
- RDS
- DB Subnet Group
- RDS Security Group
- 애플리케이션과 DB 연결
- DB 연결 장애의 증상 구분

## 반복하는 것
VPC, Private Subnet, EC2, IAM/SG, ALB 구조를 다시 사용한다.

모든 태그 가능 리소스에는 `Project=cloud-lab`, `Stage=examples`, `Example=09`을 붙인다.

## 리소스 이름표

| 리소스 | 이름 |
| --- | --- |
| ALB | `example-09-alb` |
| Target Group | `example-09-tg` |
| ALB Security Group | `example-09-alb-sg` |
| App/EC2 Security Group | `example-09-app-sg` |
| App EC2 | `example-09-app` |
| DB Subnet Group | `example-09-db-subnet-group` |
| RDS Security Group | `example-09-db-sg` |
| RDS DB Instance Identifier | `example-09-db` |

기존 VPC를 재사용하지 않고 새로 만든다면 `example-09-vpc`, `example-09-public-a/b`, `example-09-private-a/b` 형식을 사용한다.

## 이번에는 도움 없이
ALB-SG와 EC2-SG를 다시 구성하고, EC2를 Private Subnet에 배치한다.

## 목표 구조
```text
Internet
  ↓
ALB
  ↓
EC2 / App
  ↓
RDS

ALB-SG → EC2-SG → RDS-SG
```

## 구축
1. 두 AZ의 Private Subnet을 포함하는 DB Subnet Group을 만든다.
2. PostgreSQL 또는 MySQL RDS를 생성한다.
3. Public access는 비활성화한다.
4. RDS-SG inbound는 DB port를 `source=EC2-SG`로만 허용한다.
5. EC2에서 DB에 접속한다.
6. 간단한 테이블을 만들고 INSERT/SELECT를 수행한다.

## 애플리케이션 연결 보강

가능하면 단순 DB CLI 테스트에서 끝내지 않고 애플리케이션 요청 경로까지 연결한다.

예:

```text
GET /db-health
  ↓
SELECT 1
  ↓
정상: 200
DB 연결 실패: 500 또는 명시적인 unhealthy 응답
```

구현 언어/프레임워크는 자유다. 핵심은 다음 전체 흐름을 직접 보는 것이다.

```text
Client → ALB → App → RDS
```

애플리케이션 구현에 시간이 많이 든다면 이 단계는 선택으로 두고 DB CLI의 INSERT/SELECT만 완료해도 된다.

## 관찰
- RDS endpoint는 IP인가 DNS 이름인가?
- RDS가 Private인데 EC2에서 접근 가능한 이유는?
- 인터넷에서 DB에 바로 접근할 수 없는 이유는 Public access와 SG 두 관점에서 무엇인가?
- `/db-health`가 실패했을 때 ALB 자체 장애와 어떻게 구분할 수 있는가?

## 장애 실험 A — RDS SG 차단
RDS-SG에서 EC2-SG inbound rule을 제거하고 앱/CLI 연결을 시도한다.

예상 흐름:
```text
EC2는 정상
RDS도 available
하지만 network connection timeout
```

애플리케이션 endpoint가 있다면 `/db-health` 결과와 앱 로그도 함께 본다.

rule을 복구하고 다시 연결한다.

## 장애 실험 B — 잘못된 DB endpoint/port
애플리케이션의 endpoint 또는 port를 일부러 잘못 설정해 증상을 비교한다. 네트워크 차단과 설정 오류가 로그에서 어떻게 다른지 기록한다.

## 기억만으로 설명하기
- DB를 Public Subnet에 두지 않는 이유는?
- EC2-SG를 source로 지정하면 어떤 의미인가?
- 애플리케이션이 DB 연결 실패를 내면 어디부터 확인할 것인가?
- ALB가 healthy라고 해서 DB까지 정상이라고 볼 수 있는가?

## CLI 구축 검증

### 1. RDS 상태 / Endpoint / 배치

```bash
aws rds describe-db-instances --region $AWS_REGION \
  --query "DBInstances[?contains(DBInstanceIdentifier, 'example-09')].{Id:DBInstanceIdentifier,Status:DBInstanceStatus,Public:PubliclyAccessible,MultiAZ:MultiAZ,Endpoint:Endpoint.Address,Port:Endpoint.Port,Vpc:DBSubnetGroup.VpcId,Subnets:DBSubnetGroup.Subnets[].SubnetIdentifier,SG:VpcSecurityGroups[].VpcSecurityGroupId}" \
  --output json
```

특히:

- `PubliclyAccessible=false`: 인터넷 공개 DB가 아님.
- `Subnets`: DB Subnet Group이 어느 subnet들을 사용하는가.
- `Endpoint`: 애플리케이션이 실제 접속할 DNS 이름.
- `VpcSecurityGroups`: DB 접근을 제어하는 SG.

### 2. RDS Security Group

```bash
aws ec2 describe-security-groups --region $AWS_REGION \
  --group-ids <rds-sg-id> \
  --query 'SecurityGroups[].IpPermissions'
```

DB port의 source가 `0.0.0.0/0`가 아니라 **App/EC2 Security Group**인지 확인한다.

### 3. 애플리케이션 관점 검증

```bash
curl -i http://<alb-dns>/db-health
```

이 명령은 AWS control plane 설정을 조회하는 것이 아니라 **실제 사용자 요청 경로로 애플리케이션이 DB까지 연결되는지** 확인한다.

```text
RDS status=available
≠ 애플리케이션 DB 연결 정상

/db-health 성공
→ ALB → App → RDS 실제 data path까지 확인
```

### 4. 삭제 후 DB와 Snapshot 확인

```bash
aws rds describe-db-instances --region $AWS_REGION \
  --query "DBInstances[?contains(DBInstanceIdentifier, 'example-09')].[DBInstanceIdentifier,DBInstanceStatus]"

aws rds describe-db-snapshots --region $AWS_REGION --snapshot-type manual \
  --query "DBSnapshots[?contains(DBSnapshotIdentifier, 'example-09')].[DBSnapshotIdentifier,Status]"
```

DB Instance를 삭제해도 Manual Snapshot은 남을 수 있으므로 별도로 조회한다.

## 완료 체크
- [x] DB Subnet Group을 만들었다.
- [x] RDS를 Private하게 생성했다.
- [x] EC2-SG만 DB port 접근을 허용했다.
- [x] EC2에서 INSERT/SELECT를 했다.
- [x] 가능하면 App → RDS health endpoint를 확인했다. (선택 단계라 생략)
- [x] SG 차단 장애를 재현하고 복구했다.
- [x] DB 연결 실패의 후보 원인을 설명할 수 있다.

## 비용 정리
RDS는 비용이 발생하므로 실습 후 snapshot 보존 여부를 확인하고 필요 없으면 삭제한다. Manual Snapshot도 별도 과금 대상이 될 수 있으므로 의도적으로 남기는지 확인한다.

삭제 후 CLI 삭제 검증을 실행한다.

---
