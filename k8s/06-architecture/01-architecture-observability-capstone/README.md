# Lab 42 — Kubernetes 통합 장애 진단 Capstone

> **필수 종합 Lab** · 기초 01–41 복습 · `lab-capstone` Namespace · 개념 설명이 아니라 **증거를 남기는 운영 과제**

## 1. Overview — 동일한 HTTP 실패, 다른 원인

Deployment, ConfigMap, Readiness Probe, Service, EndpointSlice, CoreDNS와 Node 스케줄링을 하나의 앱으로 연결한다. 사용자 증상은 모두 "web 접속 실패"여도 Controller, Scheduler, kubelet, 네트워크의 책임을 나눠야 한다.

먼저 예측한다. Service DNS가 성공해도 앱 호출이 실패할 수 있는 경우 세 가지는? Pod `Running`과 `Ready`의 차이는? `FailedScheduling`과 `FailedCreate`는 어느 계층의 장애인가?

## 2. Build — 재현 가능한 기준 상태

저장소 루트, kubeconfig가 설정된 VM에서 진행한다.

```bash
kubectl config current-context
kubectl apply -f k8s/06-architecture/01-architecture-observability-capstone/capstone.yaml
kubectl -n lab-capstone rollout status deploy/web --timeout=180s
kubectl -n lab-capstone wait --for=condition=Ready pod/client --timeout=120s
kubectl -n lab-capstone get deploy,pod,svc,endpointslices -o wide
kubectl -n lab-capstone exec client -- nslookup web
kubectl -n lab-capstone exec client -- wget -qO- http://web
kubectl -n lab-capstone exec deploy/web -- printenv MESSAGE
```

**예상:** 1/1 Ready, web EndpointSlice의 `ready: true`, `wget`에서 nginx 기본 응답, `MESSAGE=healthy`. 이 성공 기준을 각 장애 직전에 반복해서 비교한다.

## 3. 장애 A — Selector 불일치 (Service 대상 없음)

먼저 예측: DNS 응답이 사라질까? Pod Ready는 바뀔까?

```bash
kubectl -n lab-capstone patch svc web -p '{"spec":{"selector":{"app":"missing"}}}'
kubectl -n lab-capstone get svc web -o yaml
kubectl -n lab-capstone get endpointslices -l kubernetes.io/service-name=web -o yaml
kubectl -n lab-capstone get pod -l app=web
kubectl -n lab-capstone exec client -- nslookup web
kubectl -n lab-capstone exec client -- wget -T 3 -qO- http://web
```

마지막 호출은 실패하는 것이 예상 결과다. CoreDNS/ClusterIP가 유지되는지, EndpointSlice의 대상이 사라지거나 ready endpoint가 없어지는지를 관찰한다. 실제 연결 시도 결과는 kube-proxy 구현 및 시점에 따라 다를 수 있다.

복구:

```bash
kubectl -n lab-capstone patch svc web -p '{"spec":{"selector":{"app":"web"}}}'
kubectl -n lab-capstone get endpointslices -l kubernetes.io/service-name=web
kubectl -n lab-capstone exec client -- wget -qO- http://web
```

## 4. 장애 B — Readiness 실패 (Pod Running, Ready=False)

```bash
kubectl -n lab-capstone exec deploy/web -- rm /tmp/ready
kubectl -n lab-capstone get pods -o wide
kubectl -n lab-capstone get endpointslices -l kubernetes.io/service-name=web -o yaml
kubectl -n lab-capstone exec client -- wget -T 3 -qO- http://web
```

Probe 주기·failureThreshold 반영을 기다리고 `kubectl -n lab-capstone describe pod -l app=web` 및 Events를 확인한다. 컨테이너가 Running이어도 Pod Ready=False이면 Service 라우팅 대상에서 제외될 수 있다. **Pod 재시작 횟수가 증가한다고 가정하지 않는다.**

복구:

```bash
kubectl -n lab-capstone exec deploy/web -- touch /tmp/ready
kubectl -n lab-capstone rollout status deploy/web --timeout=120s
kubectl -n lab-capstone exec client -- wget -qO- http://web
```

## 5. 장애 C — Scheduler Filter 실패

`Recreate` 전략을 사용하므로 다음 템플릿 변경 시 기존 Pod가 종료되고 새로운 Pod가 Pending이 된다. 현재는 폐기 가능한 `lab-capstone` 앱에만 적용한다.

```bash
kubectl -n lab-capstone patch deploy web --type=merge -p '{"spec":{"template":{"spec":{"nodeSelector":{"cloud-lab/impossible":"true"}}}}}'
kubectl -n lab-capstone get pods -o wide
kubectl -n lab-capstone get events --sort-by=.lastTimestamp
kubectl -n lab-capstone describe pod -l app=web
```

**예상:** `FailedScheduling`, `0/N nodes are available` 관련 Event. 리소스 부족, taint, nodeSelector, affinity 조건과 비교한다. **Readiness 장애가 아니라 Pod 자체를 배치할 수 없는 상태**다.

복구:

```bash
kubectl -n lab-capstone patch deploy web --type=merge -p '{"spec":{"template":{"spec":{"nodeSelector":null}}}}'
kubectl -n lab-capstone rollout status deploy/web --timeout=180s
kubectl -n lab-capstone exec client -- wget -qO- http://web
```

## 6. 선택 장애 D — Ingress/TLS

[Lab 40](../../05-advanced/03-ingress-canary-tls/README.md)의 앱과 Ingress를 이용해 TLS Secret 이름 불일치나 host 불일치를 재현한다. `curl -k`의 성공만으로 인증서 검증 성공이라고 판정하지 말고 CA·SNI·host를 구분한다. **별도 namespace의 리소스를 조작하기 전 소유 여부를 확인**한다.

## 7. 운영 보고서와 완료 기준

[운영 사고 기록 양식](./INCIDENT_TEMPLATE.md)을 사용한다. 각 사례마다 **증상 → 가설 2개 이상 → 가장 판별력 있는 조회 명령 → 실제 증거 → 최소 수정 → 복구 검증 → 재발 방지**를 작성한다. 정답을 먼저 읽지 않고 장애 이름을 가린 상태에서 적어도 두 사례를 독립 재현·복구한다.

선택적으로 [Metrics Server](../../guides/ADDONS.md#metrics-server)를 통한 `kubectl top`, Container/Node 로그, 상태/Events를 수집한다. 로그만 있고 관측 시간과 실제 영향 범위가 없으면 분석 완료로 표시하지 않는다.

**완료 조건:** 장애 A–C를 모두 재현하고, A/B/C 중 임의 2개를 순서 힌트 없이 진단해 복구한다. 중간 출력과 최종 HTTP 성공 증거, 운영 보고서를 남긴다. 이때 CKA의 별도 관리 작업 완료로 계산하지 않는다.

## 8. Cleanup

```bash
kubectl delete namespace lab-capstone
kubectl get namespace lab-capstone
```

Namespace가 삭제되는지 확인한다. Node label/taint, 공용 애드온, StorageClass, 다른 Lab의 PVC는 수정하지 않는다.

## 공식 참고

- [Service / EndpointSlice](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Pod Lifecycle와 Probe](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- [Scheduling / Assigned Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
