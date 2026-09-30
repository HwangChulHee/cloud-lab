# 13. Helm으로 Argo CD 설치와 템플릿 비교

> 강의 전 예습 · 참고 주제: task-helm-argocd · 환경: 별도 1.34 예습 클러스터 + Helm 3 + Python/PyYAML

기초 연결: [Controller](../../02-controllers/01-replicaset/README.md) · [RBAC](../../04-storage-security/04-serviceaccount-rbac/README.md)

## 먼저 이해할 것

Chart는 배포 템플릿 묶음, values는 설정, release는 설치 인스턴스다. chart version과 애플리케이션 version은 다르다. CRD가 이미 설치된 상태를 먼저 만들고, 이후 템플릿 생성과 Helm 설치에서 CRD 생성을 끈다. `--skip-crds`와 차트의 `crds.install=false`는 항상 같은 동작이 아니다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/13-helm-argocd`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update argo
helm show chart argo/argo-cd --version 8.6.4
helm show values argo/argo-cd --version 8.6.4 > /tmp/preview-argo-values.yaml
helm template preview-argocd argo/argo-cd --version 8.6.4 \
  --namespace preview-argocd --set crds.install=true > /tmp/preview-argo-with-crds.yaml
python3 extract_crds.py /tmp/preview-argo-with-crds.yaml /tmp/preview-argo-crds.yaml
kubectl get crd applications.argoproj.io applicationsets.argoproj.io appprojects.argoproj.io
```

마지막 조회가 NotFound인 새 예습 환경에서만 다음을 실행한다. 기존 Argo CD가 있다면 공용 CRD를 덮어쓰지 않고 별도 환경을 사용한다.

```bash
kubectl apply --server-side -f /tmp/preview-argo-crds.yaml
```

기존 CRD를 강제로 덮어쓰는 `--force-conflicts`는 사용하지 않는다.

## 2. 직접 바꿔보기

1. chart 8.6.4, namespace preview-argocd, release preview-argocd로 템플릿을 생성한다.
2. CRD 설치를 끄고 결과를 `/tmp/preview-argo-helm.yaml`에 저장한다.
3. 같은 release/version/namespace/values로 Helm 설치한다.
4. 렌더링과 설치 결과에서 CRD가 포함되지 않았는지 확인한다. UI 설정은 필요 없다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

```bash
helm list -n preview-argocd
helm get values preview-argocd -n preview-argocd
kubectl -n preview-argocd get pods
helm get manifest preview-argocd -n preview-argocd > /tmp/preview-argo-installed.yaml
python3 extract_crds.py --expect-none /tmp/preview-argo-helm.yaml
python3 extract_crds.py --expect-none /tmp/preview-argo-installed.yaml
```

Pod Ready와 `crds.install=false`, 템플릿 및 release manifest의 CRD 부재를 확인한다. 템플릿을 생성한 것만으로 설치된 것은 아니다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

```bash
helm template preview-argocd argo/argo-cd --version 8.6.4 \
  --namespace preview-argocd --set crds.install=false > /tmp/preview-argo-helm.yaml
helm install preview-argocd argo/argo-cd --version 8.6.4 \
  --namespace preview-argocd --create-namespace --set crds.install=false \
  --wait --timeout=5m
```

실패하면 Pod Events, requests, 이미지 다운로드를 확인한다. 이 과정에서는 템플릿의 리소스 이름과 설치 이름을 비교하기 쉽도록 release 이름을 동일하게 지정한다. 템플릿 CRD를 사용하는 차트에는 `--skip-crds`만으로 충분하지 않을 수 있다.

</details>

## 4. 정리 및 재실행

```bash
helm uninstall preview-argocd -n preview-argocd
kubectl delete namespace preview-argocd
```

이 실습에서 새로 설치한 CRD임을 확인한 disposable 클러스터에서만 정리한다. CRD 삭제는 해당 custom resource도 삭제하므로 다른 Argo CD가 사용하는 경우 유지한다.

```bash
kubectl delete -f /tmp/preview-argo-crds.yaml
rm -f /tmp/preview-argo-values.yaml /tmp/preview-argo-with-crds.yaml /tmp/preview-argo-crds.yaml /tmp/preview-argo-helm.yaml /tmp/preview-argo-installed.yaml
```

## 강의에서 확인할 질문

- Helm template, install, get manifest의 차이는?
- 차트 values 옵션과 Helm 공통 옵션이 다른 이유는?

[전체 예습 경로](../README.md)
