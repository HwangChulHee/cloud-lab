# Lab 34 — Dynamic Provisioning & PV Lifecycle

> 학습 단계: **중간 가이드**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../08-independent/06-storage/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

## 목표

Static/Dynamic provisioning과 PV lifecycle/ReclaimPolicy를 비교한다.

## 핵심 개념과 오해 방지

PV는 namespace에 속하지 않고 PVC는 namespace에 속한다. 일반적인 PV/PVC 바인딩은 1:1이며 큰 PV 하나에 여러 PVC가 자동 분할 연결되지는 않는다. class/accessModes/용량/volumeMode/selector/volumeName 조건을 함께 확인한다.

Available은 바인딩 가능한 상태, Bound는 PVC와 연결된 상태, Released는 이전 PVC가 없어졌으나 회수 처리가 필요한 상태다. Failed를 모든 마운트 오류의 상태라고 부르지 않는다. 마운트 실패는 Pod Events에 표시되면서 PV는 여전히 Bound일 수 있다. Retain 데이터는 수동 점검 후 재사용할 수 있으며 claimRef 처리가 필요하다. Recycle은 deprecated 상태이므로 신규 실습은 Retain/Delete에 집중한다.

`storageClassName: ""` 자체가 hostPath를 생성하는 것은 아니다. 실제 생성·마운트 시점은 backing volume 종류와 provisioner의 동작에 달려 있다. local PV에는 기존 노드 경로와 nodeAffinity가 필요하고, 그 노드가 사라진다고 다른 노드에 같은 데이터가 자동 복제되지 않는다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. `storageClassName: ""`, `fast`, 생략 세 PVC를 비교한다.
2. PV가 언제 자동 생성되는지 확인한다.
3. Available/Bound/Released 상태 변화를 만든다.
4. Retain/Delete 정책을 비교한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. PVC를 삭제한 뒤 데이터/PV가 예상과 다르게 남는 상황을 분석한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. StorageClass, PV, PVC lifecycle을 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [Retain PV로 데이터 복구하기](../../07-cka-preview/03-pv-data-recovery/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.

- [StorageClass와 지연 바인딩](../../07-cka-preview/04-storageclass-binding/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.


## CSI 내부 동작: Provision → Bind → (Attach) → Mount

PVC가 `Bound`라고 해서 컨테이너가 이미 볼륨을 마운트했다는 뜻은 아니다. StorageClass가 동적 프로비저닝을 지시하고, PV/PVC 바인딩 이후 Node 사용 단계에서 별도 오류가 발생할 수 있다.

```bash
kubectl get storageclass,pv
kubectl get pvc,pods -n <namespace> -o wide
kubectl describe pvc <pvc> -n <namespace>
kubectl describe pod <pod> -n <namespace>
```

- `PVC Pending`: StorageClass/provisioner, 용량, topology, `volumeBindingMode` 확인.
- `PVC Bound + FailedMount`: kubelet, Node, 드라이버와 마운트 Events 확인.
- CSI 드라이버에 따라 ControllerPublish(Attach) 단계가 없을 수 있다. **Local Path Provisioner는 CSI 전체 경로를 보여주는 증거가 아니다.**
- `WaitForFirstConsumer`에서는 소비 Pod의 스케줄링 제약과 볼륨 결정을 함께 다루므로 PVC만 만들어 놓고 Pending인 상태가 반드시 장애는 아니다.

이 주제를 검증할 때는 저장소 운영 전반을 깨뜨리는 대신 잘못된 StorageClass를 가진 테스트 PVC처럼 범위가 제한된 장애를 우선 사용한다. [CSI 상세 관찰](../../09-internals/06-csi-volume-lifecycle/README.md).


## 내부 동작 심화 통합 — 06-csi-volume-lifecycle

이전 INT 단원의 원리와 관찰 내용을 현재 Lab에 통합한다. 아래의 `lab-self-*`은 예전 실습 Namespace이므로 지금 Lab에 생성한 자원을 우선 사용하고, 다른 자원이 필요할 때만 독립된 테스트 Namespace를 생성한다.

### 선수 개념과 내부 동작

PVC는 저장 요구이며 PV는 해당 요청과 결합되는 리소스다. StorageClass는 드라이버, 파라미터, reclaimPolicy, volumeBindingMode를 정의한다. Immediate와 WaitForFirstConsumer는 PV 생성/바인딩의 시점을 달리한다. CSI 기반 구현에서는 외부 Provisioner와 CSI Controller/Node 서비스가 관여하고 ControllerPublish(Attach)가 필요하지 않은 드라이버도 있다. kubelet의 볼륨 준비/Mount 실패는 PVC Pending과 구분해야 한다. Local Path Provisioner는 일반적인 CSI 플러그인과 동일한 흐름을 증명하지 않는다.

### 시작 전 상태와 예측

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

### 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl get storageclass -o wide
kubectl get pv -o wide
kubectl -n lab-self-storage get pvc,pods -o wide
kubectl -n lab-self-storage describe pvc disk-data-0
kubectl -n lab-self-storage describe pod data-0
```

### 따라 하기 — 순서와 예상 결과

기존 06-storage의 Local Path StatefulSet을 실행한 상태에서 Pod/PVC/PV/StorageClass/Node의 연관관계를 표로 그린다. PVC Bound 시점과 Pod Ready 시점을 비교하고, VolumeBindingMode 및 PV nodeAffinity를 기록한다. CSI ControllerPublish/NodeStage/NodePublish는 CSI 구현이 있는 별도 환경의 관찰 항목으로 둔다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

### 고장 가설과 복구

PVC Pending은 StorageClass/provisioner/소비 Pod/토폴로지를, Pod FailedMount는 kubelet의 이벤트·Node 경로·드라이버를 조사한다. 잘못된 class를 가진 별도 PVC를 생성해 Pending 사례를 만들되 정상 PVC는 손대지 않는다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

### 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

### 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

### 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
