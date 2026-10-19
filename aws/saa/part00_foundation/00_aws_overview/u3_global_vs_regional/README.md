# u3. Global Service vs Regional Service

## 지도 확인

AWS 서비스를 사용할 때는 먼저 이 질문을 할 수 있어야 한다.

> **이 서비스는 전역(Global) 단위로 동작하는가, 특정 Region에 종속되는가?**

앞 유닛에서 AWS 인프라를 Region / AZ / Edge Location으로 나누어 봤다면, 이번에는 **AWS 서비스 자체의 범위(scope)** 를 본다.

```text
AWS
├── Global Services
│   ├── IAM
│   ├── Route 53
│   ├── CloudFront
│   └── WAF
│
└── Region-scoped Services
    ├── EC2
    ├── Elastic Beanstalk
    ├── Lambda
    └── Rekognition
```

강의에서는 일부 서비스를 Global Service로, 대부분의 AWS 서비스를 Region-scoped Service로 구분한다.

---

## 1. Regional Service

대부분의 AWS 서비스는 **특정 Region을 기준으로 사용한다.**

예를 들어 EC2 인스턴스를 서울 Region에 생성하면 그 인스턴스는 서울 Region의 리소스다.

```text
AWS Account

├── ap-northeast-2 (Seoul)
│   └── EC2 A
│
└── ap-northeast-1 (Tokyo)
    └── EC2 B
```

서울에서 만든 EC2 A와 도쿄에서 만든 EC2 B는 같은 AWS 계정 안에 있어도 서로 다른 Region에 속한다.

강의에서 Region-scoped 예시로 드는 서비스는 다음과 같다.

- **EC2** — Infrastructure as a Service
- **Elastic Beanstalk** — Platform as a Service
- **Lambda** — Function as a Service
- **Rekognition** — Software as a Service

핵심은 서비스 이름만 보는 것이 아니라 **현재 어떤 Region을 보고 있는지 항상 확인하는 습관**이다.

AWS Console에서 EC2 같은 서비스를 사용할 때 Region을 잘못 선택하면, 분명 만들어 둔 리소스가 있는데도 보이지 않는 것처럼 느껴질 수 있다.

```text
Seoul Region을 보고 있음
→ Seoul EC2는 보임
→ Tokyo EC2는 현재 화면에 나타나지 않음
```

---

## 2. Global Service

강의에서는 다음 서비스를 Global Service의 대표적인 예로 제시한다.

- **IAM** — Identity and Access Management
- **Route 53** — DNS
- **CloudFront** — Content Delivery Network
- **WAF** — Web Application Firewall

이 서비스들은 EC2처럼 특정 Region 하나를 먼저 고른 뒤 그 Region 안에서만 사용하는 서비스와는 다르게 취급된다.

```text
                    AWS Account
                        │
                ┌───────┴───────┐
                │ Global Layer  │
                │ IAM / R53 ... │
                └───────┬───────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
  Seoul Region                    Tokyo Region
      EC2                              EC2
```

지금 단계에서는 각 Global Service의 세부 동작을 파고들 필요는 없다.

중요한 건 **AWS의 모든 서비스가 Region 단위인 것은 아니다**라는 점이다.

---

## 3. 왜 이 구분이 중요한가?

### 3.1 리소스를 찾을 때

EC2처럼 Region-scoped인 서비스는 현재 선택한 Region이 중요하다.

```text
"EC2를 만들었는데 안 보인다"

확인할 것:
현재 Console의 Region이 맞는가?
```

반대로 Global Service는 EC2와 같은 방식으로 Region별 리소스를 찾는다고 생각하면 혼동이 생길 수 있다.

---

### 3.2 아키텍처를 그릴 때

AWS 시스템을 설계할 때도 범위를 구분해야 한다.

```text
                  Route 53
                     │
                 CloudFront
                     │
          ┌──────────┴──────────┐
          │                     │
     Seoul Region          Tokyo Region
          │                     │
         EC2                   EC2
```

이런 그림에서는 Global Service와 Regional Service가 서로 다른 층에 위치한다.

아직 Route 53이나 CloudFront의 세부 기능을 배우지는 않았지만, 나중에 아키텍처를 볼 때 **어떤 서비스가 Region 내부에 있고 어떤 서비스가 그 바깥에 있는지** 구분하는 데 도움이 된다.

---

## 4. Region과 서비스 범위를 혼동하지 않기

앞 유닛의 Region 개념과 이번 유닛의 Service Scope는 서로 다른 질문이다.

### Region

```text
AWS 인프라가 어느 지리적 영역에 있는가?
```

### Service Scope

```text
이 AWS 서비스가 어느 범위에서 관리되는가?
```

예를 들어:

```text
EC2
→ Region-scoped

IAM
→ Global
```

둘 다 AWS 서비스지만 관리 범위가 다르다.

---

## 5. 지금 외워둘 최소 목록

SAA 학습 초반에는 우선 이 정도만 구분하면 된다.

| Global Service | Region-scoped Service |
|---|---|
| IAM | EC2 |
| Route 53 | Elastic Beanstalk |
| CloudFront | Lambda |
| WAF | Rekognition |

나머지 서비스들은 앞으로 하나씩 공부하면서 자신의 범위를 같이 확인한다.

---

## SAA 연결

이번 내용은 단독으로 복잡한 문제를 푸는 주제라기보다, 이후 문제를 읽을 때 필요한 기본 전제에 가깝다.

### 패턴 1

> 특정 Region에 EC2 인스턴스를 생성했다.

```text
→ 해당 EC2는 Region-scoped 리소스
```

### 패턴 2

> 사용자와 AWS 리소스의 접근 권한을 관리한다.

```text
→ IAM
→ Global Service
```

### 패턴 3

> DNS 또는 전 세계 콘텐츠 배포 계층을 다룬다.

```text
Route 53 / CloudFront
→ Global Service로 분류
```

지금은 서비스별 세부 선택 문제보다 **Global인지 Regional인지 구분하는 것**까지만 가져간다.

---

## 앞으로의 연결

```text
IAM
→ 다음 Identity 파트에서 자세히 학습

EC2
→ Region / AZ 안에서 실제 서버를 생성

Route 53
→ DNS 학습에서 다시 등장

CloudFront
→ Edge Location과 연결

WAF
→ 보안 파트에서 다시 학습
```

앞으로 새로운 AWS 서비스를 만날 때 다음 질문을 습관처럼 붙인다.

> **이 서비스의 scope는 어디까지인가?**

이번 유닛도 기본 분류를 익히는 내용이므로 별도 유제와 3문장 요약은 생략한다.
