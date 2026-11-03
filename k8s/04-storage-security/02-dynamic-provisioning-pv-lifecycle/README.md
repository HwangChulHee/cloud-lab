# Lab 34 — Dynamic Provisioning & PV Lifecycle

> 학습 단계: **중간 가이드**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../05-advanced/01-statefulset/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

## 목표

Static/Dynamic provisioning과 PV lifecycle/ReclaimPolicy를 비교한다.

## 핵심 개념과 오해 방지

PV는 namespace에 속하지 않고 PVC는 namespace에 속한다. 일반적인 PV/PVC 바인딩은 1:1이며 큰 PV 하나에 여러 PVC가 자동 분할 연결되지는 않는다. class/accessModes/용량/volumeMode/selector/volumeName 조건을 함께 확인한다.

Available은 바인딩 가능한 상태, Bound는 PVC와 연결된 상태, Released는 이전 PVC가 없어졌으나 회수 처리가 필요한 상태다. Failed를 모든 마운트 오류의 상태라고 부르지 않는다. 마운트 실패는 Pod Events에 표시되면서 PV는 여전히 Bound일 수 있다. Retain 데이터는 수동 점검 후 재사용할 수 있으며 claimRef 처리가 필요하다. Recycle은 deprecated 상태이므로 신규 실습은 Retain/Delete에 집중한다.

`storageClassName: ""` 자체가 hostPath를 생성하는 것은 아니다. 실제 생성·마운트 시점은 backing volume 종류와 provisioner의 동작에 달려 있다. local PV에는 기존 노드 경로와 nodeAffinity가 필요하고, 그 노드가 사라진다고 다른 노드에 같은 데이터가 자동 복제되지 않는다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## CSI·Provisioner 내부 동작

`StorageClass`는 provisioner·parameters·reclaimPolicy·volumeBindingMode를 정의한다. 일반적인 CSI 구현에서는 외부 provisioner와 CSI Controller/Node component가 협력하며, 경우에 따라 Attach 단계가 생략될 수 있다. PVC `Bound`는 Pod 볼륨 `Mount` 성공과 다른 단계다. Local Path Provisioner를 CSI 전체 과정의 증거로 오인하지 않는다.

## 실행형 Lab — PVC → PV → Pod Mount → Data → Cleanup

다음 절차가 **공식 수행 과제**다. 이전 INT 심화 설명은 CSI가 있는 드라이버와 로컬 프로비저너의 차이를 이해하는 참고 개념으로 사용한다.

**전제:** `kubectl get sc local-path`이 성공해야 한다. 없으면 [Local Path 설치](../../guides/ADDONS.md#local-path-provisioner)를 완료한다. 원래 `local-path` 이름이 다른 StorageClass를 쓰는 환경에서는 `dynamic.yaml`의 `storageClassName`을 실제 Class로 바꾼다.

```bash
kubectl get storageclass local-path -o yaml
kubectl apply -f k8s/04-storage-security/02-dynamic-provisioning-pv-lifecycle/dynamic.yaml
kubectl -n lab-dynamic-storage get pvc,pod -o wide
kubectl -n lab-dynamic-storage wait --for=condition=Ready pod/reader --timeout=180s
kubectl -n lab-dynamic-storage get pvc,pod -o wide
kubectl -n lab-dynamic-storage describe pvc data
kubectl -n lab-dynamic-storage exec reader -- sh -c 'echo persistent-marker > /data/marker'
kubectl -n lab-dynamic-storage exec reader -- cat /data/marker
```

**예상:** WaitForFirstConsumer일 경우 Pod 생성 전 PVC Pending이 가능하고, 정상 바인딩 이후 PVC Bound, Pod Ready이며 파일에 `persistent-marker`가 있다.

```bash
PV_NAME=$(kubectl -n lab-dynamic-storage get pvc data -o jsonpath='{.spec.volumeName}')
kubectl get pv "$PV_NAME" -o wide
kubectl get pv "$PV_NAME" -o jsonpath='{.spec.persistentVolumeReclaimPolicy}{"\n"}'
kubectl -n lab-dynamic-storage delete pod reader --wait=true
kubectl apply -f k8s/04-storage-security/02-dynamic-provisioning-pv-lifecycle/dynamic.yaml
kubectl -n lab-dynamic-storage wait --for=condition=Ready pod/reader --timeout=180s
kubectl -n lab-dynamic-storage exec reader -- cat /data/marker
```

**예상:** Pod UID가 달라져도 동일 PVC와 데이터가 유지된다. `local-path`는 Node 로컬 경로를 사용하므로 PV의 Node Affinity가 다른 Node로의 스케줄링을 제한할 수 있다. 이 과제로 **분산 스토리지 복제가 검증됐다고 판단하지 않는다.**

## 장애 진단과 복구

- **PVC Pending:** Class/provisioner가 존재하는가? `volumeBindingMode=WaitForFirstConsumer`인가? 소비 Pod가 생겼고 실제 스케줄 가능한가?
- **PVC Bound + Pod Pending:** Pod의 Node selector/taint/PV topology 및 Events를 확인한다.
- **PVC Bound + FailedMount:** kubelet/노드 경로와 provisioner Events를 확인한다.
- **PVC Released/Retain:** 데이터는 자동 삭제되지 않을 수 있으며 claimRef/재사용 정책을 점검한다.

잘못된 Class에 PVC를 만들어 실패시키는 실습은 이미 [Lab 33](../01-longhorn-storageclass/README.md)에서 수행하므로 반복하지 않는다.

## Cleanup / 복습

```bash
kubectl delete namespace lab-dynamic-storage
kubectl get pv "$PV_NAME" --ignore-not-found
```

ReclaimPolicy가 Delete면 provisioner 정리 완료 후 PV도 사라지는지 확인하고, Retain이면 실제 데이터 보존과 수동 정리 범위를 검토한다. `StorageClass`는 공유 리소스이므로 이 Lab의 Namespace 삭제와 무관하며 임의로 삭제하지 않는다.

**인출 질문:** Bound와 Mounted는 왜 다른가? CSI ControllerPublish를 Local Path에서 반드시 볼 수 있는가? Node 로컬 PVC를 다른 Worker로 옮기면 왜 데이터가 따라오지 않는가?
