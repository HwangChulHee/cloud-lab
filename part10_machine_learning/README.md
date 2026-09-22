# 10부 — Machine Learning for SAA

이 파트는 **ML 모델 개발 실습**이 아니라, SAA에서 AWS의 managed ML 서비스를 **입력 / 출력 / 대표 use case 기준으로 구분**하기 위한 Coverage 파트다.

강의 마지막 Summary의 핵심은 다음과 같다.

```text
Rekognition
→ face detection / labeling / celebrity recognition

Transcribe
→ audio → text

Polly
→ text → audio

Translate
→ language translation

Lex
→ conversational bot

Connect
→ cloud contact center

Comprehend
→ NLP

SageMaker AI
→ ML model build/train

Kendra
→ ML-powered document search

Personalize
→ real-time personalized recommendations

Textract
→ scanned document text/data extraction
```

## Chapters

- [ ] [43. Rekognition](./43_rekognition/README.md)
- [ ] [44. Transcribe / Polly / Translate](./44_transcribe_polly_translate/README.md)
- [ ] [45. Comprehend](./45_comprehend/README.md)
- [ ] [46. Lex](./46_lex/README.md)
- [ ] [47. SageMaker](./47_sagemaker/README.md)
- [ ] [48. Textract](./48_textract/README.md)
- [ ] [49. Kendra / Personalize 등](./49_kendra_personalize/README.md)

## 입력 → 출력으로 먼저 구분

```text
Image / Video
→ Rekognition

Speech
→ Transcribe
→ Text

Text
→ Polly
→ Speech

Text
→ Translate
→ 다른 언어 Text

Speech / Text
→ Lex
→ Intent

Text
→ Comprehend
→ Sentiment / Entities / Topics

Historical Data
→ SageMaker
→ ML Model / Prediction

Documents
→ Kendra
→ Search Answer

User / Item Data
→ Personalize
→ Recommendation

Scanned Document
→ Textract
→ Text / Forms / Tables
```

## 시험에서 특히 헷갈리는 비교

```text
Rekognition
vs
Textract
→ 이미지/영상 분석 vs 문서 data extraction

Transcribe
vs
Lex
→ speech-to-text vs intent/chatbot

Comprehend
vs
Kendra
→ NLP insight vs enterprise document search

SageMaker
vs
Personalize
→ 직접 ML model 개발 vs recommendation managed service

OpenSearch
vs
Kendra
→ 범용 full-text search vs ML-powered document search
```

## 학습 순서

```text
43 Rekognition
Image / Video
      ↓
44 Transcribe / Polly / Translate
Speech / Text / Language
      ↓
45 Comprehend
NLP
      ↓
46 Lex
Conversational Bot
      ↓
47 SageMaker
Custom ML Model
      ↓
48 Textract
Document Extraction
      ↓
49 Kendra / Personalize
Search / Recommendation
```

## 학습 깊이

이 파트는 **Coverage 중심**이다.

각 서비스마다 다음 세 질문에 답할 수 있으면 우선 충분하다.

```text
입력은 무엇인가?
출력은 무엇인가?
어떤 문제에서 이 서비스를 선택하는가?
```

현재 `examples/01~16`의 필수 선행조건은 아니며, 별도 ML 실습을 깊게 진행하는 것이 목표도 아니다.
