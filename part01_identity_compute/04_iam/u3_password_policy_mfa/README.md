# u3. Password Policy와 MFA

## 지도 확인

IAM에서 권한을 올바르게 나누는 것만큼 중요한 것이 **계정 자체를 보호하는 것**이다.

강의에서는 이 부분을 크게 두 가지로 나눈다.

```text
Password Policy
MFA
```

---

## 1. Password Policy

AWS에서는 IAM User의 비밀번호 정책을 설정할 수 있다.

강의에서 다루는 항목은 다음과 같다.

- 최소 비밀번호 길이
- 대문자 요구
- 소문자 요구
- 숫자 요구
- 특수문자 요구
- 사용자가 자신의 비밀번호를 변경할 수 있도록 허용
- 일정 시간이 지나면 비밀번호 변경 요구
- 이전 비밀번호 재사용 방지

핵심은 단순하다.

```text
약한 비밀번호
→ 계정 탈취 위험 증가

강한 비밀번호 정책
→ 계정 보호 강화
```

---

## 2. MFA

MFA는 Multi-Factor Authentication이다.

강의에서는 다음 두 요소의 조합으로 설명한다.

```text
Password
+
Security Device
```

즉 비밀번호가 유출되더라도 추가 인증 요소가 없으면 로그인하기 어렵게 만든다.

특히 Root Account와 IAM User를 보호하는 핵심 수단으로 다룬다.

---

## 3. MFA Device

강의에서는 다음과 같은 유형을 소개한다.

```text
Virtual MFA Device
Security Key
Hardware MFA Device
```

예시로 모바일 인증 앱이나 물리적인 보안 키가 등장한다.

시험에서는 특정 제품 이름보다 다음 구조를 기억하면 충분하다.

```text
Something you know
→ password

Something you own
→ MFA device
```

---

## 4. Root Account와 MFA

Root Account는 AWS 계정 전체에 매우 강한 권한을 가지고 있다.

따라서 강의의 Best Practice와 연결하면 다음 흐름으로 이해할 수 있다.

```text
Root Account
→ 평소 사용하지 않음
→ MFA로 보호
```

---

## 5. Password와 MFA의 역할 차이

Password Policy는 비밀번호 자체를 더 안전하게 관리하도록 만든다.

MFA는 비밀번호 외에 추가 인증 요소를 요구한다.

```text
Password Policy
→ 첫 번째 인증 요소 강화

MFA
→ 두 번째 인증 요소 추가
```

둘 중 하나를 대신 사용하는 관계가 아니라 함께 계정 보안을 강화하는 관계다.

---

## SAA 연결

시험에서 다음 표현이 나오면 바로 연결한다.

```text
비밀번호가 탈취되어도 계정을 보호하고 싶다
→ MFA

IAM User의 비밀번호 복잡도를 강제하고 싶다
→ Password Policy

Root Account 보안 강화
→ MFA 적용 고려
```

---

## 실제 학습 체크

AWS 계정을 사용하고 있다면 강의를 따라가면서 다음 화면의 위치를 확인해본다.

```text
IAM
→ Account settings / Password policy

Security credentials
→ MFA
```

지금 단계에서는 설정을 무작정 변경하는 것보다 **어떤 보안 기능이 어디에 있는지 확인**하는 것만으로도 충분하다.

이번 유닛도 개념이 단순하므로 별도 유제와 3문장 요약은 생략한다.
