# Advanced Examples — AWS CLI Verification & Cleanup

Optional/Advanced Example 전용 CLI 검증 문서다.

```bash
export AWS_REGION=ap-northeast-2
aws sts get-caller-identity
```

> 출력에 Access Key, Secret Key, 비밀번호 같은 민감정보를 포함하지 않는다.

---

# A01 — PrivateLink Service Access

## 1. 두 VPC 확인

```bash
aws ec2 describe-vpcs --region $AWS_REGION \
  --filters 'Name=tag:Project,Values=cloud-lab' \
            'Name=tag:Stage,Values=examples-advanced' \
            'Name=tag:Example,Values=A01' \
  --query 'Vpcs[].{Name:Tags[?Key==`Name`]|[0].Value,Id:VpcId,CIDR:CidrBlock,State:State}' \
  --output table
```

판단 포인트:

```text
Provider = 10.1.0.0/16
Consumer = 10.2.0.0/16
```

ID를 기록한다.

```bash
export PROVIDER_VPC_ID=<provider-vpc-id>
export CONSUMER_VPC_ID=<consumer-vpc-id>
```

## 2. VPC Peering이 없는지 확인

Provider가 requester인 경우:

```bash
aws ec2 describe-vpc-peering-connections --region $AWS_REGION \
  --filters "Name=requester-vpc-info.vpc-id,Values=$PROVIDER_VPC_ID" \
  --query 'VpcPeeringConnections[].{Id:VpcPeeringConnectionId,Requester:RequesterVpcInfo.VpcId,Accepter:AccepterVpcInfo.VpcId,Status:Status.Code}' \
  --output table
```

Provider가 accepter인 경우도 확인한다.

```bash
aws ec2 describe-vpc-peering-connections --region $AWS_REGION \
  --filters "Name=accepter-vpc-info.vpc-id,Values=$PROVIDER_VPC_ID" \
  --query 'VpcPeeringConnections[].{Id:VpcPeeringConnectionId,Requester:RequesterVpcInfo.VpcId,Accepter:AccepterVpcInfo.VpcId,Status:Status.Code}' \
  --output table
```

A01용 두 VPC 사이 Peering이 없어야 한다.

## 3. Consumer Route Table 확인

```bash
aws ec2 describe-route-tables --region $AWS_REGION \
  --filters "Name=vpc-id,Values=$CONSUMER_VPC_ID" \
  --query 'RouteTables[].{Name:Tags[?Key==`Name`]|[0].Value,Id:RouteTableId,Routes:Routes[].{Destination:DestinationCidrBlock,Gateway:GatewayId,Nat:NatGatewayId,Peering:VpcPeeringConnectionId,TGW:TransitGatewayId},Subnets:Associations[].SubnetId}' \
  --output json
```

판단 포인트:

```text
10.1.0.0/16 → Peering/TGW/VPN 같은 Provider route가 없어야 함
```

## 4. Provider NLB 확인

```bash
aws elbv2 describe-load-balancers --region $AWS_REGION \
  --names advanced-a01-nlb \
  --query 'LoadBalancers[].{Name:LoadBalancerName,Scheme:Scheme,Type:Type,State:State.Code,Vpc:VpcId,DNS:DNSName,AZs:AvailabilityZones[].ZoneName}' \
  --output table
```

판단 포인트:

```text
Scheme = internal
Type   = network
Vpc    = Provider VPC
```

Target Group:

```bash
export TG_ARN=$(aws elbv2 describe-target-groups --region $AWS_REGION \
  --names advanced-a01-tg \
  --query 'TargetGroups[0].TargetGroupArn' --output text)

aws elbv2 describe-target-health --region $AWS_REGION \
  --target-group-arn $TG_ARN \
  --query 'TargetHealthDescriptions[].{Target:Target.Id,Port:Target.Port,State:TargetHealth.State,Reason:TargetHealth.Reason,Description:TargetHealth.Description}' \
  --output table
```

Target이 `healthy`인지 확인한다.

## 5. Endpoint Service 확인

```bash
aws ec2 describe-vpc-endpoint-service-configurations --region $AWS_REGION \
  --query 'ServiceConfigurations[].{Id:ServiceId,Name:ServiceName,State:ServiceState,Acceptance:AcceptanceRequired,NLBs:NetworkLoadBalancerArns,PrivateDNS:PrivateDnsName}' \
  --output table
```

A01 Endpoint Service의 `ServiceId`를 기록한다.

```bash
export SERVICE_ID=<vpce-svc-id>
```

Allowed Principal:

```bash
aws ec2 describe-vpc-endpoint-service-permissions --region $AWS_REGION \
  --service-id $SERVICE_ID \
  --query 'AllowedPrincipals[].{Type:PrincipalType,Principal:Principal}' \
  --output table
```

Endpoint Connection:

```bash
aws ec2 describe-vpc-endpoint-connections --region $AWS_REGION \
  --service-id $SERVICE_ID \
  --query 'VpcEndpointConnections[].{Endpoint:VpcEndpointId,Vpc:VpcId,State:VpcEndpointState,Owner:VpcEndpointOwner}' \
  --output table
```

판단 포인트:

```text
Endpoint Service → NLB 연결
AcceptanceRequired = true
Consumer endpoint connection = accepted/available 계열 상태
```

## 6. Consumer Interface Endpoint 확인

```bash
aws ec2 describe-vpc-endpoints --region $AWS_REGION \
  --filters "Name=vpc-id,Values=$CONSUMER_VPC_ID" \
  --query 'VpcEndpoints[].{Id:VpcEndpointId,Type:VpcEndpointType,State:State,Service:ServiceName,Vpc:VpcId,Subnets:SubnetIds,ENIs:NetworkInterfaceIds,SGs:Groups[].GroupId,DNS:DnsEntries[].DnsName}' \
  --output json
```

A01 Endpoint ID를 기록한다.

```bash
export ENDPOINT_ID=<vpce-id>
```

판단 포인트:

```text
Type  = Interface
State = available
Vpc   = Consumer VPC
ENI   = 1개 이상
DNS   = endpoint-specific private DNS entries 존재
```

## 7. Endpoint ENI / private IP 확인

```bash
export ENDPOINT_ENIS=$(aws ec2 describe-vpc-endpoints --region $AWS_REGION \
  --vpc-endpoint-ids $ENDPOINT_ID \
  --query 'VpcEndpoints[0].NetworkInterfaceIds' --output text)

aws ec2 describe-network-interfaces --region $AWS_REGION \
  --network-interface-ids $ENDPOINT_ENIS \
  --query 'NetworkInterfaces[].{Id:NetworkInterfaceId,Vpc:VpcId,Subnet:SubnetId,PrivateIP:PrivateIpAddress,SGs:Groups[].GroupId,Status:Status,Description:Description}' \
  --output table
```

Endpoint ENI의 IP가 `10.2.x.x`인지 확인한다.

## 8. Endpoint Security Group 확인

```bash
export ENDPOINT_SG_ID=<endpoint-security-group-id>

aws ec2 describe-security-groups --region $AWS_REGION \
  --group-ids $ENDPOINT_SG_ID \
  --query 'SecurityGroups[].{Name:GroupName,Id:GroupId,Ingress:IpPermissions,Egress:IpPermissionsEgress}' \
  --output json
```

판단 포인트:

```text
TCP 80 inbound source = Consumer EC2 SG
```

## 9. Consumer EC2에서 DNS / HTTP 검증

Endpoint DNS 중 하나를 기록한다.

```bash
aws ec2 describe-vpc-endpoints --region $AWS_REGION \
  --vpc-endpoint-ids $ENDPOINT_ID \
  --query 'VpcEndpoints[0].DnsEntries[].DnsName' \
  --output table
```

Consumer EC2에서:

```bash
getent hosts <interface-endpoint-dns>
curl -v http://<interface-endpoint-dns>/
```

판단 포인트:

```text
DNS → Consumer VPC의 10.2.x.x Endpoint ENI IP
HTTP → Provider 서비스 응답 성공
```

Provider EC2의 실제 private IP로는 직접 연결되지 않아야 한다.

```bash
curl --connect-timeout 3 http://<provider-ec2-private-ip>/
```

## 10. 장애 전/중/복구 비교

Endpoint-SG TCP 80 rule을 제거하기 전/중/복구 후 다음을 반복한다.

```bash
aws ec2 describe-vpc-endpoints --region $AWS_REGION \
  --vpc-endpoint-ids $ENDPOINT_ID \
  --query 'VpcEndpoints[0].{State:State,DNS:DnsEntries[].DnsName,ENIs:NetworkInterfaceIds}'
```

Consumer EC2:

```bash
getent hosts <interface-endpoint-dns>
curl --connect-timeout 3 -v http://<interface-endpoint-dns>/
```

SG 문제에서는 Endpoint 자체가 `available`이어도 HTTP가 실패할 수 있다.

Provider Target 장애 때는:

```bash
aws elbv2 describe-target-health --region $AWS_REGION \
  --target-group-arn $TG_ARN \
  --query 'TargetHealthDescriptions[].{Target:Target.Id,State:TargetHealth.State,Reason:TargetHealth.Reason}' \
  --output table
```

을 함께 비교한다.

---

# A01 삭제 후 잔존 리소스 검사

삭제 순서는 A01 README를 따른다.

## Interface Endpoint

```bash
aws ec2 describe-vpc-endpoints --region $AWS_REGION \
  --filters 'Name=tag:Project,Values=cloud-lab' \
            'Name=tag:Stage,Values=examples-advanced' \
            'Name=tag:Example,Values=A01' \
  --query 'VpcEndpoints[].{Id:VpcEndpointId,State:State,Service:ServiceName}' \
  --output table
```

의도적으로 남긴 것이 없다면 결과가 비어 있어야 한다.

## Endpoint Service

```bash
aws ec2 describe-vpc-endpoint-service-configurations --region $AWS_REGION \
  --query "ServiceConfigurations[?contains(ServiceName, 'vpce-svc')].{Id:ServiceId,Name:ServiceName,State:ServiceState,NLBs:NetworkLoadBalancerArns}" \
  --output table
```

다른 Endpoint Service가 있을 수 있으므로 **A01 service ID인지 확인하고 판단**한다.

## NLB / Target Group

```bash
aws elbv2 describe-load-balancers --region $AWS_REGION \
  --query "LoadBalancers[?starts_with(LoadBalancerName, 'advanced-a01')].[LoadBalancerName,State.Code]" \
  --output table

aws elbv2 describe-target-groups --region $AWS_REGION \
  --query "TargetGroups[?starts_with(TargetGroupName, 'advanced-a01')].[TargetGroupName,TargetGroupArn]" \
  --output table
```

## EC2 / EBS

```bash
aws ec2 describe-instances --region $AWS_REGION \
  --filters 'Name=tag:Stage,Values=examples-advanced' \
            'Name=tag:Example,Values=A01' \
            'Name=instance-state-name,Values=pending,running,stopping,stopped' \
  --query 'Reservations[].Instances[].{Id:InstanceId,Name:Tags[?Key==`Name`]|[0].Value,State:State.Name}' \
  --output table

aws ec2 describe-volumes --region $AWS_REGION \
  --filters 'Name=tag:Stage,Values=examples-advanced' \
            'Name=tag:Example,Values=A01' \
  --query 'Volumes[].{Id:VolumeId,State:State,Size:Size}' \
  --output table
```

## VPC

```bash
aws ec2 describe-vpcs --region $AWS_REGION \
  --filters 'Name=tag:Stage,Values=examples-advanced' \
            'Name=tag:Example,Values=A01' \
  --query 'Vpcs[].{Id:VpcId,CIDR:CidrBlock,Name:Tags[?Key==`Name`]|[0].Value}' \
  --output table
```

## Endpoint ENI 보조 확인

Interface Endpoint를 삭제하면 연결된 Endpoint ENI도 제거되어야 한다.

삭제 직전에 기록한 ENI ID가 있다면:

```bash
aws ec2 describe-network-interfaces --region $AWS_REGION \
  --network-interface-ids <recorded-endpoint-eni-id>
```

`InvalidNetworkInterfaceID.NotFound`가 나오면 해당 ENI는 제거된 것이다.

## 최종 판단

```text
Interface Endpoint 없음
Endpoint ENI 없음
A01 Endpoint Service 없음
advanced-a01 NLB 없음
advanced-a01 Target Group 없음
A01 EC2/EBS 없음
A01 Provider/Consumer VPC 없음
```

여기까지 확인해야 실습 종료로 본다.
