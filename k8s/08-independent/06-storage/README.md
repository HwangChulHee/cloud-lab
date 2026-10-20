# 06. PVC·StorageClass·StatefulSet로 수명 비교하기

## 내부 동작 연결

[INT-06 내부 원리 심화](../../09-internals/06-csi-volume-lifecycle/README.md)에서 이 단계의 객체가 어느 컴포넌트와 Linux 계층을 거쳐 처리되는지 확인한다. 연결된 심화는 현재 단계를 성공적으로 실행한 후 학습한다. 실제 검증은 별도로 기록한다.

## 먼저 이해할 것

emptyDir는 Pod 수명, hostPath는 특정 노드 경로, PVC는 저장소 요청이다. PV는 실제 저장소와 연결 조건을 나타낸다. StorageClass는 provisioner와 생성/바인딩 정책을 정의한다. StatefulSet은 이름과 Pod별 PVC를 유지하지만 DB 복제·선출·백업을 구현하지 않는다.

## 정적 저장소를 먼저 실행하기

[03 Retain 데이터 복구](../../07-cka-preview/03-pv-data-recovery/README.md)를 끝낸다. worker SSH 경로 준비, 고유 문구 기록, Pod/PVC 삭제, claimRef 회수와 재연결, 정확한 문구 비교를 풀이와 함께 실행한다. 해당 문서의 PV/호스트 경로 정리까지 완료한다. 이것으로 hostPath/local 데이터가 자동으로 다른 노드에 복제되지 않는 점도 확인한다.

## 동적 저장소 준비

[공용 애드온 준비](../ADDONS.md#local-path-provisioner)에서 Local Path Provisioner를 준비한다. 아래는 이름이 고정된 provisioner `rancher.io/local-path`용이다. Longhorn을 이미 사용 중이어도 이 실습에는 Local Path를 별도로 사용하거나 원본을 복사해 class/provisioner를 일관되게 바꾼다. 기본 StorageClass annotation은 변경하지 않는다.

Local Path는 노드 디렉터리를 생성하는 학습용 저장소다. 요청한 용량 제한과 복제된 스토리지의 가용성을 제공한다고 가정하지 않는다. Longhorn 설치/운영 자체는 선택 확장 주제이고 StorageClass 개념의 선행 조건이 아니다.

## 따라 하기

```bash
kubectl apply -f k8s/08-independent/06-storage/setup.yaml
kubectl -n lab-self-storage rollout status statefulset/data --timeout=180s
kubectl -n lab-self-storage get pods,pvc -o wide
kubectl get pv
kubectl -n lab-self-storage exec data-0 -- sh -c 'echo data-zero > /data/marker'
kubectl -n lab-self-storage exec data-1 -- sh -c 'echo data-one > /data/marker'
kubectl -n lab-self-storage exec data-0 -- cat /data/marker
kubectl -n lab-self-storage exec data-1 -- cat /data/marker
```

data-0/data-1와 disk-data-0/disk-data-1 각각의 PVC가 생기고 Bound가 된다. 같은 mountPath지만 두 파일 내용은 다르다. PVC만 있고 Pod가 없을 때 WaitForFirstConsumer로 Pending일 수 있는 이유를 설명한다.

## 삭제 → 복구 → 축소 비교

```bash
STORAGE_OLD_UID=$(kubectl -n lab-self-storage get pod data-0 -o jsonpath='{.metadata.uid}')
kubectl -n lab-self-storage delete pod data-0 --wait=true
python3 k8s/08-independent/wait_for_pod.py lab-self-storage data-0 --different-uid "$STORAGE_OLD_UID" --timeout 180
kubectl -n lab-self-storage exec data-0 -- cat /data/marker
kubectl -n lab-self-storage scale statefulset data --replicas=1
kubectl -n lab-self-storage wait --for=delete pod/data-1 --timeout=120s
kubectl -n lab-self-storage get pvc
kubectl -n lab-self-storage scale statefulset data --replicas=2
python3 k8s/08-independent/wait_for_pod.py lab-self-storage data-1 --timeout 180
kubectl -n lab-self-storage exec data-1 -- cat /data/marker
```

이름은 같아도 Pod UID는 바뀌고 data-zero가 남아야 한다. [대기 도구](../wait_for_pod.py)는 Pod가 잠깐 없는 구간도 기다리며 새 UID와 Ready를 함께 확인한다. Pod 삭제만으로 StatefulSet generation이 바뀌지는 않으므로 rollout status만으로 재생성 완료를 판정하지 않는다. 대기 실패 시 다음 exec를 진행하지 말고 describe pod와 PVC Events를 확인한다. scale-down 뒤에도 PVC가 남고 scale-up하면 data-one을 다시 읽는다. mount 실패는 Pod Events에서, binding 실패는 PVC Events에서 확인한다.

## StorageClass 비교 확장

[04 지연 바인딩](../../07-cka-preview/04-storageclass-binding/README.md)을 실행해 소비 Pod 생성 전후의 지연 바인딩과 default class를 비교한다. class.yaml의 provisioner placeholder를 위 준비에서 확인한 값으로 바꾸는 단계부터 진행한다.

## 누적 복습 — 다음 단계 전에

앞 단계의 개념을 현재 증상에 다시 연결한다. 문서를 닫고 세 질문에 답하며, 어려운 질문은 실제 spec/status/Events를 근거로 다시 설명한다.

1. PVC Pending과 Pod FailedMount의 차이는?
2. WaitForFirstConsumer가 필요한 이유는?
3. emptyDir와 PV의 생명주기는?

관련 내부 심화를 할 경우 이 단계의 **namespace를 정리하기 전에** 진행한다. 개념만 읽을 때는 리소스 재생성을 강제하지 않는다.

## 완료와 정리

Retain과 Delete 중 누가 데이터를 지우는지, RWO가 한 Pod인지 한 노드인지 설명한다. 다음 삭제는 이 단계의 테스트 데이터를 없애므로 비교가 끝난 뒤 실행한다.

```bash
kubectl -n lab-self-storage scale statefulset data --replicas=0
kubectl -n lab-self-storage wait --for=delete pod -l app=data --timeout=120s
kubectl delete namespace lab-self-storage
kubectl get pv
```

이 단계 PVC에 연결됐던 PV가 Delete 정책으로 정리됐는지 확인한 다음 `kubectl delete storageclass lab-self-local`을 실행한다. Provisioner가 실패하면 Events/로그로 원인을 해결하고 PV 정리를 확인한다. 공용 provisioner는 다음 재실습에 남긴다.

다음: [07 인증·권한](../07-security/README.md).

[독립 학습 순서](../README.md)
