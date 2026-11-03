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
