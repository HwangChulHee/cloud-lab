# 08. 최소 권한 NetworkPolicy

> 독립 실행 가능한 확장 실습 · 참고 주제: task-networkpolicy · 환경: NetworkPolicy를 실제 집행하는 CNI

기초 연결: [Namespace](../../01-core-objects/13-namespace/README.md) · [Labels/Selectors](../../01-core-objects/02-label-selector/README.md)

[독립 과정에서의 위치](../../08-independent/08-operations/README.md). 처음에는 예시 풀이를 참고해 구축하고, 두 번째에는 요구사항만 보고 실행한다. 강의 수강은 선행 조건이 아니다.

## 먼저 이해할 것

NetworkPolicy는 선택된 Pod의 ingress/egress 허용 범위를 누적한다. deny-all을 유지하면서 필요한 허용 정책을 추가한다. 송신 측 egress와 수신 측 ingress가 둘 다 허용돼야 한다. 같은 peer 안의 namespaceSelector와 podSelector는 AND 조건이다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/08-networkpolicy`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

```bash
kubectl apply -f setup.yaml
kubectl -n preview-backend rollout status deploy/backend --timeout=120s
kubectl -n preview-frontend wait --for=condition=Ready pod --all --timeout=120s
BACKEND_IP=$(kubectl -n preview-backend get pod -l app=backend -o jsonpath='{.items[0].status.podIP}')
kubectl -n preview-frontend exec frontend -- wget -T 3 -qO- "http://$BACKEND_IP"
kubectl apply -f deny-all.yaml
kubectl -n preview-frontend exec frontend -- wget -T 3 -qO- "http://$BACKEND_IP"
```

적용 전 성공·적용 후 실패여야 한다. 정책 전파에 약간 시간이 걸릴 수 있다. 계속 성공하면 CNI 집행 기능부터 확인한다. API에 객체가 저장됐다는 사실은 집행의 증거가 아니다.

## 2. 직접 바꿔보기

1. `candidates/`의 정책 중 가장 제한적이면서 frontend → backend:80을 허용하는 수신 정책을 고른다.
2. 송신 측 frontend와 검증용 other 모두 backend:80으로만 egress를 허용한다. other의 송신을 열어둬야 backend ingress가 other를 실제로 거부하는지 검증할 수 있다.
3. deny-all은 유지한다.
4. `other` Pod는 여전히 접근할 수 없어야 한다.

여기서는 Pod IP로 시험한다. Service DNS 이름으로 확장하려면 별도로 DNS egress를 허용해야 한다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

```bash
kubectl -n preview-frontend exec frontend -- wget -T 3 -qO- "http://$BACKEND_IP"
kubectl -n preview-frontend exec other -- wget -T 3 -qO- "http://$BACKEND_IP"
kubectl get netpol -n preview-frontend
kubectl get netpol -n preview-backend
```

frontend만 성공하고 other는 timeout이어야 한다. other가 송신 정책 때문에 차단되면 광범위한 수신 정책도 정답처럼 보이므로, solution의 송신 정책은 두 클라이언트 모두를 선택한다. 양쪽 deny-all이 남아 있어야 한다. Pod가 재생성됐다면 BACKEND_IP를 다시 조회한다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

```bash
kubectl apply -f candidates/restrictive.yaml
# 아직 송신 측이 막혀 있으므로 요청은 실패한다.
kubectl apply -f solution.yaml
```

수신 정책 차이를 확실히 보려면 최소 egress를 둔 상태에서 restrictive를 제거하고 too-broad를 잠시 적용한다. 이때 other까지 성공하면 광범위 수신 허용이 검출된 것이다. 검증 후 too-broad를 삭제하고 restrictive를 복구한다.

비교 명령은 다음과 같다. other의 송신이 허용된 `solution.yaml`을 먼저 적용한 상태에서 실행한다.

```bash
kubectl -n preview-backend delete netpol allow-frontend
kubectl apply -f candidates/too-broad.yaml
kubectl -n preview-frontend exec other -- wget -T 3 -qO- "http://$BACKEND_IP"
# 위 요청이 성공하는 것을 관찰한 뒤 광범위 수신 허용을 제거한다.
kubectl -n preview-backend delete netpol too-broad
kubectl apply -f candidates/restrictive.yaml
kubectl -n preview-frontend exec frontend -- wget -T 3 -qO- "http://$BACKEND_IP"
kubectl -n preview-frontend exec other -- wget -T 3 -qO- "http://$BACKEND_IP"
```

정책 전파 후 frontend는 성공, other는 다시 실패해야 한다. 너무 넓은 정책을 먼저 적용했다면 삭제한다. 정책은 합집합이라 restrictive 정책을 추가해도 기존 광범위 허용이 취소되지 않는다.

```bash
kubectl -n preview-backend delete netpol too-broad wrong-label --ignore-not-found
```

</details>

## 4. 정리 및 재실행

```bash
kubectl delete namespace preview-frontend preview-backend
```

## 스스로 설명할 질문

- ingress만 허용했는데 통신이 안 될 수 있는 이유는?
- 두 selector를 같은 peer에 쓰는 것과 서로 다른 peer로 쓰는 것은 어떻게 다른가?

[전체 확장 경로](../README.md)
