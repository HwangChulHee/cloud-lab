# u4. Imported Certificates & Expiration Monitoring

ACM이 직접 발급한 인증서뿐 아니라 외부 CA나 다른 시스템에서 만든 Public Certificate를 ACM에 Import해서 사용할 수도 있다.

## 1. Imported Certificate

```text
외부에서 인증서 생성
 ↓
ACM에 Import
 ↓
ALB / CloudFront / API Gateway 등에 연결
```

차이는 **자동 갱신 여부**다.

ACM이 직접 발급한 인증서는 자동 갱신을 지원하지만, Import한 인증서는 ACM이 자동으로 새 인증서를 만들어 갱신하지 않는다.

```text
Imported Certificate 만료 임박
→ 외부에서 새 인증서 발급
→ ACM에 새 인증서 Import
→ 교체
```

## 2. Expiration Monitoring

강의에서는 Import 인증서 만료를 놓치지 않도록 EventBridge와 AWS Config를 활용할 수 있는 흐름을 다룬다.

ACM은 만료가 다가오는 인증서에 대한 이벤트를 발생시킬 수 있고, EventBridge를 통해 알림이나 자동화로 연결할 수 있다.

```text
ACM Expiration Event
 ↓
EventBridge
 ↓
SNS / Lambda / 기타 처리
```

AWS Config의 관리형 Rule을 이용해 인증서 만료 상태를 점검하는 방식도 연결된다.

## 예시

회사 정책상 외부 CA에서 발급한 인증서를 사용해야 한다고 해보자.

```text
1. 외부 CA 인증서 발급
2. ACM Import
3. ALB에 연결
4. 만료 감시
5. 만료 전 새 인증서 발급 및 재수입
```

ACM 콘솔에 인증서가 있다고 해서 모든 인증서가 자동 갱신되는 것은 아니라는 점이 핵심이다.

## SAA 판단

```text
ACM이 직접 발급
→ Automatic Renewal 지원

외부 인증서를 ACM에 Import
→ 사용 가능

Imported Certificate
→ 자동 갱신되지 않음

인증서 만료 감시/이벤트 기반 알림
→ ACM + EventBridge

규정 준수 형태로 만료 여부 점검
→ AWS Config managed rule 고려
```
