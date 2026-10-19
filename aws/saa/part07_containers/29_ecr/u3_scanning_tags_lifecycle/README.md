# u3. ECR Scanning / Tags / Lifecycle

강의는 ECR이 단순 image storage 이상으로 다음 기능을 제공한다고 설명한다.

```text
Image vulnerability scanning
Image tags
Lifecycle management
Version 관리
```

## 1. Image Tags

```text
my-app:v1
my-app:v2
my-app:2026-09-22
```

Tag는 어느 Image를 배포할지 식별하는 데 사용한다.

운영에서는 `latest` 하나만 의존하기보다 배포 버전을 추적할 수 있는 tag 전략이 중요하다.

## 2. Vulnerability Scanning

Container Image의 package vulnerability를 검사할 수 있다.

11부 Security와 연결하면 Amazon Inspector가 ECR Image scanning과 연결되는 구조도 기억한다.

## 3. Lifecycle

오래된 Image가 계속 쌓이지 않도록 lifecycle policy로 정리할 수 있다.

```text
최근 N개 image 유지
오래된 untagged image 제거
```

## SAA 감각

```text
Container image 취약점 점검
→ ECR scanning / Inspector 연결

오래된 image 자동 정리
→ Lifecycle Policy
```
