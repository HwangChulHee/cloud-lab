# u2. Files, Directories와 Permission

## 지도 확인

클라우드에서 Linux 서버를 다루다 보면 결국 거의 모든 설정과 상태가 파일로 연결된다.

```text
애플리케이션 코드
환경설정 파일
로그 파일
SSH 키
systemd service 파일
Nginx 설정
TLS 인증서
```

따라서 이번 유닛의 목표는 Linux 파일 시스템을 깊게 공부하는 것이 아니라, **서버에서 파일을 찾고 읽고 수정하고, 권한 문제를 구분할 수 있는 수준**까지 익히는 것이다.

이번 유닛에서는 다음만 잡는다.

- 절대 경로 / 상대 경로
- 기본 디렉터리 이동과 파일 확인
- 파일 내용 확인
- 사용자 / 그룹 / 권한
- `rwx`와 숫자 권한
- `chmod`, `chown`
- 서버 운영에서 자주 만나는 Permission denied

---

## 1. Linux 파일 시스템

Linux는 하나의 루트 디렉터리 `/`에서 시작한다.

```text
/
├── etc
├── home
├── var
├── usr
├── tmp
└── ...
```

Windows의 `C:\`, `D:\`처럼 드라이브마다 별도의 최상위 경로가 있는 방식과는 다르게 생각하면 된다.

서버를 운영할 때 자주 보게 되는 경로는 대략 다음 정도다.

```text
/etc
→ 시스템과 서비스 설정 파일

/home
→ 일반 사용자 홈 디렉터리

/var/log
→ 여러 서비스의 로그

/tmp
→ 임시 파일

/usr
→ 프로그램 및 라이브러리
```

모든 디렉터리 구조를 외울 필요는 없다.

중요한 것은 문제가 생겼을 때 "설정은 어디에 있고 로그는 어디에서 볼까?"를 찾아갈 수 있는 것이다.

---

## 2. 현재 위치와 경로

현재 디렉터리를 확인한다.

```bash
pwd
```

예:

```text
/home/ubuntu/cloud-lab
```

파일과 디렉터리를 확인한다.

```bash
ls
ls -l
ls -la
```

디렉터리를 이동한다.

```bash
cd /var/log
cd ..
cd ~
```

### 절대 경로

루트 `/`에서부터 전체 위치를 적는다.

```text
/etc/nginx/nginx.conf
/home/ubuntu/app/main.py
```

### 상대 경로

현재 위치를 기준으로 적는다.

현재 위치가:

```text
/home/ubuntu/app
```

이라면:

```bash
cat main.py
cat ./main.py
```

둘 다 같은 파일을 가리킬 수 있다.

상위 디렉터리는 `..`로 표현한다.

```bash
cd ..
```

---

## 3. 파일과 디렉터리 기본 조작

파일 생성:

```bash
touch test.txt
```

디렉터리 생성:

```bash
mkdir logs
mkdir -p app/config
```

복사:

```bash
cp source.txt target.txt
cp -r source_dir target_dir
```

이동 또는 이름 변경:

```bash
mv old.txt new.txt
```

삭제:

```bash
rm test.txt
rm -r directory
```

운영 서버에서는 특히 `rm -r` 같은 명령을 습관적으로 빠르게 입력하지 않는 편이 좋다.

삭제 전에 현재 경로와 대상을 확인하는 습관이 중요하다.

```bash
pwd
ls
```

---

## 4. 파일 내용 확인

짧은 파일은:

```bash
cat app.conf
```

긴 파일은:

```bash
less app.log
```

앞부분 확인:

```bash
head app.log
```

마지막 부분 확인:

```bash
tail app.log
```

로그를 실시간으로 따라가려면:

```bash
tail -f app.log
```

이 명령은 서버 운영에서 자주 사용한다.

```text
애플리케이션에 요청 발생
        ↓
로그 파일에 기록
        ↓
tail -f 로 실시간 확인
```

이후 CloudWatch Logs를 공부할 때도 기본 사고방식은 같다.

---

## 5. User와 Group

Linux 파일에는 보통 다음 정보가 연결되어 있다.

```text
owner
 group
 permission
```

예를 들어:

```bash
ls -l
```

결과가 다음과 같다고 하자.

```text
-rw-r----- 1 ubuntu app 1250 Sep 7 10:00 config.yml
```

여기서 중요한 부분은:

```text
ubuntu
→ 파일 owner

app
→ 파일 group

rw-r-----
→ permission
```

현재 사용자를 확인하려면:

```bash
whoami
```

사용자와 그룹 정보를 조금 더 자세히 보면:

```bash
id
```

---

## 6. Permission: rwx

Linux 권한은 기본적으로 세 집단에 대해 나뉜다.

```text
user(owner)
group
others
```

각 집단은 다음 권한을 가질 수 있다.

```text
r = read
w = write
x = execute
```

예를 들어:

```text
-rwxr-xr--
```

세 묶음으로 나누면:

```text
rwx | r-x | r--
user  group others
```

의미는:

```text
owner
→ 읽기, 쓰기, 실행 가능

group
→ 읽기, 실행 가능

others
→ 읽기만 가능
```

---

## 7. 숫자 권한

권한은 숫자로도 표현한다.

```text
r = 4
w = 2
x = 1
```

합산해서 표현한다.

```text
7 = rwx
6 = rw-
5 = r-x
4 = r--
```

따라서:

```bash
chmod 755 script.sh
```

는:

```text
owner  = rwx
 group = r-x
others = r-x
```

를 의미한다.

그리고:

```bash
chmod 600 private.key
```

는:

```text
owner  = rw-
group   = ---
others  = ---
```

이다.

SSH private key처럼 민감한 파일에서 이런 제한된 권한이 중요해진다.

---

## 8. chmod와 chown

파일 권한 변경:

```bash
chmod 644 config.txt
chmod 755 deploy.sh
```

소유자 변경:

```bash
sudo chown ubuntu:ubuntu app.log
```

재귀적으로 디렉터리 전체 소유자를 바꾸는 경우도 있다.

```bash
sudo chown -R ubuntu:ubuntu /opt/myapp
```

하지만 운영 서버에서는 무작정 `chmod 777` 또는 `chown -R`부터 사용하는 습관을 피하는 것이 좋다.

문제를 해결하는 것처럼 보여도 실제 원인을 숨기거나 불필요하게 권한을 넓힐 수 있기 때문이다.

```text
Permission denied
        ↓
777 부여
```

보다 먼저 다음을 확인하는 게 낫다.

```text
누가 실행하고 있는가?
누가 파일 owner인가?
어떤 group인가?
어떤 permission이 필요한가?
```

---

## 9. 디렉터리의 x 권한

파일에서 `x`는 실행 권한이라고 이해하기 쉽다.

하지만 디렉터리의 `x`는 조금 다르게 볼 필요가 있다.

디렉터리에 `x` 권한이 있어야 그 디렉터리 안으로 들어가거나 내부 경로에 접근할 수 있다.

예를 들어 파일 자체에 읽기 권한이 있어도 상위 디렉터리를 통과할 권한이 없다면 접근하지 못할 수 있다.

```text
/opt/myapp/config.yml

config.yml 권한 정상
        ↑
하지만 /opt/myapp 디렉터리 접근 권한 없음
        ↓
Permission denied
```

운영에서 권한 문제를 볼 때 파일 하나만 보지 말고 상위 디렉터리 권한도 함께 확인해야 하는 이유다.

---

## 10. Cloud Engineer 관점의 Permission denied

다음 상황을 생각해보자.

```text
EC2
 ↓
systemd
 ↓
FastAPI
 ↓
/var/log/myapp/app.log
```

애플리케이션이 `ubuntu` 사용자가 아니라 `myapp` 사용자로 실행되고 있다고 하자.

로그 디렉터리가 다음처럼 되어 있다면:

```text
owner: root
permission: 700
```

`myapp` 프로세스는 해당 디렉터리에 파일을 쓸 수 없다.

결과적으로 애플리케이션에서 다음과 같은 문제가 발생할 수 있다.

```text
Permission denied
```

이때 문제는 AWS Security Group도, EC2 상태도 아니다.

```text
OS 파일 권한 문제
```

이다.

클라우드 장애를 볼 때도 계층을 구분해야 한다.

```text
AWS resource
Network
OS
Process
File permission
Application
```

---

## 11. sudo는 무엇인가

일반 사용자가 관리자 권한이 필요한 명령을 실행할 때 `sudo`를 사용한다.

```bash
sudo systemctl restart nginx
sudo chown ubuntu:ubuntu app.log
```

그렇다고 모든 명령에 `sudo`를 붙이는 것이 좋은 습관은 아니다.

가능하면 필요한 작업에만 관리자 권한을 사용한다.

이 사고방식은 이후 IAM의 **Least Privilege**와도 연결된다.

```text
Linux
→ 필요한 OS 권한만 부여

AWS IAM
→ 필요한 AWS 권한만 부여
```

구현 방식은 다르지만 "필요 이상의 권한을 주지 않는다"는 운영 원칙은 같다.

---

## 최소 명령어 정리

지금 단계에서는 아래 정도만 익숙해지면 충분하다.

```bash
pwd
ls -l
ls -la
cd
mkdir
cp
mv
rm
cat
less
head
tail
tail -f
whoami
id
chmod
chown
```

권한 숫자도 우선 다음 정도는 바로 읽을 수 있으면 좋다.

```text
644
755
600
```

---

## 앞으로의 연결

```text
EC2 SSH key
→ private key permission

systemd
→ 어떤 Linux user로 프로세스를 실행하는가?

Nginx
→ 설정 파일과 로그 파일은 어디에 있는가?

FastAPI
→ 실행 사용자가 파일에 접근할 수 있는가?

Docker
→ container 내부 user / volume permission

IAM
→ Linux permission과는 별개지만 Least Privilege 원칙은 동일
```

이번 유닛 역시 기본 조작 성격이 강하므로 별도 유제와 3문장 요약은 생략한다.
