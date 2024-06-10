## 📃카카오톡 대화 요약 머신
<hr>
사용 목적: 읽은 대화 중 재확인 해야할 내용이 많이 있을때

![img.png](assets%2Fimg.png)
![img_3.png](assets%2Fimg_3.png)
![img_4.png](assets%2Fimg_4.png)
![img_1.png](assets%2Fimg_1.png)
![img.png](img.png)
**Requirement**
1. Openai api key <br>
2. gmail <br>
3. gmail password
<hr>

**Gmail 앱 비밀번호 설정하기**
1. 구글 보안 2단계 인증
2. 구글 계정 페이지 → 앱 비밀번호 → 앱 비밀번호 만들기 
3. Gmail 설정(오른쪽 상단) → 모든 설정 보기
4. 전달 및 POP/IMAP → IMAP 사용 체크 → 변경사항 저장
<hr>

**.env 파일 생성하기** <br>
OPENAI_API_KEY = 'your_api_key' <br>
EMAIL = 'your_email_address' <br>
PWD = 'your_gmail_app_password' 

**views**
your_email_address 에 자신이 사용할 이메일 넣기 
1. email = 'FROM "your_email_address"'
