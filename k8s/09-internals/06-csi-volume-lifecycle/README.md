# CSI Provisioning·Binding·Attach·Mount

> 분류: **운영 심화** · 선수 학습: [독립 학습](../../08-independent/README.md)의 06-storage 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

PVC는 저장 요구이며 PV는 해당 요청과 결합되는 리소스다. 이 단원에서는 실제 컴포넌트의 동작 순서를 학습하고 관찰 증거와 연결한다.

**학습 결과:** CSI Provisioning·Binding·Attach·Mount의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 핵심 질문에서 내부 원리까지

**PVC Bound인데 Pod가 실패할 수 있을까?**

### 실행 흐름을 따라가기

PV/PVC Binding은 할당 관계이고, CSI 드라이버의 Attach/Publish/Mount는 노드 사용 준비 과정이다. 구현에 따라 Attach가 없을 수 있으며 Local Path는 일반 CSI 드라이버가 아니다.

### 예상 상태 해석 예시

PVC Pending이면 binding/provisioner를, PVC Bound + FailedMount면 kubelet/Node/드라이버를 조사한다.

> 이 예시는 학습용이며 실제 클러스터 실행 결과가 아니다. 환경·CNI·버전에 따라 출력이 다를 수 있다.

### 개념을 이해했는지 확인하기

- WaitForFirstConsumer와 Scheduler의 관계는?
- 이 과정에서 **API 객체 상태를 만드는 주체**와 **실제 Node에서 실행하는 주체**는 각각 누구인가?
- 비슷한 증상을 유발할 수 있는 다른 원인 하나를 들고 확인할 첫 증거를 설명할 수 있는가?

## 선수 개념과 내부 동작

PVC는 저장 요구이며 PV는 해당 요청과 결합되는 리소스다. StorageClass는 드라이버, 파라미터, reclaimPolicy, volumeBindingMode를 정의한다. Immediate와 WaitForFirstConsumer는 PV 생성/바인딩의 시점을 달리한다. CSI 기반 구현에서는 외부 Provisioner와 CSI Controller/Node 서비스가 관여하고 ControllerPublish(Attach)가 필요하지 않은 드라이버도 있다. kubelet의 볼륨 준비/Mount 실패는 PVC Pending과 구분해야 한다. Local Path Provisioner는 일반적인 CSI 플러그인과 동일한 흐름을 증명하지 않는다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../08-independent/README.md)의 06-storage 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

### 예시: PVC가 Bound인데 파일이 보이지 않는다면?

`data-pvc`를 만든다고 가정한다. `StorageClass` 선택 → `PV/PVC Binding` → 소비 Pod의 Node 결정 → 드라이버/Node에서 볼륨 준비와 mount → 컨테이너 경로 사용으로 이어질 수 있다. **CSI 구현에 따라 Attach 단계가 없거나 순서가 달라질 수 있다.**

| 증상 | 우선 확인 | 원리 |
|---|---|---|
| PVC Pending | StorageClass, provisioner, WaitForFirstConsumer | 볼륨 미할당/바인딩 지연 |
| PVC Bound + Pod Pending | Pod Events, nodeAffinity, 스케줄링 | 저장소는 연결됐지만 Pod 배치 문제 |
| PVC Bound + FailedMount | kubelet Events, driver, Node 경로 | Node에서 volume 준비 실패 |

현재 Local Path 실습으로 CSI `ControllerPublishVolume`을 실행했다고 판단해서는 안 된다.

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

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

## 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

## 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
