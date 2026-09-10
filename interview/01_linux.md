# 01. Linux

## 핵심 질문

1. Linux에서 CPU를 많이 사용하는 프로세스를 어떻게 찾나요?
2. 메모리를 많이 사용하는 프로세스를 어떻게 찾나요?
3. 특정 포트를 어떤 프로세스가 사용 중인지 어떻게 확인하나요?
4. `ps`, `top`, `htop`의 용도를 설명해보세요.
5. `df`와 `du`의 차이는 무엇인가요?
6. 디스크가 100% 찼는데 어떤 순서로 조사하겠습니까?
7. `chmod 755`가 의미하는 것은 무엇인가요?
8. 프로세스와 스레드의 차이는 무엇인가요?
9. zombie process란 무엇인가요?
10. systemd와 `systemctl`의 역할은 무엇인가요?
11. 서비스가 실행되지 않을 때 어디서 로그를 확인하나요?
12. Load Average 1, 5, 15분 값은 무엇을 의미하나요?
13. inode가 고갈되면 어떤 현상이 발생하나요?
14. soft link와 hard link의 차이는 무엇인가요?
15. SIGTERM과 SIGKILL의 차이는 무엇인가요?

## 자주 쓰는 확인 명령

```bash
top
ps aux --sort=-%cpu
ps aux --sort=-%mem
ss -lntp
free -m
df -h
du -sh *
systemctl status <service>
journalctl -u <service>
```

## 실전형 질문

### 서버의 8080 포트 서비스가 외부에서 안 열립니다. 어떻게 확인하시겠어요?

답변 흐름 예시:

```text
1. 애플리케이션 프로세스가 실행 중인지 확인
2. 8080 포트를 실제로 listen 중인지 확인
3. localhost에서 curl로 응답 확인
4. OS firewall 확인
5. Security Group / NACL / Route 확인
6. Load Balancer 사용 시 target health 확인
```

명령 예시:

```bash
ss -lntp
curl localhost:8080
systemctl status myapp
journalctl -u myapp
```
