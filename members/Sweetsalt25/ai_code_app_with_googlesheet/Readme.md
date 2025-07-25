# AI Coding + Google Sheet 로 10분만에 Web App만들기

주의사항 : 아래 과정을 진행시 Google 계정에 여러개의 계정이 로그인되어 있지 않고 대표계정 하나만 로그인 되어 있어야 합니다.
<br>
# 1. 🔑Google AI Studio에서 API key발급받기
 https://aistudio.google.com 접속 → Get API Key 클릭 → Create API Key 클릭 → Key가 생성되면 복사해서 적어두기
<br>

![image](https://github.com/user-attachments/assets/3c4ff68b-90d2-48c3-8fe2-ce30e06e0edb)
<br>

![image](https://github.com/user-attachments/assets/ac3a0ecd-95ee-406f-b929-3b26c0ef7f8e)
<br>

![image](https://github.com/user-attachments/assets/22e27195-3d40-4fd6-b901-bd550caa2dda)
<br>

# 2. 🧭Claude ai 접속하여 로그인 하기
https://claude.ai/login  에 접속하여 로그인을 한다.
![image](https://github.com/user-attachments/assets/9c3b8300-735a-4c75-b14e-03a44dbb60b9)
<br>

# 3. Claude Prompt - 앱과 연동할 구글시트 및 화면 인터페이스 🪟 구성하기 
나의 말:
```
자, 너는 지금부터 지상 최고의 구글 Apps Sciprt 웹 앱 개발자다!
이번에 새로운 프로젝트로 "해외 여행 가이드 앱"을 만들려고 해.
앱 주요 기능과 사용자 흐름은 다음과 같아.

== [앱 주요 기능] 시작 ==
1. 사용자가 여행할 나라나 지역 또는 도시를 입력하고, 인원수(혼자가는지, 여러병이 가는지), 성별, 나이, 여행 스타일, 여행일수, 예산규모 등을 선택하면
구글 Gemini API를 사용해서 여행경로와 일정을 추천해주는 웹 앱을 만들고 싶어.
2. 이 앱은 1회성으로 쓰는 앱이야. 웹 앱 화면에 결과 히스토리를 표시할 필요는 없어.
3. 다만 내부 관리용으로, 출력 결과는 구글 시트에 자동으로 기록.
== [앱 주요 기능] 끝 ==

== [사용자 흐름] 시작 ==
1. 사용자가 여행할 나라, 지역 또는 도시를 선택. 이것은 일반 텍스트상지로 자유롭게 입력하고독 함
2. 인원수, 성별, 나이, 여행스타일(휴양지, 커플여행, 한 가족여행(4인이내), 대규모 가족여행(12인 이상)), 여행일수(1일~7일까지), 예산규모(백만원/인당, 2백만원/인당) 등등을 선택
3. [여행경로 및 일정 추천] 버튼을 클릭하면 각 일자별 추천 일정과 경로흫 출력
== [사용자 흐름] 끝 ==

데이터는 구글 시트에서 "기록" 시트 하나로 관리할 거야.
위와 같이 만들려면, 구글 시트의 필드와 화면 인터페이스는 어떻게 구성하면 좋을까?
머리글 순번으로 간략하게 알려줘.
```
<br>

Claude 답변:  답변생성중 무료버전의 응답길이 제한으로 [계속] 버튼이 나오고 멈추는경우 버튼을 눌러준다.
```
구글 시트 "기록" 시트의 필드 구성과 화면 인터페이스를 다음과 같이 제안합니다:
구글 시트 "기록" 시트 필드 구성

타임스탬프 - 요청 일시
여행지 - 사용자가 입력한 나라/지역/도시
인원수 - 여행 참가자 수
성별 - 남성/여성/혼성
나이대 - 20대/30대/40대/50대 이상
여행스타일 - 휴양지/커플여행/가족여행(4인이내)/대규모가족여행(12인이상)
여행일수 - 1일~7일
예산규모 - 백만원/인당, 2백만원/인당
추천결과 - Gemini API 응답 내용 (긴 텍스트)
사용자IP - 접속자 식별용 (선택사항)

웹 앱 화면 인터페이스 구성

제목 영역 - "해외 여행 가이드 앱"
여행지 입력 - 텍스트 입력창 (placeholder: "예: 일본 도쿄, 프랑스 파리")
인원수 선택 - 드롭다운 (1명~12명 이상)
성별 선택 - 라디오 버튼 (남성/여성/혼성)
나이대 선택 - 드롭다운 (20대/30대/40대/50대 이상)
여행스타일 선택 - 드롭다운 (4가지 옵션)
여행일수 선택 - 드롭다운 (1일~7일)
예산규모 선택 - 라디오 버튼 (백만원/2백만원 인당)
추천 버튼 - "여행경로 및 일정 추천" 버튼
결과 표시 영역 - 일자별 추천 일정 출력 구역
로딩 표시 - API 호출 중 로딩 스피너

이런 구조로 하면 사용자 경험도 좋고 데이터 관리도 체계적으로 할 수 있을 것 같습니다!
```
본인의 Google spreadsheet에서 빈 Spreadsheet 를 생성하고 Claude가 추천한 column명을 입력한다. (사용자IP는 제외)  

![image](https://github.com/user-attachments/assets/7c40a758-f043-4b7e-ba3b-c59f292b84e7)

# 4. 💻App동작에 사용할 Gemini API model선택 및 App 제작시 필요한 code 작성하기

Google Gemini AI model은 다음과 같은 모델이 있다.   
https://ai.google.dev/gemini-api/docs/models?hl=ko#model-versions

| model | |
|--|--|
|2.5 Pro|쵀대 응답정확도와  최첨단 성능을 갖춘 가장 강력한 사고모델|
2.5 Flash|가성비가 가장우수하며 다양한 기능을 제공하는 모델|
|2.0 Flash|차세대 기능과 향샹된 기능을 갖춘 최신 멀티모달 모델|
<br>

App code작성에 필요한 prompt 를 완성한다.  


나의 말:
```
좋아. 너가 알려준 대로 아래와 같이 구성했어.
웹 앱 개발을 시작해보자. code.gs 와 index.html 코드를 각각 작성해줘.

== [백엔드 구성] 시작 ===
1. 사용할 외부 API
- Gemini API : [위에서 생성한 본인의 API Key]
- 모델은 Gemini 1.5 Flash 를 사용할거야.  <- 본인이 사용할 모델을 명시한다. 무료에서 가장빠른모델로 선정.

2. 구글 시트 구조
- 구글시트 ID : https://docs.google.com/spreadsheets/d/1BS8dcR1a-7ciF6Wot0RHd0q849aFaTPhPOYPuyVzU5M/edit?gid=0#gid=0
- 시트명 : 출력결과    <- sheet1 을 renmae해서 쓴다.
- 필드 구조 : "타임스탬프	여행지	인원수	성별	나이대	여행스타일	여행일수	예산규모	추천결과"
== [백엔드 구성] 끝 ===

== [화면 인터페이스 구성] 시작 ==  <- 이전에 Claude가 답변했던 것 그대로 입력
1. 제목 영역 - "해외 여행 가이드 앱"
2. 여행지 입력 - 텍스트 입력창 (placeholder: "예: 일본 도쿄, 프랑스 파리")
3. 인원수 선택 - 드롭다운 (1명~12명 이상)
4. 성별 선택 - 라디오 버튼 (남성/여성/혼성)
5. 나이대 선택 - 드롭다운 (20대/30대/40대/50대 이상)
6. 여행스타일 선택 - 드롭다운 (솔로여행, 휴양여행, 커플여행, 부부여행, 한 가족여행, 대가족 여행, 비즈니스 출장)
7. 여행일수 선택 - 드롭다운 (1일~7일)
8. 예산규모 선택 - 라디오 버튼 (50만원/백만원/2백만원 인당)
9. 추천 버튼 - "여행경로 및 일정 추천" 버튼
10. 결과 표시 영역 - 일자별 추천 일정 출력 구역
11. 로딩 표시 - API 호출 중 로딩 스피너
== [화면 인터페이스 구성] 끝 ==

== [추가 요청] 시작 ==
- 모든 개발은 구글 Apps Script + HTML/CSS/JS 로 진행할거야.
- 최신 트렌드에 맞춰서 세련되고 시원한 여름느낌이 물씬 나는 상큼하고, 접속했을때 행복한 감정이 드는 디자인으로 꾸며줘.
- 모바일에 대응할 수 있도록 반응형 CSS로 작성해.
== [추가 요청] 끝 ==

```
 
Claude 답변:
```
해외 여행 가이드 앱을 위한 코드를 작성해드리겠습니다!
<br>
code.gs - Google Apps Script 백엔드코드 // Google Apps Script 백엔드 코드 (code.gs)
<br>
const GEMINI_API_KEY = 'AIzaSyBaCcNgPOu6P-5ahJ5U-kuuf0UO6UhQp8Y';
const SPREADSHEET_ID = '1BS8dcR1a-7ciF6Wot0RHd0q849aFaTPhPOYPuyVzU5M';
const SHEET_NAME = '출력결과';
<br>
function doGet() {
  return HtmlService.creatindex.html - 해외 여행 가이드 앱 UI대화형 아티팩트 완성했습니다! 🎉
<br>
코드 설명
code.gs (백엔드)
<br>
Gemini API 연동: 1.5 Flash 모델을 사용하여 여행 추천 생성
구글 시트 연동: 모든 요청과 결과를 자동으로 기록
에러 처리: API 호출 실패 시 적절한 오류 메시지 반환
프롬프트 최적화: 일정별로 구체적인 추천을 받도록 구성
<br>
index.html (프론트엔드)
<br>
트렌디한 디자인: 그라데이션과 글래스모피즘 효과로 현대적인 느낌
여름 상큼 테마: 파란색-보라색 그라데이션으로 시원한 느낌
완전 반응형: 모바일, 태블릿, 데스크톱 모든 기기에 최적화
부드러운 애니메이션: 폼 요소들이 순차적으로 나타나는 효과
직관적인 UX: 로딩 스피너, 에러 처리, 결과 표시까지 완벽 구현
<br>
설정 방법
<br>
Google Apps Script 프로젝트 생성
code.gs 파일에 백엔드 코드 붙여넣기
index.html 파일 생성 후 프론트엔드 코드 붙여넣기
웹 앱으로 배포 (모든 사용자 액세스 허용)
구글 시트에 "출력결과" 시트가 자동으로 생성됩니다
<br>
API 키와 시트 ID는 이미 설정되어 있으니 바로 사용 가능합니다! 혹시 추가 수정이나 기능이 필요하시면 말씀해 주세요! 🚀
```
![image](https://github.com/user-attachments/assets/2f79aa4e-2ffb-4a76-b199-63ee52a82e2f)
<br>

두 개의 결과물 파일이 만들어진다. 

# 5. 완성된 code를 Apps Script로 옮기기
위에서 생성해둔 Googlesheet로 와서 중간의 "확장 프로그램" -> "Apps Script"를 선책한다.

![image](https://github.com/user-attachments/assets/e76150c4-144a-4887-94e5-3777b02337a6)
<br>

![image](https://github.com/user-attachments/assets/14fbe9a6-7665-4d2a-b039-4f9894b74f44)
<br>

Apps Script 의 project명을 "스마트 여행가이드 앱 프로젝트" 라고 변경하고, claude의 산출물에서 code.gs 를 클릭하여 우측 상단의 "복사" 를 클릭  
Apps Script 의 project의 code.gs의 기본 내용은 삭제하고 붙여넣기를 한다. 
<br>
![image](https://github.com/user-attachments/assets/22b7927f-282a-4b35-bf68-40d6185c45f3)

Apps Script 의 project의 파일 + 버튼을 클릭하고 HTML을 선택한다.
![image](https://github.com/user-attachments/assets/4ed76a4e-343d-4cf4-a13d-96576707c24a)
<br>

파일명은 index 라고 입력하고 엔터를 치면 index.html 파일이 추가된다. 기본 내용은 삭제하고, Claude가 생성한 index.html 내용을 붙여 넣는다.
![image](https://github.com/user-attachments/assets/351d8267-3e6c-4eb3-ad70-88bdb8ffd497)

# 여기까지 하면 App의 개발은 다 끝난것!!!!!!😂

# 6. 배포하기
Apps Script에서 Deploy > New Deployment   
![image](https://github.com/user-attachments/assets/5460afc5-25fe-4f7b-820b-f9764fa84ab4)
<br>

New Deployment type 에서 설정 아이콘을 클릭하고 "Web App"을 선택한다.    
설명에 "스마트 여행가이드 앱 V1"   
인증정보 : 작성자 본인  
사용자: Google 계정이 있는 사용자 또는 모든사용자   
로 설정한다.  
<br>
<br>
😒단! 모든사용자로 할 경우 API사용 한도제한이나 과다 비용이 청구될 수 있다.!!  
<br>  

![image](https://github.com/user-attachments/assets/941807f8-7d80-474a-996b-0d823a6a45ed)
<br>

배포를 누르면 Authorize Access 가 나오는데 이것을 클릭하고   
![image](https://github.com/user-attachments/assets/7b554ac6-9db1-446e-8066-b56bedc712ca)
<br>

본인 Google계정을 선택하고  
![image](https://github.com/user-attachments/assets/11102fae-ab46-4399-8855-8d43ccf30e50)  
<br>

Advanced 를 선책하고  
![image](https://github.com/user-attachments/assets/294ee91d-7d5a-4c6c-9b24-bfa5e9eaac54)
<br>

본인이 생성한 App 이름을 클릭하고  
![image](https://github.com/user-attachments/assets/abdd9b3d-ba58-463c-8fc4-f7808cf2db2d)
<br>

Allow 를 클릭해 접근 권한을 승인해 준다.  
![image](https://github.com/user-attachments/assets/46e035c0-971b-41b8-b3fc-3cb9a8f4b360)
<br>

그러면 App의 배포가 완료된다.  
![image](https://github.com/user-attachments/assets/de928eae-b918-4f00-8cea-eaffb1159cb1)
<br>
Web App의 URL을 복사해서 핸드폰이나 PC에서 아무 브라우저에서 URL에 들어가면 App 이 실행된다
<br>

# 7. 부분 개선하기
나의 말:  
```
동작은 잘 되는데 응답결과가 markdown으로 출력되고 있어. markdown 형식이 아닌 보기좋은 문서 형식으로 출력하고 싶어. 지금부터 지구 최고의 Google Apps Script 개발자 이자 UI/UX 전문가로서 사용자 친화적이고 보기 좋은 결과를 출력하도록 코드를 수정해줘
```

Claude 응답:  
```
마크다운을 예쁜 HTML 형식으로 변환하여 출력하도록 코드를 수정해드리겠습니다!index.html - 해외 여행 가이드 앱 UI대화형 아티팩트 ∙ 버전 2 index.html - 해외 여행 가이드 앱 UI대화형 아티팩트 ∙ 버전 3 code.gs - Google Apps Script 백엔드코드 ∙ 버전 2 function generatePrompt(formData) {
  const { destination, people, gender, age, style, days, budget } = formData;
  
  return `당신은 전문 여행 가이드입니다. 다음 정보를 바탕으로 상세한 여행 일정을 추천해주세요.

여행 정보:
- 여행지: ${destination}
- 인원수: ${people}
- 성별: ${gender}
- 나이대: ${agcode.gs - Google Apps Script 백엔드코드 ∙ 버전 3 function generateDayTemplate(days) {
  let template = '';
  for (let i = 1; i <= days; i++) {
    template += `
📅 **${i}일차**
- 오전 (09:00-12:00): 구체적인 장소와 활동
- 점심 (12:00-13:00): 추천 식당과 메뉴
- 오후 (13:00-17:00): 주요 관광지와 체험 활동
- 저녁 (17:00-19:00): 석식 장소와 분완벽하게 수정했습니다! 🎨✨
주요 개선사항
1. 마크다운 → 아름다운 HTML 변환

formatMarkdownToHTML() 함수: 마크다운을 시각적으로 멋진 HTML로 변환
구조화된 레이아웃: 각 섹션별로 다른 배경색과 스타일 적용
이모지 제목: 🌟📍📅💰✈️ 등의 이모지가 포함된 제목들을 예쁘게 스타일링

2. 섹션별 차별화된 디자인

📍 여행 개요: 일반 섹션 스타일
📅 일차별 계획: 투명한 배경의 카드 형태
💰 예산 가이드: 빨강-청록 그라데이션 배경
✈️ 여행 팁: 파랑-보라 그라데이션 배경

3. 인터랙티브 요소

호버 효과: 리스트 항목에 마우스를 올리면 살짝 이동
글래스모피즘: 반투명 배경과 블러 효과
그라데이션 테두리: 각 섹션마다 아름다운 테두리 효과

4. 백엔드 프롬프트 개선

더 상세한 템플릿: 시간대별 구체적인 일정 요청
체계적인 예산 가이드: 항목별 세분화된 비용 정보
실용적인 팁: 구체적이고 유용한 여행 정보 제공

5. 사용자 경험 최적화

읽기 쉬운 타이포그래피: 적절한 행간과 글꼴 크기
시각적 계층구조: 제목-부제목-내용의 명확한 구분
색상 대비: 가독성을 위한 최적화된 색상 조합

이제 마크다운 텍스트가 아닌 아름답고 구조화된 여행 가이드가 출력됩니다! 각 섹션이 시각적으로 구분되고, 호버 효과와 그라데이션으로 더욱 매력적인 결과물을 확인할 수 있습니다. 🚀
```
# 8. 수정배포 하기
새로 생성된 code.gs 과 index.html로 변경하고,   Deploy -> Test Deployment 를 선택한다.  
생성된 TEST용 URL에 접속해 동작을 확인한다.  
<br>
확인이 다 되었으면 Deploy -> Manage deployment -> 편집 -> 버전명 변경 -> Deploy

![image](https://github.com/user-attachments/assets/adf65fda-d062-4594-b779-6810d89d5936)
<br>

# 9. URL 단축 서비스 이용

이렇게 만들어진 App은 접근을 위한 link의 길이가 매우 길어서 사용시나 link 공유가 신경이 쓰이게 되는데, 이 경우 URL 단축서비스를 사용하면 된다.  
<br>

대표적인 URL 단축서비스는 다음과 같은것이 있다.
- https://url.kr/ : 무료plan (하루 5000회 click, domain 유지 기간 3년, 로그인 필요 없음)
- https://bitly.com/ : 무료 plan ( 무제한 click, URL link 관리, Google계정 사용, 무료버전은 광고표시됨 )







Reference 
- https://www.youtube.com/watch?v=vCMYu2T5B4c&t=324s
- https://www.oppadu.com/ai-apps-script-10min/
