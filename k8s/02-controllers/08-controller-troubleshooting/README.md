# Lab 24 — Controller Troubleshooting: Desired vs Observed

> **종합 진단 Lab** · Namespace `lab-controller-diagnosis` · Lab 17–23의 ReplicaSet, Deployment, DaemonSet, Job 개념 재사용

## 1. Overview — 왜 Pod를 지워도 다시 생길까?

Deployment Controller는 ReplicaSet을, ReplicaSet Controller는 Pod의 개수를 조정한다. Scheduler는 미배치 Pod의 Node를 선택하고, kubelet은 배치된 Node에서 컨테이너를 실행한다. 각 Controller는 API Server의 상태를 watch/list하고 **실제와 원하는 상태 차이를 반복 조정(Reconciliation)**한다. 변경 알림을 한 번 놓쳤다고 영원히 동작하지 않는 단순 이벤트 핸들러가 아니다.

`metadata.generation`은 spec 변경에 따라 증가하고 `status.observedGeneration`은 Controller가 관측한 세대를 나타낸다. 두 값의 차이는 잠시 정상일 수 있지만 오래 지속된다면 Controller 조정·권한·API 연결 등을 확인한다.

## 2. Build — 정상 복제본과 소유 관계 확인

```bash
kubectl apply -f k8s/02-controllers/08-controller-troubleshooting/controller-diagnosis.yaml
kubectl -n lab-controller-diagnosis rollout status deploy/web --timeout=180s
kubectl -n lab-controller-diagnosis get deploy,rs,pods,jobs -o wide
kubectl -n lab-controller-diagnosis get deployment web -o jsonpath='{.metadata.generation}{" / "}{.status.observedGeneration}{"\n"}'
kubectl -n lab-controller-diagnosis get rs -o custom-columns=NAME:.metadata.name,OWNER:.metadata.ownerReferences[0].name,DESIRED:.spec.replicas,READY:.status.readyReplicas
kubectl -n lab-controller-diagnosis get pods -l app=web -o custom-columns=NAME:.metadata.name,OWNER:.metadata.ownerReferences[0].name,UID:.metadata.uid,NODE:.spec.nodeName
```

**예상:** Deployment 2/2 Ready, ReplicaSet의 ownerReference가 Deployment, Pod의 ownerReference는 ReplicaSet이다. Job `completed`는 `Complete`가 되더라도 Pod가 남을 수 있다.

## 3. 장애 A — Pod 직접 삭제

```bash
kubectl -n lab-controller-diagnosis get pods -l app=web -o wide
WEB_POD=$(kubectl -n lab-controller-diagnosis get pod -l app=web -o jsonpath='{.items[0].metadata.name}')
kubectl -n lab-controller-diagnosis delete pod "$WEB_POD"
kubectl -n lab-controller-diagnosis get pods -l app=web -o wide
kubectl -n lab-controller-diagnosis get rs -o wide
```

**예상:** ReplicaSet이 새 Pod를 생성하여 desired=2로 수렴한다. 삭제된 Pod와 새 Pod의 UID는 다르다. Deployment 객체 자체가 직접 컨테이너를 재시작한 것은 아니다.

## 4. 장애 B — 잘못된 이미지로 Rollout 정체

```bash
kubectl -n lab-controller-diagnosis set image deploy/web web=example.invalid/k8s/no-image:bad
kubectl -n lab-controller-diagnosis get deploy,rs,pods -o wide
kubectl -n lab-controller-diagnosis describe deployment web
kubectl -n lab-controller-diagnosis get events --sort-by=.lastTimestamp
```

**예상:** 신규 ReplicaSet은 이미지 Pull 실패로 Ready를 확보하지 못한다. RollingUpdate 전략 덕분에 이전 정상 Pod 일부가 남을 수 있다. `ProgressDeadlineExceeded`는 설정된 deadline 이후 나타날 수 있으므로 **즉시 발생한다고 단정하지 않는다**. 이 사례의 첫 증거는 Deployment/ReplicaSet의 spec/status와 새 Pod Events다.

복구:

```bash
kubectl -n lab-controller-diagnosis set image deploy/web web=nginx:1.28-alpine
kubectl -n lab-controller-diagnosis rollout status deploy/web --timeout=180s
kubectl -n lab-controller-diagnosis get deploy,rs,pods -o wide
```

## 5. 실패 증상별 책임 계층 비교

| 사용자에게 보이는 상태 | 결정적 증거 | 먼저 확인할 곳 |
|---|---|---|
| Deployment Ready 개수 부족 | ReplicaSet desired/current/ready, Pod Events | Controller → Scheduler → kubelet |
| Pod가 Pending | FailedScheduling Event | Node label, affinity, taint, requests |
| Pod가 ImagePullBackOff | Pull 실패 Event, Container status | Image 이름, registry 연결, credentials |
| Pod가 Running지만 Ready=False | Probe 상태, EndpointSlice ready condition | kubelet/앱 |
| Job이 성공한 뒤 Pod가 남음 | Job Complete, Pod Succeeded | Job 완료와 TTL/정리 정책 |

DaemonSet의 Node별 Pod 수 불일치는 [Lab 21](../05-daemonset/README.md), Job 재시도는 [Lab 22](../06-job/README.md)를 연결해 진단한다. 이 Lab에서 동일한 자원 변경 과제를 전부 반복하지 않는다.

## 6. Cleanup / Evidence / Recall

```bash
kubectl delete namespace lab-controller-diagnosis
```

완료 기준: 정상 2/2 → Pod 삭제 후 새 UID/2/2 → 잘못된 이미지 배포에서 새 ReplicaSet/Events → 이미지 원복 후 2/2 → Namespace 정리.

인출 질문: (1) Watch가 끊겨도 Controller가 다시 일치 상태를 맞출 수 있는 이유 (2) ownerReference가 Pod 재생성을 결정하는가, 최종적으로 원하는 replica 수를 유지하는 주체는 누구인가 (3) `observedGeneration`이 같아도 왜 Pod가 Ready가 아닐 수 있는가?

[공식 Controller 개념](https://kubernetes.io/docs/concepts/architecture/controller/).
