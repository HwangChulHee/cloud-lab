# 09. Troubleshooting Scenarios

면접에서 가장 중요한 영역 중 하나입니다. 정답 하나를 맞히는 것보다, 어떤 순서로 범위를 좁히는지를 설명하는 연습을 합니다.

## 1. 사이트 접속 불가

```text
DNS
 ↓
Load Balancer
 ↓
Security Group / NACL
 ↓
Route
 ↓
Instance
 ↓
Process
 ↓
Port
 ↓
Application
```

질문:
- DNS가 정상 resolve되는지 어떻게 확인하나요?
- ALB target이 unhealthy라면 다음으로 무엇을 보나요?
- timeout과 connection refused라면 조사 방향이 어떻게 달라지나요?

## 2. CPU 100%

```text
top / ps
 ↓
어떤 process?
 ↓
traffic 증가?
 ↓
application bug?
 ↓
CPU-bound workload?
 ↓
scale-up / scale-out / 최적화
```

## 3. 메모리가 계속 증가

```text
free / top / ps
 ↓
특정 process 확인
 ↓
memory leak?
 ↓
OOMKill?
 ↓
application log / runtime metric
```

## 4. 디스크 100%

```text
df -h
 ↓
du
 ↓
큰 파일 / directory 확인
 ↓
log / docker image / temp file 확인
 ↓
cleanup / log rotation / storage 확장
```

inode 사용량도 함께 확인할 수 있습니다.

```bash
df -i
```

## 5. ALB Target Unhealthy

```text
Health Check path
 ↓
Health Check port
 ↓
Security Group
 ↓
EC2 process
 ↓
Application endpoint
```

## 6. RDS가 느림

```text
CPU
connections
memory
IOPS / latency
slow query
lock
 ↓
원인에 따라
query optimization / index
read replica
instance resize
cache
RDS Proxy
```

## 7. Pod CrashLoopBackOff

```bash
kubectl get pods
kubectl describe pod <pod>
kubectl logs <pod>
kubectl logs <pod> --previous
```

확인 후보:
- application crash
- 환경변수 / Secret / ConfigMap
- dependency 연결 실패
- OOM
- probe 실패

## 8. Pod Pending

```text
describe / events
 ↓
CPU·Memory 부족?
PVC?
nodeSelector / affinity?
taint / toleration?
scheduler 조건?
```

## 9. 배포 직후 5xx 급증

```text
배포 시각과 장애 시각 비교
 ↓
신규 버전 metric / log 확인
 ↓
사용자 영향 판단
 ↓
필요 시 rollback
 ↓
정상화 확인
 ↓
Root Cause Analysis
```

## 10. Terraform apply 일부 실패

```text
Terraform state 확인
 ↓
실제 infrastructure 확인
 ↓
terraform plan
 ↓
drift / 부분 생성 확인
 ↓
import / state 조정 여부 판단
 ↓
재-apply
```

## 답변 템플릿

트러블슈팅 질문을 받으면 아래 구조로 답합니다.

```text
1. 증상을 정확히 확인하겠습니다.
2. 사용자 영향 범위를 확인하겠습니다.
3. 최근 변경 사항을 확인하겠습니다.
4. 상위 계층부터 범위를 좁히겠습니다.
5. metric / log / command로 가설을 검증하겠습니다.
6. 영향이 크면 우선 복구 또는 완화하겠습니다.
7. 이후 원인을 분석하고 재발 방지 조치를 하겠습니다.
```
