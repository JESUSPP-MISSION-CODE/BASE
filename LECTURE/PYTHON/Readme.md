
# 환경설정
## 1. Python 다운로드 설치
[python.org](https://www.python.org/downloads/) 에 접속하여 3.13.3 버전을 다운받아 설치 한다.
<img src="https://github.com/user-attachments/assets/bce0984a-a3a3-4afd-a376-53b4b34eb346"  width="800px" height="250px"></img>  
설치시 Add python.exe to PATH 를 체크하고 설치  
<img src="https://github.com/user-attachments/assets/2155217f-9572-4f39-a6a0-96f2e2163a14" width="550px" height="350px"></img>  
<br>
## 2. Visaul Studio Code 다운로드 및 설치
Python 개발 환경으로 가장 많이 쓰이는 프로그램이 Visual Studio Code와 PyCharm 입니다.  
동영상강의와 동일하게 진행하기 위해 Visual Studio Code로 설치합니다.
[Visual Studio Code download](https://code.visualstudio.com/) 에 접속하여 다운받아 설치한다.
![image](https://github.com/user-attachments/assets/f4ebb1e0-1dda-4a4e-a327-679e77de7e9c)
![image](https://github.com/user-attachments/assets/53197bf7-5c1d-4d20-8973-5ab44ad74eeb)
![image](https://github.com/user-attachments/assets/129ebde5-5274-4e2c-827d-94951fe9b7c1)


## 3. VS Code 실행, Python Extension 설치 
VS Code 실행후 왼쪽 아래 Extension icon을 클릭 > Python 을 선택하고 install 클릭
![image](https://github.com/user-attachments/assets/8ef54bb2-8c7e-402e-86c9-8314a58bb976)  
<br>
Extension icon을 클릭 > 입력창에 python env을 입력하고 Pythonn Environments install 클릭
![image](https://github.com/user-attachments/assets/f7e3adbe-9dc7-486c-88ec-e087f4cbf863)

## 4. project 생성

C 드라이브 하위에 jesuspp 라는 폴더를 만든다.  
VS Code 메뉴에서 File > Open Folder를 선택하고 위에서 생성한 jesuspp 폴더를 선택한다.  
Do you trust the authors of the files in this folder?  
화면이 나오면 YES 를 클릭한다.  
![image](https://github.com/user-attachments/assets/cdc7fbc2-841c-4c67-a426-3012bf6e8c43)
<br>  
EXPLOERE 화면에서 New File을 클릭하고 app.py 라는 파일을 생성한다.  
![image](https://github.com/user-attachments/assets/7b89baca-327b-454c-84ca-a359548fb09a)


## 5. venv설정
python 확장팩 아이콘을 누르고 ENVIRONMENT MANAGERS 를 클릭하고, venv 옆의 '+' 버튼을 누른다.  
![image](https://github.com/user-attachments/assets/65f30db7-4ecc-46bd-afe1-a45253cc9bdd)
<br>
메뉴 선택에서 Quick Create 를 선택한다.  
![image](https://github.com/user-attachments/assets/0828e69e-a452-4169-8461-3e7971ab3739)

## 6. powershell 관련 에러 발생시 관리자 모드 실행 설정
app.py 에 아무 code 나 작성하고 실행시 
```
& : 이 시스템에서 스크립트를 실행할 수 없으므로 C:\jesuspp\.venv\Scripts\Activate.ps1 파일을 로드할 수 없습니다.
```
라고 나오면 powershell의 실행 모드를 설정해 주어야 한다.  
<br>
검색에서 powershell을 검색하고 관리자모드로 실행을 한다.
![image](https://github.com/user-attachments/assets/47dc2d34-7501-4a4e-9fff-6ac70433c92a)
powershell 화면에 
```
Set-ExecutionPolicy RemoteSigned
```
라고 입력후 'Y' 를 선택해 준다.
![image](https://github.com/user-attachments/assets/40b580ab-8d3e-4745-ac91-b45036a6112f)
<br>
파일에 
```
print("aaa")
```
입력하고 실행 버튼 눌렀을때 아래와 같이 에러 없이 실행되면 환경설정은 다 된 것입니다.
![image](https://github.com/user-attachments/assets/661e293d-47de-4024-a08b-94b176064c4c)

## VS Code에서 Extention을 설치 했으나 Python Environments Icon이 나타나지 않는경우
https://github.com/microsoft/vscode-python-environments/issues/584
VS Code에서 Python Environments Extention을 설치하면 좌측 메뉴에 Python Icon이 나타나야 하는데 나타나지 않는경우 

Ctrl+Shift+P 버튼을 누르고 입력창에 다음 항목을 입력합니다.
```
python.useEnvironmentsExtension
```

아래와 같이 Enable the Python Environments Extension 앞의 check box를 켜줍니다. 
<img width="1028" height="472" alt="image" src="https://github.com/user-attachments/assets/557bcf68-d4da-4ff9-9029-a73f16461827" />
