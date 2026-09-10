# u3. AMI

## 지도 확인

AMI(Amazon Machine Image)는 EC2 인스턴스를 빠르게 만들기 위한 이미지다.

```text
EC2 설정 완료
→ AMI 생성
→ 같은 구성을 가진 새 EC2 실행
```

---

## 개념

AMI에는 운영체제뿐 아니라 애플리케이션, 설정, 모니터링 도구 등 인스턴스 구성을 미리 담아둘 수 있다.

장점은 새 인스턴스를 실행할 때 매번 긴 설치 작업을 반복하지 않아도 된다는 점이다.

AMI는 Region 단위 리소스지만 다른 Region으로 복사할 수 있다.

종류:

- AWS가 제공하는 Public AMI
- 직접 만드는 Custom AMI
- AWS Marketplace AMI

---

## AMI 생성 흐름

강의 흐름은 다음과 같다.

```text
EC2 실행
→ 필요한 설정/소프트웨어 설치
→ 데이터 일관성을 위해 인스턴스 정지
→ AMI 생성
→ AMI에서 새 EC2 실행
```

AMI를 만들면 관련 EBS Snapshot도 함께 생성된다.

---

## SAA 연결

```text
동일하게 설정된 EC2를 빠르게 반복 생성
→ Custom AMI

다른 Region에서도 같은 이미지 사용
→ AMI Copy

부팅 후 긴 설치 시간을 줄이고 싶음
→ 미리 구성한 AMI 사용
```

AMI는 Auto Scaling에서도 다시 등장하므로 여기서는 기본 개념만 잡는다.
