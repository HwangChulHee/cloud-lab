# u8. S3 Access Points & Object Lambda

## 1. Access Point가 왜 필요한가

하나의 큰 S3 Bucket을 여러 팀이 같이 사용한다고 해보자.

```text
/company-data
├── finance/
├── sales/
└── analytics/
```

모든 접근 규칙을 하나의 거대한 Bucket Policy에 계속 추가하면 정책이 복잡해진다.

S3 Access Point는 같은 Bucket을 바라보더라도 **사용 목적별로 별도 접근점과 별도 정책**을 만들 수 있게 한다.

```text
Finance Access Point
→ /finance/* R/W

Sales Access Point
→ /sales/* R/W

Analytics Access Point
→ 전체 Read
```

각 Access Point는 자체 DNS 이름과 Access Point Policy를 가질 수 있다.

## 2. VPC Origin Access Point

Access Point를 VPC 내부에서만 접근하도록 구성할 수도 있다.

```text
EC2 in VPC
 ↓
VPC Endpoint
 ↓
S3 Access Point
 ↓
Bucket
```

이 경우 VPC Endpoint Policy, Access Point Policy, Bucket Policy가 함께 접근 여부에 영향을 줄 수 있다.

## 3. S3 Object Lambda

같은 원본 Object를 여러 애플리케이션이 서로 다른 형태로 받고 싶다고 해보자.

원본:

```json
{
  "name": "Kim",
  "phone": "010-1234-5678"
}
```

분석용 앱에는 개인정보를 가리고 싶다면:

```json
{
  "name": "Kim",
  "phone": "***"
}
```

매번 별도 파일을 저장하는 대신 Object Lambda를 이용해 **조회 시 Lambda가 객체를 변환한 뒤 반환**할 수 있다.

사용 사례:

```text
PII 마스킹
XML → JSON 변환
이미지 resize / watermark
호출자별 데이터 가공
```

흐름은 다음처럼 이해하면 된다.

```text
Application
 ↓
S3 Object Lambda Access Point
 ↓
Lambda가 변환
 ↓
원본 S3 Object
```

## SAA 판단

```text
한 Bucket을 여러 팀/앱이 서로 다른 정책으로 접근
→ S3 Access Points

VPC 내부에서만 Access Point 사용
→ VPC Origin + VPC Endpoint

원본 객체를 복제 저장하지 않고 요청 시 변환
→ S3 Object Lambda
```
