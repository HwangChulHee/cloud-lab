# u1. Process와 Service

## 지도 확인

클라우드에서 EC2 같은 가상 서버를 사용하기 시작하면 결국 그 안에서는 Linux 프로세스가 애플리케이션을 실행한다.

웹 서버, FastAPI, Nginx, Docker 데몬 같은 것도 모두 결국 Linux 위에서 동작하는 프로세스다.

따라서 클라우드 엔지니어에게 Linux는 별도의 학문이라기보다, **서버 상태를 확인하고 장애 원인을 찾기 위한 기본 도구**에 가깝다.

이번 유닛에서는 깊게 들어가지 않고 다음만 확실히 잡는다.

- 프로세스란 무엇인가
- PID가 무엇인가
- foreground / background 프로세스
- 프로세스 상태를 확인하는 기본 명령어
- 프로세스를 종료하는 방법
- systemd service가 왜 필요한가

---

## 1. Process란 무엇인가

프로그램은 디스크에 저장된 실행 가능한 코드이고, 프로세스는 그 프로그램이 실제로 실행 중인 상태다.

예를 들어 Python 파일 자체는 단순한 파일이다.

```text
app.py
```

하지만 다음처럼 실행하면:

```bash
python3 app.py
```

운영체제는 Python 프로그램을 실행하고 하나의 프로세스를 만든다.

```text
program
  ↓ 실행
process
```

서버에서 "애플리케이션이 살아 있는가?"라는 질문은 결국 상당 부분 다음 질문으로 바뀐다.

```text
해당 프로세스가 실행 중인가?
```

---

## 2. PID

Linux의 각 프로세스에는 **PID(Process ID)** 라는 번호가 붙는다.

실행 중인 프로세스를 확인할 때 가장 기본적인 명령어가 `ps`다.

```bash
ps aux
```

특정 프로세스만 찾고 싶다면 보통 `grep`과 같이 사용한다.

```bash
ps aux | grep python
```

또는:

```bash
pgrep -af python
```

예를 들어 다음처럼 보일 수 있다.

```text
ubuntu   1542 ... python3 app.py
```

여기서 `1542`가 PID라고 생각하면 된다.

운영 중에는 프로세스 이름보다 PID를 기준으로 상태를 확인하거나 종료하는 경우가 많다.

---

## 3. Foreground와 Background

쉘에서 명령어를 실행하면 기본적으로 foreground에서 실행된다.

```bash
python3 app.py
```

이 상태에서는 해당 프로세스가 터미널을 점유한다.

`Ctrl + C`를 누르면 일반적으로 프로세스에 종료 신호를 보내 실행을 중단한다.

간단히 background로 실행하려면 `&`를 사용할 수 있다.

```bash
python3 app.py &
```

그러나 서버 애플리케이션을 실제 운영할 때 단순히 `&`만 사용하는 것은 충분하지 않다.

SSH 연결이 끊기거나 서버가 재부팅되었을 때 애플리케이션이 다시 실행되어야 하기 때문이다.

그래서 이후에는 `systemd` 같은 서비스 관리자를 사용한다.

---

## 4. 프로세스 상태 확인

클라우드에서 장애가 발생했을 때 가장 먼저 확인하게 되는 것 중 하나가 "프로세스가 실제로 떠 있는가"이다.

자주 사용하는 명령어는 다음 정도만 먼저 익힌다.

```bash
ps aux
```

전체 프로세스 목록을 확인한다.

```bash
pgrep -af nginx
```

특정 프로세스를 찾는다.

```bash
top
```

CPU와 메모리 사용량을 포함한 프로세스 상태를 실시간으로 확인한다.

환경에 따라 `htop`을 사용할 수도 있지만 기본적으로 `top`을 먼저 알아두는 편이 좋다.

---

## 5. 프로세스 종료와 Signal

프로세스를 종료할 때는 보통 `kill` 명령어를 사용한다.

```bash
kill 1542
```

`kill`이라는 이름 때문에 무조건 프로세스를 강제 종료하는 명령처럼 보이지만, 실제로는 프로세스에 **signal을 보내는 명령**이다.

기본적으로는 SIGTERM을 보낸다.

```text
SIGTERM
→ 가능하면 정상적으로 종료해라
```

프로세스가 종료되지 않을 때 다음을 볼 수 있다.

```bash
kill -9 1542
```

이는 SIGKILL을 보낸다.

```text
SIGKILL
→ 즉시 강제로 종료
```

운영에서는 가능하면 먼저 정상 종료(SIGTERM)를 시도하고, 정말 필요할 때 강제 종료를 사용한다.

왜냐하면 애플리케이션이 종료 과정에서 연결 정리, 파일 기록, 요청 마무리 같은 작업을 수행해야 할 수 있기 때문이다.

---

## 6. Process가 죽으면 서비스도 죽는다

다음 구조를 생각해보자.

```text
Internet
   ↓
EC2
   ↓
FastAPI process
```

EC2 자체는 정상적으로 실행 중이어도 FastAPI 프로세스가 죽으면 사용자는 애플리케이션에 접근하지 못한다.

즉:

```text
서버가 살아 있다
!=
애플리케이션이 살아 있다
```

이 구분은 나중에 AWS에서 매우 중요해진다.

예를 들어:

```text
EC2 Instance State
→ running

Application Process
→ stopped
```

이라면 EC2 콘솔에서는 서버가 정상처럼 보이지만 실제 서비스는 장애 상태일 수 있다.

이 때문에 Load Balancer의 Health Check, CloudWatch Monitoring 등이 필요해진다.

---

## 7. systemd와 Service

Linux 서버에서 장기간 실행되는 애플리케이션은 보통 서비스로 관리한다.

많은 Linux 배포판에서는 `systemd`가 이를 담당한다.

예를 들어 Nginx 상태를 확인할 수 있다.

```bash
systemctl status nginx
```

시작:

```bash
sudo systemctl start nginx
```

중지:

```bash
sudo systemctl stop nginx
```

재시작:

```bash
sudo systemctl restart nginx
```

부팅 시 자동 시작:

```bash
sudo systemctl enable nginx
```

`systemd`를 사용하는 가장 큰 이유 중 하나는 서버 프로그램의 생명주기를 사람이 직접 관리하지 않아도 되게 만드는 것이다.

```text
EC2 reboot
   ↓
systemd start
   ↓
application start
```

이후 EC2에 FastAPI를 배포할 때 직접 `.service` 파일을 만들어 이 흐름을 실습한다.

---

## 8. Cloud Engineer 관점

서버 장애를 볼 때 최소한 다음 순서를 떠올릴 수 있어야 한다.

```text
1. EC2 자체가 실행 중인가?
2. 애플리케이션 프로세스가 실행 중인가?
3. 해당 포트에서 실제로 listen 중인가?
4. OS 내부에서는 정상인데 외부에서만 접근이 안 되는가?
```

문제의 위치를 단계적으로 좁혀가는 것이 중요하다.

예를 들어:

```text
EC2 running
FastAPI process running
localhost 요청 성공
외부 요청 timeout
```

이라면 애플리케이션 자체보다는 Security Group, Network ACL, Route 같은 네트워크 계층을 의심할 수 있다.

반대로:

```text
EC2 running
FastAPI process 없음
```

이라면 AWS 네트워크보다 애플리케이션 프로세스나 서비스 설정을 먼저 확인해야 한다.

이런 식으로 앞으로 Linux와 AWS를 하나의 장애 분석 흐름으로 연결한다.

---

## 최소 명령어 정리

지금 단계에서는 다음 명령어 정도만 익숙해지면 충분하다.

```bash
ps aux
pgrep -af <name>
top
kill <pid>
kill -9 <pid>
systemctl status <service>
systemctl start <service>
systemctl stop <service>
systemctl restart <service>
systemctl enable <service>
```

명령어 옵션을 전부 외울 필요는 없다.

중요한 것은 **프로세스 상태를 확인하고, 실행/종료하고, 서비스로 관리할 수 있다는 것**이다.

---

## 앞으로의 연결

```text
EC2
→ Linux 서버

EC2 User Data
→ 부팅 시 명령 실행

systemd
→ 애플리케이션 자동 시작

ALB Health Check
→ 프로세스/애플리케이션의 실제 응답 확인

CloudWatch
→ CPU, 메모리, 로그 등의 관측

Docker
→ 프로세스를 컨테이너 단위로 관리
```

이번 유닛은 기본 조작 개념이므로 별도 유제와 3문장 요약은 생략한다.
