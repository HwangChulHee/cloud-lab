# 16. CRD 조회와 kubectl explain 문서 추출

> 강의 전 예습 · 참고 주제: task-crd · 환경: 기존 클러스터

기초 연결: [API/kubeconfig](../../04-storage-security/03-x509-kubeconfig-api/README.md) · [kubectl 관찰](../../00-foundation/02-kubectl-observation-basics/README.md)

## 먼저 이해할 것

CRD는 새 API의 스키마를 등록하고 Custom Resource는 그 API의 객체다. Controller/Operator가 있어야 객체를 실제 동작으로 연결한다. 이 작은 Certificate는 조회·스키마 학습용이며 인증서를 발급하지 않는다. `.yaml` 확장자 파일에도 요구에 따라 표 형식이나 설명 텍스트를 저장할 수 있다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/16-crd-discovery`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

```bash
kubectl apply -f setup.yaml
kubectl wait --for=condition=Established crd/certificates.preview.cloud-lab.local --timeout=60s
kubectl apply -f sample.yaml
kubectl api-resources --api-group=preview.cloud-lab.local
kubectl -n preview-crd get certificates.preview.cloud-lab.local
```

## 2. 직접 바꿔보기

1. 예습 CRD만 기본 표 출력으로 조회해 `/tmp/preview-resources.yaml`에 저장한다. `-o yaml`은 사용하지 않는다.
2. Certificate의 `spec.subject` 문서를 `/tmp/preview-subject.yaml`에 저장한다.
3. sample의 organizations를 배열 대신 문자열로 바꿔 스키마 검증 오류를 관찰한다.
4. cert-manager가 설치된 별도 환경에서는 같은 작업을 실제 cert-manager CRD에 대해 반복한다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

```bash
cat /tmp/preview-resources.yaml
cat /tmp/preview-subject.yaml
kubectl -n preview-crd get certificates.preview.cloud-lab.local sample -o yaml
```

첫 파일은 CRD 기본 표 출력, 둘째 파일은 subject의 설명과 하위 필드 문서여야 한다. sample 객체 생성이 실제 인증서 발급을 의미하지 않는 것도 설명한다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

```bash
kubectl get crd certificates.preview.cloud-lab.local > /tmp/preview-resources.yaml
kubectl explain certificates.preview.cloud-lab.local.spec.subject --api-version=preview.cloud-lab.local/v1 > /tmp/preview-subject.yaml
kubectl -n preview-crd patch certificates.preview.cloud-lab.local sample --type=merge \
  -p '{"spec":{"subject":{"organizations":"wrong-type"}}}'
```

마지막 명령은 타입 오류로 거절돼야 한다. cert-manager가 **이미 설치된 경우** 실제 자료 주제를 추가로 확인한다.

```bash
kubectl get crds | grep cert-manager.io > /tmp/preview-cert-manager-resources.yaml
kubectl explain certificates.cert-manager.io.spec.subject --api-version=cert-manager.io/v1 > /tmp/preview-cert-manager-subject.yaml
```

다른 API group에 같은 kind가 있을 수 있으므로 리소스 이름에 group을 붙이고 api-version도 명시한다. api-version 옵션만으로는 리소스 이름 탐색의 모호함이 해결되지 않을 수 있다.

</details>

## 4. 정리 및 재실행

```bash
kubectl delete namespace preview-crd
kubectl delete crd certificates.preview.cloud-lab.local
rm -f /tmp/preview-resources.yaml /tmp/preview-subject.yaml /tmp/preview-cert-manager-resources.yaml /tmp/preview-cert-manager-subject.yaml
```

공용 cert-manager CRD는 삭제하지 않는다.

## 강의에서 확인할 질문

- CRD, Custom Resource, Controller는 각각 무엇인가?
- 파일 확장자와 실제 출력 형식을 구분해야 하는 이유는?

[전체 예습 경로](../README.md)
