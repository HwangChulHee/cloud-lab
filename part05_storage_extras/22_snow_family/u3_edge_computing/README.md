# u3. Snowball Edge Computing

Edge Computing은 **데이터가 생성되는 장소에서 바로 처리**하는 개념이다.

강의 예:

```text
truck on the road
ship on the sea
mining station underground
```

이런 곳은 인터넷 연결이 제한적이고 충분한 compute resource가 없을 수 있다.

## 구조

```text
Edge Location
   ↓
Snowball Edge
   ├→ preprocess data
   ├→ machine learning
   └→ media transcoding
```

강의에서는 Snowball Edge에서 EC2 Instances 또는 Lambda functions를 실행할 수 있다고 설명한다.

## 왜 edge에서 처리하나?

```text
모든 raw data를 cloud로 보낼 수 없음
→ local preprocessing
→ 필요한 결과만 전달

네트워크 연결 불안정
→ 현장에서 compute
```

## 기억할 문장

> Snowball Edge는 migration device이면서, 인터넷이 제한된 현장에서 데이터를 생성 즉시 처리하는 edge compute 장비로도 사용할 수 있다.
