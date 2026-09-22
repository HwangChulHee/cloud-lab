# 47. Amazon SageMaker AI

Amazon SageMaker AI는 **개발자와 data scientist가 ML model을 만들기 위한 fully managed service**다.

강의의 범위는 세부 ML 알고리즘보다 **ML model lifecycle을 한 곳에서 관리하는 서비스**라는 점을 이해하는 것이다.

## Units

- [ ] [u1. Managed ML Platform](./u1_managed_ml_platform/README.md)
- [ ] [u2. Build / Train / Tune / Predict](./u2_build_train_tune_predict/README.md)
- [ ] [u3. Aurora Machine Learning Integration](./u3_aurora_integration/README.md)
- [ ] [u4. SAA Selection](./u4_saa_selection/README.md)

## 전체 흐름

```text
Historical Data
      ↓
Build ML Model
      ↓
Train & Tune
      ↓
New Data
      ↓
Apply Model
      ↓
Prediction
```

## 핵심

SageMaker가 해결하는 문제는 ML 과정마다 별도 서버/환경을 직접 구성해야 하는 복잡성을 줄이는 것이다.
