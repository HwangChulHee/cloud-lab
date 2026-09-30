# 예습 자료 검증 기록

작성 시점: 2026-09-30. 이 기록은 자료의 정적 검증과 Helm 렌더링 결과이며 실제 사용자 클러스터에서 모든 실습을 실행한 기록은 아니다.

## 완료한 검사

| 검사 | 결과 |
|---|---|
| 실습 구성 | 16개 주요 실습, 각 실습의 구축·과제·검증·힌트·정리·질문 확인 |
| Markdown 상대 링크 | k8s 전체의 로컬 링크 대상 존재 확인 |
| bash 코드 블록 | 86개 명령 블록의 `bash -n` 검사 통과 |
| YAML 파싱과 기본 연결 | 60개 객체 파싱, preview namespace, Deployment selector, volumeMount/volume 연결 확인 |
| Kubernetes/Gateway API 스키마 | 58개 통과, invalid/error 0, 학습용 CRD 정의/인스턴스 2개는 외부 스키마 부재로 제외 |
| Argo CD chart 8.6.4 | Helm 3.16.4로 Kubernetes 1.34 대상으로 실제 렌더링 |
| chart CRD 분리 | crds.install=true에서 CRD 3개 추출, false에서 CRD 0개 확인 |
| CRD 제외 chart 리소스 | Kubernetes 1.34 스키마로 50개 통과 |
| git diff | 공백 오류 없음 |

## 재확인 명령

저장소 루트에서 PyYAML과 kubeconform을 준비한 뒤 실행한다.

```bash
python3 k8s/07-cka-preview/check_materials.py
kubeconform -strict -summary -kubernetes-version 1.27.2 \
  -schema-location default \
  -schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json' \
  -ignore-missing-schemas k8s/07-cka-preview
git diff --check
```

Placeholder를 실제 환경 값으로 바꾼 뒤에는 server-side dry-run도 수행할 수 있다. custom resource는 CRD가 먼저 설치돼 있어야 한다.

```bash
kubectl apply --dry-run=server -f 해당파일.yaml
```

정적 검사는 이미지 다운로드, 실제 CNI 정책 집행, 노드 자원 여유, Controller의 route 처리, 런타임 설치를 보장하지 않는다. 각 실습 문서의 실제 요청·상태·복구 검증을 수행한 후에 학습 완료로 표시한다.
