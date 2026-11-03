# Lab 37 — kubeconfig Context와 인증 범위 (Dashboard 선택)

> **필수:** context의 cluster/user/namespace 전환 및 오류 진단 · **선택:** 이미 설치된 Dashboard UI 로그인. Dashboard를 새로 설치하지 않아도 기본 과제를 완료할 수 있다.

## 1. Concept / Recall

kubeconfig는 **클러스터 연결 정보**, **사용자 인증 정보**, **context(클러스터·사용자·기본 Namespace의 조합)**를 관리한다. Context 전환은 RBAC 권한을 새로 부여하지 않는다. Context의 namespace는 명령에 `-n`이 없을 때 기본 조회 범위를 결정한다.

`admin.conf`나 `kubectl config view --raw` 출력에는 관리자 키/토큰이 들어갈 수 있으므로 GitHub에 저장하거나 터미널 출력 전체를 공유하지 않는다.

## 2. Build — 원본 kubeconfig를 변경하지 않고 연습

이 명령은 인증서 경로가 상대경로여도 재현되도록 `--flatten`으로 포함시킨 kubeconfig를 민감한 임시 파일로 복사한다. 임시 파일은 600 권한으로 만들고 실습 종료 시 삭제한다.

```bash
kubectl config current-context
kubectl config get-contexts
kubectl create namespace lab-context
umask 077
CTX_TMP=$(mktemp)
kubectl config view --raw --flatten > "$CTX_TMP"
chmod 600 "$CTX_TMP"
CTX_CLUSTER=$(kubectl config view --minify -o jsonpath='{.contexts[0].context.cluster}')
CTX_USER=$(kubectl config view --minify -o jsonpath='{.contexts[0].context.user}')
kubectl --kubeconfig="$CTX_TMP" config set-context lab-context --cluster="$CTX_CLUSTER" --user="$CTX_USER" --namespace=lab-context
kubectl --kubeconfig="$CTX_TMP" config use-context lab-context
kubectl --kubeconfig="$CTX_TMP" config get-contexts
kubectl --kubeconfig="$CTX_TMP" get pods
kubectl --kubeconfig="$CTX_TMP" get pods -n default
```

**예상:** `lab-context`에서 `get pods`는 `lab-context` Namespace, `-n default`는 default를 조회한다. 원본 `kubectl config current-context`는 바뀌지 않는다.

## 3. Break & Diagnose — Context는 올바르지만 Namespace가 없는 경우

```bash
kubectl --kubeconfig="$CTX_TMP" config set-context lab-context --namespace=missing-lab-namespace
kubectl --kubeconfig="$CTX_TMP" get pods
kubectl --kubeconfig="$CTX_TMP" config get-contexts
```

**예상:** 없는 Namespace이므로 `get pods`가 NotFound 계열 오류를 낸다. 이 현상을 API Server 미연결, 인증 실패, RBAC Forbidden과 구분한다. 특정 Context를 선택했다고 해서 ServiceAccount/RoleBinding이 만들어지는 것은 아니다.

## 4. Recover / Cleanup

```bash
kubectl --kubeconfig="$CTX_TMP" config set-context lab-context --namespace=lab-context
kubectl --kubeconfig="$CTX_TMP" get pods
kubectl config current-context
rm -f "$CTX_TMP"
unset CTX_TMP CTX_CLUSTER CTX_USER
kubectl delete namespace lab-context
```

원본 kubeconfig로 현재 context와 기존 cluster를 다시 확인한다. 복사된 임시 파일에 관리 권한이 들어 있으므로 실습 중 공유하지 않는다.

## 5. 선택 확장: 기존 Dashboard UI

대상 클러스터에 Dashboard가 **이미 설치되어 있는 경우에만**, [Lab 35의 제한된 Token](../03-x509-kubeconfig-api/README.md) 또는 [Lab 36의 RoleBinding](../04-serviceaccount-rbac/README.md)을 사용해 허용된 리소스 범위를 비교한다. Dashboard를 사용하지 않는 경우에는 `kubectl auth can-i --as`와 API 응답으로 인증/인가 차이를 검증한다. 무분별하게 cluster-admin 권한의 Dashboard Token을 만들지 않는다.

## 인출 질문 / 완료 기준

- kubeconfig의 cluster·user·context 세 요소는 각각 무엇을 선택하는가?
- `-n`과 context namespace가 충돌할 때 무엇이 우선하는가?
- `NotFound`, `Unauthorized`, `Forbidden`를 어떤 증거로 구별하는가?

임시 context 설정 → Namespace 변경으로 조회 범위 변화 → 잘못된 Namespace 오류 → Context 복원 → 임시 자격증명 파일 삭제까지 확인하면 완료한다.
