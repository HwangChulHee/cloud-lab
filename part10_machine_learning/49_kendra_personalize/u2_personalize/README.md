# u2. Amazon Personalize

Amazon Personalize는 **real-time personalized recommendation**을 애플리케이션에 넣기 위한 fully managed ML service다.

## 대표 기능

강의 예:

```text
personalized product recommendations
re-ranking
customized direct marketing
```

예:

```text
User bought gardening tools
        ↓
Amazon Personalize
        ↓
다음에 살 상품 추천
```

## Integration

강의에서는 결과를 다음 channel에 연결할 수 있다고 설명한다.

```text
Websites & Apps
Mobile Apps
SMS
Emails
```

S3 data를 읽고 real-time data integration도 사용할 수 있다.

## 핵심

강의는 직접 ML solution을 build/train/deploy하는 기간을 줄여 recommendation 기능을 빠르게 구현하는 서비스로 설명한다.

## SageMaker와 구분

```text
직접 ML model을 build/train
→ SageMaker

추천 기능 자체를 managed service로 빠르게 구현
→ Personalize
```
