# Lab 38 — StatefulSet

> 학습 단계: **가이드 축소**

## 강의 없이 시작하기

이 README가 이 주제의 **공식 학습·실습 기록**입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [이전 독립 코스의 추가 실행 자산](../../05-advanced/01-statefulset/README.md)은 고유 예제나 YAML이 필요할 때 참고하며 별도로 중복 완료하지 않습니다.

## 목표

고정 identity, 순차 동작, Pod별 영속 볼륨을 ReplicaSet과 비교한다.

## 핵심 개념과 오해 방지

StatefulSet은 안정적인 ordinal 이름, 네트워크 identity와 PVC 연결을 관리한다. DB의 primary 선출, 복제, 샤딩, 데이터 백업은 DB나 Operator가 별도로 담당하며 Pod를 여러 개 만든 것만으로 DB 고가용성이 완성되지 않는다.

기본 OrderedReady의 scale-up/down 순서를 관찰한다. podManagementPolicy=Parallel이면 scale 순서가 달라지고, StatefulSet 객체 삭제 자체가 역순의 안전한 종료를 보장하는 것은 아니다. 순차 종료를 보려면 먼저 scale-to-zero를 관찰한다. volumeClaimTemplates는 Pod별 PVC를 만들지만 실제 PV의 동적 생성에는 StorageClass/provisioner 또는 미리 준비한 매칭 PV가 필요하다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. ReplicaSet과 StatefulSet을 각각 scale해 이름/생성 순서를 비교한다.
2. volumeClaimTemplates로 Pod별 PVC 생성을 확인한다.
3. Pod별 파일을 만들고 재생성 후 동일 PVC 재연결을 확인한다.
4. Headless Service DNS로 개별 Pod를 호출한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. StatefulSet Pod 하나를 삭제하고 이름/볼륨이 어떻게 복구되는지 관찰한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Stateless와 Stateful workload의 차이를 설명한다.

## Cleanup

StatefulSet 삭제나 scale-down은 기본적으로 volumeClaimTemplates의 PVC를 삭제하지 않는다. 실습에서 생성한 PVC 이름을 먼저 확인하고 필요한 데이터가 없는 경우에만 개별 삭제한다. PVC/PV의 Retain/Delete 정책과 실제 저장소 정리도 확인한다.

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 병합 심화 — StatefulSet과 PVC의 생명주기

예전 독립 과정의 동적 저장소 예제는 같은 Lab에 있는 [확장 YAML](./extended-setup.yaml)을 사용한다. StorageClass provisioner가 준비됐는지 먼저 확인하고, 없으면 [공용 애드온 안내](../../guides/ADDONS.md)를 참고한다.

```bash
kubectl apply -f k8s/05-advanced/01-statefulset/extended-setup.yaml
kubectl -n lab-self-storage rollout status statefulset/data --timeout=180s
kubectl -n lab-self-storage get pods,pvc -o wide
kubectl -n lab-self-storage exec data-0 -- sh -c 'echo data-zero > /data/marker'
kubectl -n lab-self-storage exec data-1 -- sh -c 'echo data-one > /data/marker'
kubectl -n lab-self-storage delete pod data-0 --wait=true
python3 k8s/05-advanced/01-statefulset/wait_for_pod.py lab-self-storage data-0 --timeout 180
kubectl -n lab-self-storage exec data-0 -- cat /data/marker
kubectl -n lab-self-storage scale statefulset data --replicas=1
kubectl -n lab-self-storage get pvc
kubectl -n lab-self-storage scale statefulset data --replicas=2
kubectl -n lab-self-storage exec data-1 -- cat /data/marker
```

Pod가 삭제되어 UID가 바뀌더라도 StatefulSet의 PVC 데이터가 유지되는지 비교한다. Scale-down 시 PVC 유지 여부, Pod의 재생성 여부, WaitForFirstConsumer에서 PVC Pending이 정상일 수 있는 조건을 설명한다. 볼륨 Binding과 Mount 실패를 구분하고, 데이터 보존 정책을 확인한 후 실습 Namespace/PVC를 정리한다. 이 실습은 별도의 08단계 완료 항목으로 계산하지 않는다.
