# Pyinstaller
PyInstaller는 Python 스크립트를 독립실행 가능한 실행 파일로 변환해주는 도구입니다.   

## PyInstaller 설치
```
pip install pyinstaller
```

##기본 사용법
### 1. 기본 명령어
```
pyinstaller your_script.py
```
### 2. 주요 옵션들
- --onefile 또는 -F: 단일 실행 파일로 생성
- --windowed 또는 -w: 콘솔 창 없이 실행 (GUI 앱용)
- --noconsole: Windows에서 콘솔 창 숨김
