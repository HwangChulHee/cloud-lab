# u3. SageMaker / Aurora Machine Learning

강의의 Aurora Machine Learning에서는 Aurora와 SageMaker를 직접 통합할 수 있다고 설명한다.

```text
Application
   ↓ SQL Query
Aurora
   ↓
SageMaker
   ↓ prediction
Aurora
   ↓
Query Result
```

강의에서 지원 서비스로:

```text
SageMaker
→ any ML model

Comprehend
→ sentiment analysis
```

를 언급한다.

대표 use case:

```text
fraud detection
ads targeting
sentiment analysis
product recommendations
```

## 기억할 문장

> Aurora Machine Learning은 SQL query 흐름에서 SageMaker/Comprehend prediction을 애플리케이션에 연결한다.
