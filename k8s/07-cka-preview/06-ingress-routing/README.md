# 06. Ingress의 host와 path 라우팅

> 독립 실행 가능한 확장 실습 · 참고 주제: task-ingress · 환경: 기존 클러스터 + 설치된 Ingress Controller

기초 연결: [Ingress Routing](../../05-advanced/02-ingress-routing/README.md) · [Service DNS](../../01-core-objects/06-service-dns/README.md)

[독립 과정에서의 위치](../../08-independent/08-operations/README.md). 처음에는 예시 풀이를 참고해 구축하고, 두 번째에는 요구사항만 보고 실행한다. 강의 수강은 선행 조건이 아니다.

## 먼저 이해할 것

Ingress는 규칙이며 Controller가 실제 트래픽을 처리한다. Host header와 path가 함께 맞아야 한다. 이 backend는 모든 경로에서 200을 반환하므로 rewrite annotation 없이 라우팅 자체에 집중할 수 있다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/06-ingress-routing`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

```bash
kubectl get ingressclass
kubectl get pods,svc -A | grep -i ingress
kubectl apply -f setup.yaml
kubectl -n preview-ingress rollout status deploy/web --timeout=120s
```

Controller가 없으면 이 단계에서 멈추고 별도 예습 환경의 Controller를 준비한다. 기존 controller의 namespace/service 이름과 접근 방법(NodePort 또는 port-forward)을 기록한다.

## 2. 직접 바꿔보기

host `preview.local`, path `/echo`, backend `web:80`인 Ingress를 만든다. ingressClassName은 실제 설치된 클래스 이름을 사용한다.

1. 올바른 host/path로 요청한다.
2. 다른 Host header 또는 `/other` 경로로 요청해 비교한다.
3. backend Service 이름을 틀리게 바꾼 뒤 진단하고 복구한다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

Controller Service를 실제 namespace/name으로 port-forward한다. 예: `kubectl -n CONTROLLER_NS port-forward svc/CONTROLLER_SERVICE 8080:80`. 다른 셸에서:

```bash
curl -i -H 'Host: preview.local' http://localhost:8080/echo
curl -i -H 'Host: wrong.local' http://localhost:8080/echo
kubectl -n preview-ingress describe ingress web
kubectl -n preview-ingress get endpointslices -l kubernetes.io/service-name=web
```

정상 경로는 200과 `ingress-preview-ok`다. 다른 host/path는 이 실습 backend로 가지 않아야 한다. 실패 상태코드는 controller의 기본 backend 설정에 따라 다를 수 있다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

`solution.yaml`의 `REPLACE_INGRESS_CLASS`를 실제 값으로 바꾸고 apply한다.

```bash
kubectl apply -f solution.yaml
kubectl -n preview-ingress patch ingress web --type=json \
  -p='[{"op":"replace","path":"/spec/rules/0/http/paths/0/backend/service/name","value":"missing"}]'
kubectl -n preview-ingress describe ingress web
kubectl apply -f solution.yaml
```

Ingress → Service → EndpointSlice → Pod 순서로 따라간다.

</details>

## 4. 정리 및 재실행

port-forward를 종료하고 실행한다. 공용 Controller는 유지한다.

```bash
kubectl delete namespace preview-ingress
```

## 스스로 설명할 질문

- IngressClass와 Ingress Controller는 각각 무엇인가?
- Host header만 바꿨는데 응답이 달라지는 이유는?

[전체 확장 경로](../README.md)
