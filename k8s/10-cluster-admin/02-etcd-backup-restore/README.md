# etcd snapshot·restore·검증

> 분류: **CKA 필수** · 선수 학습: [독립 학습](../../08-independent/README.md)의 ADM-01 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

etcd는 Kubernetes API 상태 저장소이며 PersistentVolume 내부 데이터 백업을 대신하지 않는다. 이 단원은 단순한 명령어 암기가 아니라 Kubernetes API 객체의 변화와 실제 Node/Runtime에서 일어나는 현상을 연결하는 학습이다.

**학습 결과:** etcd snapshot·restore·검증의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 선수 개념과 내부 동작

etcd는 Kubernetes API 상태 저장소이며 PersistentVolume 내부 데이터 백업을 대신하지 않는다. snapshot save는 TLS 인증서와 endpoint가 필요할 수 있다. 최신 etcd는 etcdutl snapshot restore를 지원한다. 복원 시 기존 data dir을 보존하고 새 디렉터리를 만들어 static Pod manifest의 hostPath/etcd 인자를 일치시켜야 한다. 스냅샷 시점 이후의 API 변경은 복원 시 사라질 수 있다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../08-independent/README.md)의 ADM-01 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
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

복구 완료 기준은 **동일한 조회나 요청으로 정상 결과를 다시 얻는 것**이다. 관찰할 수 없는 구현(예: CSI driver 미설치, kube-proxy 대체 데이터 평면)은 미검증으로 기록한다.

## 스스로 설명할 문제

1. **etcd snapshot·restore·검증**이 필요한 이유를 사용자가 겪을 수 있는 실제 문제로 설명할 수 있는가?
2. 이 현상을 만든 API 객체와 실제 실행한 컴포넌트는 각각 무엇인가?
3. 위 예시의 실패 원인과 동일한 외부 증상을 보이는 다른 원인은 무엇이며 첫 번째로 어떤 증거를 확인할 것인가?
4. Pod/Node 또는 Controller를 재시작하지 않고도 진단 가능한 정보는 무엇인가?

## 환경 및 정리

원래 실습 namespace와 공용 애드온은 연결된 기본 단계의 정리 지침을 따른다. Node taint/route/CNI/etcd 및 Kubernetes 패키지 변경은 별도 안전 조건이 명시된 경우에만 수행한다. 실제 VM 실행 여부는 [CHECKPOINTS](../../08-independent/CHECKPOINTS.md)에 별도로 기록한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[10-cluster-admin 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
