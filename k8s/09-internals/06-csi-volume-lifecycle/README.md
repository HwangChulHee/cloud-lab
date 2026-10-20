# CSI Provisioning·Binding·Attach·Mount

> 분류: **운영 심화** · 선수 학습: [독립 학습](../../08-independent/README.md)의 06-storage 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

PVC는 저장 요구이며 PV는 해당 요청과 결합되는 리소스다. 이 단원은 단순한 명령어 암기가 아니라 Kubernetes API 객체의 변화와 실제 Node/Runtime에서 일어나는 현상을 연결하는 학습이다.

**학습 결과:** CSI Provisioning·Binding·Attach·Mount의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 선수 개념과 내부 동작

PVC는 저장 요구이며 PV는 해당 요청과 결합되는 리소스다. StorageClass는 드라이버, 파라미터, reclaimPolicy, volumeBindingMode를 정의한다. Immediate와 WaitForFirstConsumer는 PV 생성/바인딩의 시점을 달리한다. CSI 기반 구현에서는 외부 Provisioner와 CSI Controller/Node 서비스가 관여하고 ControllerPublish(Attach)가 필요하지 않은 드라이버도 있다. kubelet의 볼륨 준비/Mount 실패는 PVC Pending과 구분해야 한다. Local Path Provisioner는 일반적인 CSI 플러그인과 동일한 흐름을 증명하지 않는다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../08-independent/README.md)의 06-storage 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

## 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl get storageclass -o wide
kubectl get pv -o wide
kubectl -n lab-self-storage get pvc,pods -o wide
kubectl -n lab-self-storage describe pvc disk-data-0
kubectl -n lab-self-storage describe pod data-0
```

## 따라 하기 — 순서와 예상 결과

기존 06-storage의 Local Path StatefulSet을 실행한 상태에서 Pod/PVC/PV/StorageClass/Node의 연관관계를 표로 그린다. PVC Bound 시점과 Pod Ready 시점을 비교하고, VolumeBindingMode 및 PV nodeAffinity를 기록한다. CSI ControllerPublish/NodeStage/NodePublish는 CSI 구현이 있는 별도 환경의 관찰 항목으로 둔다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

## 고장 가설과 복구

PVC Pending은 StorageClass/provisioner/소비 Pod/토폴로지를, Pod FailedMount는 kubelet의 이벤트·Node 경로·드라이버를 조사한다. 잘못된 class를 가진 별도 PVC를 생성해 Pending 사례를 만들되 정상 PVC는 손대지 않는다.

복구 완료 기준은 **동일한 조회나 요청으로 정상 결과를 다시 얻는 것**이다. 관찰할 수 없는 구현(예: CSI driver 미설치, kube-proxy 대체 데이터 평면)은 미검증으로 기록한다.

## 스스로 설명할 문제

1. **CSI Provisioning·Binding·Attach·Mount**이 필요한 이유를 사용자가 겪을 수 있는 실제 문제로 설명할 수 있는가?
2. 이 현상을 만든 API 객체와 실제 실행한 컴포넌트는 각각 무엇인가?
3. 위 예시의 실패 원인과 동일한 외부 증상을 보이는 다른 원인은 무엇이며 첫 번째로 어떤 증거를 확인할 것인가?
4. Pod/Node 또는 Controller를 재시작하지 않고도 진단 가능한 정보는 무엇인가?

## 환경 및 정리

원래 실습 namespace와 공용 애드온은 연결된 기본 단계의 정리 지침을 따른다. Node taint/route/CNI/etcd 및 Kubernetes 패키지 변경은 별도 안전 조건이 명시된 경우에만 수행한다. 실제 VM 실행 여부는 [CHECKPOINTS](../../08-independent/CHECKPOINTS.md)에 별도로 기록한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
