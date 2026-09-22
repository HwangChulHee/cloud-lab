# u2. SageMaker Build / Train / Tune / Predict

강의의 단순화된 ML process:

```text
Historical Data
      ↓
Build
      ↓
ML Model
      ↓
Train and Tune
      ↓
New Data
      ↓
Apply Model
      ↓
Prediction
```

예시에서는 AWS/IT 경력, 학습 시간 같은 historical data를 사용해 시험 점수를 예측한다.

## 핵심

```text
Pre-built AI API 호출
→ Rekognition / Comprehend / Textract 등

직접 data로 ML model을 build/train
→ SageMaker
```

이 차이를 우선 기억한다.
