# Lab 36 — ServiceAccount, RBAC 그리고 Pod Security Admission

> **기초 필수** · 인증(주체) → 인가(RBAC) → Admission(정책) 구분 · Namespace `lab-rbac` / `lab-int-psa`

## 1. Concept & Recall

Kubernetes API 요청은 대략 **Authentication → Authorization → Admission → 저장(etcd)** 순서로 처리된다. 인증 실패(401), 인증은 됐으나 인가 실패(403), RBAC가 허용해도 Admission 정책 위반으로 거절되는 경우는 원인이 다르다.

- **ServiceAccount:** Namespace 안의 워크로드용 API 주체. TokenRequest로 짧은 수명의 토큰을 생성할 수 있다.
- **Role:** Namespace 범위의 API 리소스/verb 권한 규칙.
- **RoleBinding:** Role 또는 ClusterRole을 특정 Namespace의 주체에 연결한다.
- **ClusterRoleBinding:** cluster-wide 또는 cluster-scoped 권한 연결. 불필요한 `*` 권한을 부여하지 않는다.
- **Pod Security Admission (PSA):** RBAC가 요청을 허용한 후에도 Pod spec의 보안 수준에 따라 거부할 수 있다.

## 2. Build — 최소 권한 Role/RoleBinding

```bash
kubectl apply -f k8s/04-storage-security/04-serviceaccount-rbac/rbac.yaml
kubectl -n lab-rbac get serviceaccount,roles,rolebindings,pods
kubectl auth can-i list pods -n lab-rbac --as=system:serviceaccount:lab-rbac:reader
kubectl auth can-i list services -n lab-rbac --as=system:serviceaccount:lab-rbac:reader
kubectl auth can-i list pods -n default --as=system:serviceaccount:lab-rbac:reader
```

**예상:** 첫 질문은 `yes`, 다음 두 질문은 `no`. `kubectl auth can-i --as`는 관리자 등 impersonate 권한이 있는 주체로 실행해야 한다. 관리자 kubeconfig를 외부에 공유하지 않는다.

## 3. Break & Diagnose — RoleBinding 상실

```bash
kubectl -n lab-rbac delete rolebinding pod-reader
kubectl auth can-i list pods -n lab-rbac --as=system:serviceaccount:lab-rbac:reader
kubectl -n lab-rbac get role,rolebinding
```

**예상:** ServiceAccount와 Role이 남아 있어도 연결이 없으므로 `no`. 단순히 Role 생성만으로 권한이 부여되지는 않는다.

## 4. Recover

```bash
kubectl apply -f k8s/04-storage-security/04-serviceaccount-rbac/rbac.yaml
kubectl auth can-i list pods -n lab-rbac --as=system:serviceaccount:lab-rbac:reader
```

**예상:** `yes`로 복구. 별도의 API Token과 x509 직접 호출 실습은 [Lab 35](../03-x509-kubeconfig-api/README.md)에서 이어서 수행한다.

## 5. Admission — 허용된 API 주체라도 Pod 생성이 거부될 수 있음

**전용 Namespace에만** `restricted` PSA 정책을 적용한다.

```bash
kubectl create namespace lab-int-psa
kubectl label namespace lab-int-psa pod-security.kubernetes.io/enforce=restricted
kubectl auth can-i create pods -n lab-int-psa
kubectl apply --dry-run=server -f k8s/04-storage-security/04-serviceaccount-rbac/unsafe-pod.yaml
kubectl apply --dry-run=server -f k8s/04-storage-security/04-serviceaccount-rbac/restricted-pod.yaml
kubectl -n lab-int-psa get pods
```

**예상:** 관리 주체에게 `create pods` 권한이 있더라도 `privileged:true`를 포함한 `unsafe-pod`는 restricted PSA에 의해 거부된다. `restricted-pod`는 `runAsNonRoot`, `allowPrivilegeEscalation:false`, `capabilities.drop: [ALL]`, `seccompProfile: RuntimeDefault`를 포함하여 **server-side dry-run 통과**를 목표로 한다. dry-run은 Pod를 생성하지 않으므로 `get pods`가 빈 상태인 것은 정상이다.

단, Pod spec을 Admission이 승인한 것과 해당 이미지가 실제 비root로 실행되는 것은 별도의 검증이다. 호스트 노드에서 privilege를 허용하는 테스트 Pod를 실제 생성하지 않는다.

## 6. Cleanup / Explain

```bash
kubectl delete namespace lab-rbac lab-int-psa
```

**완료 기준:** (1) Namespace별 allowed/denied 결과, (2) RoleBinding 삭제/복구, (3) RBAC allow + PSA deny 구별, (4) PSA dry-run 오류와 허용 사례, (5) cleanup 증거를 남긴다.

인출 질문: RoleBinding이 ClusterRole을 참조하면 권한 범위는 어떻게 되는가? 동일한 403이라도 RBAC와 Admission을 구분할 근거는? Base64 인코딩된 Secret이 암호화된 것인가?

공식 참고: [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) · [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/).
