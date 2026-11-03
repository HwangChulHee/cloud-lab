# Lab 40 — Ingress Canary & TLS

> 학습 단계: **가이드 축소**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [현재 문서의 Ingress·TLS 통합 확장](./README.md#통합-확장-실습--ingresstlshpa)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

## 목표

가중치/헤더 기반 Canary와 HTTPS 종료를 실험한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. v1/v2 backend를 준비한다.
2. 기존 격리된 ingress-nginx 학습 환경에서만 nginx.ingress.kubernetes.io/canary와 canary-weight로 일부 요청을 v2에 전달한다. 이 annotation은 Ingress 표준이 아니므로 다른 Controller에 그대로 적용하지 않는다. 신규 환경에서는 해당 구현의 트래픽 분할 기능 또는 Gateway API HTTPRoute의 backendRefs.weight로 대체한다.
3. header 기반 Canary를 확인한다.
4. TLS Secret을 만들고 HTTPS Ingress를 구성한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 잘못된 TLS Secret 또는 host를 설정하고 실제 인증서/SNI/응답을 비교한 뒤 복구한다. Controller에 따라 기본 인증서로 HTTPS 연결이 계속될 수 있으므로 curl -k의 성공만으로 정상 TLS 설정이라고 판단하지 않는다. 자체 서명 인증서는 --cacert와 --resolve로 검증한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Blue/Green과 Canary의 트래픽 전환 차이를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [Ingress에서 Gateway API로 전환](../../07-cka-preview/07-gateway-migration/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.


## 통합 확장 실습 — Ingress·TLS·HPA

기존 독립 과정의 고유 실습을 이 Lab에 통합했다. 리소스는 별도의 `lab-self-*` namespace를 사용하므로 정상/장애/복구/정리를 모두 검증한 후 삭제한다.

### Ingress 준비와 따라 하기

[애드온 준비](../../guides/ADDONS.md#traefik-ingress)를 따라 학습용 Traefik을 설치한다. 기존 ingress-nginx를 새로 설치할 필요는 없다. 아래 class와 annotation은 이 전용 Traefik 기준이다.

```bash
kubectl apply -f k8s/05-advanced/03-ingress-canary-tls/extended-setup.yaml
kubectl -n lab-self-edge rollout status deploy/web --timeout=120s
kubectl -n lab-self-ingress rollout status deploy/traefik --timeout=120s
kubectl -n lab-self-ingress port-forward svc/traefik 8080:80 8443:443
```

port-forward를 계속 둔 채 **같은 Linux 머신의 두 번째 셸**에서 실행한다. Windows 브라우저가 VM의 localhost에 바로 접속한다고 가정하지 않는다.

```bash
curl -i -H 'Host: study.local' http://127.0.0.1:8080/
curl -i -H 'Host: wrong.local' http://127.0.0.1:8080/
kubectl -n lab-self-edge get ingress,svc,pods
```

첫 요청은 nginx HTML과 200, 두 번째는 이 backend로 라우팅되지 않아 기본 설정의 404를 예상한다. 외부 IP가 없어도 port-forward로 Controller의 라우팅을 학습할 수 있다.

### TLS를 암호화와 이름 검증까지 확인하기

```bash
EDGE_TMP=$(mktemp -d)
openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
  -keyout "$EDGE_TMP/tls.key" -out "$EDGE_TMP/tls.crt" \
  -subj '/CN=study.local' -addext 'subjectAltName=DNS:study.local'
chmod 600 "$EDGE_TMP/tls.key"
kubectl -n lab-self-edge create secret tls web-tls --cert="$EDGE_TMP/tls.crt" --key="$EDGE_TMP/tls.key"
kubectl apply -f k8s/05-advanced/03-ingress-canary-tls/extended-tls.yaml
curl --fail --max-time 5 --retry 10 --retry-delay 2 --retry-max-time 60 --retry-all-errors \
  --cacert "$EDGE_TMP/tls.crt" --resolve study.local:8443:127.0.0.1 https://study.local:8443/
openssl verify -CAfile "$EDGE_TMP/tls.crt" -verify_hostname study.local "$EDGE_TMP/tls.crt"
openssl verify -CAfile "$EDGE_TMP/tls.crt" -verify_hostname wrong.local "$EDGE_TMP/tls.crt"
```

curl은 Controller 반영 지연을 고려해 재시도하며 정상 응답은 nginx HTML이다. 첫 verify는 OK, 두 번째는 hostname mismatch로 실패해야 한다. 두 번째 실패는 의도한 결과이고, 같은 신뢰 인증서도 이름이 다르면 검증을 통과하지 못함을 Controller 동작과 분리해 확인한다. 정상 curl이 실패하면 다음 장애를 주입하지 말고 port-forward/Ingress/Secret/Controller 로그를 먼저 확인한다.

### Secret 참조 오류를 Controller 로그와 비교하기

```bash
kubectl -n lab-self-edge patch ingress web-tls --type=merge -p '{"spec":{"tls":[{"hosts":["study.local"],"secretName":"missing"}]}}'
curl --cacert "$EDGE_TMP/tls.crt" --resolve study.local:8443:127.0.0.1 https://study.local:8443/
kubectl -n lab-self-ingress logs deploy/traefik --since=2m
kubectl -n lab-self-edge get ingress web-tls -o yaml
```

missing 참조가 저장된 것과 Controller의 Secret 조회 오류를 확인한다. 요청이 성공해도 주입 자체가 실패했다고 단정하지 않는다. Controller는 이전 인증서나 설정을 보존할 수 있고, 전파에 지연이 있을 수 있다. 요청 결과와 로그를 기록한 후 복구한다.

```bash
kubectl apply -f k8s/05-advanced/03-ingress-canary-tls/extended-tls.yaml
curl --fail --max-time 5 --retry 10 --retry-delay 2 --retry-max-time 60 --retry-all-errors \
  --cacert "$EDGE_TMP/tls.crt" --resolve study.local:8443:127.0.0.1 https://study.local:8443/
```

Secret 오류와 인증서 이름 불일치는 서로 다른 검증이다. `curl -k` 성공만으로 TLS 복구를 판정하지 않는다. 새 연결에서 cacert 검증이 돌아올 때 완료한다.

### HPA와 NetworkPolicy를 이어 실행하기

[Metrics Server 준비](../../guides/ADDONS.md#metrics-server)를 마친 뒤 [02 HPA](../../07-cka-preview/02-hpa-behavior/README.md)를 실행한다. 첫 회에는 solution.yaml을 사용하고, 사용량/request/목표 비율로 원하는 replicas를 계산한다. 두 번째에는 solution을 보지 않고 같은 조건을 만든다. 부하 부족과 metrics 누락을 구분한다.

[08 NetworkPolicy](../../07-cka-preview/08-networkpolicy/README.md)는 집행 가능한 CNI에서 실행한다. frontend 성공/other 실패를 모두 확인해야 완료다. 현재 CNI가 집행하지 않으면 객체 작성은 연습할 수 있지만 차단 실습 완료로 체크하지 않는다. 기본 01–08 학습을 계속할 수 있고, 별도 플랫폼 경로에서 CNI 설치 후 이 과제를 다시 검증한다.

### 최종 과제: 정답을 보기 전에 원인부터 좁히기

앞 단계의 환경을 필요할 때 다시 만들고 **장애를 한 번에 하나씩** 주입한다. 각 사례에서 변경 전 정상 증거, 실패 증거, 원인, 복구 뒤 동일 요청의 성공을 기록한다. 기록 양식은 [단계별 완료 기준](../CHECKPOINTS.md)을 사용한다.

| 장애 | 사용할 환경 | 가장 먼저 찾을 근거 |
|---|---|---|
| Service selector를 missing으로 변경 | 04 | DNS는 성공하는지, EndpointSlice에 주소가 있는지 |
| readiness 파일 삭제 | 05 | Ready condition과 endpoint.ready, restartCount |
| 이미지 태그 오타 | 03 | Pending/Waiting 상태와 ImagePull Events |
| namespace quota 초과 | 확장 11 | ReplicaSet FailedCreate와 실제 Pod 생성 여부 |
| RoleBinding 삭제 | 07 | can-i와 403, 인증 주체 |
| TLS Secret 오타 | 이번 08 | Controller 로그, 인증서/SNI, backend 연결 |

힌트 없이 두 사례를 복구하고, 직접 고른 세 번째 사례에서 예상과 실제를 비교한다. 정상 Pod만 보고 전체 Service가 정상이라고 결론내리지 않는다.

### 정리

첫 번째 셸의 port-forward를 Ctrl+C로 종료한다. 별도 확장 실습 namespace/PV/PriorityClass 정리는 각 문서대로 먼저 끝낸다.

```bash
kubectl delete namespace lab-self-edge
rm -f "$EDGE_TMP/tls.key" "$EDGE_TMP/tls.crt"
rmdir "$EDGE_TMP"
unset EDGE_TMP
```

공용 애드온은 바로 삭제하지 않는다. 학습을 모두 끝내고 애드온 정리 조건을 만족했을 때 ADDONS의 정리를 따른다.

### 다음 경로

[확장·플랫폼 경로](../../guides/PLATFORM.md)에서 Gateway/Helm/제어 평면/CNI/CRI를 이어간다. Canary는 일반 Ingress 표준 기능이 아니므로 신규 경로에서는 Gateway의 가중치 과제를 사용한다. 강의를 듣는다면 이 단계 이후 개념 설명을 비교하는 보충 자료로 사용할 수 있다.

[독립 학습 순서](../../README.md)
