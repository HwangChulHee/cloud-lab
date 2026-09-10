# 09. Auto Scaling

SAA 강의의 High Availability & Scalability 섹션에서 Auto Scaling Group(ASG)을 정리한다.

시험 전에는 **왜 인스턴스 수를 자동으로 조절하는지**, **어떤 기준으로 늘리고 줄이는지**, **ELB와 어떻게 함께 동작하는지**를 이해하는 데 집중한다.

## Units

- [ ] u1. Auto Scaling Group 기본 구조
- [ ] u2. Scaling Policies
- [ ] u3. CloudWatch Alarms와 Scale Out / Scale In
- [ ] u4. Predictive Scaling과 Scheduled Scaling
- [ ] u5. Cooldown과 안정화
- [ ] u6. ELB + ASG 통합

## SAA 선택 지도

```text
트래픽 증가에 따라 EC2 수 자동 증가
→ Auto Scaling Group

평균 CPU를 일정 수준으로 유지
→ Target Tracking Scaling

CloudWatch Alarm 조건에 따라 정해진 수만큼 증감
→ Simple / Step Scaling

매주 금요일 17시에 미리 서버 증가
→ Scheduled Scaling

과거 패턴을 학습해 미리 scale out
→ Predictive Scaling

한 번 scale 한 뒤 잠시 추가 조정 대기
→ Cooldown

비정상 인스턴스 제외 + 새 인스턴스 추가 + 트래픽 분산
→ ELB + ASG
```

다음 단원은 RDS, Aurora, ElastiCache로 이어진다.
