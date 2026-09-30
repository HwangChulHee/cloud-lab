# 확장·플랫폼 경로 — 기본 과정 이후에 진행하기

기본 8단계는 기존 클러스터에서 앱의 실행과 진단을 익히는 경로다. 아래는 별도 VM의 설치·제어 평면·Gateway/Helm까지 이어가는 경로다. 모든 확장을 먼저 설치하고 시작할 필요는 없다. 기본 8단계의 완료와 이 경로의 완료는 별도로 기록한다.

## 1. 별도 클러스터의 준비 조건

Ubuntu 22.04 VM 세 개를 준비한다. control-plane은 2 CPU/4GiB, worker는 각각 2 CPU/3GiB 이상을 시작 기준으로 하고, 호스트가 부족하면 기존 VM을 정지한 후 새 VM을 만든다. SSH/인터넷 연결, 노드 사이 통신과 시간 동기화를 확인한다.

| 역할 | 예시 호스트 이름 | 예시 노드 IP |
|---|---|---|
| control-plane | modern-control | 192.168.56.40 |
| worker 1 | modern-worker1 | 192.168.56.41 |
| worker 2 | modern-worker2 | 192.168.56.42 |

주소가 기존 VM/호스트/VPN과 겹치면 다른 주소를 선택한다. Pod CIDR은 `10.244.0.0/16`, Service CIDR은 `10.96.0.0/12`를 예시로 사용하되 실제 라우팅과 겹치지 않아야 한다. 노드의 192.168.56.0/24를 Pod CIDR에 포함하지 않는다.

VM 생성은 VirtualBox의 새 Ubuntu VM 또는 본인이 사용하는 Vagrant 방식으로 한다. 기존 Rocky 클러스터에 아래 OS 명령을 실행하지 않는다. 새 Ubuntu VM이 있고 SSH할 수 있는 시점부터 아래 절차는 강의 없이 진행할 수 있다.

## 2. 새 VM 세 곳 모두: OS와 containerd 준비

노드별 hostname과 IP를 앞 표대로 설정한 상태에서 진행한다. 아래 containerd 설정 생성은 **새 VM에서만** 실행한다.

```bash
sudo swapoff -a
sudo sed -i '/[[:space:]]swap[[:space:]]/s/^/#/' /etc/fstab
sudo apt-get update
sudo apt-get install -y containerd curl ca-certificates gpg git openssl python3 python3-yaml
sudo modprobe overlay
sudo modprobe br_netfilter
printf 'overlay\nbr_netfilter\n' | sudo tee /etc/modules-load.d/cloud-lab.conf
cat <<'SYSCTL' | sudo tee /etc/sysctl.d/99-cloud-lab.conf
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward = 1
SYSCTL
sudo sysctl --system
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml > /dev/null
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
sudo systemctl enable --now containerd
sudo systemctl restart containerd
sudo systemctl status containerd --no-pager
```

containerd가 active이고 CRI가 활성화된 default config인지 확인한다. kubelet은 systemd cgroup driver를 사용하므로 런타임과 맞춘다.

## 3. 새 VM 세 곳 모두: Kubernetes 패키지

자료와 맞춘 1.34.2를 실습용으로 고정한다. 운영 버전 선택을 대신하는 값은 아니다. apt-cache 결과에 해당 패키지가 없으면 임의로 다른 minor를 섞지 말고 저장소/네트워크를 확인한다.

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.34/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
printf 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.34/deb/ /\n' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
apt-cache madison kubeadm
sudo apt-get install -y kubelet=1.34.2-1.1 kubeadm=1.34.2-1.1 kubectl=1.34.2-1.1
sudo apt-mark hold kubelet kubeadm kubectl
sudo systemctl enable --now kubelet
# 각 VM에서 그 VM의 실제 host-only IP로 바꾼다.
MODERN_NODE_IP=REPLACE_THIS_NODE_IP
printf 'KUBELET_EXTRA_ARGS=--node-ip=%s\n' "$MODERN_NODE_IP" | sudo tee /etc/default/kubelet
sudo systemctl restart kubelet
```

초기화 전 kubelet이 반복 재시작하는 것은 설정이 아직 없기 때문일 수 있다. runtime 상태와 로그를 함께 본다.

## 4. control-plane 한 곳: 초기화

actual node IP를 확인한 뒤 실행한다. 여러 NIC가 있으면 advertise address와 kubelet node IP가 실제 host-only 네트워크인지 확인한다.

```bash
ip -br address
sudo kubeadm init --kubernetes-version v1.34.2 \
  --apiserver-advertise-address=192.168.56.40 \
  --pod-network-cidr=10.244.0.0/16 --service-cidr=10.96.0.0/12 \
  --cri-socket=unix:///var/run/containerd/containerd.sock
mkdir -p "$HOME/.kube"
sudo install -m 600 -o "$(id -u)" -g "$(id -g)" /etc/kubernetes/admin.conf "$HOME/.kube/config"
sudo kubeadm token create --print-join-command
cat <<'CRI' | sudo tee /etc/crictl.yaml
runtime-endpoint: unix:///var/run/containerd/containerd.sock
image-endpoint: unix:///var/run/containerd/containerd.sock
timeout: 10
CRI
sudo crictl info
```

출력된 join 명령을 **두 worker의 SSH 셸**에서 sudo로 실행한다. 토큰은 저장소에 올리지 않는다. 출력의 IP/해시를 임의로 외운 값으로 대체하지 않는다. 여러 NIC에서 node IP가 NAT 주소로 잡히면 각 VM의 `/etc/default/kubelet`에 `KUBELET_EXTRA_ARGS=--node-ip=실제노드IP`를 설정하고 kubelet을 재시작해 INTERNAL-IP를 확인한다.

control-plane에서 레포를 clone하고 [14 CNI 설치](../07-cka-preview/14-cni-install/README.md)를 실행한다. 선택한 Pod CIDR 10.244.0.0/16을 Installation에 넣는다. CNI 설치 전에 Node NotReady/CoreDNS Pending이 생길 수 있다. CNI 설치 후 **3개 Node Ready, CoreDNS Ready, 다른 노드 Pod 연결**을 확인한다. 08 NetworkPolicy의 frontend 허용/other 차단도 실행한다. 14의 선행 조건은 08의 개념 이해이며, CNI가 없는 상태에서 08을 먼저 성공시킬 필요는 없다.

스냅샷은 OS/runtime 준비 후와 CNI 설치 완료 후에 각각 만든다. 이후 09 장애 복구는 이 별도 클러스터에서만 수행한다.

## 5. Helm과 Gateway 준비

control-plane의 Linux 셸에서 Helm 3와 Python/PyYAML을 준비한다. 아래는 amd64 VM용이다. 다른 아키텍처면 그 플랫폼의 공식 배포 파일을 사용한다.

```bash
HELM_TMP=$(mktemp -d)
curl -fsSL https://get.helm.sh/helm-v3.16.4-linux-amd64.tar.gz -o "$HELM_TMP/helm.tar.gz"
curl -fsSL https://get.helm.sh/helm-v3.16.4-linux-amd64.tar.gz.sha256sum -o "$HELM_TMP/helm.sha256"
HELM_EXPECTED=$(awk '{print $1}' "$HELM_TMP/helm.sha256")
printf '%s  %s\n' "$HELM_EXPECTED" "$HELM_TMP/helm.tar.gz" | sha256sum -c -
tar -xzf "$HELM_TMP/helm.tar.gz" -C "$HELM_TMP"
sudo install -m 755 "$HELM_TMP/linux-amd64/helm" /usr/local/bin/helm
helm version
rm -rf "$HELM_TMP"
unset HELM_TMP HELM_EXPECTED
```

checksum이 실패하면 tar/install로 넘어가지 않는다. [13 Helm/Argo CD](../07-cka-preview/13-helm-argocd/README.md)는 Chart/values/CRD/render→install을 실제로 비교하며 강의 영상 없이 해당 순서를 따라 진행한다.

Gateway는 **새 1.34 클러스터**에서 CRD와 Controller를 함께 준비한다. 기존 Gateway CRD/Controller가 있으면 아래 설치를 덮어쓰지 않고 [환경 안내](../07-cka-preview/ENVIRONMENT.md)의 호환성을 대조한다. 공식 호환표에 있는 학습용 고정 조합은 Gateway API 1.4.1 / NGINX Gateway Fabric 2.3.0이다.

```bash
kubectl apply --server-side -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.4.1/standard-install.yaml
helm install ngf oci://ghcr.io/nginx/charts/nginx-gateway-fabric \
  --version 2.3.0 --namespace nginx-gateway --create-namespace
kubectl -n nginx-gateway get pods
kubectl get gatewayclass
```

기본 GatewayClass 이름/Accepted condition을 확인한다. [07 Gateway 전환](../07-cka-preview/07-gateway-migration/README.md)의 REPLACE_GATEWAY_CLASS를 실제 값으로 바꾼다. LoadBalancer 외부 IP가 없는 VM에서는 문서대로 해당 Gateway 데이터 평면 Service를 찾아 port-forward한다. 기본 08에서 사용한 Traefik도 이 클러스터에 설치하면 old Ingress를 lab-traefik으로 비교할 수 있다. 같은 이름의 다른 클러스터 리소스와 혼동하지 않도록 매번 current-context를 확인한다.

## 6. 확장 순서와 완료 조건

| 순서 | 실습 | 먼저 끝낼 것 | 완료 증거 |
|---:|---|---|---|
| 1 | [14 CNI](../07-cka-preview/14-cni-install/README.md) → [08 정책](../07-cka-preview/08-networkpolicy/README.md) | 위 bootstrap | 3개 Node/CoreDNS Ready, 정책 양성/음성 테스트 |
| 2 | [09 제어 평면 복구](../07-cka-preview/09-control-plane-recovery/README.md) | 정상 상태 스냅샷, crictl endpoint | SSH/CRI 로그로 복구, readyz/핵심 Pod 정상 |
| 3 | [13 Helm](../07-cka-preview/13-helm-argocd/README.md) | 기본 Controller/RBAC, Helm/PyYAML | render와 설치 리소스, CRD 생성 on/off 비교 |
| 4 | [07 Gateway](../07-cka-preview/07-gateway-migration/README.md) | HTTP/TLS, Gateway 준비 | Accepted/ResolvedRefs/Programmed와 실제 HTTPS |
| 5 | [15 CRI](../07-cka-preview/15-cri-linux-preparation/README.md) | 별도 Ubuntu VM과 해당 실습의 Docker/패키지 | CRI endpoint에 crictl 응답, bridge/IP forwarding |

15는 이미 containerd로 동작하는 클러스터의 런타임을 교체하는 과정이 아니다. 패키지 입수·OS/아키텍처 확인은 해당 문서의 선행 조건이다. 처음에는 위 containerd bootstrap으로 CRI 역할을 익히고, Docker adapter 비교가 필요할 때 별도 VM의 15를 수행한다.

## Canary는 Gateway 확장으로 진행

07의 TLS route를 정상 검증한 뒤 [Canary 가중치 비교](./CANARY.md)를 실행한다. 이전 ingress-nginx annotation 과제와 현대 Gateway 과제를 필수 순서에 함께 넣지 않는다. header 기반과 비율 기반 분할의 목적을 나눠 설명한다.

## 정리와 남은 범위

각 확장 문서의 namespace/CRD/Helm release 정리를 먼저 수행한다. 직접 만든 VM을 더 쓰지 않으면 VirtualBox/Vagrant에서 해당 **새 VM만** 삭제한다. 기존 기초 클러스터는 유지한다. 이 경로는 HA control-plane, kubeadm upgrade, etcd snapshot restore 전체 과정을 포함하지 않는다. 강의 없이 실행할 수 있는 범위와 CKA 전체 대비 범위는 구분한다.

공식 참고: [kubeadm 설치](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/), [클러스터 생성](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/), [container runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes/), [Helm 설치](https://helm.sh/docs/intro/install/), [NGF 설치](https://docs.nginx.com/nginx-gateway-fabric/install/helm/).

[독립 학습 순서](./README.md)
