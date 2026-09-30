# 05. Service와 NodePort 연결 추적

> 강의 전 예습 · 참고 주제: task-service · 환경: 기존 클러스터

기초 연결: [NodePort](../../01-core-objects/05-service-nodeport/README.md) · [Labels/Selectors](../../01-core-objects/02-label-selector/README.md)

## 먼저 이해할 것

containerPort는 포트를 설명하는 메타데이터다. 애플리케이션이 실제로 listen해야 통신된다. Service selector가 Pod label과 맞아야 EndpointSlice에 backend가 생긴다. port, targetPort, nodePort는 각각 다르다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/05-service-nodeport`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

```bash
kubectl apply -f setup.yaml
kubectl -n preview-service rollout status deploy/web --timeout=120s
kubectl -n preview-service get pods --show-labels
```

## 2. 직접 바꿔보기

Deployment에 containerPort 80/TCP를 추가하고 Service `web`을 만든다. Service는 80/TCP를 같은 컨테이너 포트에 전달하고 NodePort로도 노출해야 한다. nodePort는 자동 할당한다.

성공 후 selector를 `app=missing`으로 바꾸고, 다시 복구한다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

```bash
kubectl -n preview-service get svc web
kubectl -n preview-service get endpointslices -l kubernetes.io/service-name=web
kubectl get nodes -o wide
```

Service 출력의 실제 nodePort와 접근 가능한 worker IP를 사용해 `curl http://WORKER_IP:NODE_PORT`를 실행한다. 기대 결과는 Nginx 응답이다. EndpointSlice에는 Ready Pod 주소가 있어야 한다. NodePort가 안 되면 노드 방화벽과 접근 경로도 확인한다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

```bash
kubectl -n preview-service patch deploy web --type=strategic \
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"web","ports":[{"containerPort":80,"protocol":"TCP"}]}]}}}}'
kubectl apply -f solution.yaml
kubectl -n preview-service patch svc web -p '{"spec":{"selector":{"app":"missing"}}}'
kubectl -n preview-service get endpointslices -l kubernetes.io/service-name=web
kubectl apply -f solution.yaml
```

프로토콜은 HTTP이므로 `https://`로 시험하지 않는다.

</details>

## 4. 정리 및 재실행

```bash
kubectl delete namespace preview-service
```

## 강의에서 확인할 질문

- Service가 있어도 EndpointSlice가 비어 있을 수 있는 이유는?
- containerPort를 추가한다고 Nginx의 listen 포트가 바뀌는가?

[전체 예습 경로](../README.md)
