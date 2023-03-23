# Docker 이미지 생성을 위한 베이스 이미지 설정
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# 작업 디렉토리 생성 및 설정
WORKDIR /

# 필요한 라이브러리 및 패키지 설치
COPY requirements.txt .
RUN set -x && pip install -r requirements.txt

# 소스코드 복사
COPY . ./app

# 컨테이너가 실행될 때 실행할 명령어 설정
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
