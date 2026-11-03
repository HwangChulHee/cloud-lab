# 별도 Kubernetes 클러스터 구축 — CKA 관리 실습 환경

> **실행 대상:** 기존 Rocky Linux 8 / Kubernetes 1.27.2 학습 클러스터가 아닌 **새로 만든 폐기 가능한 Ubuntu 24.04 VM 3대**. VM 스냅샷을 먼저 생성한다. kubeadm/etcd/업그레이드 실습은 기존 학습 클러스터에서 절대 진행하지 않는다.

## 0. 버전과 주소 계획

2026-11-03 기준 공식 지원 minor는 **1.35 / 1.36 / 1.37**이며, 본 예제는 학습 환경의 재현성을 위해 **1.36** 패키지 저장소를 사용한다. 실제 설치 가능한 최신 patch를 같은 minor에서 선택하고 control-plane 및 worker의 kubeadm/kubelet 버전을 맞춘다. 다음 설치 전에 [공식 릴리스](https://kubernetes.io/releases/), [kubeadm 설치](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) 문서에서 호환성을 확인한다.

| VM | 역할 | 예시 주소 |
|---|---|---|
| cp1 | Control Plane | 192.168.56.40 |
| worker1 | Worker | 192.168.56.41 |
| worker2 | Worker | 192.168.56.42 |

위 IP는 **예시**다. 실제 NIC/IP, RAM, CPU, 연결성을 점검하고 사용자 VM에 맞게 대체한다. 각 VM은 2 CPU 이상, 충분한 RAM, 서로 통신 가능한 고유 hostname, 인터넷 또는 내부 mirror가 필요하다. VM 주소와 Pod CIDR/Service CIDR이 겹치면 안 된다.

## 1. 모든 VM — OS·커널 준비

각 VM에서 실행한다.

```bash
sudo swapoff -a
sudo modprobe overlay
sudo modprobe br_netfilter
cat <<'EOF' | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
cat <<'EOF' | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF
sudo sysctl --system
free -h
ip -br addr
```

재부팅 후에도 swap이 활성화되는 환경이면 **새 VM에서만** `/etc/fstab`의 swap 항목과 systemd swap 설정을 점검해 영구적으로 비활성화한다. 커널 모듈은 배포판/런타임 및 CNI에 따라 다를 수 있다. VM 방화벽은 무조건 끄지 말고 [필수 포트](https://kubernetes.io/docs/reference/networking/ports-and-protocols/)와 선택한 CNI의 요구 사항을 허용한다.

## 2. 모든 VM — containerd 설치와 CRI 확인

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg containerd
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml >/dev/null
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
sudo systemctl enable --now containerd
sudo systemctl restart containerd
sudo systemctl is-active containerd
sudo grep -n 'SystemdCgroup' /etc/containerd/config.toml
```

`/etc/containerd/config.toml`의 `disabled_plugins`에 `cri`가 있다면 제거한 뒤 재시작한다. kubelet과 containerd의 cgroup driver는 `systemd`로 통일한다. `containerd` 패키지의 CRI 지원 및 실제 socket은 설치 후 확인한다.

## 3. 모든 VM — kubeadm, kubelet, kubectl 설치

```bash
K8S_MINOR=v1.36
sudo mkdir -p /etc/apt/keyrings
curl -fsSL "https://pkgs.k8s.io/core:/stable:/$K8S_MINOR/deb/Release.key" |
  sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/$K8S_MINOR/deb/ /" |
  sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
kubeadm version
kubelet --version
```

멀티라인 파이프는 줄 끝 문법을 유지한다. `kubelet`은 `kubeadm init/join` 전에는 정상 실행되지 않을 수 있다. 이때 서비스 상태만 보고 설치 실패로 결론 내리지 않는다.

## 4. Control Plane(cp1) — init

Pod CIDR은 **선택한 CNI의 설치 설정과 반드시 일치**시킨다. 예시는 VM LAN과 겹치지 않는 Pod CIDR `10.244.0.0/16`을 사용하지만 VM 네트워크와 겹치면 다른 대역을 선택하고 Calico 설정도 함께 바꾼다.

```bash
sudo kubeadm init \
  --apiserver-advertise-address=192.168.56.40 \
  --pod-network-cidr=10.244.0.0/16 \
  --cri-socket=unix:///run/containerd/containerd.sock
mkdir -p "$HOME/.kube"
sudo install -o "$(id -u)" -g "$(id -g)" -m 600 /etc/kubernetes/admin.conf "$HOME/.kube/config"
kubectl get nodes -o wide
kubectl -n kube-system get pods -o wide
```

**예상:** API Server는 응답하나 CNI 미설치 시 Node NotReady/CoreDNS Pending일 수 있다. `kubeadm init`이 출력한 Join 명령과 token은 민감 정보이므로 공개 저장소·스크린샷에 게시하지 않는다.

## 5. CNI 설치 (Control Plane)

[Calico 공식 설치 문서](https://docs.tigera.io/calico/latest/getting-started/kubernetes/quickstart)를 기준으로 **해당 Kubernetes 버전과 호환되는** Calico 릴리스, Operator/CRD와 IPPool을 확인해 적용한다. 임의의 latest YAML을 바로 실행하거나 현재 1.27 실습 VM의 CNI를 제거해서는 안 된다.

### 고정 버전 Calico 설치 예시 (Kubernetes 1.36)

2026-11-03 기준 Calico 공식 가이드의 **v3.33.0** Operator/CRD 방식이다. 다른 Kubernetes minor에서는 공식 호환표와 manifest를 다시 확인한다. 처음 설치하는 **새 1.36 클러스터에서만** 진행한다.

```bash
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.33.0/manifests/v3_projectcalico_org.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.33.0/manifests/tigera-operator.yaml
curl -fsSLo /tmp/calico-custom-resources.yaml \
  https://raw.githubusercontent.com/projectcalico/calico/v3.33.0/manifests/custom-resources.yaml
sed -i 's@cidr: 192.168.0.0/16@cidr: 10.244.0.0/16@' /tmp/calico-custom-resources.yaml
grep -nE 'cidr:|encapsulation:|ipPools:' /tmp/calico-custom-resources.yaml
```

**필수 검토:** Calico 다운로드 매니페스트의 기본 CIDR `192.168.0.0/16`을 아래 명령으로 `10.244.0.0/16`으로 바꾼다. 이후 `/tmp/calico-custom-resources.yaml`의 `Installation.spec.calicoNetwork.ipPools` CIDR이 `kubeadm init --pod-network-cidr`와 동일한지 확인한다. 다르면 파일을 수정한 뒤에만 적용한다. VM LAN/Service 네트워크와 겹치면 안 된다. 이 예제는 `10.244.0.0/16`을 가정한다.

```bash
kubectl apply -f /tmp/calico-custom-resources.yaml
kubectl get tigerastatus
kubectl -n calico-system get pods -o wide
```

Operator, Calico node, 네트워크 구성요소가 준비될 때까지 기다리고 Conditions/Events를 확인한다. 배포가 실패하면 CRD, Operator 로그, IPPool CIDR을 우선 확인한다. 한편 기존 1.27 Calico 설정을 이것으로 덮어쓰지 않는다.

CNI 설치가 끝나면:

```bash
kubectl get nodes -o wide
kubectl get pods -n kube-system -o wide
kubectl get pods -A -o wide
```

CNI가 준비되기 전의 NotReady와 준비 후 Ready를 기록하고, 실패 시 `kubectl describe node`, kubelet journal, CNI Pod Events를 순서대로 확인한다.

## 6. Worker — Join

cp1에서 `kubeadm token create --print-join-command`로 현재 유효한 join 명령을 생성한다. Worker에서 그 명령에 `--cri-socket unix:///run/containerd/containerd.sock`을 붙여 실행한다. 외부 문서의 토큰·CA 해시를 복사해 쓰지 않는다.

```bash
# cp1
kubeadm token create --print-join-command

# 두 Worker에서 각각 위 출력값을 검증해 sudo로 실행
# sudo kubeadm join ... --cri-socket unix:///run/containerd/containerd.sock

# cp1
kubectl get nodes -o wide
kubectl -n kube-system get pods -o wide
```

**예상:** 3개 Node Ready, CoreDNS Ready. 이후 테스트 Deployment/Service를 생성해 같은 노드와 다른 노드 간 Pod 통신을 검증한다.

## 7. 증거·오류·복구

| 장애 | 1차 확인 | 복구 범위 |
|---|---|---|
| kubeadm preflight 실패 | swap, CRI socket, 포트, hostname | OS/CRI 설정 수정 후 재시도 |
| init 이후 Node NotReady | kubelet journal, CNI 설치/Pod CIDR | CNI 구성 수정 |
| join timeout | cp1:6443 TCP 연결, token, CA hash | 연결/토큰 복구 |
| CoreDNS Pending | Node Ready, CNI Pod 상태, taint | CNI 및 스케줄링 상태 수정 |
| 새 Pod가 Running인데 HTTP 실패 | Pod IP, Service EndpointSlice, kube-proxy/CNI | 실제 문제 계층만 수정 |

각 단계마다 **예상 출력 → 실제 출력 → 가설 → 수정 → 재확인**을 기록한다. 성공 판단은 `kubectl get nodes`뿐 아니라 DNS와 크로스 노드 통신까지 포함한다.

## 8. 이후 관리 실습

- [ADM-01 kubeadm bootstrap](../10-cluster-admin/01-kubeadm-bootstrap/README.md)
- [ADM-02 etcd Snapshot/Restore](../10-cluster-admin/02-etcd-backup-restore/README.md)
- [ADM-03 kubeadm Upgrade](../10-cluster-admin/03-kubeadm-upgrade/README.md)
- [ADM-04 CNI 및 네트워크](../10-cluster-admin/04-cni-cluster-network/README.md)

etcd 복원·kubeadm 업그레이드·HA는 **VM snapshot을 복원할 수 있는 별도 연습 환경**에서 수행한다. 이 문서는 설치 재현 가이드이며 모든 버전·CNI 조합의 실기 검증을 마쳤다는 의미는 아니다.
