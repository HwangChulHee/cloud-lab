# 07. 인증서·Token·RBAC·context를 실제 요청으로 확인하기

## 먼저 이해할 것

인증은 누구인지, 권한은 무엇을 할 수 있는지, Admission은 요청이 정책을 만족하는지를 확인한다. kubeconfig는 서버·인증 정보·context를 묶는다. context는 사용할 cluster/user/namespace 조합이고 namespace를 바꾼다고 사용자 권한이 줄지는 않는다. 관리자와 ServiceAccount의 권한을 나눠 확인한다.

## 따라 하기: 제한된 주체

```bash
kubectl apply -f k8s/08-independent/07-security/setup.yaml
kubectl auth can-i list pods -n lab-self-security --as=system:serviceaccount:lab-self-security:reader
kubectl auth can-i delete pods -n lab-self-security --as=system:serviceaccount:lab-self-security:reader
kubectl auth can-i list secrets -n lab-self-security --as=system:serviceaccount:lab-self-security:reader
kubectl auth can-i list pods -n default --as=system:serviceaccount:lab-self-security:reader
```

순서대로 yes/no/no/no를 예상한다. `--as`를 쓰는 관리자에게 impersonate 권한이 필요하다. 기본 kubeadm 관리자 환경을 기준으로 한다.

## 인증서로 API를 직접 호출하기

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

## ServiceAccount token으로 허용/거부 비교

```bash
SA_TOKEN=$(kubectl -n lab-self-security create token reader --duration=10m)
curl -sS --cacert "$SECURITY_TMP/ca.crt" -H "Authorization: Bearer $SA_TOKEN" -o /dev/null -w '%{http_code}\n' "$API_SERVER/api/v1/namespaces/lab-self-security/pods"
curl -sS --cacert "$SECURITY_TMP/ca.crt" -H "Authorization: Bearer $SA_TOKEN" -o /dev/null -w '%{http_code}\n' "$API_SERVER/api/v1/namespaces/lab-self-security/secrets"
```

200/403을 예상한다. token 없이 요청하면 환경에 따라 익명 주체의 403 또는 인증 실패 401일 수 있으므로 모든 403을 인증 성공한 사용자 문제로 단정하지 않는다.

## context를 현재 설정과 분리하기

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

## 실패 → 복구

```bash
kubectl -n lab-self-security delete rolebinding pod-reader
kubectl auth can-i list pods -n lab-self-security --as=system:serviceaccount:lab-self-security:reader
kubectl apply -f k8s/08-independent/07-security/setup.yaml
kubectl auth can-i list pods -n lab-self-security --as=system:serviceaccount:lab-self-security:reader
```

no → yes를 예상한다. token 재발급 없이 binding 복구만으로 권한이 돌아오는 이유를 설명한다. 이어 [16 CRD 탐색](../../07-cka-preview/16-crd-discovery/README.md)을 끝내면 API group/kind/schema도 연결된다.

## 완료와 정리

```bash
kubectl delete namespace lab-self-security
rm -f "$SECURITY_TMP/ca.crt" "$SECURITY_TMP/client.crt" "$SECURITY_TMP/client.key" "$SECURITY_TMP/reader.conf"
rmdir "$SECURITY_TMP"
unset SA_TOKEN API_SERVER SECURITY_TMP
umask "$SECURITY_OLD_UMASK"
unset SECURITY_OLD_UMASK
```

다음: [08 노출·확장·통합 진단](../08-operations/README.md).

[독립 학습 순서](../README.md)
