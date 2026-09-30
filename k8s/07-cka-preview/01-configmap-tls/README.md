# 01. ConfigMap으로 TLS 설정 바꾸기

> 강의 전 예습 · 참고 주제: task-configmap / 카페 immutable 보충 · 환경: 기존 1.27 클러스터 + openssl/curl

기초 연결: [ConfigMap 파일 마운트](../../01-core-objects/12-configmap-secret-mount/README.md) · [롤링 업데이트](../../02-controllers/03-deployment-rollingupdate-rollback/README.md)

## 먼저 이해할 것

ConfigMap은 설정 파일을, Secret은 인증서와 키를 전달한다. 파일을 바꿔도 애플리케이션이 설정을 다시 읽어야 한다. 이 실습은 `subPath` 마운트라 기존 Pod의 파일도 자동 갱신되지 않는다. TLS 지원 여부는 실제 handshake로 확인한다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/01-configmap-tls`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

```bash
kubectl create namespace preview-config
openssl req -x509 -nodes -newkey rsa:2048 -days 2 \
  -keyout /tmp/preview-tls.key -out /tmp/preview-tls.crt \
  -subj '/CN=preview.local' -addext 'subjectAltName=DNS:preview.local'
kubectl -n preview-config create secret tls web-tls \
  --key=/tmp/preview-tls.key --cert=/tmp/preview-tls.crt
kubectl apply -f setup.yaml
kubectl -n preview-config rollout status deploy/web --timeout=120s
kubectl -n preview-config port-forward svc/web 8443:443
```

마지막 명령은 유지하고, 두 번째 셸에서 확인한다.

```bash
curl -k --tlsv1.3 --tls-max 1.3 https://localhost:8443
curl -k --tlsv1.2 --tls-max 1.2 https://localhost:8443
```

TLS 1.3은 성공하고 1.2는 실패해야 한다. curl 자체가 TLS 1.3을 지원하지 않으면 `curl -V`부터 확인한다.

## 2. 직접 바꿔보기

1. TLS 1.2와 1.3을 모두 허용한다.
2. ConfigMap만 바꾼 상태와 Pod를 재생성한 상태의 차이를 관찰한다.
3. 검증 후 ConfigMap을 immutable로 만든다. 다시 수정하려고 할 때의 오류를 관찰한다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

```bash
kubectl -n preview-config get cm nginx-config -o yaml
kubectl -n preview-config exec deploy/web -- cat /etc/nginx/nginx.conf
curl -k --tlsv1.2 --tls-max 1.2 https://localhost:8443
```

재시작 후 port-forward가 끊기면 다시 실행한다. `preview tls ok`를 확인하고 `immutable: true`도 확인한다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

```bash
kubectl apply -f solution-config.yaml
kubectl -n preview-config rollout restart deploy/web
kubectl -n preview-config rollout status deploy/web --timeout=120s
kubectl -n preview-config patch cm nginx-config --type=merge -p '{"immutable":true}'
```

immutable 설정은 마지막에 한다. immutable ConfigMap의 데이터는 수정할 수 없으므로 재실습은 namespace 삭제 후 구축부터 시작한다.

</details>

## 4. 정리 및 재실행

port-forward를 Ctrl+C로 종료한다.

```bash
kubectl delete namespace preview-config
rm -f /tmp/preview-tls.key /tmp/preview-tls.crt
```

## 강의에서 확인할 질문

- env, 일반 volume, subPath의 ConfigMap 변경 반영은 어떻게 다른가?
- 인증서 검증 실패와 TLS 버전 협상 실패는 어떻게 구분하는가?

[전체 예습 경로](../README.md)
