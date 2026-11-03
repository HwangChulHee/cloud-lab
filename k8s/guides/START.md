# 시작 준비 — 이미 만든 3노드 클러스터에서 출발하기

이 기본 과정은 레포에 기록된 Windows + Vagrant의 Kubernetes 1.27.2/containerd 클러스터에서 출발한다. 강의 영상이나 원본 PDF가 필요하지 않다. 새 1.34 클러스터를 만들고 싶다면 [플랫폼 준비](./PLATFORM.md)를 사용한다. 기본 과정을 시작하기 위해 기존 클러스터를 업그레이드하지 않는다.

## 실행 위치를 먼저 정하기

Windows PowerShell에서 사용 중인 Vagrant 프로젝트 폴더로 이동한 뒤 `vagrant ssh master-node`로 들어간다. VM 이름이 다르면 `vagrant status`에 나온 이름을 사용한다. 이후 bash/kubectl 명령은 이 Linux 셸에서 실행한다. worker 작업이라고 표시한 것만 별도의 worker SSH 셸에서 실행한다.

관리자 kubeconfig를 아직 준비하지 않았다면 아래를 실행한다. 기존 config가 있으면 복사 단계를 건너뛰고 그 context를 확인한다.

```bash
mkdir -p "$HOME/.kube"
test ! -e "$HOME/.kube/config" && sudo install -m 600 -o "$(id -u)" -g "$(id -g)" /etc/kubernetes/admin.conf "$HOME/.kube/config"
kubectl config current-context
kubectl get nodes -o wide
kubectl -n kube-system get pods -o wide
command -v git curl openssl python3
```

3개 노드가 Ready이고 CoreDNS가 Running/Ready여야 한다. NotReady면 먼저 `kubectl describe node NODE_NAME`과 kube-system Events를 확인한다. namespace만 바꿔도 해결되는 문제라고 가정하지 않는다. 도구가 없으면 Rocky의 `sudo dnf install -y git curl openssl python3`, Ubuntu의 `sudo apt-get install -y git curl openssl python3`를 해당 OS에서 사용한다.

## 저장소 준비

Linux VM에 저장소가 없을 때만 clone한다. 이미 있으면 해당 저장소에서 현재 변경 사항을 확인한 뒤 `git pull --ff-only`로 업데이트한다. 아래 `cd cloud-lab` 이후 경로가 모든 기본 실습의 작업 기준이다.

```bash
git clone https://github.com/HwangChulHee/cloud-lab.git
cd cloud-lab
pwd
ls k8s/08-independent
```

Pod 생성은 API Server의 승인·저장, Controller의 원하는 상태 조정, scheduler의 노드 선택, kubelet/runtime의 실행으로 이어진다. 독립 Pod는 Controller의 개수 복구 대상이 아니다. [개념 지도](../07-cka-preview/CONCEPT_BRIDGE.md)의 1번 표로 구성 요소 역할을 먼저 읽는다.

Pod/Service 실습은 아직 Metrics Server·Ingress·동적 스토리지가 필요 없다. [애드온 준비](./ADDONS.md)는 06 저장소와 08 운영 단계에 도착했을 때 진행한다. 이미 설치된 애드온은 재사용한다.

## 실습 입력값

- `REPLACE_WORKER_HOSTNAME`: `kubectl get nodes -L kubernetes.io/hostname`의 worker label 값. node 이름과 label 값이 같다고 암묵적으로 가정하지 않는다.
- `NODE_IP:NODE_PORT`: 실제 INTERNAL-IP와 Service의 nodePort. PowerShell에서 호출할 때는 `curl.exe`를 사용한다.
- `POD_NAME`, `CONTAINER_ID`: 바로 앞 조회에서 찾은 실제 이름/ID.
- port-forward 요청은 port-forward를 실행한 **같은 머신**의 두 번째 셸에서 한다. 기본 주소는 localhost다.

## 첫 실행에서 확인할 것

[01 Pod](./01-pods/README.md)의 Ready 대기가 실패하면 `kubectl -n lab-self-pods describe pod pair`를 확인한다. 이미지 pull, CNI, 배치, init container 실패를 구분하고 원인을 해결한 뒤 다시 대기한다. 문서의 timeout은 성공을 대신하지 않는다. 명령은 코드 블록별로 실행하고 예상 결과를 확인한 뒤 다음 블록으로 넘어간다. 의도한 실패라고 적힌 명령을 제외하고 오류나 timeout이 나오면 진행을 멈추고 원인을 해결한다. watch/port-forward는 안내된 시점에 Ctrl+C로 종료하거나 별도 셸에서 유지한다.

`lab-self-*` 이름과 `cloud-lab/self-study` taint key는 이 과정 전용이다. 같은 이름의 기존 리소스가 있다면 이전 실습이 정리됐는지 확인하고 기존 목적을 모르는 리소스를 덮어쓰지 않는다. 강제로 시스템 리소스를 삭제할 필요는 없다.

[독립 학습 순서](./README.md)
