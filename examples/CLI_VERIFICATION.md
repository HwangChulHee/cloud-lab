# AWS CLI Verification & Cleanup Guide

각 Example은 콘솔에서 구축한 뒤 **AWS CLI 출력으로 구조를 검증**하고, 종료 후 **잔존 리소스가 없는지 다시 검증**한다.

목표는 단순히 `됐다/안 됐다`를 보는 것이 아니라, CLI 출력만 보고도 다음을 판단할 수 있게 하는 것이다.

```text
구축 결과
→ CLI로 상태/연결 관계 출력
→ 출력 내용을 ChatGPT에 붙여넣기
→ 구조가 요구사항에 맞는지 검토
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

가능하면 리소스 이름을 `example-NN-*` 형식으로 만든다. 예: `example-05-vpc`, `example-07-asg`.

CLI 출력은 비밀값을 포함하지 않는 범위에서 그대로 붙여넣으면 된다. Access Key, Secret Key, DB 비밀번호, presigned URL 전체 값은 공유하지 않는다.

---

## 01 — Single EC2 Web

### 구축 검증

```bash
aws ec2 describe-instances \
  --region $AWS_REGION \
  --filters 'Name=tag:Name,Values=example-01-*' 'Name=instance-state-name,Values=pending,running,stopping,stopped' \
  --query 'Reservations[].Instances[].{Id:InstanceId,State:State.Name,PublicIP:PublicIpAddress,PrivateIP:PrivateIpAddress,Subnet:SubnetId,Vpc:VpcId,SG:SecurityGroups[].GroupId}' \
  --output table
```

```bash
aws ec2 describe-security-groups \
  --region $AWS_REGION \
  --filters 'Name=tag:Name,Values=example-01-*' \
  --query 'SecurityGroups[].{Name:GroupName,Id:GroupId,Ingress:IpPermissions}'
```

판단 포인트: EC2가 running, Public/Private IP 존재, HTTP 80 inbound 존재.

### 삭제 검증

```bash
aws ec2 describe-instances --region $AWS_REGION --filters 'Name=tag:Name,Values=example-01-*' 'Name=instance-state-name,Values=pending,running,stopping,stopped' --query 'Reservations[].Instances[].InstanceId'
aws ec2 describe-volumes --region $AWS_REGION --filters 'Name=tag:Name,Values=example-01-*' --query 'Volumes[].{Id:VolumeId,State:State}'
```

둘 다 `[]`이면 주요 과금 리소스가 남지 않은 상태다.

---

## 02 — ALB + Two EC2

### 구축 검증

```bash
aws ec2 describe-instances --region $AWS_REGION --filters 'Name=tag:Name,Values=example-02-*' 'Name=instance-state-name,Values=running' --query 'Reservations[].Instances[].{Id:InstanceId,AZ:Placement.AvailabilityZone,PrivateIP:PrivateIpAddress}' --output table
aws elbv2 describe-load-balancers --region $AWS_REGION --names example-02-alb --query 'LoadBalancers[].{DNS:DNSName,State:State.Code,Scheme:Scheme,Vpc:VpcId,AZs:AvailabilityZones[].ZoneName}'
aws elbv2 describe-target-groups --region $AWS_REGION --names example-02-tg --query 'TargetGroups[].{Arn:TargetGroupArn,Protocol:Protocol,Port:Port,Vpc:VpcId,HealthPath:HealthCheckPath}'
```

Target Group ARN을 넣는다.

```bash
export TG_ARN=<target-group-arn>
aws elbv2 describe-target-health --region $AWS_REGION --target-group-arn $TG_ARN --query 'TargetHealthDescriptions[].{Target:Target.Id,State:TargetHealth.State,Reason:TargetHealth.Reason}' --output table
```

판단 포인트: EC2 2대, 가능하면 서로 다른 AZ, ALB active, Target 2개 healthy.

### 삭제 검증

```bash
aws elbv2 describe-load-balancers --region $AWS_REGION --query "LoadBalancers[?contains(LoadBalancerName, 'example-02')].[LoadBalancerName,State.Code]"
aws elbv2 describe-target-groups --region $AWS_REGION --query "TargetGroups[?contains(TargetGroupName, 'example-02')].TargetGroupName"
aws ec2 describe-instances --region $AWS_REGION --filters 'Name=tag:Name,Values=example-02-*' 'Name=instance-state-name,Values=pending,running,stopping,stopped' --query 'Reservations[].Instances[].InstanceId'
```

---

## 03 — ALB Health Check

### 구축/장애 검증

```bash
export TG_ARN=<target-group-arn>
aws elbv2 describe-target-groups --region $AWS_REGION --target-group-arns $TG_ARN --query 'TargetGroups[].{Path:HealthCheckPath,Interval:HealthCheckIntervalSeconds,Timeout:HealthCheckTimeoutSeconds,Healthy:HealthyThresholdCount,Unhealthy:UnhealthyThresholdCount,Matcher:Matcher.HttpCode}'
aws elbv2 describe-target-health --region $AWS_REGION --target-group-arn $TG_ARN --query 'TargetHealthDescriptions[].{Target:Target.Id,State:TargetHealth.State,Reason:TargetHealth.Reason,Description:TargetHealth.Description}' --output table
```

판단 포인트: 정상 시 healthy, nginx 중지/잘못된 health path에서는 해당 target이 unhealthy, 복구 후 다시 healthy.

### 삭제 검증

Example 02와 동일한 ALB/TG/EC2 검증을 사용한다.

---

## 04 — Security Group Layering

### 구축 검증

```bash
aws ec2 describe-security-groups --region $AWS_REGION \
  --filters 'Name=tag:Name,Values=example-04-*' \
  --query 'SecurityGroups[].{Name:GroupName,Id:GroupId,Ingress:IpPermissions}'
```

필요하면 SG ID를 직접 지정해 더 자세히 본다.

```bash
aws ec2 describe-security-groups --region $AWS_REGION --group-ids <alb-sg-id> <ec2-sg-id>
```

판단 포인트: ALB-SG는 80/443을 클라이언트에 허용하고, EC2-SG의 HTTP source는 `0.0.0.0/0`가 아니라 ALB-SG ID여야 한다.

### 삭제 검증

```bash
aws ec2 describe-security-groups --region $AWS_REGION --filters 'Name=tag:Name,Values=example-04-*' --query 'SecurityGroups[].{Id:GroupId,Name:GroupName}'
```

---

## 05 — VPC Public / Private Subnets

### 구축 검증

```bash
export VPC_ID=$(aws ec2 describe-vpcs --region $AWS_REGION --filters 'Name=tag:Name,Values=example-05-vpc' --query 'Vpcs[0].VpcId' --output text)
echo $VPC_ID

aws ec2 describe-subnets --region $AWS_REGION --filters "Name=vpc-id,Values=$VPC_ID" --query 'Subnets[].{Name:Tags[?Key==`Name`]|[0].Value,Id:SubnetId,CIDR:CidrBlock,AZ:AvailabilityZone,PublicIP:MapPublicIpOnLaunch}' --output table
aws ec2 describe-route-tables --region $AWS_REGION --filters "Name=vpc-id,Values=$VPC_ID" --query 'RouteTables[].{Name:Tags[?Key==`Name`]|[0].Value,Id:RouteTableId,Routes:Routes,Associations:Associations[].SubnetId}'
aws ec2 describe-internet-gateways --region $AWS_REGION --filters "Name=attachment.vpc-id,Values=$VPC_ID" --query 'InternetGateways[].{Id:InternetGatewayId,Attachments:Attachments}'
```

판단 포인트: 4개 subnet, CIDR 비중복, 2AZ, public route table에 `0.0.0.0/0 → igw-*`, private 쪽에는 해당 route 없음.

### 삭제 검증

```bash
aws ec2 describe-vpcs --region $AWS_REGION --filters 'Name=tag:Name,Values=example-05-vpc' --query 'Vpcs[].VpcId'
aws ec2 describe-internet-gateways --region $AWS_REGION --filters 'Name=tag:Name,Values=example-05-*' --query 'InternetGateways[].InternetGatewayId'
aws ec2 describe-nat-gateways --region $AWS_REGION --filter 'Name=tag:Name,Values=example-05-*' 'Name=state,Values=pending,available,deleting,failed' --query 'NatGateways[].{Id:NatGatewayId,State:State}'
```

---

## 06 — Private EC2 Access

### 구축 검증

```bash
aws ec2 describe-instances --region $AWS_REGION --filters 'Name=tag:Name,Values=example-06-*' 'Name=instance-state-name,Values=running' --query 'Reservations[].Instances[].{Name:Tags[?Key==`Name`]|[0].Value,Id:InstanceId,PublicIP:PublicIpAddress,PrivateIP:PrivateIpAddress,Subnet:SubnetId,IamProfile:IamInstanceProfile.Arn}' --output table
aws ec2 describe-nat-gateways --region $AWS_REGION --filter 'Name=state,Values=available,pending' --query 'NatGateways[].{Id:NatGatewayId,Subnet:SubnetId,State:State}' --output table
aws ssm describe-instance-information --region $AWS_REGION --query 'InstanceInformationList[].{Instance:InstanceId,Ping:PingStatus,Agent:AgentVersion}' --output table
```

판단 포인트: private EC2는 Public IP가 없어야 하고, ALB를 통한 서비스 접근은 가능해야 한다. SSM을 사용하는 경우 PingStatus가 Online.

### 삭제 검증

```bash
aws ec2 describe-nat-gateways --region $AWS_REGION --filter 'Name=tag:Name,Values=example-06-*' 'Name=state,Values=pending,available,deleting,failed' --query 'NatGateways[].{Id:NatGatewayId,State:State}'
aws ec2 describe-addresses --region $AWS_REGION --query "Addresses[?Tags[?Key=='Name' && contains(Value, 'example-06')]].{AllocationId:AllocationId,PublicIp:PublicIp}"
```

NAT Gateway와 연결용 Elastic IP가 특히 남지 않았는지 확인한다.

---

## 07 — ALB + Auto Scaling Group

### 구축 검증

```bash
aws autoscaling describe-auto-scaling-groups --region $AWS_REGION --auto-scaling-group-names example-07-asg --query 'AutoScalingGroups[].{Min:MinSize,Desired:DesiredCapacity,Max:MaxSize,Instances:Instances[].{Id:InstanceId,AZ:AvailabilityZone,Health:HealthStatus,Lifecycle:LifecycleState},TG:TargetGroupARNs}'
aws ec2 describe-launch-templates --region $AWS_REGION --launch-template-names example-07-lt --query 'LaunchTemplates[].{Id:LaunchTemplateId,Latest:LatestVersionNumber,Default:DefaultVersionNumber}'
```

Target Group health도 02와 같은 명령으로 확인한다.

판단 포인트: ASG Desired 수만큼 EC2 존재, InService/Healthy, Target Group과 연결.

### 삭제 검증

```bash
aws autoscaling describe-auto-scaling-groups --region $AWS_REGION --auto-scaling-group-names example-07-asg --query 'AutoScalingGroups[].AutoScalingGroupName'
aws ec2 describe-launch-templates --region $AWS_REGION --filters 'Name=launch-template-name,Values=example-07-*' --query 'LaunchTemplates[].LaunchTemplateName'
```

---

## 08 — Scaling & Recovery

### 구축/장애 검증

```bash
aws autoscaling describe-auto-scaling-groups --region $AWS_REGION --auto-scaling-group-names example-08-asg --query 'AutoScalingGroups[].{Desired:DesiredCapacity,Min:MinSize,Max:MaxSize,Instances:Instances[].{Id:InstanceId,Health:HealthStatus,Lifecycle:LifecycleState}}'
aws autoscaling describe-scaling-activities --region $AWS_REGION --auto-scaling-group-name example-08-asg --max-items 10 --query 'Activities[].{Time:StartTime,Status:StatusCode,Cause:Cause,Description:Description}' --output table
aws autoscaling describe-policies --region $AWS_REGION --auto-scaling-group-name example-08-asg --query 'ScalingPolicies[].{Name:PolicyName,Type:PolicyType,Target:TargetTrackingConfiguration.TargetValue}'
```

판단 포인트: 인스턴스 terminate 후 새 인스턴스가 생성된 활동 기록, 부하 실험 후 DesiredCapacity 변화 및 scaling activity 존재.

### 삭제 검증

ASG/Launch Template/ALB/TG/EC2가 모두 비어 있는지 02와 07 명령을 함께 실행한다.

---

## 09 — Private RDS

### 구축 검증

```bash
aws rds describe-db-instances --region $AWS_REGION --query "DBInstances[?contains(DBInstanceIdentifier, 'example-09')].{Id:DBInstanceIdentifier,Status:DBInstanceStatus,Public:PubliclyAccessible,MultiAZ:MultiAZ,Endpoint:Endpoint.Address,Port:Endpoint.Port,Vpc:DBSubnetGroup.VpcId,Subnets:DBSubnetGroup.Subnets[].SubnetIdentifier,SG:VpcSecurityGroups[].VpcSecurityGroupId}" --output json
```

```bash
aws ec2 describe-security-groups --region $AWS_REGION --group-ids <rds-sg-id> --query 'SecurityGroups[].IpPermissions'
```

판단 포인트: RDS `available`, `PubliclyAccessible=false`, DB Subnet Group에 private subnet 2개 이상, DB port source가 EC2-SG.

### 삭제 검증

```bash
aws rds describe-db-instances --region $AWS_REGION --query "DBInstances[?contains(DBInstanceIdentifier, 'example-09')].[DBInstanceIdentifier,DBInstanceStatus]"
aws rds describe-db-snapshots --region $AWS_REGION --snapshot-type manual --query "DBSnapshots[?contains(DBSnapshotIdentifier, 'example-09')].[DBSnapshotIdentifier,Status]"
```

---

## 10 — RDS Failure & Recovery

### 구축/복구 검증

```bash
aws rds describe-db-instances --region $AWS_REGION --query "DBInstances[?contains(DBInstanceIdentifier, 'example-10')].{Id:DBInstanceIdentifier,Status:DBInstanceStatus,MultiAZ:MultiAZ,AZ:AvailabilityZone,SecondaryAZ:SecondaryAvailabilityZone,ReplicaSource:ReadReplicaSourceDBInstanceIdentifier,ReadReplicas:ReadReplicaDBInstanceIdentifiers,BackupRetention:BackupRetentionPeriod}"
aws rds describe-events --region $AWS_REGION --source-type db-instance --duration 180 --query 'Events[].{Time:Date,Source:SourceIdentifier,Message:Message}' --output table
```

판단 포인트: Multi-AZ 여부, replica 관계, backup retention, failover 관련 이벤트를 시간순으로 설명할 수 있어야 한다.

### 삭제 검증

```bash
aws rds describe-db-instances --region $AWS_REGION --query "DBInstances[?contains(DBInstanceIdentifier, 'example-10')].[DBInstanceIdentifier,DBInstanceStatus]"
aws rds describe-db-snapshots --region $AWS_REGION --snapshot-type manual --query "DBSnapshots[?contains(DBSnapshotIdentifier, 'example-10')].[DBSnapshotIdentifier,Status]"
```

---

## 11 — S3 + IAM Role

### 구축 검증

```bash
aws s3api get-bucket-location --bucket <bucket-name>
aws s3api get-public-access-block --bucket <bucket-name>
aws iam get-role --role-name <role-name> --query 'Role.{Name:RoleName,Arn:Arn,Trust:AssumeRolePolicyDocument}'
aws iam list-attached-role-policies --role-name <role-name>
aws iam list-role-policies --role-name <role-name>
```

EC2에서 실행:

```bash
aws sts get-caller-identity
aws s3 ls s3://<bucket-name>
echo hello > /tmp/hello.txt
aws s3 cp /tmp/hello.txt s3://<bucket-name>/verification/hello.txt
aws s3 cp s3://<bucket-name>/verification/hello.txt -
```

판단 포인트: EC2가 long-lived access key 없이 IAM Role 자격증명으로 S3에 접근.

### 삭제 검증

```bash
aws s3api list-buckets --query "Buckets[?contains(Name, 'example-11')].Name"
aws iam list-roles --query "Roles[?contains(RoleName, 'example-11')].RoleName"
aws iam list-instance-profiles --query "InstanceProfiles[?contains(InstanceProfileName, 'example-11')].InstanceProfileName"
```

---

## 12 — S3 Security & Recovery

### 구축 검증

```bash
aws s3api get-bucket-versioning --bucket <bucket-name>
aws s3api get-public-access-block --bucket <bucket-name>
aws s3api get-bucket-encryption --bucket <bucket-name>
aws s3api get-bucket-lifecycle-configuration --bucket <bucket-name>
aws s3api list-object-versions --bucket <bucket-name> --max-items 20
```

판단 포인트: Versioning Enabled, Public Access Block 활성화, encryption/lifecycle 요구사항 확인, 삭제한 객체의 delete marker/이전 version 관찰 가능.

### 삭제 검증

Versioned bucket은 모든 version과 delete marker를 지워야 bucket 삭제가 가능하다.

```bash
aws s3api list-object-versions --bucket <bucket-name> --query '{Versions:Versions[].{Key:Key,VersionId:VersionId},DeleteMarkers:DeleteMarkers[].{Key:Key,VersionId:VersionId}}'
aws s3api list-buckets --query "Buckets[?contains(Name, 'example-12')].Name"
```

---

## 13 — Route 53 + ACM + HTTPS

### 구축 검증

```bash
aws route53 list-hosted-zones --query 'HostedZones[].{Name:Name,Id:Id,Private:Config.PrivateZone}' --output table
aws route53 list-resource-record-sets --hosted-zone-id <hosted-zone-id> --query 'ResourceRecordSets[].{Name:Name,Type:Type,Alias:AliasTarget.DNSName,Values:ResourceRecords[].Value}' --output table
aws acm list-certificates --region $AWS_REGION --query 'CertificateSummaryList[].{Domain:DomainName,Arn:CertificateArn}' --output table
aws acm describe-certificate --region $AWS_REGION --certificate-arn <certificate-arn> --query 'Certificate.{Domain:DomainName,Status:Status,InUseBy:InUseBy}'
aws elbv2 describe-listeners --region $AWS_REGION --load-balancer-arn <alb-arn> --query 'Listeners[].{Port:Port,Protocol:Protocol,Certificates:Certificates[].CertificateArn,Actions:DefaultActions[].Type}'
```

외부 확인:

```bash
curl -I http://<domain>
curl -I https://<domain>
```

판단 포인트: DNS alias가 ALB를 가리키고 ACM certificate `ISSUED`, ALB 443 listener가 certificate 사용, HTTP→HTTPS redirect가 의도대로 동작.

### 삭제 검증

```bash
aws elbv2 describe-load-balancers --region $AWS_REGION --query "LoadBalancers[?contains(LoadBalancerName, 'example-13')].LoadBalancerName"
aws acm list-certificates --region $AWS_REGION --query "CertificateSummaryList[?contains(DomainName, '<domain-fragment>')].[DomainName,CertificateArn]"
aws route53 list-hosted-zones --query "HostedZones[?contains(Name, '<domain-fragment>')].[Name,Id]"
```

Hosted Zone/인증서는 다른 용도로 계속 사용할 경우 삭제하지 않는다.

---

## 14 — CloudWatch Observability

### 구축 검증

```bash
aws cloudwatch describe-alarms --region $AWS_REGION --query "MetricAlarms[?contains(AlarmName, 'example-14')].{Name:AlarmName,State:StateValue,Metric:MetricName,Namespace:Namespace,Threshold:Threshold,Comparison:ComparisonOperator}" --output table
aws logs describe-log-groups --region $AWS_REGION --log-group-name-prefix example-14 --query 'logGroups[].{Name:logGroupName,Retention:retentionInDays,Bytes:storedBytes}' --output table
aws cloudwatch list-metrics --region $AWS_REGION --namespace AWS/EC2 --metric-name CPUUtilization --max-items 20
```

판단 포인트: Alarm이 의도한 metric/namespace/dimension에 연결되고 로그가 실제 수집되는지 확인.

### 삭제 검증

```bash
aws cloudwatch describe-alarms --region $AWS_REGION --query "MetricAlarms[?contains(AlarmName, 'example-14')].AlarmName"
aws logs describe-log-groups --region $AWS_REGION --log-group-name-prefix example-14 --query 'logGroups[].logGroupName'
```

---

## 15 — Troubleshooting Web Stack

이 단계에서는 명령 하나로 정답을 찾지 않는다. 증상에 따라 아래 순서로 출력한다.

```bash
# 1. ALB 상태
aws elbv2 describe-load-balancers --region $AWS_REGION --names <alb-name>

# 2. Target 상태
aws elbv2 describe-target-health --region $AWS_REGION --target-group-arn <tg-arn>

# 3. EC2 상태/네트워크
aws ec2 describe-instances --region $AWS_REGION --instance-ids <instance-id>

# 4. SG
aws ec2 describe-security-groups --region $AWS_REGION --group-ids <sg-id-1> <sg-id-2>

# 5. Route
aws ec2 describe-route-tables --region $AWS_REGION --filters Name=vpc-id,Values=<vpc-id>

# 6. RDS
aws rds describe-db-instances --region $AWS_REGION --db-instance-identifier <db-id>

# 7. ASG 활동
aws autoscaling describe-scaling-activities --region $AWS_REGION --auto-scaling-group-name <asg-name> --max-items 10

# 8. Alarm
aws cloudwatch describe-alarms --region $AWS_REGION
```

이 출력을 증상 설명과 함께 붙여넣으면 트래픽 경로를 따라 원인을 같이 좁힐 수 있다.

### 삭제 검증

16의 최종 잔존 리소스 검사를 사용한다.

---

## 16 — Final Guided Architecture

### 전체 구축 검증

```bash
aws ec2 describe-vpcs --region $AWS_REGION --filters 'Name=tag:Name,Values=example-16-*' --query 'Vpcs[].{Name:Tags[?Key==`Name`]|[0].Value,Id:VpcId,CIDR:CidrBlock}'
aws ec2 describe-subnets --region $AWS_REGION --filters 'Name=tag:Name,Values=example-16-*' --query 'Subnets[].{Name:Tags[?Key==`Name`]|[0].Value,Id:SubnetId,CIDR:CidrBlock,AZ:AvailabilityZone}' --output table
aws elbv2 describe-load-balancers --region $AWS_REGION --query "LoadBalancers[?contains(LoadBalancerName, 'example-16')].{Name:LoadBalancerName,State:State.Code,DNS:DNSName,AZs:AvailabilityZones[].ZoneName}"
aws autoscaling describe-auto-scaling-groups --region $AWS_REGION --query "AutoScalingGroups[?contains(AutoScalingGroupName, 'example-16')].{Name:AutoScalingGroupName,Min:MinSize,Desired:DesiredCapacity,Max:MaxSize,Instances:Instances[].InstanceId}"
aws rds describe-db-instances --region $AWS_REGION --query "DBInstances[?contains(DBInstanceIdentifier, 'example-16')].{Id:DBInstanceIdentifier,Status:DBInstanceStatus,Public:PubliclyAccessible,MultiAZ:MultiAZ}"
aws cloudwatch describe-alarms --region $AWS_REGION --query "MetricAlarms[?contains(AlarmName, 'example-16')].[AlarmName,StateValue]"
```

S3/Route53/IAM은 실제 사용한 이름을 넣어 11~13 명령으로 추가 확인한다.

### 최종 잔존 리소스 검사

실습 종료 후 아래 결과를 한 번에 복사해 붙여넣는다.

```bash
echo '=== EC2 ==='
aws ec2 describe-instances --region $AWS_REGION --filters 'Name=tag:Name,Values=example-*' 'Name=instance-state-name,Values=pending,running,stopping,stopped' --query 'Reservations[].Instances[].{Name:Tags[?Key==`Name`]|[0].Value,Id:InstanceId,State:State.Name}' --output table

echo '=== ALB/NLB ==='
aws elbv2 describe-load-balancers --region $AWS_REGION --query "LoadBalancers[?starts_with(LoadBalancerName, 'example-')].[LoadBalancerName,State.Code]" --output table

echo '=== Target Groups ==='
aws elbv2 describe-target-groups --region $AWS_REGION --query "TargetGroups[?starts_with(TargetGroupName, 'example-')].TargetGroupName" --output table

echo '=== ASG ==='
aws autoscaling describe-auto-scaling-groups --region $AWS_REGION --query "AutoScalingGroups[?starts_with(AutoScalingGroupName, 'example-')].[AutoScalingGroupName,DesiredCapacity]" --output table

echo '=== Launch Templates ==='
aws ec2 describe-launch-templates --region $AWS_REGION --query "LaunchTemplates[?starts_with(LaunchTemplateName, 'example-')].LaunchTemplateName" --output table

echo '=== RDS ==='
aws rds describe-db-instances --region $AWS_REGION --query "DBInstances[?starts_with(DBInstanceIdentifier, 'example-')].[DBInstanceIdentifier,DBInstanceStatus]" --output table

echo '=== Manual RDS Snapshots ==='
aws rds describe-db-snapshots --region $AWS_REGION --snapshot-type manual --query "DBSnapshots[?starts_with(DBSnapshotIdentifier, 'example-')].[DBSnapshotIdentifier,Status]" --output table

echo '=== NAT Gateways ==='
aws ec2 describe-nat-gateways --region $AWS_REGION --filter 'Name=state,Values=pending,available,deleting,failed' --query "NatGateways[?Tags[?Key=='Name' && starts_with(Value, 'example-')]].[NatGatewayId,State]" --output table

echo '=== Elastic IPs ==='
aws ec2 describe-addresses --region $AWS_REGION --query "Addresses[?Tags[?Key=='Name' && starts_with(Value, 'example-')]].[AllocationId,PublicIp]" --output table

echo '=== EBS Volumes ==='
aws ec2 describe-volumes --region $AWS_REGION --filters 'Name=tag:Name,Values=example-*' --query 'Volumes[].{Id:VolumeId,State:State,Size:Size}' --output table

echo '=== CloudWatch Alarms ==='
aws cloudwatch describe-alarms --region $AWS_REGION --query "MetricAlarms[?starts_with(AlarmName, 'example-')].AlarmName" --output table

echo '=== Log Groups ==='
aws logs describe-log-groups --region $AWS_REGION --query "logGroups[?starts_with(logGroupName, 'example-')].[logGroupName,storedBytes]" --output table

echo '=== S3 Buckets ==='
aws s3api list-buckets --query "Buckets[?starts_with(Name, 'example-')].Name" --output table
```

모든 섹션이 비어 있으면 핵심 실습 리소스는 대부분 정리된 상태다. 단, Route 53 Hosted Zone, ACM 인증서, IAM Role/Policy, Security Group, VPC Endpoint 등은 이름/사용 목적에 따라 별도 확인한다.

## 나에게 검토 요청할 때

다음 형태로 보내면 된다.

```text
Example 09 완료.
아래는 구축 검증 CLI 출력이야.
<출력 붙여넣기>

이 구조가 README 요구사항을 만족하는지 봐줘.
```

또는:

```text
Example 09 리소스 삭제했어.
아래는 삭제 검증 CLI 출력이야.
<출력 붙여넣기>

과금될 만한 리소스가 남아 있는지 봐줘.
```

CLI 출력만으로 확정하기 어려운 부분이 있으면 어떤 추가 명령이 필요한지 이어서 확인한다.
