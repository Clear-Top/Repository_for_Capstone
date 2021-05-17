#Capstone_Design
https://github.com/brightyoun/LPSR-Recognition 참조 <br/>
https://github.com/apoorva-dave/LicensePlateDetector-deployment-flask 참조 <br/>
http://pr.gachon.ac.kr/ALPR.html <br/>
http://blog.naver.com/PostView.nhn?blogId=sogangori&logNo=221093668692&parentCategoryNo=&categoryNo=6&viewDate=&isShowPopularPosts=false&from=postView <br/>
https://github.com/azizsiyaev/korean_car_licence_plate_detection_and_recognition <br/>

#훈련용 <br/>
https://www.youtube.com/watch?v=mmj3nxGT2YQ [참조] <br/>
https://colab.research.google.com/drive/1_GdoqCJWXsChrOiY8sZMr_zbr_fH-0Fg?usp=sharing [참조] <br/>
https://morioh.com/p/696345dcfa49 <br/>


<br />
<br />
#pretrained model for lpd + car detection<br />
<a href='https://drive.google.com/uc?export=download&id=1NcJtEwboqtQ9u27lerYOqS3kUrg6cGKv'>yolov4_cfg</a> <br /><br />
<a href='https://drive.google.com/uc?export=download&id=1a-Nkl7Hc4Lx27L72qaBZFmkbcIyEcQvA'>yolov4_weights</a> <br/><br/>

# Flask 기반의 SR-LPR 어플리케이션 구현
Baseline모델은 LPSR-Recognition 구조를 Keras로 구현 및 훈련 진행
웹 디자인 + 모델 훈련 + 나온 결과를 통해 추가적인 기능 구현을 최우선 목표로 진행

# Input [Image,Video] 에 따라 다르게 구현해야하는지 의문.
SISR을 이용하여 의도적인 Down Sampling을 통한 모델 훈련, SRGAN을 사용해보는것도 괜찮아보임.

# Dataset
https://sejonguniversity-my.sharepoint.com/personal/minhdl_sju_ac_kr/_layouts/15/onedrive.aspx?originalPath=aHR0cHM6Ly9zZWpvbmd1bml2ZXJzaXR5LW15LnNoYXJlcG9pbnQuY29tLzpmOi9nL3BlcnNvbmFsL21pbmhkbF9zanVfYWNfa3IvRXJSTXE4MjNWbkJLdlNrbHB0bjJXYklCLUp4TDdwS3QzaE91aVk4RTNvV2tyUT9ydGltZT1iNXlXOVNMNDJFZw&id=%2Fpersonal%2Fminhdl%5Fsju%5Fac%5Fkr%2FDocuments%2Fradish%20project%20dataset%2FCapstone%5Fdataset%2Flicense%20plate%20dataset <br/>

* * *
```
작성일 : 2021/05/18(월) 01:00
```
# About UX/UI Design
> Flask 상에서 index.html 파일을 **"main_page.html"** 로 대체할 예정.
> 현재 추론을 실행하고 리스트조회가 가능한 HTML의 틀만 완성된 상태.
> 맵조회 관련페이지 디자인이 끝나가고 있기때문에, 서둘러서 작업할 예정.
> 나머지 디자인은 천천히 시간을 두고 작업할 예정

> ## 작업예정 (main_page.html)
- ~~맵조회부분에서 **차량검색**을 통해 DB에서부터 불러온 "차량번호"를 통해, 버튼컴포넌트 제작예정~~
- 차량번호마다 Marker(인스턴스)의 색깔을 다르게 구현예정
- 지역 or 구역 or 개수제한  에 따라 클러스터링 구현예정
- ~~**리스트조회부분**에서 사진을 넣을 DisplayBox 부분과 결과를 반환받을 DisplayBox를 각각 구현할 예정~~
- ~~버튼에 기능도 삽입할 예정~~
- ~~전체차량 조회 기능추가~~
- ~~전체차량 버튼에서 원하는 차량번호로 자동스크롤 및 Blink기능 추가~~
- 맵 API에게 차량번호 + 위도 + 경도 정보전달
- 메인페이지 오른쪽아랫부분에 **Remote Controller** 만들기


> ## 문제점 (mapPage.html)
- Marker의 **색깔변경 불가능** => <u>색깔대신 다른 망안 검토중</u>
- 차량검색 직후 DB에서 차량번호를 뽑아옴 (1개 or 전체) 그러나, 인스턴스조회 시에 **DB에 다시 접근** 해야만 한다. => <u>애초에 모든정보를 데려올까???</u>
