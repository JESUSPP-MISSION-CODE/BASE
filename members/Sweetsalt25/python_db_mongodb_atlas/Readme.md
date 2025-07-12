# python DB - MongoDB Atlas

MongoDB: 가장 많이 활용되고 있는 NoSQL DB  
<br>
딕셔너리(파이썬), JSON 형태와 동일한 구조를 가짐 : {Key:Value}  

## MongoDB 사용방식
- 내 컴퓨터에 설치 : localhost로만 사용
- 크라우드 서비스를 이용 : web에서 자유로이 서비스

## MongoDB Atlas (클라우드 무료버전) 설치하기
- MongoDB Atlas 무료버전 제한사항 : DB용량 512MB
- URL : https://www.mongodb.com/ko-kr/products/platform/atlas-database  

- Google계정으로 가입후 좌측메뉴에서 Cluster > Build a cluster 를 클릭한다.  
Region 에서 Seoul을 선택한다 .  
DB에 접근권한을 가지는 user의 id/pw를 설정해 준다. 

- Connection configuration  
    - Drivers : Node.js, Go 등에서 access
    - Compass : Local PC에 Compass라는 app을 설치하고 이를 통해 atlas의 Data를 조회/조작할수있다 (반드시 설치를 권장) 
    - Shell :
    - MongoDB VS Code : 

- Compass를 설치하고 connection url 을 기록해 둔다.
```
mongodb+srv://twkwon7300:<db_password>@cluster0.3r7vlij.mongodb.net/
```
- DB가 생성되고 나면 Security option을 확인해 본다.
    - Database Access : 본인계정이 등록되어 있어야 한다.
    - Network Access : DB생성시 접속한 본인 IP address 1개가 등록되어 있다.  
    DB에 접근할수 있는 IP를 설정하려면 +ADD IP ADDRESS 를 클릭하고 ALLOW ACCESS FROM ANYWHERE를 클릭한다.   

## DB에 접속하기
- Compass App을 실행한다. 
- Add new connection을 클릭하고 URI에 위에 복사해둔 내용을 넣어준다.  
이 때 pw 부분을 Database Access권한에 입력되어 있전 계정의 pw로 입력해 준다.
- 접속 userid를 입력하고 SAVE를 누른다. 
- 생성된 connection에서 CONNECT를 눌러서 정상접속되면 admin, local, sample_mlfix 등의 하위 메뉴가 나타난다
