# Lab 35 — X509, kubeconfig & API

> 학습 단계: **가이드 축소**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../04-storage-security/03-x509-kubeconfig-api/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

## 목표

kubectl 뒤의 인증서 기반 API 접근을 직접 확인한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. `/etc/kubernetes/admin.conf`의 cluster/user/context 구조를 확인한다.
2. client certificate/key를 추출해 API Server `/api/v1/nodes`를 HTTPS로 호출한다.
3. `kubectl proxy` 방식과 직접 6443 접근을 비교한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 잘못된/없는 인증 정보로 API 호출해 인증 실패를 확인한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. kubectl이 어떤 인증 정보로 API Server에 접근하는지 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [CRD 조회와 kubectl explain 문서 추출](../../07-cka-preview/16-crd-discovery/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.


## 독립 심화: 인증서와 토큰으로 API 직접 요청

관리자 kubeconfig의 현재 API server와 CA, **테스트 전용** 클라이언트 인증서를 사용해 `curl --cacert ... --cert ... --key ... "$API_SERVER/api/v1/nodes"` 요청을 검증한다. 이는 관리자 권한이므로 개인 키·토큰·`kubectl config view --raw` 출력은 절대 커밋하지 않는다.

그다음 제한된 ServiceAccount에 대해 `kubectl create token <sa> -n <namespace> --duration=10m`으로 짧은 유효기간의 토큰을 발급하고 `Authorization: Bearer`를 사용해 허용된 Pod 목록 요청과 금지된 Secret 목록 요청의 HTTP 상태를 비교한다. 인증(Authentication), 인가(Authorization), Admission 거절을 구분하며 **403만 보고 인증 실패로 단정하지 않는다**.

파일 격리는 `umask 077`, `mktemp -d`로 수행하고 종료 시 키·토큰 파일을 제거한다. 실행 명령 예제: [x509/RBAC 직접 요청](../../04-storage-security/03-x509-kubeconfig-api/README.md). 기존 전역 kubeconfig를 덮어쓰지 말고 별도의 임시 `--kubeconfig` 파일로 context 변화를 확인한다.


## 통합 확장 실습 — API 인증·인가

기존 독립 과정의 고유 실습을 이 Lab에 통합했다. 리소스는 별도의 `lab-self-*` namespace를 사용하므로 정상/장애/복구/정리를 모두 검증한 후 삭제한다.

### 따라 하기: 제한된 주체

```bash
kubectl apply -f k8s/04-storage-security/03-x509-kubeconfig-api/extended-setup.yaml
kubectl auth can-i list pods -n lab-self-security --as=system:serviceaccount:lab-self-security:reader
kubectl auth can-i delete pods -n lab-self-security --as=system:serviceaccount:lab-self-security:reader
kubectl auth can-i list secrets -n lab-self-security --as=system:serviceaccount:lab-self-security:reader
kubectl auth can-i list pods -n default --as=system:serviceaccount:lab-self-security:reader
```

순서대로 yes/no/no/no를 예상한다. `--as`를 쓰는 관리자에게 impersonate 권한이 필요하다. 기본 kubeadm 관리자 환경을 기준으로 한다.

### 인증서로 API를 직접 호출하기

kubeadm 인증서 기반 kubeconfig를 준비한 Linux 셸에서 실행한다. 임시 파일은 같은 셸에서 만들고 정리한다. data가 비어 있으면 파일 경로/token 기반 kubeconfig일 수 있으므로 이 코드를 계속 실행하지 않고 START의 kubeadm kubeconfig 준비를 확인한다.

```bash
SECURITY_OLD_UMASK=$(umask)
umask 077
SECURITY_TMP=$(mktemp -d)
API_SERVER=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')
kubectl config view --raw --minify -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' | base64 -d > "$SECURITY_TMP/ca.crt"
kubectl config view --raw --minify -o jsonpath='{.users[0].user.client-certificate-data}' | base64 -d > "$SECURITY_TMP/client.crt"
kubectl config view --raw --minify -o jsonpath='{.users[0].user.client-key-data}' | base64 -d > "$SECURITY_TMP/client.key"
test -s "$SECURITY_TMP/ca.crt" && test -s "$SECURITY_TMP/client.crt" && test -s "$SECURITY_TMP/client.key"
openssl x509 -in "$SECURITY_TMP/client.crt" -noout -subject -issuer -dates
curl --cacert "$SECURITY_TMP/ca.crt" --cert "$SECURITY_TMP/client.crt" --key "$SECURITY_TMP/client.key" "$API_SERVER/api/v1/nodes"
```

테스트가 실패하면 이후 curl을 실행하지 않는다. 정상 응답은 NodeList JSON이다. 개인 키와 token, `config view --raw` 출력은 저장소나 학습 기록에 넣지 않는다.

### ServiceAccount token으로 허용/거부 비교

```bash
SA_TOKEN=$(kubectl -n lab-self-security create token reader --duration=10m)
curl -sS --cacert "$SECURITY_TMP/ca.crt" -H "Authorization: Bearer $SA_TOKEN" -o /dev/null -w '%{http_code}\n' "$API_SERVER/api/v1/namespaces/lab-self-security/pods"
curl -sS --cacert "$SECURITY_TMP/ca.crt" -H "Authorization: Bearer $SA_TOKEN" -o /dev/null -w '%{http_code}\n' "$API_SERVER/api/v1/namespaces/lab-self-security/secrets"
```

200/403을 예상한다. token 없이 요청하면 환경에 따라 익명 주체의 403 또는 인증 실패 401일 수 있으므로 모든 403을 인증 성공한 사용자 문제로 단정하지 않는다.

### context를 현재 설정과 분리하기

```bash
kubectl --kubeconfig="$SECURITY_TMP/reader.conf" config set-cluster study --server="$API_SERVER" --certificate-authority="$SECURITY_TMP/ca.crt" --embed-certs=true
kubectl --kubeconfig="$SECURITY_TMP/reader.conf" config set-credentials reader --token="$SA_TOKEN"
kubectl --kubeconfig="$SECURITY_TMP/reader.conf" config set-context study-reader --cluster=study --user=reader --namespace=lab-self-security
kubectl --kubeconfig="$SECURITY_TMP/reader.conf" config use-context study-reader
kubectl --kubeconfig="$SECURITY_TMP/reader.conf" get pods
kubectl --kubeconfig="$SECURITY_TMP/reader.conf" get secrets
kubectl config current-context
```

별도 파일의 context와 원래 관리자 context가 다르다. 두 번째 조회는 Forbidden이다. Dashboard 같은 UI도 같은 API/RBAC를 사용한다. UI 설치는 본 과정의 필수가 아니며 [기초 37](../../04-storage-security/05-dashboard-auth-contexts/README.md)은 이미 설치한 UI가 있을 때 권한 비교를 추가한다.

### 실패 → 복구

```bash
kubectl -n lab-self-security delete rolebinding pod-reader
kubectl auth can-i list pods -n lab-self-security --as=system:serviceaccount:lab-self-security:reader
kubectl apply -f k8s/04-storage-security/03-x509-kubeconfig-api/extended-setup.yaml
kubectl auth can-i list pods -n lab-self-security --as=system:serviceaccount:lab-self-security:reader
```

no → yes를 예상한다. token 재발급 없이 binding 복구만으로 권한이 돌아오는 이유를 설명한다. 이어 [16 CRD 탐색](../../07-cka-preview/16-crd-discovery/README.md)을 끝내면 API group/kind/schema도 연결된다.

### 누적 복습 — 다음 단계 전에

앞 단계의 개념을 현재 증상에 다시 연결한다. 문서를 닫고 세 질문에 답하며, 어려운 질문은 실제 spec/status/Events를 근거로 다시 설명한다.

1. RBAC와 Admission의 책임 차이는?
2. ServiceAccount와 RoleBinding의 관계는?
3. Forbidden 오류를 어떻게 구분할까?

관련 내부 심화를 할 경우 이 단계의 **namespace를 정리하기 전에** 진행한다. 개념만 읽을 때는 리소스 재생성을 강제하지 않는다.

### 완료와 정리

```bash
kubectl delete namespace lab-self-security
rm -f "$SECURITY_TMP/ca.crt" "$SECURITY_TMP/client.crt" "$SECURITY_TMP/client.key" "$SECURITY_TMP/reader.conf"
rmdir "$SECURITY_TMP"
unset SA_TOKEN API_SERVER SECURITY_TMP
umask "$SECURITY_OLD_UMASK"
unset SECURITY_OLD_UMASK
```

다음: [08 노출·확장·통합 진단](../08-operations/README.md).

[독립 학습 순서](../../README.md)
