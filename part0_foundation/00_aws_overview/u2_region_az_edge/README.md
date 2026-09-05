# u2. Region / Availability Zone / Edge Location

## 지도 확인

AWS 인프라는 전 세계 하나의 거대한 데이터센터가 아니라, 여러 **Region**과 각 Region 안의 여러 **Availability Zone(AZ)** 으로 나뉜다.

또 사용자에게 콘텐츠를 더 가까이서 전달하기 위한 **Edge Location**이 별도로 존재한다.

```text
AWS Global Infrastructure
├── Region
│   ├── Availability Zone A
│   ├── Availability Zone B
│   └── Availability Zone C
└── Edge Locations
```

이번 유닛의 목표는 세 용어를 외우는 것이 아니라, 각각이 **지연시간, 장애 격리, 고가용성**과 어떤 관계가 있는지 이해하는 것이다.

---

## 1. Region

Region은 특정 지리적 영역에 위치한 AWS 인프라의 묶음이다.

예를 들어 다음과 같은 이름을 사용한다.

```text
ap-northeast-2  # Seoul
us-east-1       # N. Virginia
ap-northeast-1  # Tokyo
```

대부분의 AWS 서비스는 특정 Region을 기준으로 생성된다.

예를 들어 서울 Region에서 EC2를 생성하면 그 EC2는 자동으로 도쿄나 미국 Region에 존재하는 것이 아니다.

### Region을 선택할 때 고려할 것

SAA에서는 보통 다음 네 가지 기준으로 Region 선택 문제를 판단한다.

1. **Compliance**
   - 데이터가 특정 국가나 지역 안에 있어야 하는가?

2. **Latency**
   - 주요 사용자와 가까운 Region은 어디인가?

3. **Service availability**
   - 필요한 AWS 서비스나 기능이 해당 Region에서 제공되는가?

4. **Pricing**
   - 동일한 서비스라도 Region에 따라 가격이 다를 수 있다.

예를 들어 사용자의 대부분이 한국에 있고 특별한 이유가 없다면 서울 Region이 자연스러운 선택이 될 수 있다.

하지만 법적 요구사항이나 특정 서비스의 지원 여부가 있다면 단순히 거리만으로 결정할 수 없다.

---

## 2. Availability Zone (AZ)

하나의 Region은 여러 Availability Zone으로 구성된다.

```text
Region: ap-northeast-2

├── AZ A
├── AZ B
├── AZ C
└── AZ D
```

AZ는 단순히 서버 한 대를 의미하지 않는다.

하나 이상의 물리적 데이터센터로 이루어진 독립적인 장애 영역이며, 각 AZ는 전력·네트워크 등의 장애가 다른 AZ로 함께 번질 가능성을 줄이도록 분리되어 있다.

동시에 같은 Region의 AZ끼리는 빠른 네트워크로 연결되어 있다.

이 구조 덕분에 애플리케이션을 여러 AZ에 나누어 배치할 수 있다.

```text
                 Region

        AZ A                 AZ B
     ┌────────┐           ┌────────┐
     │  EC2   │           │  EC2   │
     └────────┘           └────────┘
          \                  /
           \                /
             Load Balancer
```

AZ A 전체에 문제가 생겨도 AZ B의 서버가 살아 있다면 서비스를 계속 제공할 수 있다.

이게 이후에 계속 등장할 **Multi-AZ / High Availability**의 기반이다.

### 중요한 구분

```text
Region 장애 대응
!=
AZ 장애 대응
```

두 AZ를 사용한다고 해서 Region 전체 장애까지 대비한 것은 아니다.

```text
Multi-AZ
→ 하나의 Region 안에서 장애 격리

Multi-Region
→ Region 자체의 장애까지 고려
```

둘은 비용과 복잡도가 크게 다르다.

---

## 3. Edge Location

Edge Location은 Region이나 AZ처럼 애플리케이션 서버를 일반적으로 배치하는 공간으로 이해하면 안 된다.

주요 목적은 **사용자에게 더 가까운 위치에서 콘텐츠나 네트워크 요청을 처리하는 것**이다.

대표적인 예가 CloudFront다.

```text
Origin
Seoul Region
    │
    │
CloudFront
    │
    ├── Edge Location: Seoul
    ├── Edge Location: Tokyo
    └── Edge Location: New York
            │
          Users
```

미국 사용자가 매번 서울의 원본 서버까지 정적 파일을 요청하는 대신 가까운 Edge Location에서 캐시된 콘텐츠를 받으면 지연시간을 줄일 수 있다.

Edge Location은 이후 CloudFront를 공부할 때 다시 자세히 다룬다.

---

## 4. 세 개념을 한 번에 보기

```text
Global AWS Infrastructure

┌─────────────────────────────────────┐
│ Region: Seoul                       │
│                                     │
│   AZ A             AZ B             │
│  ┌──────┐          ┌──────┐         │
│  │ EC2  │          │ EC2  │         │
│  └──────┘          └──────┘         │
│                                     │
│            RDS / ALB / ...          │
└─────────────────────────────────────┘

             ↓ content distribution

      Edge Locations around users
```

정리하면:

| 개념 | 의미 | 주된 판단 기준 |
|---|---|---|
| Region | 지리적으로 분리된 AWS 영역 | 규제, 지연시간, 서비스 지원, 가격 |
| AZ | Region 내부의 독립적인 장애 영역 | 고가용성, 장애 격리 |
| Edge Location | 사용자 가까이 위치한 AWS 접점 | 콘텐츠 전달, 지연시간 감소 |

---

## SAA 연결

이 영역에서는 세부 숫자보다 **어떤 문제를 어떤 범위에서 해결하는가**가 중요하다.

### 패턴 1

> 하나의 데이터센터 장애에도 서비스를 계속 제공해야 한다.

```text
→ 여러 Availability Zone 사용
```

### 패턴 2

> 전 세계 사용자에게 정적 콘텐츠를 낮은 지연시간으로 제공해야 한다.

```text
→ Edge Location을 사용하는 CloudFront 계열을 고려
```

### 패턴 3

> 데이터가 법적으로 특정 국가/지역을 벗어나면 안 된다.

```text
→ Region 선택이 핵심
```

### 패턴 4

> 하나의 AWS Region 전체 장애까지 대비해야 한다.

```text
→ Multi-AZ만으로는 부족
→ Multi-Region 아키텍처 고려
```

---

## 앞으로의 연결

이 개념들은 이후 거의 모든 AWS 아키텍처의 좌표계가 된다.

```text
EC2
→ 어떤 Region / AZ에 있는가?

RDS Multi-AZ
→ 왜 서로 다른 AZ를 사용하는가?

ALB
→ 여러 AZ의 서버로 어떻게 요청을 분산하는가?

CloudFront
→ Region과 Edge Location은 어떤 관계인가?

Disaster Recovery
→ AZ 장애와 Region 장애는 어떻게 다른가?
```

이번 유닛은 기본 개념 확인이 목적이므로 별도 유제와 3문장 요약은 생략한다.
