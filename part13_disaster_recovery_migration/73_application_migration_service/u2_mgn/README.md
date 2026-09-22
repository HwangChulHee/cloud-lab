# u2. AWS Application Migration Service (MGN)

AWS Application Migration Service는 **physical / virtual / cloud server를 AWS로 lift-and-shift(rehost)**하는 서비스다.

강의에서는 CloudEndure Migration의 발전형이며 AWS Server Migration Service(SMS)를 대체한다고 설명한다.

## 기본 구조

```text
Corporate Data Center / Any Cloud
Disks + OS + Apps + DB
          ↓
AWS Replication Agent
          ↓ continuous replication
AWS Staging Area
Low-cost EC2 + EBS
          ↓ cutover
AWS Production
Target EC2 + EBS
```

## 강의 핵심

```text
physical servers 지원
virtual servers 지원
cloud-based servers 지원
wide range of OS / platform / database
continuous replication
minimal downtime
lift-and-shift / rehost
```

## Rehost

Application을 크게 재설계하지 않고 server workload를 AWS의 native EC2 환경으로 옮기는 전략이다.

## 기억할 문장

> MGN은 기존 server를 지속 복제하다가 cutover 시점에 AWS EC2 기반으로 전환하는 rehost 서비스다.
