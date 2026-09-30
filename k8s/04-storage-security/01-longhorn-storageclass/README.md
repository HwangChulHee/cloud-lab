# Lab 33 — Longhorn & StorageClass

> 학습 단계: **중간 가이드**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/06-storage/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

로컬 3노드 클러스터에 동적 스토리지 계층을 추가한다.

## Recall

Static PV/PVC에서 관리자가 PV를 준비했던 흐름을 떠올리고, 이번에는 provisioner가 어떤 부분을 대신하는지 확인한다.

## Build & Observe

1. 모든 노드의 iSCSI 요구사항을 확인한다.
2. Longhorn을 설치하고 `longhorn-system` Pod 상태를 확인한다.
3. Longhorn이 제공하는 StorageClass와 provisioner를 확인한다.
4. 실습용 `fast` StorageClass를 만들고 `provisioner: driver.longhorn.io`를 확인한다.

## Safe Failure Exercise

Longhorn 내부 Controller를 일부러 중지시키지는 않는다. Storage 계층 자체를 망가뜨리면 원인 범위가 불필요하게 커지기 때문이다.

대신 존재하지 않는 StorageClass 이름을 참조하는 PVC를 하나 만든다.

1. PVC가 Pending인지 확인한다.
2. `kubectl describe pvc`와 Events에서 원인을 찾는다.
3. 잘못 만든 PVC를 삭제하고 올바른 storageClassName으로 새 PVC를 만든다. storageClassName을 기존 PVC에서 임의로 수정할 수 있다고 가정하지 않는다. 다음 실습에서 Dynamic Provisioning을 진행한다.

## 완료 검증

1. StorageClass와 provisioner의 관계를 설명한다.
2. StorageClass 이름이 잘못됐을 때 어느 리소스부터 확인해야 하는지 설명한다.

## Cleanup

실패 확인용 PVC만 삭제한다. Longhorn과 `fast` StorageClass는 다음 Storage 실습에서 재사용하므로 유지한다.

## 설명하기

> PVC가 StorageClass를 지정하면 ______가 실제 PV/Volume 생성을 담당한다.

## 연결된 확장 실습

- [StorageClass와 지연 바인딩](../../07-cka-preview/04-storageclass-binding/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
