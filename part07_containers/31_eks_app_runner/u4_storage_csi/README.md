# u4. EKS Storage / CSI

EKS에서 persistent storage를 연결할 때 강의에서는 **StorageClass와 CSI(Container Storage Interface) driver**를 강조한다.

## 구조

```text
Pod
 ↓
Persistent Volume Claim
 ↓
StorageClass
 ↓
CSI Driver
 ↓
AWS Storage
```

## 강의에서 언급하는 Storage

```text
Amazon EBS
Amazon EFS
Amazon FSx for Lustre
Amazon FSx for NetApp ONTAP
```

## EBS

Block storage.

일반적으로 특정 AZ와 연결되는 특성이 있으므로 Pod scheduling과 함께 고려해야 한다.

## EFS

Shared file storage.

강의에서는 **EFS가 Fargate와 함께 사용할 수 있다**는 점을 강조한다.

```text
Multiple Pods
   ↓
Amazon EFS
```

## FSx

특정 고성능/특수 filesystem 요구에서 선택할 수 있다.

SAA에서는 제품 세부 운영보다 "EKS persistent storage는 CSI driver와 StorageClass를 통해 AWS storage에 연결한다"는 흐름이 중요하다.

## SAA 판단

```text
EKS persistent block storage
→ EBS CSI

shared filesystem
→ EFS

Fargate + persistent shared file
→ EFS 고려
```

## 기억할 문장

> EKS storage는 Kubernetes StorageClass와 CSI driver를 통해 EBS/EFS/FSx 같은 AWS storage를 연결한다.
