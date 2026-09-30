# 08. Ingress·TLS·HPA와 통합 장애 진단

## 먼저 이해할 것

Ingress는 요청 규칙이고 Controller가 실제 연결을 처리한다. Host header로 HTTP 라우팅을, SNI와 인증서 이름으로 HTTPS 연결을 확인한다. HPA는 metrics에 따라 Pod 수를 바꿀 뿐 노드를 늘리지 않는다. 여기까지 배운 배치·권한·저장소·네트워크를 연결해 장애 위치를 좁힌다.

## Ingress 준비와 따라 하기

[애드온 준비](../ADDONS.md#traefik-ingress)를 따라 학습용 Traefik을 설치한다. 기존 ingress-nginx를 새로 설치할 필요는 없다. 아래 class와 annotation은 이 전용 Traefik 기준이다.

```bash
kubectl apply -f k8s/08-independent/08-operations/setup.yaml
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

## TLS를 암호화와 이름 검증까지 확인하기

```bash
EDGE_TMP=$(mktemp -d)
openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
  -keyout "$EDGE_TMP/tls.key" -out "$EDGE_TMP/tls.crt" \
  -subj '/CN=study.local' -addext 'subjectAltName=DNS:study.local'
chmod 600 "$EDGE_TMP/tls.key"
kubectl -n lab-self-edge create secret tls web-tls --cert="$EDGE_TMP/tls.crt" --key="$EDGE_TMP/tls.key"
kubectl apply -f k8s/08-independent/08-operations/tls.yaml
curl --cacert "$EDGE_TMP/tls.crt" --resolve study.local:8443:127.0.0.1 https://study.local:8443/
kubectl -n lab-self-edge patch ingress web-tls --type=merge -p '{"spec":{"tls":[{"hosts":["study.local"],"secretName":"missing"}]}}'
curl --cacert "$EDGE_TMP/tls.crt" --resolve study.local:8443:127.0.0.1 https://study.local:8443/
kubectl apply -f k8s/08-independent/08-operations/tls.yaml
```

정상 TLS 응답은 nginx HTML이다. 잘못된 Secret이 반영되면 인증서 검증/라우팅이 실패한다. Controller의 이전 설정 보존·인증서 반영 지연 여부도 로그로 확인한다. `curl -k` 성공만으로 TLS 복구를 판정하지 않는다. 새 연결에서 cacert 검증이 돌아올 때 완료한다.

## HPA와 NetworkPolicy를 이어 실행하기

[Metrics Server 준비](../ADDONS.md#metrics-server)를 마친 뒤 [02 HPA](../../07-cka-preview/02-hpa-behavior/README.md)를 실행한다. 첫 회에는 solution.yaml을 사용하고, 사용량/request/목표 비율로 원하는 replicas를 계산한다. 두 번째에는 solution을 보지 않고 같은 조건을 만든다. 부하 부족과 metrics 누락을 구분한다.

[08 NetworkPolicy](../../07-cka-preview/08-networkpolicy/README.md)는 집행 가능한 CNI에서 실행한다. frontend 성공/other 실패를 모두 확인해야 완료다. 현재 CNI가 집행하지 않으면 객체 작성은 연습할 수 있지만 차단 실습 완료로 체크하지 않는다. 기본 01–08 학습을 계속할 수 있고, 별도 플랫폼 경로에서 CNI 설치 후 이 과제를 다시 검증한다.

## 최종 과제: 정답을 보기 전에 원인부터 좁히기

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

## 정리

첫 번째 셸의 port-forward를 Ctrl+C로 종료한다. 별도 확장 실습 namespace/PV/PriorityClass 정리는 각 문서대로 먼저 끝낸다.

```bash
kubectl delete namespace lab-self-edge
rm -f "$EDGE_TMP/tls.key" "$EDGE_TMP/tls.crt"
rmdir "$EDGE_TMP"
unset EDGE_TMP
```

공용 애드온은 바로 삭제하지 않는다. 학습을 모두 끝내고 애드온 정리 조건을 만족했을 때 ADDONS의 정리를 따른다.

## 다음 경로

[확장·플랫폼 경로](../PLATFORM.md)에서 Gateway/Helm/제어 평면/CNI/CRI를 이어간다. Canary는 일반 Ingress 표준 기능이 아니므로 신규 경로에서는 Gateway의 가중치 과제를 사용한다. 강의를 듣는다면 이 단계 이후 개념 설명을 비교하는 보충 자료로 사용할 수 있다.

[독립 학습 순서](../README.md)
