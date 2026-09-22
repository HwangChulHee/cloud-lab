# u3. Rekognition Content Moderation

Rekognition Content Moderation은 이미지/영상에서 **부적절하거나 원치 않거나 공격적인 콘텐츠**를 탐지한다.

대표 사용 영역:

```text
Social Media
Broadcast Media
Advertising
E-commerce
```

## Confidence Threshold

강의에서는 탐지 결과에 **Minimum Confidence Threshold**를 설정할 수 있다고 설명한다.

```text
Confidence 높음
→ 자동 flag

애매한 결과
→ manual review 고려
```

## Amazon A2I

민감한 결과를 **Amazon Augmented AI (A2I)**로 보내 사람이 수동 검토하는 흐름도 소개한다.

```text
Image
 ↓
Rekognition
 ↓
Confidence / Flag
 ↓
Optional Manual Review in A2I
```

## 기억할 문장

> 이미지/영상 유해성 검토는 Rekognition Content Moderation, 애매한 결과는 A2I 수동 검토로 연결할 수 있다.
