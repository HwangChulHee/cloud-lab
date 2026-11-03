# 별도 Kubernetes 클러스터 운영 실습 가이드

기본 00–06 Lab은 기존 Vagrant 3노드 클러스터에서 진행하며, 파괴적 클러스터 변경은 격리된 VM 또는 스냅샷 복원 가능한 환경에서만 연습한다.

## 선수 조건과 운영 원칙

- 실제 Kubernetes/컨테이너 런타임 버전, CNI, OS와 공식 문서 호환성을 먼저 확인한다.
- 기존 1.27.2 기본 학습 클러스터를 임의로 업그레이드하지 않는다.
- etcd snapshot/restore, kubeadm upgrade, HA control plane은 반드시 백업·복구 계획과 별도 VM을 확보한 다음 수행한다.
- 설치·관리 실행 절차는 [ADM-01~07](../10-cluster-admin/README.md)를 공식 학습 경로로 사용한다.

## 구성과 순서

1. 별도 클러스터에 kubeadm bootstrap을 완료하고 노드 Ready를 확인한다.
2. 사용 중인 CNI의 설치 상태와 네트워크 정책 집행 조건을 확인한다.
3. etcd snapshot을 저장하고 무결성을 확인한다. 복원은 폐기 가능한 환경에서 검증한다.
4. kubeadm/컴포넌트 업그레이드는 버전별 공식 가이드를 기준으로 진행한다.
5. Gateway API, Helm, Ingress, Canary는 [CKA 확장 과정](../07-cka-preview/README.md)에서 독립적으로 학습한다.

## 참고

- [CKA 환경 조건](../07-cka-preview/ENVIRONMENT.md)
- [Gateway 전환](../07-cka-preview/07-gateway-migration/README.md)
- [CNI](../07-cka-preview/14-cni-install/README.md)
- [제어 평면 복구](../07-cka-preview/09-control-plane-recovery/README.md)

이 가이드는 작업 순서·안전 조건을 설명한다. 버전별 패키지 설치 명령은 실행 환경을 확인한 뒤 공식 Kubernetes 문서를 참고한다.
