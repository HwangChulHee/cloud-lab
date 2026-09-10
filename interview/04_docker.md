# 04. Docker

## 핵심 질문

1. Container와 VM의 차이는 무엇인가요?
2. Docker Image와 Container의 차이는 무엇인가요?
3. Dockerfile에서 `RUN`, `CMD`, `ENTRYPOINT`의 차이는 무엇인가요?
4. Docker layer란 무엇인가요?
5. Container가 실행 직후 종료됩니다. 어떻게 조사하나요?
6. Docker volume을 사용하는 이유는 무엇인가요?
7. Container 간 네트워크 통신은 어떻게 하나요?

## 실전형 질문

### Container가 바로 종료됩니다.

```text
docker ps -a
 ↓
docker logs <container>
 ↓
docker inspect <container>
 ↓
ENTRYPOINT / CMD 확인
 ↓
환경변수 / 파일 / 권한 / dependency 확인
```

추가로 application이 foreground process로 실행되고 있는지 확인합니다. Container의 주 프로세스가 종료되면 container도 종료됩니다.

### 데이터베이스 container를 삭제했더니 데이터가 사라졌습니다.

Container writable layer에만 데이터를 두었다면 container 삭제 시 함께 사라질 수 있습니다. 영속 데이터는 volume이나 외부 storage를 사용하도록 설계합니다.
