# My Refrigerator

## Get Started

| 상황 | 명령어 |
| ---- | ------ |
| 환경 불러오기 | `conda env create -f conda.yaml` |
| 환경 내보내기 | `conda env export > conda.yaml` |
| 환경 실행하기 | `conda activate my-refrigerator` |

<details>
<summary>
참고자료
</summary>

- [[Anaconda] 아나콘다 가상환경 Export 및 Import 하는 방법](https://mentha2.tistory.com/46)
- [[Anaconda] 아나콘다 환경 export, import, clone 하기](https://jh-bk.tistory.com/35)
</details>

### Configs

다음과 같은 구조의 파일입니다.
```yaml
path: "/home/ubuntu/server"

banned_keyword_list: [ '고객', '결제', '카드', '승인', '가맹점', '전화', '번호', '사업', '할부', '개월' ]
analysis_keyword_list: [ '메뉴', '단가', '수량', '금액' ]

api_key: 'API KEY'

DJANGO_CONFIG:
  SECRET_KEY: 'DJANGO SCRET KEY'

  ALLOWED_HOST: [ 'NGINX HOST NAME', '127.0.0.1' ]
  ALLOWED_CORS_ORIGIN: [ 'http://example.com', 'https://example.com' ]

RDS_CONFIG:
  ENGINE: 'RDS ENGINE'
  HOST: 'RDS ADDRESS'
  PORT: 77777
  USER: 'RDS HOST'
  PASSWORD: 'RDS PWD'
  DATABASE_NAME: 'RDS_NAME'

JWT_CONFIG:
  SECRET_KEY: 'JWT SECRET'
  ALGORITHM: 'HS256'
```


<br>

### History[New]

```cmd
# [STEP 1] 가상환경 설정
apt update -y
apt install python3-venv
python3 -m venv venv

# [STEP 2] 가상환경 진입
sourc venv/bin/activate

# [STEP 3] APT 모듈 설치
apt install libgl1-mesa-glx

apt install tesseract-ocr
apt install tesseract-ocr-eng
apt install tesseract-ocr-kor
apt install libmysqlclient-dev


# [STEP 4] PIP 모듈 설치
pip install opencv-python
pip install matplotlib
pip install pytesseract

pip install imutils
pip install scipy

pip install python-decouple
pip install django-cors-headers

pip install pydantic

pip install mysqlclient
pip install PyMySQL
pip install PyJWT
pip install PyYaml
```

### History[Legacy]

```cmd
conda create -n my-refrigerator -y

conda activate my-refrigerator

[after]
pip install opencv-python
pip install matplotlib
conda install -c conda-forge tesseract
conda install tesseract-ocr
conda install libtesseract-dev
pip install pytesseract

pip install imutils
pip install scipy
pip install orig [NOne]

pip install python-decouple
pip install django-cors-headers
pip install djangorestframework [Remove!]
pip install pydantic
pip install psycopg2 [Failure]
pip install psycopg2-binary [Success, instead of psyconpg2]

apt install libmysqlclient-dev [Dependency for mysqlclient]
pip install mysqlclient
pip install PyMySQL
pip install PyJWT
```

## Get Started(Ubuntu Only)

### [STEP-1] Python 설치

```
# apt를 최신버전으로 업데이트
apt update

# pip을 설치
# 실행 후, python -V로 확인하면 Python 2.7.17이 보임
apt install python
apt install python-pip
apt install python3-pip

# python3.8설치
# python3은 AWS에서 사용하고 있으므로 건드리지 않을 것!!
# 설치 후, python3.8 -V로 확인하면 Python 3.8.0이 보임
# 설치 후, python -V로 확인하면 Python 3.7.0이 보임
apt install python3.8

# 아래 명령어로 심볼릭 링크 경로 확인
ls -al /usr/bin/python

# 해당 경로를 변경하기 위한 라이브러리 설치
apt install update-alternatives

# 심볼릭 링크 변경이 가능한 대체 항목에 /usr/bin/python3.8을 추가
update-alternatives --install /usr/bin/python python /usr/bin/python3.8 2

# 심볼릭 링크 항목을 /usr/bin/python3.8으로 변경
# 변경 후, python -V로 확인하면 Python 3.8.0이 보임
update-alternatives --config python

# 아래 명령어로 심볼릭 링크 경로 확인
## lrwxrwxrwx 1 root root 24 Feb 2 06:45 /usr/bin/python -> /etc/alternatives/python
ls -al /usr/bin/python

# Python 3.8.0을 기준으로 pip을 업데이트
python -m pip install --upgrade pip

# PIP으로 OpenCV 설치를 위한 종속성 모듈 설치
apt install libgl1-mesa-glx
```

### [STEP-2] CORE 모듈 설치

```
# https://tesseract-ocr.github.io/tessdoc/Installation.html
sudo apt install tesseract-ocr -y
sudo apt install libtesseract-dev -y
sudo pip install pytesseract

sudo apt install tesseract-ocr-script-kor

# https://docs.opencv.org/3.4/d2/de6/tutorial_py_setup_in_ubuntu.html
sudo apt install python3-opencv -y

cd <프로젝트 경로>
cp ./assets/tesseract/kor.traineddata /usr/share/tesseract-ocr/4.00/tessdata/kor.traineddata
```