# 04. StorageClass와 지연 바인딩

> 독립 실행 가능한 확장 실습 · 참고 주제: task-storageclass · 환경: 기존 클러스터 + 동적 provisioner

기초 연결: [StorageClass](../../04-storage-security/01-longhorn-storageclass/README.md) · [동적 프로비저닝](../../04-storage-security/02-dynamic-provisioning-pv-lifecycle/README.md)

[독립 과정에서의 위치](../../08-independent/06-storage/README.md). 처음에는 예시 풀이를 참고해 구축하고, 두 번째에는 요구사항만 보고 실행한다. 강의 수강은 선행 조건이 아니다.

## 먼저 이해할 것

StorageClass는 저장소 생성 규칙이고, 실제 생성은 provisioner가 수행한다. WaitForFirstConsumer는 소비 Pod의 스케줄링 조건을 고려해 바인딩/프로비저닝을 지연시킨다. 기본 클래스 변경은 다른 실습에도 영향을 주므로 기존 값을 기록한 뒤 원복한다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/04-storageclass-binding`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

```bash
kubectl get storageclass -o yaml > /tmp/preview-sc-before.yaml
kubectl get sc -o custom-columns=NAME:.metadata.name,PROVISIONER:.provisioner,BINDING:.volumeBindingMode
```

설치된 provisioner를 확인해 `class.yaml`의 placeholder를 바꾼다. 원본 클래스에 필수 `parameters`가 있다면 그 값도 복사한다. provisioner가 없다면 연결된 기초 실습부터 진행한다. local-path 환경이면 `rancher.io/local-path`를 사용한다.

```bash
kubectl create namespace preview-class
kubectl apply -f class.yaml -f pvc.yaml
kubectl -n preview-class describe pvc data
```

아직 consumer가 없으므로 WaitForFirstConsumer 관련 이벤트와 Pending을 예상한다.

## 2. 직접 바꿔보기

1. consumer를 배포해 PVC/PV 바인딩과 노드 배치를 확인한다.
2. `preview-delayed`를 default로 설정한다.
3. disposable 클러스터에서는 기존 default의 default annotation을 false로 바꾸고, 단 하나의 default만 유지해본다. 바꾸기 전 이름과 값을 기록한다.
4. `storageClassName`을 생략한 PVC와 `""`인 PVC의 차이를 설명한다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

```bash
kubectl apply -f consumer.yaml
kubectl -n preview-class rollout status deploy/consumer --timeout=180s
kubectl -n preview-class get pvc
kubectl get sc preview-delayed -o yaml
kubectl -n preview-class exec deploy/consumer -- cat /data/message
```

PVC가 Bound이며 provisioner 이벤트가 정상인지 확인한다. annotation만 바뀌었는데 저장소가 만들어지지 않으면 provisioner 상태와 필수 parameters를 본다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

```bash
kubectl annotate sc preview-delayed storageclass.kubernetes.io/is-default-class=true --overwrite
```

기존 default를 바꾸는 경우 그 클래스에 같은 annotation을 false로 설정한다. 기존 Deployment/PVC는 수정하지 않는다. 스케줄링을 건너뛰는 `nodeName`을 consumer에 직접 지정하면 지연 바인딩이 막힐 수 있으므로 nodeSelector/affinity를 사용한다.

</details>

## 4. 정리 및 재실행

먼저 `/tmp/preview-sc-before.yaml`과 비교해 **직접 변경했던 기존 클래스의 default annotation**을 원래 값으로 돌린다. 원래 annotation이 없었다면 `kubectl annotate sc 클래스명 storageclass.kubernetes.io/is-default-class-`로 제거한다.

```bash
kubectl delete namespace preview-class
kubectl delete sc preview-delayed
kubectl get sc
```

원본 전체 YAML을 무조건 apply하지 않고 변경한 annotation만 복구한다. PVC의 PV와 실제 저장소가 Delete 정책에 따라 정리됐는지도 확인한다.

## 스스로 설명할 질문

- provisioner 문자열을 지정하는 것과 provisioner 설치는 어떻게 다른가?
- Pending이 정상 대기인 경우와 오류인 경우는 Events에서 어떻게 구분하는가?

[전체 확장 경로](../README.md)
