# 07. CI/CD

## 핵심 질문

1. CI와 CD를 설명해보세요.
2. 일반적인 CI/CD pipeline을 설계해보세요.
3. 배포 중 test가 실패하면 어떻게 처리하나요?
4. 배포 후 장애가 발생하면 어떻게 rollback하나요?
5. Rolling, Blue/Green, Canary deployment를 비교해보세요.
6. GitHub Actions 같은 CI 도구에서 secret을 어떻게 관리하나요?
7. 동일한 artifact를 dev/staging/prod에 배포하는 것이 왜 좋은가요?

## 기본 흐름

```text
push / pull request
      ↓
build
      ↓
unit / integration test
      ↓
artifact or image build
      ↓
registry push
      ↓
deploy
      ↓
health check / smoke test
      ↓
monitor
      ↓
rollback if necessary
```

## 실전형 질문

### 배포 직후 5xx가 급증했습니다.

```text
1. 배포 시점과 5xx 증가 시점 비교
2. 신규 버전과의 상관관계 확인
3. LB / application metric 및 log 확인
4. 사용자 영향이 크면 우선 rollback
5. 정상화 확인
6. 이후 root cause 분석
```

운영 장애에서는 원인 분석을 끝낸 뒤 복구하는 것보다, 사용자 영향이 명확하고 안전한 rollback 경로가 있다면 먼저 서비스 정상화를 고려할 수 있습니다.
