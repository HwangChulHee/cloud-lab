# u4. SSH, Log와 Environment

## 지도 확인

EC2를 운영하면 서버에 접속하고, 로그를 확인하고, 실행 환경을 점검하는 일이 반복된다. 이번 유닛에서는 그때 필요한 최소 개념만 정리한다.

---

## 1. SSH

SSH는 원격 Linux 서버의 shell에 안전하게 접속하기 위한 프로토콜이다.

```text
local machine
   ↓ SSH :22
remote Linux server
```

대표적인 형태:

```bash
ssh -i my-key.pem ubuntu@<public-ip>
```

AWS EC2에서는 Security Group에서 22번 포트 접근이 허용되어 있어야 하며 private key의 파일 권한도 적절해야 한다.

```bash
chmod 400 my-key.pem
```

운영에서는 가능하면 22번 포트를 전 세계에 무조건 열기보다 접근 범위를 제한한다.

---

## 2. Log

장애 원인을 찾을 때 로그는 핵심 단서다.

파일 로그:

```bash
tail -f /var/log/myapp/app.log
```

systemd 서비스 로그:

```bash
journalctl -u myapp
journalctl -u myapp -f
```

최근 로그만 본다면:

```bash
journalctl -u myapp --since "10 minutes ago"
```

중요한 질문은 단순히 "에러가 있나?"가 아니라 다음과 같다.

```text
언제 발생했는가?
어떤 요청/프로세스에서 발생했는가?
직전에는 무엇이 있었는가?
재시작 후에도 반복되는가?
```

이 사고방식은 이후 CloudWatch Logs에서도 그대로 이어진다.

---

## 3. Environment Variable

애플리케이션 설정을 환경변수로 전달하는 경우가 많다.

```bash
export APP_ENV=prod
export DB_HOST=example
```

확인:

```bash
printenv APP_ENV
env
```

단, 비밀번호나 Access Key 같은 secret을 Git repository에 기록해서는 안 된다. 뒤에서 IAM Role, SSM Parameter Store, Secrets Manager를 사용해 더 안전한 방식으로 이동한다.

---

## 4. 패키지 설치

배포판에 따라 패키지 관리자가 다르다.

Ubuntu 계열:

```bash
sudo apt update
sudo apt install nginx
```

Amazon Linux 계열에서는 `dnf` 또는 환경에 따라 `yum`을 만나게 된다.

명령어 자체를 외우는 것보다 **현재 서버가 어떤 배포판인지 확인하고 그 환경에 맞게 설치한다**는 점이 중요하다.

```bash
cat /etc/os-release
```

---

## 5. 운영 장애의 한 흐름

```text
SSH 접속 가능?
  ↓
service 상태 확인
  ↓
process / port 확인
  ↓
log 확인
  ↓
environment/config 확인
```

AWS 콘솔에서 EC2가 `running`이라고 보여도 OS와 애플리케이션 내부 문제는 별도로 조사해야 한다.

## 최소 명령어

```bash
ssh
journalctl
tail -f
printenv
env
cat /etc/os-release
```

이번 유닛까지를 Linux 최소 기반으로 잡는다. 실제 EC2 배포 단계에서 이 명령들을 다시 사용한다.

기본 도구 정리 성격이므로 별도 유제와 3문장 요약은 생략한다.
