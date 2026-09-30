# 09. 제어 평면 장애를 호스트에서 복구하기

> 강의 전 예습 · 참고 주제: task-core_components · 환경: 읽기 관찰은 기존 클러스터 / 장애 주입은 폐기 가능한 kubeadm VM

기초 연결: [클러스터 기준선](../../00-foundation/01-cluster-verification/README.md) · [아키텍처 관찰](../../06-architecture/01-architecture-observability-capstone/README.md)

## 먼저 이해할 것

API Server가 내려가면 kubectl만으로 진단할 수 없다. kubelet 로그, CRI 컨테이너 로그, static Pod manifest를 호스트에서 확인해야 한다. 이 예습은 etcd 데이터 자체를 훼손하지 않고 API Server의 연결 설정만 틀리게 만든다. 외부 etcd 주소도 암기한 IP로 바꾸지 않고 실제 endpoint·인증서 설정에서 찾는다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/09-control-plane-recovery`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

기존 클러스터에서는 아래 정상 상태 관찰까지만 진행할 수 있다.

```bash
kubectl get nodes
kubectl -n kube-system get pods -o wide
kubectl get --raw='/readyz?verbose'
```

이후는 **스냅샷을 만든 폐기 가능한 kubeadm control-plane VM의 SSH 셸**에서 진행한다. crictl endpoint가 설정돼 있어야 한다.

```bash
sudo crictl ps -a
sudo journalctl -u kubelet -n 50 --no-pager
sudo cat /etc/kubernetes/manifests/kube-apiserver.yaml
sudo cat /etc/kubernetes/manifests/etcd.yaml
sudo install -d -m 700 /var/tmp/cloud-lab-control-backup
sudo cp -a /etc/kubernetes/manifests/kube-apiserver.yaml /var/tmp/cloud-lab-control-backup/
```

기존 backup이 있으면 먼저 이전 실습이 복구됐는지 확인한다. backup은 manifests 디렉터리 밖에 둔다. static Pod 디렉터리에 백업 파일을 넣으면 kubelet이 그것도 읽을 수 있다. 외부 etcd이면 etcd.yaml이 없을 수 있으므로 실제 서버의 listen/advertise 주소와 인증서를 별도로 확인한다.

## 2. 직접 바꿔보기

폐기 VM에서만 API Server manifest의 `--etcd-servers`를 `https://127.0.0.1:12379`로 바꾼다. 원래 값을 기록한다.

```bash
sudo vi /etc/kubernetes/manifests/kube-apiserver.yaml
```

1. kubectl 요청 실패와 API Server 컨테이너 로그를 확인한다.
2. kubelet이 manifest 변경을 감지했는지 본다.
3. 잘못된 endpoint를 실제 설정에 맞게 복구한다.
4. 인증서 경로, scheme, 포트도 점검한다. etcd data directory는 변경하지 않는다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

```bash
kubectl get --raw='/readyz?verbose'
kubectl get nodes
kubectl -n kube-system get pods
```

복구 후 readyz 성공, 노드 Ready, 핵심 컴포넌트 정상 실행을 확인한다. 실습 전부터 있던 문제와 이번 장애를 구분한다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

kubectl이 실패하면 **VM SSH 셸**에서 진단한다.

```bash
sudo crictl ps -a --name kube-apiserver
sudo crictl logs CONTAINER_ID
sudo journalctl -u kubelet -n 100 --no-pager
```

CONTAINER_ID는 바로 위 결과의 실제 ID로 바꾼다. 잘못된 etcd 주소로 connection refused 등이 발생하는지 확인한다. 복구가 막히면 API를 쓰지 않고 원본을 복사한다.

```bash
sudo cp -a /var/tmp/cloud-lab-control-backup/kube-apiserver.yaml /etc/kubernetes/manifests/kube-apiserver.yaml
sudo systemctl status kubelet --no-pager
```

정상 kubelet은 변경을 자동 감지한다. 자동 반영이 안 되면 로그·서비스 상태를 먼저 확인하고 필요한 경우 `sudo systemctl restart kubelet`을 실행한다.

</details>

## 4. 정리 및 재실행

정상 상태를 확인한 뒤 호스트 backup만 삭제한다.

```bash
sudo rm -f /var/tmp/cloud-lab-control-backup/kube-apiserver.yaml
sudo rmdir /var/tmp/cloud-lab-control-backup
```

복구가 실패했으면 backup을 지우지 않고 VM 스냅샷으로 되돌린다. 기존 학습 클러스터에는 장애를 주입하지 않는다.

## 강의에서 확인할 질문

- API Server가 안 뜰 때 kubectl 대신 어떤 경로로 로그를 읽는가?
- localhost:2379가 모든 클러스터에서 정답일 수 없는 이유는?

[전체 예습 경로](../README.md)
