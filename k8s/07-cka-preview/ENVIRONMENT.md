# 예습 환경과 실행 위치

## 현재 클러스터를 먼저 확인하기

```bash
kubectl config current-context
kubectl version
kubectl get nodes -o wide
kubectl get pods -A
kubectl get sc
kubectl get ingressclass
kubectl api-resources --api-group=gateway.networking.k8s.io
kubectl top nodes
```

레포에 기록된 환경은 Windows + Vagrant + Rocky Linux 8.8, Kubernetes 1.27.2, containerd다. 강의 설치 자료는 별도 1.34/Rocky 9.6 환경이다. 실제 출력이 다르면 현재 출력을 기준으로 판단한다.

## 어디서 명령을 실행할까?

- 문서의 kubectl/helm/bash 명령은 **kubeconfig가 준비된 Linux 셸**에서 실행한다. Windows PowerShell에 bash 문법을 그대로 붙이지 않는다.
- master에서 `sudo KUBECONFIG=/etc/kubernetes/admin.conf kubectl ...`을 쓰고 있다면 실습도 같은 권한으로 실행하거나 본인 kubeconfig를 올바르게 준비한다. admin.conf를 공개 저장소에 복사하지 않는다.
- YAML을 쓰는 실습은 해당 폴더로 이동한 뒤 실행한다. 저장소는 kubectl을 실행하는 머신에도 있어야 한다. 예: `git clone https://github.com/HwangChulHee/cloud-lab.git`, `cd cloud-lab/k8s/07-cka-preview/01-configmap-tls`.
- worker의 디렉터리 생성이나 control-plane manifest 수정은 문서에 표시된 **해당 노드 SSH 셸**에서 한다. kubectl 셸과 혼동하지 않는다.
- port-forward는 앞 셸에서 계속 실행하고 두 번째 셸에서 localhost로 요청한다. 두 셸은 같은 머신을 사용한다. 종료할 때 Ctrl+C로 끊는다.
- `REPLACE_*`, `CONTAINER_ID`, Controller Service/Namespace 등은 실제 조회 값으로 바꾼다. fixture의 placeholder가 있는 YAML을 그대로 apply하지 않는다.

## 환경별 진행

| 환경 | 가능한 예습 | 선행 조건 |
|---|---|---|
| 기존 1.27.2 클러스터 | 01–06, 08, 10–12, 16, 09의 정상 관찰 | TLS 도구, Metrics Server, storage provisioner, Ingress Controller, 정책 집행 CNI는 각 실습별 필요 |
| 별도 1.34 예습 클러스터 | 07 Gateway, 13 Helm, 실제 cert-manager 추가 관찰 | 버전에 맞는 Gateway API CRD/Controller와 Ingress Controller, Helm, 충분한 VM 자원 |
| 폐기 가능한 kubeadm control-plane VM | 09의 장애 주입/복구 | 호스트 SSH, sudo, crictl, VM 스냅샷 |
| CNI 없는 새 1.34 클러스터 | 14 | kubeadm 초기화 완료, 겹치지 않는 Pod/Service/VM 네트워크 |
| 별도 Ubuntu 22.04 VM | 15 | Docker, OS/아키텍처에 맞는 cri-dockerd 패키지, sudo, crictl |

### 공용 애드온 준비 기준

이 경로는 사용자 클러스터에 공용 애드온을 자동 설치하거나 기존 CNI를 교체하지 않는다. 이미 설치된 것은 재사용한다. 없으면 아래 공식 설치 가이드에서 **실제 Kubernetes 버전과 호환되는 버전**을 선택한다. 최신 release를 오래된 1.27에 무조건 설치하지 않는다.

- [Metrics Server](https://github.com/kubernetes-sigs/metrics-server): `kubectl top`이 정상이고 metrics APIService가 Available이어야 한다. kubelet 인증서/접근 문제는 metrics-server 로그에서 진단한다.
- [Local Path Provisioner](https://github.com/rancher/local-path-provisioner) 또는 기존 Longhorn: 생성한 테스트 PVC가 실제로 Bound여야 한다. provisioner 이름만 적는 것으로 설치가 끝나지 않는다.
- Ingress는 기존 Controller를 사용한다. [커뮤니티 ingress-nginx 유지보수 종료 안내](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/)에 따라 신규 설치와 일반 실습은 유지보수되는 구현을 사용한다. 기초 Canary annotation 과제는 기존 ingress-nginx 전용 비교 과제로 구분한다. 신규 환경은 [Kubernetes Ingress Controller 목록](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)에서 유지보수되는 구현과 호환성을 확인한다.
- [Gateway API 설치](https://gateway-api.sigs.k8s.io/guides/): CRD와 Controller가 둘 다 필요하다. [NGINX Gateway Fabric 호환성](https://docs.nginx.com/nginx-gateway-fabric/overview/technical-specifications/)과 [설치 안내](https://docs.nginx.com/nginx-gateway-fabric/install/helm/)를 대조한다. 자료의 설치 예시와 공식 호환표를 별도로 대조한다. 독립 과정은 공식 표에 명시된 Gateway API 1.4.1 / NGINX Gateway Fabric 2.3.0을 사용한다. [플랫폼 준비](../08-independent/PLATFORM.md)에서 고정 버전 설치 절차를 따른다. 문서의 최신 버전 설치 명령과 과거 버전 manifest를 섞지 않는다.
- Gateway 준비 완료 기준: `kubectl get gatewayclass`에서 Accepted, Gateway/HTTPRoute API 제공, Controller Pod Ready. 실제 route를 만들어 HTTPS 요청까지 검증한다.
- [Calico](https://docs.tigera.io/calico/latest/getting-started/kubernetes/requirements): 정책 객체 생성과 실제 차단/허용은 다르다. 08의 부정 테스트를 통해 집행을 확인한다.

## 자주 막히는 곳

| 증상 | 먼저 볼 것 |
|---|---|
| ImagePullBackOff | Pod Events, 실제 이미지 태그, registry 연결, VM 시간 및 인증서 오류 |
| HPA가 unknown | metrics APIService, metrics-server 로그, CPU requests |
| PVC Pending | consumer 유무, Events, provisioner, class/accessModes/nodeAffinity |
| Ingress/Gateway 응답 실패 | Controller/클래스/Conditions, Service, EndpointSlice, Pod, Host header |
| NetworkPolicy가 효과 없음 | CNI 집행 지원, 양쪽 ingress/egress, selector와 다른 허용 정책 |
| API Server 접근 실패 | SSH 접속 후 kubelet/crictl 로그와 static Pod manifest |

## 정리 원칙

preview-* namespace와 이 과정에서 만든 이름의 cluster-scoped 리소스만 정리한다. 공용 Controller, 시스템 PriorityClass, 다른 실습 PV와 CRD는 유지한다. default StorageClass annotation 변경은 먼저 기록하고 원복한다. 호스트 설정/CNI/런타임 변경은 전용 VM 스냅샷으로 복원한다.

## 기술 참고

- [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [HPA](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [PV/PVC](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Priority/Preemption](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/)
- [Gateway HTTPRoute](https://gateway-api.sigs.k8s.io/api-types/httproute/)
- [Gateway TLS](https://gateway-api.sigs.k8s.io/guides/tls/)
- [Container Runtimes](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)
- [CRD](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
- [Argo CD Helm chart](https://github.com/argoproj/argo-helm/tree/main/charts/argo-cd)
