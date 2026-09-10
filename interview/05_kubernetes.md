# 05. Kubernetes

## 핵심 질문

1. Kubernetes를 왜 사용하나요?
2. Pod란 무엇인가요?
3. Deployment란 무엇인가요?
4. Deployment와 StatefulSet의 차이는 무엇인가요?
5. Service가 필요한 이유는 무엇인가요?
6. ClusterIP, NodePort, LoadBalancer 차이는 무엇인가요?
7. Pod가 `CrashLoopBackOff` 상태입니다. 어떻게 조사하나요?
8. `kubectl logs`와 `kubectl describe`는 언제 사용하나요?
9. readinessProbe와 livenessProbe의 차이는 무엇인가요?
10. requests와 limits의 차이는 무엇인가요?
11. Pod가 Pending 상태에서 올라오지 않는 이유에는 무엇이 있나요?
12. Rolling Update는 어떻게 동작하나요?

## 장애 대응 기본 명령

```bash
kubectl get pods
kubectl describe pod <pod>
kubectl logs <pod>
kubectl logs <pod> --previous
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl get svc
kubectl get deploy
```

## 실전형 질문

### Pod가 CrashLoopBackOff입니다.

```text
Pod 상태 확인
 ↓
describe로 event 확인
 ↓
현재 / 이전 container log 확인
 ↓
환경변수 / Secret / ConfigMap 확인
 ↓
외부 dependency 확인
 ↓
OOM / probe 실패 / application crash 여부 확인
```

### Pod가 Pending입니다.

```text
kubectl describe pod
 ↓
Scheduler event 확인
 ↓
CPU / memory 부족?
PVC binding 실패?
nodeSelector / affinity 문제?
taint / toleration 문제?
```
