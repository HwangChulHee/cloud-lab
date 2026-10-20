# 누적 복습 해설 — 먼저 스스로 답한 뒤 확인하기

아래 내용은 완전한 모범답안이 아니라 **확인할 핵심 논리와 증거**다. [8단계 학습 가이드](./README.md)의 단계별 질문을 먼저 풀고 펼쳐서 확인한다. 각 문서의 실제 실행 결과가 정답의 근거가 된다.

## 01 Pod
1. 독립 Pod에는 복구를 담당하는 ReplicaSet이 없어 삭제 후 스스로 재생성되지 않는다. 반대로 Deployment 소속 Pod는 ReplicaSet이 원하는 수량을 조정한다.
2. Pod는 네트워크 네임스페이스를 공유하므로 같은 Pod의 localhost는 공유된다. 다른 Pod는 자신의 독립된 localhost를 가진다.
3. `PodScheduled`는 Node 배치를, `Ready`는 트래픽 처리 준비를 뜻한다. `kubectl describe pod`의 Events와 Conditions로 구분한다.

## 02 Configuration
1. env 값은 컨테이너 시작 시 주입되는 반면 ConfigMap volume은 갱신될 수 있다. 애플리케이션이 파일을 다시 읽는지 확인해야 한다.
2. subPath 마운트는 ConfigMap 갱신을 자동 반영하지 않는다. 업데이트가 필요한 방식이면 마운트 구조를 바꿔야 한다.
3. kubelet이 Secret을 Pod에 전달하는 경로와 Pod의 ServiceAccount가 API에서 Secret을 직접 조회하는 권한은 별개다.

## 03 Controllers
1. Deployment는 rollout과 ReplicaSet을 관리하고 ReplicaSet은 Pod 수를 맞춘다. Pod 삭제는 Pod template 변경이 아니다.
2. 독립 Pod 삭제와 달리 소유된 Pod는 Controller에 의해 재생성될 수 있다. UID는 달라진다.
3. Deployment rollback은 Kubernetes Pod template을 되돌리는 것이며 외부 DB/파일까지 복구하지 않는다.

## 04 Networking
1. Pod IP는 Pod 네트워크 종단 주소, ClusterIP는 Service의 가상 접근 주소다. Service의 데이터 평면과 Pod의 수명은 별개다.
2. DNS는 성공해도 EndpointSlice의 Ready backend 부재, Service 포트 오류, 앱 listen/NetworkPolicy 문제로 HTTP가 실패한다.
3. readiness 실패 시 EndpointSlice ready condition 및 실제 전달 가능한 backend를 확인한다. DNS 성공만으로 서비스 정상이라고 판단하지 않는다.

## 05 Scheduling
1. FailedScheduling은 Node를 아직 배정하지 못한 단계이고 OOMKilled는 배치된 컨테이너의 메모리 종료다.
2. 스케줄링은 주로 resource requests를 보고 판단한다. limits는 실행 중 자원 제한에 적용된다.
3. Node 배정 완료와 컨테이너의 시작/준비 완료는 별도 조건이다.

## 06 Storage
1. PVC Pending은 binding/provisioning 문제, FailedMount는 kubelet·드라이버·Node 경로 문제일 수 있다.
2. WaitForFirstConsumer는 Pod의 스케줄링 요구 및 스토리지 토폴로지를 고려한 바인딩을 돕는다.
3. emptyDir은 Pod 수명에, PVC/PV는 별도 수명 정책에 따른다. StatefulSet 삭제만으로 PVC가 반드시 사라지지 않는다.

## 07 Security
1. RBAC는 Authorization, Pod Security Admission은 Admission 단계다. `can-i=yes`여도 Admission이 거부할 수 있다.
2. ServiceAccount는 Pod가 사용할 신원이고 RoleBinding은 그 주체에게 역할을 연결한다.
3. Forbidden은 호출한 사용자/ServiceAccount, `kubectl auth can-i`, 응답 메시지를 비교해 RBAC, API Admission, Namespace 정책을 구분한다.

## 08 Operations
1. DNS 성공은 이름 해석만 확인한다. EndpointSlice, 서비스 규칙, 포트, 정책, 애플리케이션을 별도로 확인한다.
2. Ingress Controller 상태와 Backend Pod Ready는 별개다. Ingress→Service→EndpointSlice→Pod 경로를 따라간다.
3. 동일한 URL·인증·포트·HTTP 요청을 다시 보내며 status/응답과 변경 전 증거를 비교한다.

**완료 원칙:** 답을 읽은 것만으로 완료 처리하지 않는다. 해당 실습의 실제 상태값이나 Events로 설명을 뒷받침해야 한다.
