# CKA 클러스터 관리

CKA 시험과 클러스터 관리 목적의 별도 학습 경로다. 기본 개념은 00–06 Lab에서 익히고, 이 폴더에서는 설치·백업·업그레이드·노드 관리 작업을 별도로 검증한다.

| ID | 모듈 | 연결 시점 | 학습 분류 |
|---|---|---|---|
| ADM-01 | [ADM-01 kubeadm 클러스터 구축](./01-kubeadm-bootstrap/README.md) | 플랫폼 | CKA 필수 |
| ADM-02 | [ADM-02 etcd Snapshot/Restore](./02-etcd-backup-restore/README.md) | ADM-01 | CKA 필수 |
| ADM-03 | [ADM-03 kubeadm 업그레이드](./03-kubeadm-upgrade/README.md) | ADM-01 | CKA 필수 |
| ADM-04 | [ADM-04 CNI와 클러스터 네트워크](./04-cni-cluster-network/README.md) | ADM-01, INT-03 | CKA 필수 |
| ADM-05 | [ADM-05 Kustomize 기본과 Overlay](./05-kustomize/README.md) | 03 완료 후 | CKA 필수 |
| ADM-06 | [ADM-06 Node drain과 PDB](./06-node-maintenance/README.md) | 05 완료 후 | CKA 필수 |
| ADM-07 | [ADM-07 HA Control Plane](./07-high-availability/README.md) | ADM-01, ADM-02 | CKA 필수·선택 실습 |

**CKA 필수 개념**과 실제 VM에서의 **CKA 필수 수행**을 별도로 기록한다. HA는 토폴로지·quorum·LB 이해를 필수로, 대규모 다중 Control Plane 구축을 선택 심화로 취급한다. etcd/업그레이드/Node 관리 작업은 안전한 별도 VM과 공식 버전별 절차를 사용한다.

공식 기본 학습 경로: [00–06 Lab](../README.md). 위험한 클러스터 변경은 [별도 플랫폼](../guides/PLATFORM.md) 경로에서만 수행한다. 관찰과 실제 실행 검증은 별도 기록한다.
