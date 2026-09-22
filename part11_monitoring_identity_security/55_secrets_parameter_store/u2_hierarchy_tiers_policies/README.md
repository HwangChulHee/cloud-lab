# u2. Parameter Store Hierarchy / Tiers / Policies

## 1. Hierarchy

강의 예시:

```text
/my-department/
  my-app/
    dev/
      db-url
      db-password
    prod/
      db-url
      db-password
```

이런 hierarchy를 사용하면 환경/팀/애플리케이션별로 parameter를 구조화할 수 있다.

관련 API:

```text
GetParameters
GetParametersByPath
```

## 2. Standard vs Advanced

강의 표 기준 핵심 차이:

```text
Standard
→ 더 적은 parameter 수
→ 최대 value size 4 KB
→ parameter policy 없음
→ 추가 storage charge 없음

Advanced
→ 더 많은 parameter 수
→ 최대 value size 8 KB
→ parameter policy 가능
→ 비용 발생
```

## 3. Parameter Policies

Advanced parameter에서 다음 policy를 설정할 수 있다.

```text
Expiration
ExpirationNotification
NoChangeNotification
```

즉 민감한 설정값의 만료/갱신을 관리할 수 있다.
