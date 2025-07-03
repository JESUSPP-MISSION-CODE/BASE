![image](https://github.com/JESUSPP-MISSION-CODE/BASE/blob/main/members/Sweetsalt25/ai_code_n8n/image/n8n-1.png)


## n8n 설치 가이드
n8n을 설치하는 방법은 여러 가지가 있지만, 가장 일반적인 방법은 Docker를 이용하는 것.  
Docker를 사용하면 n8n을 손쉽게 설치하고 관리할 수 있으며, 다양한 환경에서 일관된 성능을 보장할 수 있습니다.  

### Docker를 이용한 N8n 설치 방법
Docker를 이용하여 n8n을 설치하는 방법은 먼저 Docker를 설치한 후, n8n의 Docker 이미지를 다운로드하여 실행.  
1. Docker 설치: Docker가 설치되어 있지 않다면, [Docker 공식 웹사이트](https://www.docker.com/)에서 설치 파일을 다운로드하여 설치.  
==> 사내에서는 WSL 사용이 block됨  
2. Local환경에서 n8n 설치  
로컬 환경에서 n8n을 설치하려면 Node.js와 npm이 필요합니다. 다음은 로컬 환경에서 n8n을 설치하는 방법입니다.  
    1. Node.js 및 npm 설치: Node.js와 npm이 설치되어 있지 않다면, [Node.js 공식 웹사이트](https://nodejs.org/ko)에서 설치 파일을 다운로드하여 설치합니다.
![image](https://github.com/JESUSPP-MISSION-CODE/BASE/blob/main/members/Sweetsalt25/ai_code_n8n/image/n8n-2.png)
![image](https://github.com/JESUSPP-MISSION-CODE/BASE/blob/main/members/Sweetsalt25/ai_code_n8n/image/n8n-3.png)
    ```
    npm -v [ENTER]
    > 10.9.2
    ```

    3. n8n 설치: 터미널을 열고 다음 명령어를 입력하여 n8n을 설치합니다.
    ```
    npm install n8n -g
    ```
    위 명령어는 n8n을 전역적으로 설치합니다.
    ```
    C:\Windows\System32>npm install n8n -g
    npm error code UNABLE_TO_VERIFY_LEAF_SIGNATURE
    npm error errno UNABLE_TO_VERIFY_LEAF_SIGNATURE
    npm error request to https://registry.npmjs.org/n8n failed, reason: unable to verify the first certificate
    npm error A complete log of this run can be found in: C:\Users\twkwon\AppData\Local\npm-cache\_logs\2025-07-01T05_54_05_078Z-debug-0.log

    # 아래 명령어를 통하여 SSL 사용을 하지 않게끔 설정 변경 하면 됨
    npm config set strict-ssl false    

    C:\Windows\System32>npm install n8n -g
    npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and powerful.
    npm warn deprecated npmlog@6.0.2: This package is no longer supported.
    ...

    error command C:\Windows\system32\cmd.exe /d /s /c prebuild-install -r napi || node-gyp rebuild
    # 에러발생!!!
    npm config set cafile C:\DigitalCity.crt

    C:\Windows\System32>npm install n8n -g

    
    ```
    에러 발생시
    - Visual Studio 2019 C++ License 신청하여 설치  
    - Python 3.11 기준 설치

    ```
    pip install setuptools
    ```
    기존설치 n8n을 제거하고 재설치 하는경우

    ```
    npm cache clean --force
    npm uninstall -g n8n
    npm install -g n8n
    ```
    Initializeing n8n process에서 장시간 멈춰있는경우
    5678 port 사용여부 확인후 사용중이지 않은 port를 확인하고 그 번호로 변경하여 연결
    ```
    netstat -ano | findstr :5678
    > TCP    127.0.0.1:5678           0.0.0.0:0              LISTENING       4  > system에서 사용중
    netstat -ano | findstr :5679
    > TCP    127.0.0.1:5679           0.0.0.0:0              LISTENING       4  > system에서 사용중
    netstat -ano | findstr :5680
    > 아무것도 안나오면 빈 port 임
    set N8N_PORT=5680     > 임시 port설정
    setx N8N_PORT=5680    > system환경변수로 영구 설정
    ```
    

    3. n8n 실행: 설치가 완료되면 다음 명령어를 입력하여 n8n 서버를 실행합니다.  
    ```
    n8n
    ```
    4. n8n 웹 인터페이스 접속: 웹 브라우저를 열고 http://localhost:5678로 접속하여 n8n 웹 인터페이스에 접근합니다.
    5. 관리자 계정 등록  : n8n 웹 인터페이스에 처음 접속하면 관리자 계정을 등록해야 합니다. 관리자 계정을 등록하면 워크플로우를 생성하고 관리할 수 있습니다.  
![image](https://github.com/JESUSPP-MISSION-CODE/BASE/blob/main/members/Sweetsalt25/ai_code_n8n/image/n8n-4.png)
![image](https://github.com/JESUSPP-MISSION-CODE/BASE/blob/main/members/Sweetsalt25/ai_code_n8n/image/n8n-5.png)
![image](https://github.com/JESUSPP-MISSION-CODE/BASE/blob/main/members/Sweetsalt25/ai_code_n8n/image/n8n-6.png)
<br>

## n8n 개요와 특징
n8n은 시각적 인터페이스를 제공하여 사용자가 드래그 앤 드롭 방식으로 워크플로우를 설계할 수 있습니다.  
이를 통해 복잡한 코딩 없이도 다양한 애플리케이션과 서비스를 연결할 수 있습니다. 또한, n8n은 다음과 같은 특징을 가지고 있습니다:
<br>

- 오픈 소스: 무료로 사용 가능하며, 커뮤니티를 통해 지속적으로 업데이트됩니다.
- 다양한 노드 지원: 이메일, 데이터베이스, 웹 서비스 등 400개 이상의 노드를 제공합니다.
- 셀프 호스팅 가능: 클라우드 환경뿐만 아니라 로컬 서버에서도 운영할 수 있습니다.
- 보안 기능: OAuth 및 API 키를 통해 안전한 데이터 연동을 지원합니다.
<br>

## n8n 주요 기능
n8n은 사용자가 별도의 복잡한 프로그래밍 없이도 다양한 서비스와의 연동을 통해 자동화 워크플로우를 구성할 수 있도록 설계된 플랫폼입니다.   
이 도구의 가장 큰 특징은 오픈소스 기반이기 때문에 사용자들이 자유롭게 기능을 확장하고 커스터마이징할 수 있다는 점입니다.   
또한, 직관적인 UI와 드래그 앤 드롭 방식의 노드 연결 방식을 제공하여 누구나 쉽게 사용할 수 있습니다.  
<br>

n8n은 API 연동, 데이터 변환, 조건 분기 등의 기능을 지원하며, 이를 통해 다양한 업무 프로세스를 자동화할 수 있습니다.  
특히, n8n 사용법을 익히면 반복적인 업무를 줄이고, 오류 없이 자동으로 처리할 수 있는 시스템을 구축할 수 있어 많은 기업과 개인 사용자에게 인기를 얻고 있습니다.
<br>

- 시각적 플로우 빌더: 직관적인 인터페이스로 워크플로우를 설계할 수 있습니다.
- 다양한 노드: Gmail, Slack, Notion 등 다양한 애플리케이션과 통합 가능합니다.
- 데이터 변환 및 처리: 데이터를 필터링하거나 변환하는 기능을 제공합니다.
- 트리거 및 웹훅: 특정 이벤트 발생 시 워크플로우를 자동으로 실행할 수 있습니다.
- 에러 처리 및 디버깅: 오류 발생 시 알림을 보내거나 문제를 해결할 수 있는 기능을 제공합니다.
<br>

## 첫 워크플로우 생성하기
n8n에서 첫 워크플로우를 생성하려면, 먼저 새로운 워크플로우를 생성하고 필요한 노드를 추가해야 합니다.  
<br>

Create Workflow 버튼을 클릭하여 새로운 워크플로우를 생성 할 수 있습니다.  
워크플로우를 생성 할때는 직접 생성 할수도 있고 이미 만들어진 템플릿을 이용해서 생성 할 수 있습니다.
<br>

원하는 템플릿을 선택하여 클릭하면 아래와 같은 워크플로우가 생성됩니다.
n8n![image](https://github.com/JESUSPP-MISSION-CODE/BASE/blob/main/members/Sweetsalt25/ai_code_n8n/image/n8n-7.png)
<br>

각 노드는 특정 작업을 수행하며, 노드를 연결하여 원하는 자동화 프로세스를 설계할 수 있습니다. 예를 들어, 이메일을 자동으로 보내거나 데이터를 처리하는 등의 작업을 노드를 통해 구현할 수 있습니다.
<br>

## n8n을 활용한 업무 자동화 사례
n8n을 활용하면 다양한 업무를 자동화할 수 있습니다. 여기서는 이메일 자동화와 데이터 통합 및 보고서 생성 자동화 사례를 소개합니다.
<br>

### 이메일 자동화 워크플로우 만들기
이메일 자동화 워크플로우를 만들려면, 이메일 트리거 노드를 사용하여 특정 조건에 따라 이메일을 자동으로 보낼 수 있습니다. 예를 들어, 특정 시간에 정기적으로 이메일을 보내거나, 특정 이벤트가 발생했을 때 이메일을 발송하는 등의 작업을 자동화할 수 있습니다.
<br>


### 데이터 통합 및 보고서 생성 자동화
데이터 통합 및 보고서 생성 자동화는 n8n의 강력한 기능 중 하나입니다. 다양한 데이터 소스를 연결하여 데이터를 통합하고, 이를 기반으로 자동으로 보고서를 생성할 수 있습니다. 예를 들어, 여러 데이터베이스에서 데이터를 가져와 통합한 후, 이를 기반으로 주간 보고서를 자동으로 생성하는 워크플로우를 설계할 수 있습니다.
<br>

### N8n 사용 시 유용한 팁과 트릭
n8n을 효과적으로 사용하기 위해서는 몇 가지 유용한 팁과 트릭을 알아두는 것이 좋습니다.
<br>

#### 효율적인 워크플로우 설계 방법
효율적인 워크플로우를 설계하기 위해서는 먼저 전체 프로세스를 명확히 이해하고, 이를 기반으로 필요한 노드를 선택하여 설계해야 합니다. 또한, 워크플로우의 복잡성을 줄이기 위해 가능한 한 간단하고 직관적인 설계를 유지하는 것이 중요합니다.
<br>

#### 문제 해결 및 디버깅 팁
n8n을 사용하다 보면 예상치 못한 문제가 발생할 수 있습니다. 이때는 n8n의 디버깅 기능을 활용하여 문제를 해결할 수 있습니다. 각 노드의 실행 결과를 확인하고, 오류 메시지를 분석하여 문제의 원인을 파악할 수 있습니다.
<br>

## 마무리 하며
n8n을 통해 업무 자동화를 시작하는 방법을 요약하자면, 먼저 n8n을 설치하고 기본 사용법을 익힌 후, 실제 업무에 적용할 수 있는 워크플로우를 설계하는 것입니다. 이를 통해 반복적인 작업을 줄이고, 업무 효율성을 극대화할 수 있습니다.

# n8n Beginner Course
#### Automation : Definition 
```
"A predictable set of predetermined actions that transfers data from one  point to another"
```
#### Core concepts of automation
##### Trigger : what starts automation
- Manual
- Scheduled
    - Every min
    - Every day at 8 AM
    - Once a month at 4 PM 
- Applications
    - Webhook
    - Property update
    - From submission  
![image](https://github.com/JESUSPP-MISSION-CODE/BASE/blob/main/members/Sweetsalt25/ai_code_n8n/image/n8n-8.png)
<br>

##### Filtering : Filtering is used to allow or block certain types of data from following a path based on certain conditions

##### Actions (Apps) : Allow you to interact with applications
- Googlesheet
    - Create sheet / Get spreadsheet / Update rows
- Dropbox
    - Upload file / Get file / Create folder
- Slack
    - Get user / Send message / Get message
- salesforce
    - Get contact / Get company / Create lead

##### Mapping : Mapping is the first step to any good automation
Correctly mapping a process before automation will ensure you have visibility on the:
- Understanding of the task
- Tools that will be used
- Feasibility of the automation
- Estimation of work load
- (Sometimes) need for human intervention
<br>

Using a folowchart, list every different part of a process as a block and use arrows to link how these parts interact.
![image](https://github.com/JESUSPP-MISSION-CODE/BASE/blob/main/members/Sweetsalt25/ai_code_n8n/image/n8n-9.png)


  
  

