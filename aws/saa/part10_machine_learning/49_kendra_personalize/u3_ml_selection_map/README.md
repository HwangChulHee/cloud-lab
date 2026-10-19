# u3. AWS Machine Learning 서비스 최종 선택 지도

강의 마지막 Summary를 기준으로 10부를 한 번에 정리한다.

| 요구사항 | 서비스 |
|---|---|
| face detection / labeling / celebrity recognition | Rekognition |
| audio → text | Transcribe |
| text → audio | Polly |
| language translation | Translate |
| conversational chatbot | Lex |
| cloud contact center | Connect |
| natural language processing | Comprehend |
| ML model build/train | SageMaker AI |
| ML-powered document search | Kendra |
| real-time personalized recommendation | Personalize |
| scanned document text/data extraction | Textract |

## 입력 → 출력으로 외우기

```text
Image / Video
→ Rekognition
→ labels / faces / moderation

Speech
→ Transcribe
→ Text

Text
→ Polly
→ Speech

Text Language A
→ Translate
→ Text Language B

Speech / Text
→ Lex
→ Intent / Bot action

Text
→ Comprehend
→ Sentiment / Entities / Topics

Historical Data
→ SageMaker
→ Trained ML Model / Prediction

Documents
→ Kendra
→ Natural Language Search Result

User Behavior / Item Data
→ Personalize
→ Recommendation

Scanned Document
→ Textract
→ Text / Handwriting / Form / Table Data
```

## 가장 헷갈리는 비교

```text
Rekognition vs Textract
→ 이미지/영상 이해 vs 문서 data extraction

Transcribe vs Lex
→ speech-to-text vs intent/chatbot

Comprehend vs Kendra
→ NLP 분석 vs document search

SageMaker vs Personalize
→ 직접 ML model 개발 vs 추천 managed service

OpenSearch vs Kendra
→ 범용 search vs ML-powered enterprise document search
```

## 기억할 문장

> 10부는 ML 알고리즘을 공부하는 파트가 아니라, 입력과 원하는 결과를 보고 어떤 AWS ML 서비스를 선택할지 구분하는 Coverage 파트다.
