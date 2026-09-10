# AWS CLI Verification & Cleanup Guide

각 Example은 콘솔에서 구축한 뒤 **AWS CLI 출력으로 구조를 검증**하고, 종료 후 **잔존 리소스가 없는지 다시 검증**한다.

목표는 단순히 `됐다/안 됐다`를 보는 것이 아니라, CLI 출력만 보고도 다음을 판단할 수 있게 하는 것이다.

```text
구축 결과
→ CLI로 상태/연결 관계 출력
→ 출력 내용을 ChatGPT에 붙여넣기
→ 구조가 요구사항에 맞는지 검토
→ 장애 전/중/복구 후 비교
→ 실습 종료
→ 삭제 후 CLI로 잔존 리소스 확인
```

## 공통 준비

서울 리전을 기본으로 가정한다.

```bash
export AWS_REGION=ap-northeast-2
aws sts get-caller-identity
aws configure get region
```

## 공통 태그 규칙

태그를 지원하는 모든 실습 리소스에는 가능한 한 아래 태그를 붙인다.

```text
Project = cloud-lab
Stage   = examples
Example = 01   # 챕터 번호에 맞게 변경
```

Name은 `example-NN-*` 형식을 사용한다.

CLI 필터링은 가능하면 `Project/Stage/Example` 태그를 우선하고, API 제약이 있거나 태그 필터가 불편한 리소스는 이름 규칙을 함께 사용한다.

> CLI 출력에 Access Key, Secret Key, DB 비밀번호, presigned URL 전체 값은 포함하지 않는다.

---

# 01 — Single EC2 Web

## 구축 검증

```bash
aws ec2 describe-instances \
  --region $AWS_REGION \
  --filters \
    'Name=tag:Project,Values=cloud-lab' \
    'Name=tag:Stage,Values=examples' \
    'Name=tag:Example,Values=01' \
    'Name=instance-state-name,Values=pending,running,stopping,stopped' \
  --query 'Reservations[].Instances[].{Name:Tags[?Key==`Name`]|[0].Value,Id:InstanceId,State:State.Name,PublicIP:PublicIpAddress,PrivateIP:PrivateIpAddress,Subnet:SubnetId,Vpc:VpcId,SG:SecurityGroups[].GroupId}' \
  --output table
```

```bash
aws ec2 describe-security-groups \
  --region $AWS_REGION \
  --filters 'Name=tag:Example,Values=01' \
  --query 'SecurityGroups[].{Name:GroupName,Id:GroupId,Ingress:IpPermissions}'
```

판단 포인트: EC2 running, Public/Private IP 존재, HTTP 80 inbound 존재.

## 삭제 검증

```bash
aws ec2 describe-instances --region $AWS_REGION \
  --filters 'Name=tag:Example,Values=01' 'Name=instance-state-name,Values=pending,running,stopping,stopped' \
  --query 'Reservations[].Instances[].InstanceId'

aws ec2 describe-volumes --region $AWS_REGION \
  --filters 'Name=tag:Example,Values=01' \
  --query 'Volumes[].{Id:VolumeId,State:State}'
```

주요 결과가 `[]`이면 된다.

---

# 02 — ALB + Two EC2

## 구축 검증

```bash
aws ec2 describe-instances --region $AWS_REGION \
  --filters 'Name=tag:Example,Values=02' 'Name=instance-state-name,Values=running' \
  --query 'Reservations[].Instances[].{Id:InstanceId,AZ:Placement.AvailabilityZone,PrivateIP:PrivateIpAddress}' --output table

aws elbv2 describe-load-balancers --region $AWS_REGION --names example-02-alb \
  --query 'LoadBalancers[].{DNS:DNSName,State:State.Code,Scheme:Scheme,Vpc:VpcId,AZs:AvailabilityZones[].ZoneName}'

aws elbv2 describe-target-groups --region $AWS_REGION --names example-02-tg \
  --query 'TargetGroups[].{Arn:TargetGroupArn,Protocol:Protocol,Port:Port,Vpc:VpcId,HealthPath:HealthCheckPath}'
```

```bash
export TG_ARN=$(aws elbv2 describe-target-groups --region $AWS_REGION --names example-02-tg --query 'TargetGroups[0].TargetGroupArn' --output text)
aws elbv2 describe-target-health --region $AWS_REGION --target-group-arn $TG_ARN \
  --query 'TargetHealthDescriptions[].{Target:Target.Id,State:TargetHealth.State,Reason:TargetHealth.Reason}' --output table
```

판단 포인트: EC2 2대, 서로 다른 AZ, ALB active, Target 2개 healthy.

## 삭제 검증

```bash
aws elbv2 describe-load-balancers --region $AWS_REGION --query "LoadBalancers[?contains(LoadBalancerName, 'example-02')].[LoadBalancerName,State.Code]"
aws elbv2 describe-target-groups --region $AWS_REGION --query "TargetGroups[?contains(TargetGroupName, 'example-02')].TargetGroupName"
aws ec2 describe-instances --region $AWS_REGION --filters 'Name=tag:Example,Values=02' 'Name=instance-state-name,Values=pending,running,stopping,stopped' --query 'Reservations[].Instances[].InstanceId'
```

---

# 03 — ALB Health Check

## 구축/장애 검증

```bash
export TG_ARN=<target-group-arn>

aws elbv2 describe-target-groups --region $AWS_REGION --target-group-arns $TG_ARN \
  --query 'TargetGroups[].{Path:HealthCheckPath,Interval:HealthCheckIntervalSeconds,Timeout:HealthCheckTimeoutSeconds,Healthy:HealthyThresholdCount,Unhealthy:UnhealthyThresholdCount,Matcher:Matcher.HttpCode}'

aws elbv2 describe-target-health --region $AWS_REGION --target-group-arn $TG_ARN \
  --query 'TargetHealthDescriptions[].{Target:Target.Id,State:TargetHealth.State,Reason:TargetHealth.Reason,Description:TargetHealth.Description}' --output table
```

판단 포인트: 정상 → healthy, app 중지/잘못된 path → unhealthy, 복구 → healthy.

---

# 04 — Security Group Layering

## 구축 검증

```bash
aws ec2 describe-security-groups --region $AWS_REGION \
  --filters 'Name=tag:Example,Values=04' \
  --query 'SecurityGroups[].{Name:GroupName,Id:GroupId,Ingress:IpPermissions}'
```

판단 포인트: ALB-SG는 client 80/443 허용, EC2-SG의 app port source는 `0.0.0.0/0`가 아니라 ALB-SG ID.

---

# 05 — VPC Public / Private Subnets

## 구축 검증

```bash
export VPC_ID=$(aws ec2 describe-vpcs --region $AWS_REGION \
  --filters 'Name=tag:Name,Values=example-05-vpc' \
  --query 'Vpcs[0].VpcId' --output text)

echo $VPC_ID

aws ec2 describe-subnets --region $AWS_REGION --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'Subnets[].{Name:Tags[?Key==`Name`]|[0].Value,Id:SubnetId,CIDR:CidrBlock,AZ:AvailabilityZone,PublicIP:MapPublicIpOnLaunch}' --output table

aws ec2 describe-route-tables --region $AWS_REGION --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'RouteTables[].{Name:Tags[?Key==`Name`]|[0].Value,Id:RouteTableId,Routes:Routes,Associations:Associations[].SubnetId}'

aws ec2 describe-internet-gateways --region $AWS_REGION --filters "Name=attachment.vpc-id,Values=$VPC_ID" \
  --query 'InternetGateways[].{Id:InternetGatewayId,Attachments:Attachments}'
```

판단 포인트: subnet 4개, CIDR 비중복, 2AZ, public RT에 `0.0.0.0/0 → igw-*`, private RT에는 해당 IGW route 없음.

## 삭제 검증

```bash
aws ec2 describe-vpcs --region $AWS_REGION --filters 'Name=tag:Name,Values=example-05-vpc' --query 'Vpcs[].VpcId'
aws ec2 describe-internet-gateways --region $AWS_REGION --filters 'Name=tag:Example,Values=05' --query 'InternetGateways[].InternetGatewayId'
```

---

# 06 — Private EC2 / NAT / SSM

## 구축 검증

```bash
aws ec2 describe-instances --region $AWS_REGION \
  --filters 'Name=tag:Example,Values=06' 'Name=instance-state-name,Values=running' \
  --query 'Reservations[].Instances[].{Name:Tags[?Key==`Name`]|[0].Value,Id:InstanceId,PublicIP:PublicIpAddress,PrivateIP:PrivateIpAddress,Subnet:SubnetId,IamProfile:IamInstanceProfile.Arn}' --output table
```

```bash
aws ec2 describe-nat-gateways --region $AWS_REGION \
  --filter 'Name=tag:Example,Values=06' 'Name=state,Values=available,pending' \
  --query 'NatGateways[].{Id:NatGatewayId,Subnet:SubnetId,State:State,NatAddresses:NatGatewayAddresses[].PublicIp}' --output table
```

```bash
aws ssm describe-instance-information --region $AWS_REGION \
  --query 'InstanceInformationList[].{Instance:InstanceId,Ping:PingStatus,Agent:AgentVersion}' --output table
```

ALB/Target까지 함께 확인한다.

```bash
aws elbv2 describe-load-balancers --region $AWS_REGION --query "LoadBalancers[?contains(LoadBalancerName, 'example-06')].[LoadBalancerName,Scheme,State.Code,DNSName]"
```

판단 포인트:

```text
Private EC2 PublicIP = null
ALB = internet-facing / active
Target = healthy
NAT 사용 시 NAT = available / public subnet
SSM 사용 시 PingStatus = Online
```

## Bootstrap 장애 검증

NAT가 없는 상태에서 생성한 인스턴스와 NAT 추가 후 생성한 인스턴스를 비교한다.

EC2 내부에서 가능하면:

```bash
sudo tail -n 100 /var/log/cloud-init-output.log
systemctl status nginx --no-pager
```

CLI 출력과 함께 이 결과를 보내면 bootstrap 실패 원인을 판단하기 쉽다.

## 삭제 검증

```bash
aws ec2 describe-nat-gateways --region $AWS_REGION \
  --filter 'Name=tag:Example,Values=06' 'Name=state,Values=pending,available,deleting,failed' \
  --query 'NatGateways[].{Id:NatGatewayId,State:State}'

aws ec2 describe-addresses --region $AWS_REGION \
  --query "Addresses[?Tags[?Key=='Example' && Value=='06']].{AllocationId:AllocationId,PublicIp:PublicIp,AssociationId:AssociationId}"
```

NAT Gateway가 `deleted`가 되기 전까지 의존 리소스 삭제가 지연될 수 있다. EIP도 반드시 별도로 확인한다.

---

# 07 — ALB + Auto Scaling Group

## 구축 검증

```bash
aws autoscaling describe-auto-scaling-groups --region $AWS_REGION --auto-scaling-group-names example-07-asg \
  --query 'AutoScalingGroups[].{Min:MinSize,Desired:DesiredCapacity,Max:MaxSize,Subnets:VPCZoneIdentifier,Instances:Instances[].{Id:InstanceId,AZ:AvailabilityZone,Health:HealthStatus,Lifecycle:LifecycleState},TG:TargetGroupARNs}'

aws ec2 describe-launch-templates --region $AWS_REGION --launch-template-names example-07-lt \
  --query 'LaunchTemplates[].{Id:LaunchTemplateId,Latest:LatestVersionNumber,Default:DefaultVersionNumber}'
```

```bash
aws autoscaling describe-scaling-activities --region $AWS_REGION --auto-scaling-group-name example-07-asg --max-items 10 \
  --query 'Activities[].{Time:StartTime,Status:StatusCode,Cause:Cause,Description:Description}' --output table
```

판단 포인트: Desired 수만큼 InService/Healthy, Target Group 연결, replacement 후 새 instance 생성 기록, 새 target healthy.

## 삭제 검증

```bash
aws autoscaling describe-auto-scaling-groups --region $AWS_REGION --auto-scaling-group-names example-07-asg --query 'AutoScalingGroups[].AutoScalingGroupName'
aws ec2 describe-launch-templates --region $AWS_REGION --filters 'Name=launch-template-name,Values=example-07-*' --query 'LaunchTemplates[].LaunchTemplateName'
aws ec2 describe-instances --region $AWS_REGION --filters 'Name=tag:Example,Values=07' 'Name=instance-state-name,Values=pending,running,stopping,stopped' --query 'Reservations[].Instances[].InstanceId'
```

---

# 08 — Scaling & Recovery

## 구축/장애 검증

```bash
aws autoscaling describe-auto-scaling-groups --region $AWS_REGION --auto-scaling-group-names example-08-asg \
  --query 'AutoScalingGroups[].{Desired:DesiredCapacity,Min:MinSize,Max:MaxSize,Instances:Instances[].{Id:InstanceId,Health:HealthStatus,Lifecycle:LifecycleState}}'

aws autoscaling describe-scaling-activities --region $AWS_REGION --auto-scaling-group-name example-08-asg --max-items 20 \
  --query 'Activities[].{Time:StartTime,Status:StatusCode,Cause:Cause,Description:Description}' --output table

aws autoscaling describe-policies --region $AWS_REGION --auto-scaling-group-name example-08-asg \
  --query 'ScalingPolicies[].{Name:PolicyName,Type:PolicyType,Target:TargetTrackingConfiguration.TargetValue,Metric:TargetTrackingConfiguration.PredefinedMetricSpecification.PredefinedMetricType}'
```

CloudWatch에서 개별 EC2 CPU와 ASG 평균 CPU를 구분해서 본다.

```bash
aws cloudwatch list-metrics --region $AWS_REGION \
  --namespace AWS/EC2 --metric-name CPUUtilization \
  --query 'Metrics[].Dimensions'
```

판단 포인트:

```text
한 인스턴스만 CPU 높음 ≠ ASG 평균 CPU 반드시 높음
ASGAverageCPUUtilization이 target 초과
→ scaling activity
→ Desired 증가
```

---

# 09 — Private RDS

## 구축 검증

```bash
aws rds describe-db-instances --region $AWS_REGION \
  --query "DBInstances[?contains(DBInstanceIdentifier, 'example-09')].{Id:DBInstanceIdentifier,Status:DBInstanceStatus,Public:PubliclyAccessible,MultiAZ:MultiAZ,Endpoint:Endpoint.Address,Port:Endpoint.Port,Vpc:DBSubnetGroup.VpcId,Subnets:DBSubnetGroup.Subnets[].SubnetIdentifier,SG:VpcSecurityGroups[].VpcSecurityGroupId}" --output json
```

```bash
aws ec2 describe-security-groups --region $AWS_REGION --group-ids <rds-sg-id> \
  --query 'SecurityGroups[].IpPermissions'
```

판단 포인트: RDS available, `PubliclyAccessible=false`, private subnet 2개 이상, DB port source가 EC2-SG.

애플리케이션 `/db-health`를 만들었다면 함께 결과를 보낸다.

```bash
curl -i http://<alb-dns>/db-health
```

## 삭제 검증

```bash
aws rds describe-db-instances --region $AWS_REGION --query "DBInstances[?contains(DBInstanceIdentifier, 'example-09')].[DBInstanceIdentifier,DBInstanceStatus]"
aws rds describe-db-snapshots --region $AWS_REGION --snapshot-type manual --query "DBSnapshots[?contains(DBSnapshotIdentifier, 'example-09')].[DBSnapshotIdentifier,Status]"
```

---

# 10 — RDS Failure & Recovery

## 구축/복구 검증

```bash
aws rds describe-db-instances --region $AWS_REGION \
  --query "DBInstances[?contains(DBInstanceIdentifier, 'example-10')].{Id:DBInstanceIdentifier,Status:DBInstanceStatus,MultiAZ:MultiAZ,AZ:AvailabilityZone,SecondaryAZ:SecondaryAvailabilityZone,ReplicaSource:ReadReplicaSourceDBInstanceIdentifier,ReadReplicas:ReadReplicaDBInstanceIdentifiers,BackupRetention:BackupRetentionPeriod,Endpoint:Endpoint.Address}"

aws rds describe-events --region $AWS_REGION --source-type db-instance --duration 180 \
  --query 'Events[].{Time:Date,Source:SourceIdentifier,Message:Message}' --output table
```

판단 포인트: Multi-AZ 여부, replica 관계, backup retention, failover event, endpoint 유지 여부를 시간순으로 설명.

## 삭제 검증

```bash
aws rds describe-db-instances --region $AWS_REGION --query "DBInstances[?contains(DBInstanceIdentifier, 'example-10')].[DBInstanceIdentifier,DBInstanceStatus]"
aws rds describe-db-snapshots --region $AWS_REGION --snapshot-type manual --query "DBSnapshots[?contains(DBSnapshotIdentifier, 'example-10')].[DBSnapshotIdentifier,Status]"
```

---

# 11 — S3 + IAM Role

## 구축 검증

```bash
aws s3api get-bucket-location --bucket <bucket-name>
aws s3api get-public-access-block --bucket <bucket-name>
aws iam get-role --role-name <role-name> --query 'Role.{RoleName:RoleName,Arn:Arn,AssumeRolePolicyDocument:AssumeRolePolicyDocument}'
```

EC2 IAM Instance Profile:

```bash
aws ec2 describe-instances --region $AWS_REGION \
  --filters 'Name=tag:Example,Values=11' 'Name=instance-state-name,Values=running' \
  --query 'Reservations[].Instances[].{Id:InstanceId,IamProfile:IamInstanceProfile.Arn}'
```

EC2에서 특정 bucket을 테스트한다.

```bash
aws s3 ls s3://<bucket-name>/
aws s3 cp s3://<bucket-name>/test.txt ./test.txt
```

비교:

```bash
aws s3 ls
```

판단 포인트: 특정 bucket 최소 권한이면 `aws s3 ls`가 실패해도 이상하지 않다. `ListAllMyBuckets`와 `ListBucket`을 구분한다.

## 삭제 검증

```bash
aws s3api list-buckets --query "Buckets[?contains(Name, 'example-11')].Name"
aws iam list-roles --query "Roles[?contains(RoleName, 'example-11')].RoleName"
```

---

# 12 — S3 Security & Recovery

## 구축 검증

```bash
aws s3api get-public-access-block --bucket <bucket-name>
aws s3api get-bucket-versioning --bucket <bucket-name>
aws s3api get-bucket-encryption --bucket <bucket-name>
aws s3api list-object-versions --bucket <bucket-name>
```

선택:

```bash
aws s3api get-bucket-policy --bucket <bucket-name> --query Policy --output text
aws s3api get-bucket-lifecycle-configuration --bucket <bucket-name>
aws s3api head-object --bucket <bucket-name> --key <object-key>
```

판단 포인트: Public Access Block, Versioning=Enabled, object versions/DeleteMarkers 확인, encryption 상태 확인.

## 삭제 검증

bucket이 보이는지:

```bash
aws s3api list-buckets --query "Buckets[?contains(Name, 'example-12')].Name"
```

삭제 전에는 반드시:

```bash
aws s3api list-object-versions --bucket <bucket-name>
```

`Versions`와 `DeleteMarkers`가 모두 비어 있어야 bucket 정리가 끝난 것이다.

---

# 13 — Route 53 + ACM + HTTPS

## 구축 검증

```bash
aws route53 list-hosted-zones \
  --query 'HostedZones[].{Name:Name,Id:Id,Private:Config.PrivateZone}' --output table
```

Hosted Zone ID:

```bash
export ZONE_ID=<hosted-zone-id>
aws route53 list-resource-record-sets --hosted-zone-id $ZONE_ID \
  --query 'ResourceRecordSets[].{Name:Name,Type:Type,Alias:AliasTarget.DNSName}' --output table
```

ACM:

```bash
aws acm list-certificates --region $AWS_REGION \
  --query 'CertificateSummaryList[].{Domain:DomainName,Arn:CertificateArn}' --output table
```

```bash
export CERT_ARN=<certificate-arn>
aws acm describe-certificate --region $AWS_REGION --certificate-arn $CERT_ARN \
  --query 'Certificate.{Domain:DomainName,Status:Status,SANs:SubjectAlternativeNames,InUseBy:InUseBy}'
```

ALB Listener:

```bash
export ALB_ARN=<alb-arn>
aws elbv2 describe-listeners --region $AWS_REGION --load-balancer-arn $ALB_ARN \
  --query 'Listeners[].{Port:Port,Protocol:Protocol,Certificates:Certificates[].CertificateArn,Actions:DefaultActions}'
```

실제 응답:

```bash
curl -I http://<domain>
curl -I https://<domain>
```

판단 포인트: Alias → ALB, ACM ISSUED, 443 Listener certificate 연결, HTTP → HTTPS redirect.

## 삭제 검증

```bash
aws elbv2 describe-load-balancers --region $AWS_REGION --query "LoadBalancers[?contains(LoadBalancerName, 'example-13')].LoadBalancerName"
aws acm list-certificates --region $AWS_REGION --query "CertificateSummaryList[?contains(DomainName, 'example')].[DomainName,CertificateArn]"
```

Hosted Zone은 의도적으로 유지하는 것인지 확인한다. 도메인 운영용 Hosted Zone을 무조건 삭제하지 않는다.

---

# 14 — CloudWatch Observability

## ASG Group Metric 활성화

```bash
aws autoscaling enable-metrics-collection \
  --region $AWS_REGION \
  --auto-scaling-group-name <asg-name> \
  --granularity 1Minute
```

활성화 확인:

```bash
aws autoscaling describe-auto-scaling-groups --region $AWS_REGION --auto-scaling-group-names <asg-name> \
  --query 'AutoScalingGroups[].EnabledMetrics'
```

CloudWatch metric 확인:

```bash
aws cloudwatch list-metrics --region $AWS_REGION --namespace AWS/ApplicationELB --query 'Metrics[].MetricName' --output text
aws cloudwatch list-metrics --region $AWS_REGION --namespace AWS/EC2 --metric-name CPUUtilization --query 'Metrics[].Dimensions'
aws cloudwatch list-metrics --region $AWS_REGION --namespace AWS/AutoScaling --query 'Metrics[].MetricName' --output text
aws cloudwatch list-metrics --region $AWS_REGION --namespace AWS/RDS --query 'Metrics[].MetricName' --output text
```

Alarm:

```bash
aws cloudwatch describe-alarms --region $AWS_REGION \
  --alarm-name-prefix example-14 \
  --query 'MetricAlarms[].{Name:AlarmName,State:StateValue,Metric:MetricName,Namespace:Namespace,Threshold:Threshold}' --output table
```

Log Group:

```bash
aws logs describe-log-groups --region $AWS_REGION --log-group-name-prefix example-14 \
  --query 'logGroups[].{Name:logGroupName,StoredBytes:storedBytes,Retention:retentionInDays}' --output table
```

판단 포인트: ASG EnabledMetrics 존재, ALB/EC2/ASG/RDS metric 조회 가능, Alarm 상태 변화, Log Group 확인.

## 삭제 검증

```bash
aws cloudwatch describe-alarms --region $AWS_REGION --alarm-name-prefix example-14 --query 'MetricAlarms[].AlarmName'
aws logs describe-log-groups --region $AWS_REGION --log-group-name-prefix example-14 --query 'logGroups[].logGroupName'
```

둘 다 필요 없다면 `[]`가 되어야 한다.

---

# 15 — Troubleshooting Web Stack

장애 전/중/복구 후 같은 명령을 반복 실행한다.

## ALB / Listener

```bash
aws elbv2 describe-load-balancers --region $AWS_REGION \
  --query "LoadBalancers[?contains(LoadBalancerName, 'example-15')].{Name:LoadBalancerName,State:State.Code,DNS:DNSName}"
```

```bash
export ALB_ARN=<alb-arn>
aws elbv2 describe-listeners --region $AWS_REGION --load-balancer-arn $ALB_ARN \
  --query 'Listeners[].{Port:Port,Protocol:Protocol,Actions:DefaultActions}'
```

## Target Group / Health

```bash
export TG_ARN=<target-group-arn>
aws elbv2 describe-target-health --region $AWS_REGION --target-group-arn $TG_ARN \
  --query 'TargetHealthDescriptions[].{Target:Target.Id,State:TargetHealth.State,Reason:TargetHealth.Reason,Description:TargetHealth.Description}' --output table
```

세 상태를 구분한다.

```text
A. Target 0개
B. 일부 unhealthy
C. 모든 등록 Target unhealthy
```

중요: `모든 Target unhealthy = 반드시 503`으로 해석하지 않는다. 모두 unhealthy일 때는 ALB fail-open 동작을 관찰한다.

## HTTP 결과 기록

```bash
curl -sS -o /dev/null -w '%{http_code}\n' http://<alb-or-domain>
curl -vkI https://<domain>
```

## ASG Activity

```bash
aws autoscaling describe-scaling-activities --region $AWS_REGION --auto-scaling-group-name <asg-name> --max-items 20 \
  --query 'Activities[].{Time:StartTime,Status:StatusCode,Cause:Cause,Description:Description}' --output table
```

## RDS

```bash
aws rds describe-db-instances --region $AWS_REGION \
  --query "DBInstances[?contains(DBInstanceIdentifier, 'example-15')].{Id:DBInstanceIdentifier,Status:DBInstanceStatus,Endpoint:Endpoint.Address,Public:PubliclyAccessible}"
```

## CloudWatch Alarm

```bash
aws cloudwatch describe-alarms --region $AWS_REGION --alarm-name-prefix example-15 \
  --query 'MetricAlarms[].{Name:AlarmName,State:StateValue,Reason:StateReason}' --output table
```

판단 방식:

```text
증상
→ HTTP status/timeout
→ Listener
→ 등록 Target 수
→ Target Health
→ SG/Route
→ EC2 app/bootstrap
→ RDS/IAM
→ Metric/Log
```

---

# 16 — Final Guided Architecture

## 전체 구축 검증

### Network

```bash
aws ec2 describe-vpcs --region $AWS_REGION --filters 'Name=tag:Example,Values=16' \
  --query 'Vpcs[].{Name:Tags[?Key==`Name`]|[0].Value,Id:VpcId,CIDR:CidrBlock}' --output table

aws ec2 describe-subnets --region $AWS_REGION --filters 'Name=tag:Example,Values=16' \
  --query 'Subnets[].{Name:Tags[?Key==`Name`]|[0].Value,Id:SubnetId,CIDR:CidrBlock,AZ:AvailabilityZone,PublicIP:MapPublicIpOnLaunch}' --output table
```

### EC2 / ALB / ASG

```bash
aws ec2 describe-instances --region $AWS_REGION \
  --filters 'Name=tag:Example,Values=16' 'Name=instance-state-name,Values=running' \
  --query 'Reservations[].Instances[].{Name:Tags[?Key==`Name`]|[0].Value,Id:InstanceId,PublicIP:PublicIpAddress,PrivateIP:PrivateIpAddress,AZ:Placement.AvailabilityZone,SG:SecurityGroups[].GroupId}' --output table

aws elbv2 describe-load-balancers --region $AWS_REGION \
  --query "LoadBalancers[?contains(LoadBalancerName, 'example-16')].{Name:LoadBalancerName,Scheme:Scheme,State:State.Code,DNS:DNSName,AZ:AvailabilityZones[].ZoneName}"

aws autoscaling describe-auto-scaling-groups --region $AWS_REGION \
  --auto-scaling-group-names example-16-asg \
  --query 'AutoScalingGroups[].{Min:MinSize,Desired:DesiredCapacity,Max:MaxSize,Subnets:VPCZoneIdentifier,Instances:Instances[].{Id:InstanceId,Health:HealthStatus,Lifecycle:LifecycleState},Metrics:EnabledMetrics}'
```

### RDS

```bash
aws rds describe-db-instances --region $AWS_REGION \
  --query "DBInstances[?contains(DBInstanceIdentifier, 'example-16')].{Id:DBInstanceIdentifier,Status:DBInstanceStatus,Public:PubliclyAccessible,MultiAZ:MultiAZ,Endpoint:Endpoint.Address,Subnets:DBSubnetGroup.Subnets[].SubnetIdentifier}"
```

### S3

```bash
aws s3api get-public-access-block --bucket <bucket-name>
aws s3api get-bucket-versioning --bucket <bucket-name>
aws s3api get-bucket-encryption --bucket <bucket-name>
```

### Route 53 / HTTPS

```bash
curl -I http://<domain>
curl -I https://<domain>
```

### CloudWatch

```bash
aws cloudwatch describe-alarms --region $AWS_REGION --alarm-name-prefix example-16 \
  --query 'MetricAlarms[].{Name:AlarmName,State:StateValue,Metric:MetricName}' --output table
```

판단 포인트: 2AZ, public ALB, private EC2, ASG >=2, private RDS, S3 private/versioned, HTTPS 정상, ASG group metrics, Alarm 존재.

---

# 전체 잔존 리소스 검사

모든 Example 종료 후 실행한다. 아래 결과는 **의도적으로 유지한 리소스 외에는 비어 있어야 한다.**

## EC2

```bash
aws ec2 describe-instances --region $AWS_REGION \
  --filters 'Name=tag:Project,Values=cloud-lab' 'Name=tag:Stage,Values=examples' \
  'Name=instance-state-name,Values=pending,running,stopping,stopped' \
  --query 'Reservations[].Instances[].{Id:InstanceId,Name:Tags[?Key==`Name`]|[0].Value,Example:Tags[?Key==`Example`]|[0].Value,State:State.Name}' --output table
```

## EBS

```bash
aws ec2 describe-volumes --region $AWS_REGION \
  --filters 'Name=tag:Project,Values=cloud-lab' 'Name=tag:Stage,Values=examples' \
  --query 'Volumes[].{Id:VolumeId,State:State,Size:Size,Name:Tags[?Key==`Name`]|[0].Value}' --output table
```

## Elastic IP

```bash
aws ec2 describe-addresses --region $AWS_REGION \
  --query "Addresses[?Tags[?Key=='Project' && Value=='cloud-lab'] && Tags[?Key=='Stage' && Value=='examples']].{PublicIp:PublicIp,AllocationId:AllocationId,AssociationId:AssociationId}"
```

## NAT Gateway

```bash
aws ec2 describe-nat-gateways --region $AWS_REGION \
  --filter 'Name=tag:Project,Values=cloud-lab' 'Name=tag:Stage,Values=examples' 'Name=state,Values=pending,available,deleting,failed' \
  --query 'NatGateways[].{Id:NatGatewayId,State:State,Subnet:SubnetId}' --output table
```

## ALB

```bash
aws elbv2 describe-load-balancers --region $AWS_REGION \
  --query "LoadBalancers[?starts_with(LoadBalancerName, 'example-')].[LoadBalancerName,State.Code]" --output table
```

## Target Group

```bash
aws elbv2 describe-target-groups --region $AWS_REGION \
  --query "TargetGroups[?starts_with(TargetGroupName, 'example-')].[TargetGroupName,TargetGroupArn]" --output table
```

## ASG

```bash
aws autoscaling describe-auto-scaling-groups --region $AWS_REGION \
  --query "AutoScalingGroups[?starts_with(AutoScalingGroupName, 'example-')].[AutoScalingGroupName,DesiredCapacity]" --output table
```

## Launch Template

```bash
aws ec2 describe-launch-templates --region $AWS_REGION \
  --query "LaunchTemplates[?starts_with(LaunchTemplateName, 'example-')].[LaunchTemplateName,LaunchTemplateId]" --output table
```

## RDS

```bash
aws rds describe-db-instances --region $AWS_REGION \
  --query "DBInstances[?starts_with(DBInstanceIdentifier, 'example-')].[DBInstanceIdentifier,DBInstanceStatus]" --output table
```

## RDS Manual Snapshot

```bash
aws rds describe-db-snapshots --region $AWS_REGION --snapshot-type manual \
  --query "DBSnapshots[?starts_with(DBSnapshotIdentifier, 'example-')].[DBSnapshotIdentifier,Status,AllocatedStorage]" --output table
```

## S3 Buckets

```bash
aws s3api list-buckets --query "Buckets[?starts_with(Name, 'example-')].Name"
```

남은 bucket이 있다면 반드시 version/delete marker까지 확인한다.

```bash
aws s3api list-object-versions --bucket <bucket-name>
```

## CloudWatch Alarm

```bash
aws cloudwatch describe-alarms --region $AWS_REGION \
  --query "MetricAlarms[?starts_with(AlarmName, 'example-')].[AlarmName,StateValue]" --output table
```

## CloudWatch Log Group

```bash
aws logs describe-log-groups --region $AWS_REGION \
  --query "logGroups[?starts_with(logGroupName, 'example-')].[logGroupName,storedBytes]" --output table
```

## Route 53

```bash
aws route53 list-hosted-zones --query 'HostedZones[].{Name:Name,Id:Id,Private:Config.PrivateZone}' --output table
```

Route 53은 실제 운영 도메인의 Hosted Zone일 수 있으므로 자동으로 "남았다 = 삭제"로 판단하지 않는다. 의도적으로 유지하는지 확인한다.

---

# ChatGPT에 검증을 요청할 때

아래 형식으로 붙여넣는다.

```text
Example 08 구축 검증 요청

목표:
- ALB + ASG 2대
- Target Tracking CPU 25%
- replacement 및 scale-out 확인

<describe-auto-scaling-groups 출력>
<describe-scaling-activities 출력>
<describe-policies 출력>
<describe-target-health 출력>

판단해줘:
1. 요구사항대로 구축됐는지
2. 이상한 설정이 있는지
3. 장애 실험 결과가 기대한 동작인지
```

삭제 후에는:

```text
Example 08 삭제 검증 요청

<ASG 출력>
<EC2 출력>
<ALB 출력>
<TG 출력>
<NAT/EIP 출력>

과금될 만한 리소스가 남았는지 판단해줘.
```

CLI 출력만으로 확정할 수 없는 항목이 있으면 추가 명령을 요청받은 뒤 확인한다. **추측으로 "완전히 삭제됐다"고 판정하지 않는다.**
