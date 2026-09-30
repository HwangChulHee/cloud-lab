# 개념 슬라이드를 기존 기초에 연결하기

16개 과제에 직접 등장하지 않더라도 개념 강의에 나온 내용은 기존 기초와 함께 확인한다. 아래 표에서 익숙하지 않은 주제를 고르고 연결된 기초를 읽은 뒤 관찰 명령을 실행한다. 이 문서는 16개 예습을 시작하기 위한 짧은 개념 지도다.

## 1. 워크로드: 생성 요청부터 실행까지

| 구성 요소 | 역할 | 관찰할 것 |
|---|---|---|
| API Server | API 요청 처리와 객체 접근의 중심 | kubectl 요청, spec/status |
| etcd | 클러스터 상태 저장 | 제어 평면의 연결 설정 |
| Controller | 원하는 상태와 실제 상태의 차이를 조정 | Deployment → ReplicaSet → Pod, 재생성 |
| Scheduler | 아직 노드가 없는 Pod의 배치 결정 | Pod nodeName, Scheduled Events |
| kubelet | 노드에서 Pod 실행·상태 관리 | 노드 로그, 컨테이너 상태 |
| CRI/runtime | 컨테이너 생성·실행 | containerd/Docker 어댑터, runtime socket |
| CNI | Pod 네트워크 구성 | Pod IP, 노드 간 연결 |
| Service 데이터 평면 | Service 트래픽 전달 | kube-proxy 또는 구현의 대체 기능 |

컨테이너 개수와 Pod 개수는 다르다. 같은 Pod의 컨테이너들은 네트워크를 공유하므로 localhost로 통신할 수 있지만 파일시스템은 자동으로 공유되지 않는다. 공용 volume을 마운트해야 한다. PID namespace 공유도 기본으로 가정하지 않는다.

기초 연결: [멀티 컨테이너](../01-core-objects/01-pod-multicontainer/README.md), [ReplicaSet](../02-controllers/01-replicaset/README.md), [RollingUpdate/롤백](../02-controllers/03-deployment-rollingupdate-rollback/README.md), [아키텍처 종합](../06-architecture/01-architecture-observability-capstone/README.md).

```bash
kubectl get deploy,rs,pods -n preview-service
kubectl get pods -n preview-service -o wide
kubectl get events -n preview-service --sort-by=.lastTimestamp
```

05 Service 예습을 구축한 상태에서 controller 관계와 노드 배치를 확인한다. Pod를 삭제하면 새 Pod가 생성되지만 독립 Pod는 누가 다시 만드는지 별도로 생각해야 한다. Deployment의 self-healing과 readiness/liveness는 서로 다른 역할이다.

## 2. 저장소: Block/File/Object와 Kubernetes 리소스

| 종류 | 접근 방식 | 예시 | 예습에서 이해할 관계 |
|---|---|---|---|
| Block | 블록 장치 제공, 파일시스템 또는 raw block 사용 | 디스크, 클라우드 볼륨 | DB 데이터, PV의 volumeMode |
| File | 파일시스템 접근과 공유 | NFS | 여러 Pod의 데이터 공유, accessModes |
| Object | 객체 API 호출 | S3 | 애플리케이션이 SDK/API로 사용, 보통 PVC와 다른 경로 |

Block을 반드시 한 서버만 쓸 수 있다고 일반화하지 않는다. 실제 연결·공유 조건은 저장소 드라이버와 제품 기능에 달려 있다. object storage도 별도 드라이버로 파일 형태를 제공할 수 있지만, 기본적인 사용은 객체 API다.

| Kubernetes 개념 | 확인할 질문 |
|---|---|
| Volume | Pod가 어디에 어떤 데이터를 마운트하는가? |
| PVC | 용량·접근 모드·class·volumeMode 중 무엇을 요청했는가? |
| PV | 어떤 실제 저장소와 어떤 노드/접근 조건을 제공하는가? |
| StorageClass | 어느 provisioner로 언제 생성하는가? |
| CSI | Kubernetes와 저장소 구현을 연결하는 인터페이스는 무엇인가? |
| Retain/Delete | PVC 삭제 후 PV와 실제 데이터에 어떤 일이 생기는가? |

ReadWriteOnce는 일반적으로 한 **노드**에서 read-write를 허용하는 조건이지 반드시 한 Pod만 허용한다는 뜻이 아니다. ReadWriteOncePod는 지원되는 CSI 환경에서 한 Pod 접근을 위한 별도 모드다. PVC/PV의 `volumeMode: Filesystem`과 `Block`도 accessModes와 구분한다.

기초 연결: [emptyDir](../01-core-objects/08-volume-emptydir/README.md), [hostPath](../01-core-objects/09-volume-hostpath/README.md), [정적 PV/PVC](../01-core-objects/10-pv-pvc-static/README.md), [동적 프로비저닝](../04-storage-security/02-dynamic-provisioning-pv-lifecycle/README.md), [StatefulSet](../05-advanced/01-statefulset/README.md). 예습은 03–04로 이어간다.

## 3. 네트워크: 요청이 지나가는 경로

Service는 label/selector로 backend를 선택하고 EndpointSlice로 실제 주소를 관리한다. 이름 기반 접근은 DNS를 사용한다. Pod 재생성으로 IP가 바뀌어도 Service 이름을 계속 사용할 수 있지만 readiness와 selector가 맞아야 한다.

| 비교 | 관찰 기준 |
|---|---|
| 같은 namespace의 Service 이름 / 다른 namespace의 이름 | `web` / `web.preview-service` 등 DNS scope |
| ClusterIP / NodePort / LoadBalancer | 클러스터 내부 주소 / 노드 포트 / 외부 LB 구현 |
| Ingress 객체 / Controller | 선언한 규칙 / 실제로 요청을 처리하는 구현 |
| Gateway / HTTPRoute | listener/TLS / host·경로·backend |
| NetworkPolicy ingress / egress | 수신 허용 / 송신 허용, 양쪽 조건 |

LoadBalancer 타입을 만들었다고 로컬 VM에서 외부 IP가 자동 제공되는 것은 아니다. 외부 LB 구현이 있어야 한다. Ingress의 canary annotation과 HTTPRoute의 backend weight도 역할은 비슷해 보여도 서로 다른 API 설정이다. 이번 Gateway 예습의 기본 과제는 TLS와 경로 보존이며 트래픽 분할은 강의 후 확장할 수 있다.

기초 연결: [ClusterIP](../01-core-objects/04-service-clusterip/README.md), [DNS](../01-core-objects/06-service-dns/README.md), [Headless/Endpoint](../01-core-objects/07-headless-endpoint-externalname/README.md), [Ingress Canary/TLS](../05-advanced/03-ingress-canary-tls/README.md). 예습은 05–08로 이어간다.

## 4. 스케줄링·자원·중단 제어

| 기능 | 어떤 문제를 다루는가? | 기초 연결 |
|---|---|---|
| nodeSelector/nodeAffinity | 어떤 노드 조건을 선택할까? | [Node Affinity](../03-pod-deep-dive/05-node-affinity/README.md) |
| podAffinity/antiAffinity | 어떤 Pod와 가깝게/떨어져 배치할까? | [Pod Affinity](../03-pod-deep-dive/06-pod-affinity-antiaffinity/README.md) |
| taint/toleration | 노드가 거부하는 조건을 허용할까? | [Taints](../03-pod-deep-dive/07-taints-tolerations/README.md) |
| requests/limits | 예약할 자원과 실행 시 제한은? | [기초 자원](../01-core-objects/03-node-scheduling-resources/README.md) |
| ResourceQuota/LimitRange | namespace 총량과 개별 기본값/범위는? | [Quota](../01-core-objects/14-resourcequota-limitrange/README.md) |
| QoS | 컨테이너 자원 설정에 따른 분류는? | [QoS](../03-pod-deep-dive/04-qos/README.md) |
| PriorityClass | 스케줄링 순서와 선점 우선순위는? | [12 예습](./12-priorityclass/README.md) |
| PDB | 자발적 중단 시 가용 Pod 수를 어떻게 지킬까? | 아래 작은 관찰 실습 |

Toleration은 해당 노드로 보내는 명령이 아니다. nodeName 직접 지정은 scheduler를 우회하므로 affinity나 WaitForFirstConsumer 관찰에 섞지 않는다. QoS만으로 모든 퇴거 순서를 단정하지 않고 자원 초과 사용, Priority, 노드 상태도 함께 본다. PDB는 모든 Pod 삭제나 장애를 막는 보호막이 아니다.

### 작은 관찰: PDB와 Eviction

저장소 루트에서 다음을 실행한다. 노드를 drain하지 않고 예습 Pod 한 개의 Eviction API만 호출한다.

```bash
kubectl apply -f k8s/07-cka-preview/support/pdb.yaml
kubectl -n preview-disruption rollout status deploy/web --timeout=120s
kubectl -n preview-disruption get pdb
kubectl -n preview-disruption patch pdb web -p '{"spec":{"minAvailable":3}}'
kubectl -n preview-disruption get pdb web -w
```

ALLOWED DISRUPTIONS가 0인 것을 확인한 뒤 watch를 Ctrl+C로 종료하고 실행한다.

```bash
PDB_POD=$(kubectl -n preview-disruption get pod -l app=web -o jsonpath='{.items[0].metadata.name}')
cat > /tmp/preview-eviction.json <<EOF
{"apiVersion":"policy/v1","kind":"Eviction","metadata":{"name":"$PDB_POD","namespace":"preview-disruption"}}
EOF
kubectl create --raw "/api/v1/namespaces/preview-disruption/pods/$PDB_POD/eviction" -f /tmp/preview-eviction.json
```

PDB를 위반해 eviction할 수 없다는 응답을 예상한다. 이후 `kubectl -n preview-disruption delete pod "$PDB_POD"`는 직접 삭제라 PDB로 막히지 않는 점을 비교하고 Deployment가 다시 3개를 만드는지 확인한다. 강제 노드 장애에도 PDB가 Pod 가용성을 보장하는 것은 아니다.

```bash
kubectl -n preview-disruption rollout status deploy/web --timeout=120s
kubectl delete namespace preview-disruption
rm -f /tmp/preview-eviction.json
```

## 5. 설치와 확장 인터페이스

| 도구/인터페이스 | 담당 영역 | 이어갈 예습 |
|---|---|---|
| kubeadm | 클러스터 bootstrap과 관리 | 09의 kubeadm/static Pod 관찰 |
| Helm | Chart 렌더링과 release 관리 | 13 |
| CRD | 사용자 API 타입과 schema 등록 | 16 |
| Operator | Custom Resource를 실제 상태로 조정 | 14의 Tigera Operator, 실제 cert-manager 추가 관찰 |
| CNI | Pod 네트워크 | 14 |
| CRI | kubelet과 runtime 통신 | 15 |
| CSI | 저장소 드라이버 | 기존 동적 스토리지 실습, 03–04 |

kubelet과 runtime의 cgroup driver 일치도 런타임 준비에서 확인한다. `systemctl cat kubelet`과 실제 runtime 설정을 조사하되 기존 노드의 설정을 임의로 바꾸지 않는다. 이 예습 자료는 설치 마법사를 대체하기보다 각 구성 요소가 필요한 이유와 실패 지점을 먼저 익히는 경로다.

## 6. 요청의 승인 단계와 실패 위치

생성·변경 요청은 인증(Authentication), 권한 확인(Authorization), Admission의 기본값·정책 검사를 거쳐 저장된다. 인증 사용자라고 모든 리소스를 만들 수 있는 것은 아니고, RBAC가 허용해도 Quota나 Admission 정책이 요청을 거부할 수 있다.

| 증상 | 우선 확인할 근거 |
|---|---|
| API 401 | kubeconfig context, 인증서/token 유효성 |
| API 403 | 응답 원인과 `kubectl auth can-i`; RBAC 또는 Admission 거부 구분 |
| Deployment는 있지만 Pod가 없음 | ReplicaSet Events의 FailedCreate, Quota/LimitRange |
| Pod가 있고 Pending | Scheduled condition, requests/affinity/taints, PVC binding |
| Pod가 배치됐지만 시작 실패 | image, volume mount, init container, runtime Events |

Quota는 실제 CPU 사용률을 측정해 과부하 Pod를 퇴거시키는 기능이 아니다. namespace의 리소스 사용 집계와 생성·변경 허용 조건을 다룬다. scheduler도 단순히 `kubectl top`에서 가장 한가한 노드를 선택하지 않는다. requests와 배치 조건을 만족하는 노드를 찾은 뒤 scoring한다.

## 7. 네트워크와 관찰 도구의 경계

Node 네트워크, Pod CIDR, Service CIDR을 구분한다. 실제 클러스터 설정을 조회하고 노드/호스트/VPN 주소와 겹치지 않게 설계한다. 강의 그림의 주소를 그대로 설치값으로 복사하지 않는다. ClusterIP는 Service를 위한 가상 주소이며 일반적으로 실제 인터페이스 주소나 특정 Pod 주소가 아니다. CNI의 Pod 연결 기능과 NetworkPolicy 집행 지원도 따로 확인한다.

API Server는 객체 제어 경로이고, 일반적인 애플리케이션 HTTP 요청은 Service/Ingress/Gateway 데이터 경로로 흐른다. CoreDNS는 Service 이름 등을 해석하지만 임의 Pod 이름이 항상 DNS 이름이 되는 것은 아니다. Headless Service와 hostname/subdomain 조건을 함께 본다.

로그는 `앱 stdout/stderr → 런타임 로그 파일 → kubelet의 logs API → kubectl logs`로 관찰한다. 앱이 컨테이너 파일에만 기록하면 그 내용이 자동으로 `kubectl logs`에 나오지 않는다. 노드별 수집 에이전트와 중앙 저장소는 별도 구성이다. `kubectl logs --previous`는 직전 컨테이너 인스턴스 확인이며 영구 이력 저장소를 대신하지 않는다. Metrics Server의 최근 자원 사용량, Prometheus 같은 시계열 저장소, 앱 로그를 서로 구분한다.

일반 init container는 순차 실행 후 성공해야 앱 컨테이너가 시작된다. 1.27의 일반 init container와 1.34 예습의 `restartPolicy: Always`인 native sidecar는 종료 조건과 자원 계산이 같지 않다. [Sidecar 예습](./10-sidecar-logging/README.md)의 버전 조건을 먼저 확인한다.

공식 참고: [Admission](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/), [클러스터 로그](https://kubernetes.io/docs/concepts/cluster-administration/logging/), [Service](https://kubernetes.io/docs/concepts/services-networking/service/).

[혼합 예습 경로](./README.md)
