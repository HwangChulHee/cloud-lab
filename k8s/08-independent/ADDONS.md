# 공용 애드온 준비 — 필요한 단계에서 설치하기

모든 명령은 START의 kubeconfig가 준비된 Linux 셸, 저장소 루트에서 실행한다. 현재 애드온부터 조회하고 **해당 리소스가 없는 학습 클러스터**에만 설치한다. 조회가 Forbidden/연결 실패이면 미설치로 판단하지 말고 권한/연결을 먼저 해결한다. 이미 있는 다른 버전의 Deployment나 공용 설정을 덮어쓰지 않는다.

## Metrics Server

08의 HPA 실습에 필요하다. `kubectl top nodes`가 정상이면 설치는 생략한다.

```bash
kubectl -n kube-system get deploy metrics-server
kubectl get apiservice v1beta1.metrics.k8s.io
kubectl top nodes
```

미설치면 기본 1.27용 고정 버전 0.7.2를 설치한다. [공식 호환표](https://github.com/kubernetes-sigs/metrics-server#compatibility-matrix)는 0.7.x에 Kubernetes 1.27+를 명시한다. 최신 매니페스트를 오래된 클러스터에 무조건 설치하지 않는다.

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.7.2/components.yaml
kubectl -n kube-system rollout status deploy/metrics-server --timeout=180s
kubectl -n kube-system logs deploy/metrics-server --tail=50
kubectl top nodes
```

인증서 SAN/CA 검증 오류가 있으면 로그로 확인한다. 정상 방법은 kubelet serving 인증서를 올바르게 구성하는 것이다. 폐기 가능한 로컬 VM에서 그 인증서 오류를 확인했고 우선 metrics 실습만 진행할 때는 아래 학습용 우회를 쓸 수 있다. 다른 문제를 무조건 이 옵션으로 해결하려 하지 않는다.

```bash
kubectl -n kube-system patch deploy metrics-server --type=json \
  -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
kubectl -n kube-system rollout status deploy/metrics-server --timeout=180s
kubectl top nodes
```

이 옵션은 kubelet 인증서 검증을 생략한다. 설치한 원본 args와 변경 여부를 기록하고, 실습 외 환경의 설정으로 사용하지 않는다. APIService Available와 실제 Pod metrics를 모두 확인한다.

## Local Path Provisioner

06의 동적 저장소용이다. 먼저 `kubectl get sc`와 `kubectl -n local-path-storage get deploy`로 확인한다. 같은 provisioner가 이미 있으면 재사용한다. 이 과정은 default StorageClass annotation을 변경하지 않고 각 PVC에 class를 지정한다.

```bash
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.37/deploy/local-path-storage.yaml
kubectl -n local-path-storage rollout status deploy/local-path-provisioner --timeout=180s
kubectl get sc
kubectl -n local-path-storage logs deploy/local-path-provisioner --tail=30
```

[공식 설치와 제약](https://github.com/rancher/local-path-provisioner)은 Kubernetes 1.12+와 노드 로컬 디렉터리 사용, 용량 제한 미지원 등을 설명한다. 설치 Pod가 Ready인 것과 PVC가 실제로 Bound가 되는 것은 다르다. 06의 StatefulSet이 생성한 두 PVC까지 확인한다.

## Traefik Ingress

08의 HTTP/TLS와 확장 06에 사용할 독립 Controller다. Helm이나 Traefik CRD 없이 표준 Ingress만 사용한다. `lab-traefik` 클래스는 기존 Controller의 default class를 바꾸지 않는다. 학습용 고정 이미지 v3.6.1과 표준 apps/v1/networking.k8s.io/v1 리소스를 사용한다.

```bash
kubectl get ingressclass
kubectl apply -f k8s/08-independent/traefik.yaml
kubectl -n lab-self-ingress rollout status deploy/traefik --timeout=180s
kubectl -n lab-self-ingress logs deploy/traefik --tail=40
kubectl get ingressclass lab-traefik
```

Controller는 lab-self-edge, preview-ingress, preview-gateway 세 namespace만 감시한다. Secret/Service/Ingress 읽기는 각 namespace의 Role로, Node/IngressClass 읽기는 전용 ClusterRole로 준다. 08 문서대로 실제 HTTP/TLS 요청을 확인해야 준비 완료다. Ingress의 ADDRESS가 비어 있어도 port-forward 기반 실습은 가능하다.

확장 06의 ingressClassName placeholder는 `lab-traefik`, Controller는 namespace `lab-self-ingress`의 Service `traefik`으로 설정한다. 해당 확장의 setup이 namespace를 다시 생성해도 Role/RoleBinding은 삭제되지 않는다. namespace 정리 후 재실행한다면 `traefik.yaml`도 다시 apply해 권한을 복구한다.

참고: [Traefik Kubernetes Ingress 설정](https://doc.traefik.io/traefik/reference/install-configuration/providers/kubernetes/kubernetes-ingress/).

## 애드온 정리

개별 실습 정리는 **앱 namespace와 테스트 리소스만** 대상으로 한다. 공용 애드온은 이후 단계에서도 재사용하므로 매번 삭제하지 않는다.

전 과정을 마친 뒤, 직접 설치한 애드온만 다음과 같이 정리한다.

- Traefik: `lab-self-edge`, `preview-ingress`, `preview-gateway` 앱 실습 정리를 먼저 끝낸다. 세 namespace가 비어 있고 본인 실습 소유임을 확인한 경우에만 `kubectl delete -f k8s/08-independent/traefik.yaml`을 실행한다. 이 파일은 세 namespace도 포함한다.
- Local Path: 이 provisioner의 PVC/PV를 모두 정리하고 실제 데이터 삭제까지 확인한 뒤 설치 때 사용한 v0.0.37 URL을 `kubectl delete -f`에 전달한다. 다른 실습이 이 provisioner를 쓰면 유지한다.
- Metrics Server: 기존부터 설치된 것은 유지한다. 본인이 설치했고 앞으로 HPA/metrics를 쓰지 않을 때 설치 때 사용한 v0.7.2 URL을 `kubectl delete -f`에 전달한다.

[독립 학습 순서](./README.md)
