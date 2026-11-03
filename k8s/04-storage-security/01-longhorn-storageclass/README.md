# Lab 33 — StorageClass와 Provisioner (Longhorn은 선택 심화)

> **기초 필수:** StorageClass, CSI/Provisioner, PVC Pending 원인 · **선택 심화:** Longhorn 설치와 복제 저장소 운영

## Overview / Recall

Lab 12의 정적 PV/PVC는 관리자가 PV를 미리 준비했다. 동적 방식은 PVC의 `storageClassName`에 해당하는 StorageClass의 provisioner가 볼륨 생성을 요청한다.

- StorageClass는 데이터 자체가 아니고 **볼륨 생성을 위한 정책/프로비저너 선택**이다.
- `Immediate`는 보통 PVC 생성 시 바인딩을 시도하고 `WaitForFirstConsumer`는 첫 소비 Pod 배치와 연계한다.
- `reclaimPolicy`는 PV가 Release된 후의 처리 정책이며, `Retain`과 `Delete`를 구분한다.
- Longhorn은 CSI 기반 분산 블록 스토리지 구현의 한 예시다. **CKA 기본 개념을 배우려고 반드시 설치할 필요는 없다.**

## Build & Observe — 존재하는 프로비저너 확인

```bash
kubectl config current-context
kubectl get storageclass -o wide
kubectl get storageclass -o yaml
kubectl get csidrivers
kubectl get pods -A | grep -E 'local-path|longhorn|csi' || true
```

**예상:** 적어도 실습용 동적 provisioner 하나가 있어야 한다. 이미 설치되어 있다면 재설치하지 않는다. 없다면 [공용 애드온: Local Path](../../guides/ADDONS.md#local-path-provisioner)를 따라 별도 테스트용 설치를 준비한다. Local Path는 CSI Attach 단계를 보여주는 구현이라고 주장하지 않는다.

## Break & Diagnose — 잘못된 StorageClass를 가진 PVC

기존 PV/PVC 및 사용자 데이터를 건드리지 않는 임시 namespace에서만 진행한다.

```bash
kubectl create namespace lab-storageclass
kubectl -n lab-storageclass create -f - <<'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: missing-class
spec:
  storageClassName: intentionally-missing-class
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 64Mi
EOF
kubectl -n lab-storageclass get pvc
kubectl -n lab-storageclass describe pvc missing-class
kubectl get storageclass
```

**예상:** PVC Pending과 StorageClass를 찾지 못한다는 Event가 나타난다. 단순 `Pending`만으로 Storage backend 장애라고 단정하지 않는다. 특정 스토리지 구현은 메시지 표현이 다를 수 있다.

## Recover — 실제 StorageClass로 올바르게 재생성

```bash
kubectl -n lab-storageclass delete pvc missing-class
kubectl get storageclass -o custom-columns=NAME:.metadata.name,PROVISIONER:.provisioner,BINDMODE:.volumeBindingMode,RECLAIM:.reclaimPolicy
```

현재 클러스터에서 사용할 StorageClass 이름을 `SC_NAME`으로 선택한다. 다음 Lab 34에서 그 이름으로 PVC + 소비 Pod를 만들어 `Bound`와 Mount 성공까지 확인한다. **WaitForFirstConsumer인 PVC는 소비 Pod 생성 전 Pending이 정상일 수 있다.** 잘못된 `storageClassName`을 기존 PVC에서 임의로 수정할 수 있다고 가정하지 않는다.

## 선택 실습 — Longhorn 제품 탐구

1. 모든 노드의 iSCSI 및 디스크/마운트 요구 사항, Kubernetes 호환 버전, 리소스를 확인한다.
2. 폐기 가능한 **별도 VM 클러스터**에 [Longhorn 공식 설치 절차](https://longhorn.io/docs/)를 사용한다.
3. `kubectl get storageclass`, `kubectl -n longhorn-system get pods`, `kubectl get volumes.longhorn.io -A` 등으로 driver/engine/replica를 관찰한다.
4. replica 하나가 실패했을 때 재복제 상태를 관찰하되, 실제 운영 장애를 의도적으로 일으키지 않는다.

이 제품 심화는 **기초 Lab 완료와 별도로 선택**한다.

## Cleanup / Explain

```bash
kubectl delete namespace lab-storageclass
```

완료 기준: StorageClass가 provisioner에 무엇을 지정하는지, 잘못된 Class와 WaitForFirstConsumer의 Pending이 어떻게 다른지, PV의 `Delete`/`Retain`이 어떤 결과를 만드는지 설명한다.

다음: [Lab 34 Dynamic Provisioning](../02-dynamic-provisioning-pv-lifecycle/README.md).
