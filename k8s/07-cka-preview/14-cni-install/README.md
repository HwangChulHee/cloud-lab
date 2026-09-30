# 14. CNI 설치와 NetworkPolicy 집행 확인

> 강의 전 예습 · 참고 주제: task-cni · 환경: CNI 없는 별도 1.34 kubeadm 클러스터

기초 연결: [클러스터 관찰](../../00-foundation/01-cluster-verification/README.md) · [NetworkPolicy 예습](../../07-cka-preview/08-networkpolicy/README.md)

## 먼저 이해할 것

CNI는 Pod 네트워크를 연결하고, 구현에 따라 NetworkPolicy를 집행한다. Flannel 단독 설치만으로 이 과제의 정책 집행 요구를 만족한다고 간주하지 않는다. Calico를 선택하고 Operator와 Installation Custom Resource를 모두 설정한다. Node별 podCIDR과 클러스터 전체 Pod CIDR은 같은 개념이 아니다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/14-cni-install`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

[환경 준비](../ENVIRONMENT.md)에 따라 CNI 없는 새 클러스터를 준비한다. 기존 1.27 학습 클러스터의 CNI를 삭제하거나 교체하지 않는다.

```bash
kubectl get nodes -o wide
kubectl -n kube-system get pods -o wide
kubectl -n kube-system get cm kubeadm-config -o yaml
kubectl get nodes -o custom-columns=NAME:.metadata.name,PODCIDR:.spec.podCIDR
```

kubeadm-config의 `networking.podSubnet`과 서비스 CIDR, VM 네트워크를 기록한다. Pod CIDR은 노드·Service 네트워크와 겹치지 않게 한다. IPPool은 특정 노드의 /24를 복사하지 말고 클러스터 전체 CIDR에 맞춘다.

## 2. 직접 바꿔보기

1. manifest 방식으로 Calico v3.31.1 Operator를 설치한다.
2. 같은 버전 custom-resources를 받아 클러스터 Pod CIDR에 맞춘다.
3. Installation을 배포하고 노드·시스템 Pod 상태를 확인한다.
4. 08 NetworkPolicy의 허용 전/후 테스트로 실제 집행을 검증한다. Helm은 사용하지 않는다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

```bash
kubectl get tigerastatus
kubectl get nodes
kubectl get pods -A
kubectl get ippools.crd.projectcalico.org -o yaml
```

Calico 컴포넌트 정상, 노드 Ready, 시스템 Pod 정상에 더해 08의 기본 차단·최소 허용·other 차단이 모두 동작해야 한다. Pod 간 통신만 성공한 것으로 완료하지 않는다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

```bash
curl -fL -o /tmp/preview-tigera-operator.yaml \
  https://raw.githubusercontent.com/projectcalico/calico/v3.31.1/manifests/tigera-operator.yaml
curl -fL -o /tmp/preview-calico-custom.yaml \
  https://raw.githubusercontent.com/projectcalico/calico/v3.31.1/manifests/custom-resources.yaml
kubectl create -f /tmp/preview-tigera-operator.yaml
vi /tmp/preview-calico-custom.yaml
```

`kind: Installation`의 `spec.calicoNetwork.ipPools[].cidr`를 앞에서 조사한 전체 Pod CIDR로 설정한다. 작은 CIDR이면 blockSize가 풀보다 작은 블록을 만드는지 확인한다. 예를 들어 /24 풀에 /26 블록은 가능하지만 여러 노드가 쓸 충분한 블록 수가 필요하다.

```bash
kubectl apply -f /tmp/preview-calico-custom.yaml
kubectl get tigerastatus -w
```

버전별 지원 조건과 방화벽 포트는 [Calico 공식 설치 문서](https://docs.tigera.io/calico/latest/getting-started/kubernetes/self-managed-onprem/onpremises)를 대조한다. 최신 문서의 설치 옵션을 고정 버전에 무조건 섞지 않는다.

</details>

## 4. 정리 및 재실행

08 NetworkPolicy 리소스를 정리한다. CNI 제거 대신 **전용 VM을 CNI 설치 전 스냅샷으로 복원하거나 폐기**한다. 단순히 Operator만 삭제하는 것은 완전한 CNI 정리가 아니다.

```bash
rm -f /tmp/preview-tigera-operator.yaml /tmp/preview-calico-custom.yaml
```

## 강의에서 확인할 질문

- Operator만 설치하면 왜 Pod 네트워크가 아직 준비되지 않을 수 있는가?
- Node podCIDR과 클러스터 Pod CIDR의 차이는?

[전체 예습 경로](../README.md)
