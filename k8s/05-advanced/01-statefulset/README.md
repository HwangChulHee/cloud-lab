# Lab 38 — StatefulSet

> 학습 단계: **가이드 축소**

## 실습 안내

이 README가 해당 주제의 공식 학습 자료다. **실습 전 상태 확인 → 리소스 구축 → 정상 증거 수집 → 제한된 장애 재현 → 복구 → 정리 → 인출 질문** 순서로 진행한다. 기존 독립 코스는 별도 진도로 계산하지 않는다.

## 목표

고정 identity, 순차 동작, Pod별 영속 볼륨을 ReplicaSet과 비교한다.

## 핵심 개념과 오해 방지

StatefulSet은 안정적인 ordinal 이름, 네트워크 identity와 PVC 연결을 관리한다. DB의 primary 선출, 복제, 샤딩, 데이터 백업은 DB나 Operator가 별도로 담당하며 Pod를 여러 개 만든 것만으로 DB 고가용성이 완성되지 않는다.

기본 OrderedReady의 scale-up/down 순서를 관찰한다. podManagementPolicy=Parallel이면 scale 순서가 달라지고, StatefulSet 객체 삭제 자체가 역순의 안전한 종료를 보장하는 것은 아니다. 순차 종료를 보려면 먼저 scale-to-zero를 관찰한다. volumeClaimTemplates는 Pod별 PVC를 만들지만 실제 PV의 동적 생성에는 StorageClass/provisioner 또는 미리 준비한 매칭 PV가 필요하다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe — StatefulSet identity와 PVC 보존

[Local Path Provisioner](../../guides/ADDONS.md#local-path-provisioner)가 설치됐는지 확인한다. `lab-self-local` StorageClass가 **다른 용도로 이미 사용 중이라면 덮어쓰지 않는다.**

```bash
kubectl get storageclass
kubectl get storageclass lab-self-local --ignore-not-found
kubectl apply -f k8s/05-advanced/01-statefulset/extended-setup.yaml
kubectl -n lab-self-storage rollout status statefulset/data --timeout=180s
kubectl -n lab-self-storage get pods,pvc,svc -o wide
kubectl -n lab-self-storage get endpointslices -l kubernetes.io/service-name=data
```

**예상:** `data-0`, `data-1`이라는 안정적인 Pod 이름, 각 Pod에 대응하는 `disk-data-0`, `disk-data-1` PVC가 Bound. Headless Service는 ClusterIP 없이 Pod 주소 발견에 사용된다.

## Break & Diagnose — Pod 삭제와 데이터 보존

```bash
kubectl -n lab-self-storage exec data-0 -- sh -c 'echo data-zero > /data/marker'
kubectl -n lab-self-storage exec data-1 -- sh -c 'echo data-one > /data/marker'
kubectl -n lab-self-storage get pod data-0 -o jsonpath='{.metadata.uid}{"\n"}'
kubectl -n lab-self-storage delete pod data-0 --wait=true
python3 k8s/05-advanced/01-statefulset/wait_for_pod.py lab-self-storage data-0 --timeout 180
kubectl -n lab-self-storage get pod data-0 -o jsonpath='{.metadata.uid}{"\n"}'
kubectl -n lab-self-storage exec data-0 -- cat /data/marker
```

**예상:** UID는 바뀌었지만 Pod 이름과 데이터 `data-zero`는 유지된다. StatefulSet Controller가 안정적 Pod identity를 복원하고, StorageClass/provisioner와 PVC가 데이터 볼륨 연결을 담당한다. 이미 실행한 컨테이너의 메모리에 있던 데이터까지 보존한다고 주장하지 않는다.

## Recover & Observe — Scale-down / Scale-up

```bash
kubectl -n lab-self-storage scale statefulset data --replicas=1
kubectl -n lab-self-storage get pods,pvc
kubectl -n lab-self-storage scale statefulset data --replicas=2
kubectl -n lab-self-storage rollout status statefulset/data --timeout=180s
kubectl -n lab-self-storage get pods,pvc
kubectl -n lab-self-storage exec data-1 -- cat /data/marker
```

**예상:** 기본 `persistentVolumeClaimRetentionPolicy=Retain`에서는 scale-down으로 `data-1` Pod가 사라져도 PVC `disk-data-1`는 남는다. Scale-up하면 같은 PVC에 재연결해 `data-one`을 읽을 수 있다. 이 동작은 데이터베이스 복제/리더 선출과는 별개다.

## Cleanup — PVC와 StorageClass의 범위 확인

```bash
kubectl -n lab-self-storage get pvc
kubectl delete namespace lab-self-storage
kubectl get pv
kubectl get storageclass lab-self-local
```

Namespace 삭제 완료와 PV의 `Delete` reclaim 처리 여부를 확인한다. **이번 Lab에서 새로 만든 전용 StorageClass인지 확인한 후에만** `kubectl delete storageclass lab-self-local`을 실행한다. 공용 Local Path Provisioner Deployment 및 원래 `local-path` Class는 삭제하지 않는다.

## Explain — 완료 기준

1. StatefulSet의 ordinal, headless DNS, stable storage의 차이를 설명한다.
2. Pod 재생성 후 UID 변경과 파일 보존을 증거로 남긴다.
3. scale 2 → 1 → 2 뒤 PVC와 데이터가 유지되는 조건을 설명한다.
4. 어떤 조건에서 PVC가 자동 삭제될 수 있으며 `Retain`과 `Delete` 정책은 각각 무엇에 적용되는지 구분한다.

[공식 StatefulSet 문서](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/).
