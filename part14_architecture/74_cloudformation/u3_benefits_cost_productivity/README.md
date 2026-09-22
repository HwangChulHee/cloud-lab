# u3. CloudFormation Benefits / Cost / Productivity

강의는 CloudFormation 장점을 세 축으로 설명한다.

## Infrastructure as Code

```text
resource를 수동 생성하지 않음
변경사항을 코드로 검토
```

## Cost

Stack resource에 identifier가 붙어 비용을 묶어서 보기 쉽고, template을 기반으로 비용을 추정할 수 있다.

강의 예:

```text
Dev 환경
17:00 삭제
08:00 재생성
→ 사용하지 않는 시간 비용 절감
```

## Productivity

```text
빠른 destroy / recreate
declarative orchestration
existing template 재사용
문서화 효과
```

강의에서는 Infrastructure Composer로 resource 관계를 시각화하는 예도 보여준다.

## 기억할 문장

> CloudFormation은 재현성뿐 아니라 비용 관리와 환경 재생성 속도에도 도움을 준다.
