# 43. Amazon Rekognition

Amazon Rekognition은 **이미지와 비디오에서 객체, 사람, 텍스트, 장면, 얼굴 등을 분석하는 ML 서비스**다.

강의에서 강조하는 대표 use case:

```text
Labeling
Content Moderation
Text Detection
Face Detection / Analysis
Face Search / Verification
Celebrity Recognition
Pathing
```

## Units

- [ ] [u1. Image / Video Analysis](./u1_image_video_analysis/README.md)
- [ ] [u2. Face Analysis / Verification](./u2_face_analysis_verification/README.md)
- [ ] [u3. Content Moderation](./u3_content_moderation/README.md)
- [ ] [u4. SAA Selection](./u4_saa_selection/README.md)

## 전체 감각

```text
Image / Video
    ↓
Rekognition
    ↓
Labels / Faces / Text / Scenes / Moderation Result
```

## SAA 선택 기준

```text
이미지/영상 속 객체 탐지
→ Rekognition

얼굴 분석/검색/검증
→ Rekognition

이미지/영상의 유해 콘텐츠 탐지
→ Rekognition
```
