# Pyinstaller
PyInstaller는 Python 스크립트를 독립실행 가능한 실행 파일로 변환해주는 도구입니다.   

## PyInstaller 설치
```
pip install pyinstaller
```

## 기본 사용법
### 1. 기본 명령어
```
pyinstaller your_script.py
```
### 2. 주요 옵션들
- --onefile 또는 -F: 단일 실행 파일로 생성
- --windowed 또는 -w: 콘솔 창 없이 실행 (GUI 앱용)
- --noconsole: Windows에서 콘솔 창 숨김
- --icon=icon.ico: 아이콘 지정
- --name=app_name: 실행 파일 이름 지정
- --add-data: 추가 데이터 파일 포함
- --hidden-import: 숨겨진 import 모듈 지정

### 3. 자주 사용하는 명령어 조합
```bash
# 단일 파일로 생성
pyinstaller --onefile script.py

# GUI 앱 (콘솔 창 없음)
pyinstaller --onefile --windowed script.py

# 아이콘 포함
pyinstaller --onefile --windowed --icon=app.ico script.py
```

### 4. 문제 해결 팁
일반적인 문제들:
- ModuleNotFoundError: --hidden-import 옵션 사용
- 파일 크기가 큰 경우: --exclude-module로 불필요한 모듈 제외
- 백신이 차단하는 경우: 코드 서명 또는 백신 예외 등록
- 느린 시작: --onedir 옵션 고려 (여러 파일로 분산)



