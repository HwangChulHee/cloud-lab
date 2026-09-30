# 03. Retain PV로 데이터 복구하기

> 강의 전 예습 · 참고 주제: task-pvpvc · 환경: 기존 클러스터 + worker SSH

기초 연결: [정적 PV/PVC](../../01-core-objects/10-pv-pvc-static/README.md) · [PV 수명주기](../../04-storage-security/02-dynamic-provisioning-pv-lifecycle/README.md)

## 먼저 이해할 것

Deployment 삭제, PVC 삭제, 저장소 데이터 삭제는 서로 다르다. Retain PV는 PVC가 없어져도 데이터를 보존하지만 이전 claimRef가 남으면 자동으로 새 PVC와 연결되지 않는다. 작은 파일로 데이터 보존을 검증하며 DB 설치는 생략한다. local PV는 특정 노드의 디렉터리이므로 nodeAffinity가 필요하다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/03-pv-data-recovery`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

```bash
kubectl get nodes -L kubernetes.io/hostname
```

worker 한 대를 선택해 `pv.yaml`의 `REPLACE_WORKER_HOSTNAME`을 그 노드의 hostname label 값으로 바꾼다. **선택한 worker의 SSH 셸**에서 전용 디렉터리를 만든다.

```bash
sudo mkdir -p /var/tmp/cloud-lab-preview-data
```

kubectl 셸로 돌아와 실행한다.

```bash
kubectl create namespace preview-storage
kubectl apply -f pv.yaml -f pvc.yaml -f workload.yaml
kubectl -n preview-storage rollout status deploy/writer --timeout=120s
kubectl -n preview-storage exec deploy/writer -- cat /data/message
kubectl get pv preview-retained-pv
```

## 2. 직접 바꿔보기

1. Deployment만 삭제한 뒤 다시 배포해 파일이 남는지 확인한다.
2. Deployment를 삭제하고 PVC도 삭제해 PV가 Released로 바뀌는지 본다.
3. 기존 PV를 재사용해 PVC와 Deployment를 복구한다. 새 PV는 만들지 않는다.

```bash
kubectl -n preview-storage delete deploy writer
kubectl -n preview-storage delete pvc data
kubectl get pv preview-retained-pv -o yaml
```

PVC 삭제가 멈추면 아직 이를 사용하는 Pod가 남았는지 확인한다. finalizer를 강제로 지우지 않는다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

```bash
kubectl get pv preview-retained-pv
kubectl -n preview-storage get pvc data
kubectl -n preview-storage exec deploy/writer -- cat /data/message
```

PV/PVC가 Bound이고 파일 내용이 `saved-before-recovery`인지 확인한다. 파일이 새로 생성된 것인지 구분하려면 장애 전 직접 고유 문구로 바꿔두어도 좋다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

이전 PVC가 정말 삭제되고 사용 중인 Pod가 없는 것을 확인한 뒤 claimRef를 해제한다.

```bash
kubectl patch pv preview-retained-pv --type=json \
  -p='[{"op":"remove","path":"/spec/claimRef"}]'
kubectl apply -f pvc.yaml -f workload.yaml
kubectl -n preview-storage rollout status deploy/writer --timeout=120s
```

`storageClassName: ""`는 default StorageClass를 사용하지 않겠다는 뜻이다. 이름만 `local-path`라고 쓴다고 provisioner가 설치되는 것은 아니다.

</details>

## 4. 정리 및 재실행

```bash
kubectl delete namespace preview-storage
kubectl delete pv preview-retained-pv
```

Pod가 모두 사라진 뒤 **선택했던 worker**에서 이 실습의 파일과 빈 디렉터리만 정리한다.

```bash
sudo rm -f /var/tmp/cloud-lab-preview-data/message
sudo rmdir /var/tmp/cloud-lab-preview-data
```

Retain은 호스트 파일까지 삭제해주지 않는다. 재실행은 디렉터리 생성부터 시작한다.

## 강의에서 확인할 질문

- Available, Bound, Released의 차이는?
- 기존 PV 재사용과 새 PV 자동 생성은 어떤 필드로 구분하는가?

[전체 예습 경로](../README.md)
