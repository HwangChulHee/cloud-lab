# 15. CRI와 Linux 네트워크 매개변수 준비

> 독립 실행 가능한 확장 실습 · 참고 주제: task-cri · 환경: 별도 Ubuntu 22.04 VM + Docker + 로컬 cri-dockerd 패키지

기초 연결: [클러스터 runtime 확인](../../00-foundation/01-cluster-verification/README.md)

[독립 과정에서의 위치](../../08-independent/PLATFORM.md). 처음에는 예시 풀이를 참고해 구축하고, 두 번째에는 요구사항만 보고 실행한다. 강의 수강은 선행 조건이 아니다.

## 먼저 이해할 것

Docker API와 Kubernetes CRI는 다르다. cri-dockerd는 Docker를 CRI에 연결하는 어댑터다. containerd를 사용하는 기존 노드를 바꾸는 실습이 아니라 별도 Linux VM을 준비하는 실습이다. `.deb`/dpkg는 Ubuntu 계열이며 Rocky Linux에는 그대로 적용할 수 없다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/15-cri-linux-preparation`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

폐기 가능한 Ubuntu VM에서 스냅샷을 만든다. Docker 설치 및 실행을 확인하고 공식 배포의 Ubuntu 22.04/amd64용 cri-dockerd `.deb`를 VM에 준비한다. 자료의 파일 이름을 실제 존재하는 패키지로 착각하지 않는다.

```bash
cat /etc/os-release
uname -m
sudo systemctl status docker --no-pager
ls ~/cri-dockerd*.deb
sysctl net.ipv4.ip_forward net.ipv6.conf.all.forwarding net.netfilter.nf_conntrack_max
lsmod | grep br_netfilter
```

Docker나 패키지가 없으면 [cri-dockerd 공식 설치 안내](https://github.com/Mirantis/cri-dockerd)에서 OS/아키텍처에 맞게 준비한다. 설치 전과 후 패키지·sysctl 상태를 기록한다.

## 2. 직접 바꿔보기

1. 준비한 `.deb`를 dpkg로 설치한다.
2. 패키지가 제공하는 실제 systemd unit 이름을 확인하고 service/socket을 활성화한다.
3. br_netfilter 모듈을 현재와 재부팅 후에도 로드하게 한다.
4. 아래 네 값을 설정하고 실제 조회로 검증한다.

| 매개변수 | 값 |
|---|---:|
| net.bridge.bridge-nf-call-iptables | 1 |
| net.ipv6.conf.all.forwarding | 1 |
| net.ipv4.ip_forward | 1 |
| net.netfilter.nf_conntrack_max | 131072 |

노드 join이나 기존 runtime 교체는 하지 않는다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

```bash
sudo systemctl status cri-docker.service cri-docker.socket --no-pager
lsmod | grep br_netfilter
sysctl net.bridge.bridge-nf-call-iptables
sysctl net.ipv6.conf.all.forwarding
sysctl net.ipv4.ip_forward
sysctl net.netfilter.nf_conntrack_max
sudo crictl --runtime-endpoint unix:///var/run/cri-dockerd.sock info
```

unit 이름과 socket 경로는 설치된 패키지의 `systemctl cat`에서 확인한다. 네 값의 실제 조회와 CRI info 응답을 확인한다. 네트워크 플러그인을 설치하지 않은 VM이면 RuntimeReady와 NetworkReady를 구분한다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

파일명을 확인하고 **한 개의 실제 패키지**를 지정해 설치한다. 예:

```bash
sudo dpkg -i ~/cri-dockerd_0.3.9.3-0.ubuntu-jammy_amd64.deb
sudo systemctl list-unit-files 'cri-docker*'
sudo systemctl enable --now cri-docker.socket cri-docker.service
sudo modprobe br_netfilter
printf '%s\n' br_netfilter | sudo tee /etc/modules-load.d/cloud-lab-preview.conf
cat <<'EOF' | sudo tee /etc/sysctl.d/99-cloud-lab-preview.conf
net.bridge.bridge-nf-call-iptables=1
net.ipv6.conf.all.forwarding=1
net.ipv4.ip_forward=1
net.netfilter.nf_conntrack_max=131072
EOF
sudo sysctl --system
```

패키지의 실제 unit 이름이 다르면 그 이름을 사용한다. 의존성 설치 오류가 나면 dpkg 출력에서 필요한 패키지를 확인한다. 파일 저장 성공과 커널 값 적용 성공은 별도 검증이다.

</details>

## 4. 정리 및 재실행

전용 VM을 설치 전 스냅샷으로 복원한다. 설정 파일만 지워도 이미 바뀐 커널 값과 활성화한 서비스는 자동 원복되지 않는다. 기존 학습 클러스터의 runtime이나 sysctl은 수정하지 않는다.

## 스스로 설명할 질문

- runtime socket이 응답하는 것과 Pod 네트워크가 준비된 것은 어떻게 다른가?
- modprobe 없이 bridge sysctl을 적용할 때 어떤 오류가 생길 수 있는가?

[전체 확장 경로](../README.md)
