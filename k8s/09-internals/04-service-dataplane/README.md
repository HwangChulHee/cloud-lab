# INT-04 Service와 kube-proxy 데이터 경로

> 분류: **운영 심화** · 연결/선행: **04 완료 후** · [기본 학습](../../08-independent/README.md) · [환경 기준](../../07-cka-preview/ENVIRONMENT.md)

## Overview — 왜 배우는가?

Service/EndpointSlice 제어 경로와 커널 기반 패킷 전달을 구분한다. 기존의 관련 실습과 연결해, 객체 조회에 그치지 않고 **컴포넌트의 판단 → Linux/Runtime의 실행 → 상태·로그·이벤트 증거**를 이어서 설명한다.

## 선수 지식과 동작 원리

먼저 kube-proxy 존재·proxyMode·CNI 대체 여부를 확인한다. kube-proxy iptables 모드면 커널의 netfilter가 Service DNAT를 실행하고 conntrack이 연결 상태를 유지한다. kube-proxy는 각 패킷을 사용자 공간으로 중계하지 않는다.

## 예측 후 관찰

실행 전에 (1) 예상 상태, (2) 이 상태를 책임지는 컴포넌트, (3) 검증할 증거를 먼저 적는다. 아래 명령은 Linux/bash 셸에서 실행한다. 리소스가 이미 만들어져 있어야 하는 명령은 연결된 이전 단계를 먼저 수행한다.

```bash
kubectl -n kube-system get ds kube-proxy
kubectl -n kube-system get cm kube-proxy -o yaml
kubectl -n lab-self-network get svc,endpointSlices
sudo iptables-save -t nat | grep -E 'KUBE-SVC|KUBE-SEP' | head -20
sudo conntrack -L | head
```

출력이 비어 있거나 오류가 나면 도구 부재·리소스 미준비·실제 장애를 구분한다. 비어 있는 값이나 실패를 정상 동작의 증거로 사용하지 않는다.

## 장애 가설 → 증거 → 복구

Service selector를 잘못 설정해 EndpointSlice 변화를 확인하고 curl/wget 실패를 비교한 뒤 복구한다. 기존 04의 실습을 재사용한다.

가설과 관찰 결과가 일치하는지 기록하고, 최소한의 변경으로 복구한 뒤 **처음과 같은 명령/요청**으로 성공을 확인한다. 이 문서는 안전한 관찰 순서가 기본이며, 위험한 장애 주입은 명시한 별도 VM에서만 수행한다.

## 환경 제약 및 정리

iptables-save/conntrack은 별도 설치가 필요할 수 있다. iptables 모드가 아니면 이 출력이 필수 성공 조건이 아니다. IPVS는 최신 버전에서 deprecated, nftables 모드는 최신 환경에서만 별도 비교한다.

- Kubernetes 1.27.2에서 실제 실행한 내용과 최신 버전의 공식 설명을 구분한다.
- 이 문서 작성만으로 사용자 VM 실행 완료를 뜻하지 않는다.
- 실습 완료 기록: [CHECKPOINTS](../../08-independent/CHECKPOINTS.md).

## 설명 질문

1. 이 상태는 어떤 컴포넌트가 만들거나 갱신하는가?
2. 정상과 장애를 구분하는 가장 작은 증거는 무엇인가?
3. 같은 증상이 다른 계층에서도 발생할 수 있다면 어떻게 반증할까?

## 공식 문서

- [Kubernetes Architecture](https://kubernetes.io/docs/concepts/architecture/)
- [Service virtual IP](https://kubernetes.io/docs/reference/networking/virtual-ips/)
- [kubeadm upgrade](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)

[모듈 목차](../README.md) · [독립 학습](../../08-independent/README.md)
