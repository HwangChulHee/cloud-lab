# u4. Session Store & Stateless Application

## 지도 확인

강의에서는 ElastiCache를 **사용자 세션을 공유하는 저장소**로 사용하는 대표 아키텍처를 다룬다.

```text
User
 ↓ login
App Instance A
 ↓
ElastiCache
 ↓ shared session
App Instance B
```

사용자가 다음 요청에서 다른 App Instance로 가더라도 같은 세션 데이터를 읽을 수 있다.

---

## 1. 왜 세션 공유가 필요한가

로드밸런서 뒤에 여러 서버가 있다고 하자.

```text
ALB
├─ App A
├─ App B
└─ App C
```

로그인 세션을 App A의 로컬 메모리에만 저장하면 다음 요청이 App B로 갔을 때 세션을 찾지 못할 수 있다.

```text
첫 요청
User → App A → login session 저장

다음 요청
User → App B → session 없음
```

---

## 2. ElastiCache를 Session Store로 사용

세션을 중앙 cache에 저장하면 모든 App Instance가 같은 세션을 읽을 수 있다.

```text
App A ─┐
App B ─┼→ ElastiCache Session Store
App C ─┘
```

이렇게 하면 애플리케이션 서버 자체에 사용자 상태를 덜 의존하게 된다.

---

## 3. Stateless Application과 연결

강의에서는 ElastiCache가 애플리케이션을 **stateless하게 만드는 데 도움을 줄 수 있다**고 설명한다.

여기서 stateless는 각 App Instance가 사용자 세션을 자기 로컬 메모리에만 들고 있지 않는다는 의미로 이해하면 된다.

```text
App Instance
→ 쉽게 추가/교체 가능

Session
→ shared external store
```

Auto Scaling과 잘 맞는 이유도 여기 있다.

---

## 4. TTL

세션 데이터는 영구 보관할 필요가 없는 경우가 많다.

그래서 TTL을 사용해 일정 시간이 지나면 만료하도록 설계할 수 있다.

```text
login
→ session key 생성
→ TTL 30분
→ 활동 없으면 만료
```

강의의 Session Store 패턴에서도 TTL 개념이 연결된다.

---

## SAA 판단

```text
여러 EC2/App Instance가 로그인 상태를 공유
→ ElastiCache Session Store

Auto Scaling으로 서버가 자주 추가/교체
+ 세션을 서버 로컬에 두고 싶지 않음
→ shared cache 기반 session store 고려
```

## Recall Check

- 세션을 각 EC2 로컬에만 저장하면 어떤 문제가 생길 수 있는가?
- ElastiCache를 사용하면 왜 앱을 stateless하게 만들기 쉬워지는가?
- Session Store에서 TTL은 왜 유용한가?
