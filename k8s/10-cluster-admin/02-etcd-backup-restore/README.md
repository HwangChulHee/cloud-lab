# etcd snapshot·restore·검증

> 분류: **CKA 필수** · 선수 학습: [독립 학습](../../08-independent/README.md)의 ADM-01 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

etcd는 Kubernetes API 상태 저장소이며 PersistentVolume 내부 데이터 백업을 대신하지 않는다. 이 단원에서는 실제 컴포넌트의 동작 순서를 학습하고 관찰 증거와 연결한다.

**학습 결과:** etcd snapshot·restore·검증의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 핵심 질문에서 내부 원리까지

**etcd Snapshot은 PVC 데이터까지 복원할까?**

### 실행 흐름을 따라가기

etcd는 Kubernetes API 상태를 저장한다. 스냅샷 시점 이후 객체 변경은 복원 시 사라질 수 있고 PV 파일 데이터 백업은 별도로 해야 한다.

### 예상 상태 해석 예시

ConfigMap을 Snapshot 전후로 바꿨다면 복원 시 이전 API 객체 값으로 돌아갈 수 있다.

> 이 예시는 학습용이며 실제 클러스터 실행 결과가 아니다. 환경·CNI·버전에 따라 출력이 다를 수 있다.

### 개념을 이해했는지 확인하기

- etcd 복원과 애플리케이션 데이터 복원은 어떻게 다른가?
- 이 과정에서 **API 객체 상태를 만드는 주체**와 **실제 Node에서 실행하는 주체**는 각각 누구인가?
- 비슷한 증상을 유발할 수 있는 다른 원인 하나를 들고 확인할 첫 증거를 설명할 수 있는가?

## 선수 개념과 내부 동작

etcd는 Kubernetes API 상태 저장소이며 PersistentVolume 내부 데이터 백업을 대신하지 않는다. snapshot save는 TLS 인증서와 endpoint가 필요할 수 있다. 최신 etcd는 etcdutl snapshot restore를 지원한다. 복원 시 기존 data dir을 보존하고 새 디렉터리를 만들어 static Pod manifest의 hostPath/etcd 인자를 일치시켜야 한다. 스냅샷 시점 이후의 API 변경은 복원 시 사라질 수 있다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../08-independent/README.md)에서 [ADM-01](../01-kubeadm-bootstrap/README.md) 과정을 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

## 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl -n kube-system get pod -l component=etcd -o wide
sudo grep -E 'listen-client-urls|cert-file|key-file|data-dir' /etc/kubernetes/manifests/etcd.yaml
sudo ls -l /etc/kubernetes/pki/etcd
```

## 따라 하기 — 순서와 예상 결과

폐기 가능한 kubeadm Control Plane에서 VM 스냅샷을 먼저 만든다. 1) 테스트 ConfigMap 생성. 2) etcd manifest에서 접속 endpoint·CA/cert/key를 확인. 3) ETCDCTL_API=3 etcdctl --endpoints=... --cacert=... --cert=... --key=... snapshot save /safe/snapshot.db. 4) etcdutl snapshot status로 스냅샷 확인. 5) 테스트 ConfigMap 변경. 6) control plane을 정지한 복구 창에서 etcdutl snapshot restore ... --data-dir=<new-dir> 로 복원. 7) manifest의 data-dir 인자 및 hostPath를 변경·복원 데이터 소유권을 맞춰 재기동. 8) API/etcd health와 ConfigMap 복원 시점 상태를 확인. 구체적인 endpoint/인자는 환경에서 읽은 값으로만 채운다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

## 고장 가설과 복구

정상 복원되지 않으면 manifest 인자와 mount가 같은 디렉터리를 가리키는지, TLS/파일 권한 및 etcd 로그를 점검한다. 복구가 실패하면 VM 스냅샷으로 되돌린다. multi-member etcd에서는 별도의 클러스터 복원 절차가 필요하다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

## 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

## 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[10-cluster-admin 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
