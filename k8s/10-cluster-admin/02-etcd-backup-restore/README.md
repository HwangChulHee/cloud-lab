# ADM-02 etcd Snapshot/Restore

> 분류: **CKA 필수** · 연결/선행: **ADM-01** · [기본 학습](../../08-independent/README.md) · [환경 기준](../../07-cka-preview/ENVIRONMENT.md)

## Overview — 왜 배우는가?

etcd 저장 상태의 백업/복원과 실제 워크로드 데이터 복원을 구분한다. 기존의 관련 실습과 연결해, 객체 조회에 그치지 않고 **컴포넌트의 판단 → Linux/Runtime의 실행 → 상태·로그·이벤트 증거**를 이어서 설명한다.

## 선수 지식과 동작 원리

별도 kubeadm VM에서 etcdctl API=3 snapshot save 후 snapshot status를 확인한다. 복구는 기존 snapshot/데이터 디렉터리를 보존하고 etcdutl snapshot restore로 별도 data-dir을 생성한 뒤 etcd static Pod manifest의 data-dir 연결을 안전하게 전환한다.

## 예측 후 관찰

실행 전에 (1) 예상 상태, (2) 이 상태를 책임지는 컴포넌트, (3) 검증할 증거를 먼저 적는다. 아래 명령은 Linux/bash 셸에서 실행한다. 리소스가 이미 만들어져 있어야 하는 명령은 연결된 이전 단계를 먼저 수행한다.

```bash
kubectl -n kube-system get pods -l component=etcd -o wide
sudo ls -l /etc/kubernetes/pki/etcd
sudo grep -E 'listen-client-urls|cert-file|key-file' /etc/kubernetes/manifests/etcd.yaml
```

출력이 비어 있거나 오류가 나면 도구 부재·리소스 미준비·실제 장애를 구분한다. 비어 있는 값이나 실패를 정상 동작의 증거로 사용하지 않는다.

## 장애 가설 → 증거 → 복구

Snapshot 전후에 학습용 ConfigMap을 생성해 복원 시점에 따른 객체 상태를 확인한다. restore 직후 control plane 정상성과 kube-system Pod Ready를 검증한다.

가설과 관찰 결과가 일치하는지 기록하고, 최소한의 변경으로 복구한 뒤 **처음과 같은 명령/요청**으로 성공을 확인한다. 이 문서는 안전한 관찰 순서가 기본이며, 위험한 장애 주입은 명시한 별도 VM에서만 수행한다.

## 환경 제약 및 정리

원격 접속이 끊길 수 있다. VM 스냅샷과 복구 경로 확보 후 전용 환경에서만 실행. 인증서·endpoint는 실제 etcd manifest에서 추출한다. 이 문서는 절차 개요이며 실제 데이터 경로/버전별 명령은 공식 etcd 복원 문서와 대조한다.

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
