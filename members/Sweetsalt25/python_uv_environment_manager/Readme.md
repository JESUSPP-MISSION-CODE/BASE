# 개요
Python 생태계는 오랫동안 패키지 관리, 버전 관리, 가상환경 관리, 빌드 도구 등이 파편화되어 혼란스럽다는 평가를 받아왔습니다.  
Astral이 만든 uv는 2024년 초에 출시되어, pip, poetry, conda 등 다양한 도구들의 장점을 통합하고, Rust를 활용한 초고속 의존성 해석(Resolver)으로 큰 주목을 받고 있습니다.  
Anthropic, OpenAI 를 포함한 실제 ML/DS(데이터 사이언스), 백엔드, 오픈소스 프로젝트 등 여러 분야에서 uv 도입 사례가 급격히 늘고 있습니다.  
<br>

# Python 패키징이 복잡해진 역사
## 1. 초기 시절: easy_install
- 2000년대 후반~2010년대 초반에는 PyPI와 pip 가 지금처럼 성숙하지 않았습니다.  
- 당시에는 easy_install 이 사실상 유일한 선택지였고, 설치한 패키지를 제거하거나, 설치된 패키지 버전을 지정·고정하는 기능이 부족해 많은 불편이 있었습니다.  
<br>

## 2. pip의 등장
- pip는 requirements.txt를 통해 의존성을 고정하고 설치할 수 있는 기능을 제공하면서, 그야말로 Python 커뮤니티의 표준이 되었습니다.  
- Python 공식 배포판에도 점차 포함되어 사실상 “파이썬 하면 pip”라는 인식이 굳어지기도 했습니다.  
<br>

## 3. conda의 등장과 머신러닝 생태계
- conda는 주로 NumPy, SciPy 같은 과학 컴퓨팅 라이브러리를 쉽게 설치하고자 하는 목적에서 개발되었습니다.  
- 하지만 conda 는 별도의 패키지 저장소(Anaconda Cloud, conda-forge)를 사용하고, pip 와는 분리된 자체 의존성 해석 방식, 가상환경 관리 방식을 채택하고 있어서 생태계가 이원화되는 문제를 야기했습니다.  
- 그 결과, 리서쳐와 서비스 개발자 간의 소통 문제가 빈번히 발생해 왔습니다.  
<br>

## 4. poetry의 부상
- poetry는 pyproject.toml과 poetry.lock 기반으로 의존성을 엄격히 고정하고, 여러 플랫폼에서 재현 가능한 빌드를 제공한다는 점에서 각광을 받았습니다.  
- 단점으로는, 복잡한 의존성을 가진 프로젝트에서 해석 속도가 느리다는 점이 종종 지적되었습니다.  
- 그럼에도 Poetry는 “제대로 동작하는 것을 보장한다” 는 확실한 장점을 가진 덕분에, 비교적 규모가 큰 팀이나 오픈소스 프로젝트에서 널리 채택되었습니다.  
- pyenv, pipx, pipenv, pip-tools 등의 도구도 각자 가상환경·의존성 관리, Python 버전 관리, 종속성 락(lock) 파일 관리 등 다양한 문제를 해결하고자 시도했습니다.  
- 하지만 이런 도구마다 관점이 달라서, 서로 비슷한 기능이 겹치거나, 설정 방식이 달라 숙련된 개발자조차 혼란스러워하는 지점이 많았습니다.  
----

# uv의 등장
## 1. uv가 해결하려는 문제
- uv는 Rust로 작성된 고속 의존성 해석 엔진을 앞세워, 가상환경 생성, 의존성 관리, 파이썬 버전 관리, 패키징, 포매터/린터 같은 서드파티 도구 실행을 한번에 알잘딱 처리합니다.
<br>

## 2. 주요 특징
### 성능(Performance)
- Rust 기반 Resolver로 의존성 설치 속도가 pip나 poetry 대비 10~100배 빠르다는 공식 벤치마크가 있습니다.
- 캐싱과 최적화를 적극 활용하여 대규모 프로젝트에서도 빠른 설치 및 업데이트가 가능합니다.
<br>

### 사용 편의성(Usability)
- uv add 등 단순화된 CLI 명령어로 대부분의 작업을 수행할 수 있습니다.
- .venv 폴더나 파이썬 버전 설정(.python-version 등)을 직접 신경 쓰지 않아도 자동으로 생성·관리해줍니다.
- Rust에서 “Cargo 하나로 빌드, 의존성 관리, 패키징, 배포 등 모든 작업”을 해결하는 것처럼, Python 환경에서도 “uv 하나로” 가능하게끔 디자인되어 있습니다.
- Astral의 CEO Charlie Marsh 및 rye 개발자 Armin Ronacher 등이 Python tooling 역사의 문제점을 충분히 연구하고, 그 교훈을 uv에 반영했습니다.
- uv는 오픈소스로 공개되어 있으며, 활발한 커뮤니티 피드백을 받고 있습니다.
- “단일 툴이 지배해야 생태계를 발전시킨다” 라는 Armin Ronacher의 글처럼, uv를 함께 발전시키려는 커뮤니티 움직임이 확산되고 있습니다.
<br>

# uv 사용 방법: 시작부터 배포까지
## 1. 프로젝트 생성
```
uv init uv-demo
cd uv-demo
```
- uv init 명령어를 통해 새로운 uv 프로젝트를 초기화합니다.
- uv-demo 폴더가 생성되고, 내부 구조는 대략 다음과 같습니다:
```
uv-demo/
├── .python-version
├── .gitignore
├── pyproject.toml
├── hello.py
└── README.md
```
- .python-version을 통해 파이썬 버전이 고정됩니다.
- pyproject.toml 은 의존성 및 프로젝트 메타데이터를 정의하는 핵심 파일입니다.
- .venv 폴더는 아직 보이지 않을 수 있는데, 의존성을 추가하면 자동으로 생성됩니다.
<br>

## 2. 의존성 설치 & 성능 비교
다음 requirements.txt 를 통해 다양한 의존성을 한꺼번에 설치해보겠습니다:
```
kuzu==0.7.1
lancedb==0.17.0
llama-index==0.12.8
llama-index-llms-openai==0.3.12
llama-index-embeddings-openai==0.3.1
llama-index-graph-stores-kuzu==0.6.0
llama-index-vector-stores-lancedb==0.3.0
numpy==2.2.1
polars==1.18.0
pyarrow==18.1.0
python-dotenv==1.0.1

# 사전 준비: 캐시 정리
`uv clean cache`
`pip cache purge`
`poetry cache clear - all .`
```
### 1) pip 사용 시
```
python -m venv .venv      # 로컬 가상환경 생성
source .venv/bin/activate # 가상환경 활성화
time pip install -r requirements.txt
```
- 설치 시간: 약 18.3초(테스트 예시 기준)
- 주의 사항: 가상환경을 활성화하는 작업을 잊으면 시스템 전역에 설치해버릴 위험이 있습니다.

### 2) poetry 사용 시
```
rm -rf .venv             # 기존 가상환경 제거
poetry init              # poetry 설정 초기화
poetry shell             # poetry가 만든 가상환경 진입
time poetry install      # 의존성 설치
```
- 설치 시간: 약 6.3초
- poetry는 `poetry.lock`을 생성하고, 이를 기반으로 의존성을 세심하게 관리합니다.
- 사용 시 poetry shell에 들어가야 하므로, 약간 귀찮을 수 있습니다.

### 4) uv 사용 시
```
uv init                           # pyproject.toml 생성(필요 시)
time uv add -r requirements.txt   # 의존성 설치
```
- 설치 시간: 약 2.3초
- .venv 폴더가 자동으로 생성되고, 가상환경을 별도로 활성화할 필요가 없습니다.
- 이후 `uv run` 명령어로 Python 파일을 실행할 때, 자동으로 .venv 환경이 적용됩니다.
<br>

### 요약: 설치 시간 비교
|도구 |설치 시간|
|--|--|
|pip |18.3초 |
|poetry |6.3초 |
|uv |2.3초 |

- uv가 pip 대비 8배, poetry 대비 3배 가까이 빠른 결과가 나왔습니다.
- 실제 대규모 프로젝트에서는 의존성 충돌이나 빌드 과정이 더 복잡해져, uv의 속도 우위가 더욱 뚜렷해질 가능성이 큽니다.
----

# 인터랙티브 개발과 uv
## 1. 인터랙티브 환경(예: VS Code, Cursor IDE)
- 프로젝트 초기 단계나 실험 단계에서, IDE/에디터 내장 대화형 실행(Shift+Enter 등) 을 자주 활용합니다.
- `ipykernel`을 이용하면 Jupyter notebook처럼 코드 셀 단위로 빠르게 실행·테스트할 수 있지만, 가상환경이 매번 달라지면 불편합니다.
<br>

## uv의 장점
- 동일한 .venv 가상 환경을 IDE가 바로 인식하도록 해줍니다.
- 예를 들어, uv add -- dev ipykernel 명령을 통해 개발용 의존성(dev dependency group) 으로 - ipykernel을 설치해두면, IDE가 이를 자동으로 감지해 가상환경 커널을 연결합니다.
```
uv add -r requirements.txt  # 주요 의존성 설치
uv add --dev ipykernel      # 개발용(인터랙티브) 의존성 추가
```
- 이로써 주피터 노트북처럼 별도의 커널을 생성·관리할 필요가 현저히 줄어듭니다.
- 팀원들이 다른 에디터를 쓰더라도, uv sync만 하면 동일한 .venv 를 재현할 수 있죠.
  
## 2. Jupyter 노트북 vs IDE 내장 커널
- 기존에는 Jupyter Lab이나 노트북에서 python -m ipykernel install ...등 추가 작업을 해야 했지만, uv는 프로젝트 폴더 하나만 공유하면, 그 안의 .venv 와 pyproject.toml, uv.lock 으로 곧바로 동일한 가상 환경을 복원할 수 있습니다.
----

# 명령줄 실행
## 1. uv run
- Python 스크립트를 CLI에서 실행할 때도, uv가 알아서 가상환경을 적용해줍니다.
```
# hello.py 예시
import polars as pl

df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
print("Hello from uv-demo!")
# 명령줄에서
uv run hello.py
# 출력: Hello from uv-demo!
```
1. Python이 설치되어 있는지 확인 및 설치(필요 시)
2. .venv 가상환경 생성 및 활성화
3. pyproject.toml 기반 의존성 설치
4. 코드 실행…
이 모든 과정을 uv run 한 줄로 해결합니다.

## 2. uv sync
- CI/CD 등 자동화 환경에서 uv sync만으로 프로젝트에 필요한 Python 버전과 .venv 가 자동으로 맞춰집니다.

## 3. 의존성 잠금파일(uv.lock)
- poetry.lock 처럼 `uv.lock` 파일을 생성해 의존성 버전을 고정합니다.
- 빠른 빌드와 재현성을 동시에 보장합니다.
----

# 명령어 몇 개를 소개합니다

## uv init
- 새로운 uv 프로젝트 초기화, pyproject.toml 생성

## uv add <패키지명>
- 특정 패키지 추가
- uv add -r requirements.txt로 `requirements.txt` 전체 추가 가능

## uv sync
- pyproject.toml 과 uv.lock 파일을 기준으로 가상환경 재생성 및 동기화

## uv run <파일명.py>
- 가상환경을 자동 적용하여 파이썬 스크립트 실행

## uvx <툴> (`uv tool run` 명령의 축약형)
- ruff, mypy 등 서드파티 명령을 자동으로 설치·실행해줌
예) uvx ruff check .
----

# 코드 포매팅 & 린팅: `uvx`로 ruff 사용하기
- 기존 Python 프로젝트에서 black, isort, flake8 를 따로 설치·관리했어야 했다면, uv에서는 uvx ruff 라는 단순 명령어로 linter+formatter 역할을 ruff가 대신합니다.
```
uvx ruff check .
uvx ruff format *.py --line-length 100
```
- ruff는 이미 여러 툴(black, isort, flake8 등) 의 기능을 결합하고, Rust 기반으로 매우 빠른 포매팅·체킹을 제공합니다.
- uv와 ruff를 함께 쓰면, 코드 스타일 관리가 훨씬 간소화됩니다.
----

# uv로 무엇을 대체할 수 있나?
- 개인적으로 uv를 쓰면서, 다음 도구들을 거의 사용하지 않게 됐습니다:
    - pip: 패키지 설치
    - pyenv: 파이썬 버전 관리
    - poetry: 의존성·빌드 관리
    - venv: 가상환경 생성
    - pipenv: 환경+의존성 관리
- 대규모 팀 환경일수록, 도구 하나로 끝낸다 라는 데서 오는 이점이 큽니다.
- 프로젝트 빌드·실행·배포 파이프라인에서 uv를 중심에 두면, Rust/Go처럼 깔끔한 개발자 경험을 누릴 수 있다는 것이 핵심 포인트입니다.
----

# 마무리: uv가 열어줄 새로운 Python 생태계

- uv는 아직 출시된 지 1년 남짓밖에 안 되었지만, 성능과 사용성 모두에서 기존 파이썬 툴들과 확연히 차별화된 인상을 주며 급속도로 확산 중입니다.
- Python 생태계가 Rust나 Ruby, Go처럼 “툴 하나로 모든 것을 처리”한다는 문화를 받아들인다면, 오랫동안 지적되었던 ‘파편화’ 문제가 크게 해소될 것입니다.
- 아울러, uv는 오픈소스로 누구나 기여할 수 있고, Astral 팀과 커뮤니티가 긴밀히 협업하고 있습니다.
아직 도입을 망설이고 계시다면, 작은 프로젝트라도 시도해보시길 권합니다. 처음 세팅부터, 의존성 관리와 배포까지 확실한 편의성을 체감할 수 있을 겁니다.

### Reference : https://github.com/prrao87/uv-demo
