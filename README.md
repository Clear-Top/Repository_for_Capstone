#Capstone_Design





#훈련용 <br/>




#주의
본 repo는 2021/06/11일 기점으로 public 으로 전환될 예정입니다.<br/>

<br />
<br />
#pretrained model for lpd + car detection<br />
<a href='https://drive.google.com/uc?export=download&id=1NcJtEwboqtQ9u27lerYOqS3kUrg6cGKv'>yolov4_cfg</a> <br /><br />
<a href='https://drive.google.com/uc?export=download&id=1a-Nkl7Hc4Lx27L72qaBZFmkbcIyEcQvA'>yolov4_weights</a> <br/><br/>

# Dataset

* * *
```
작성일 : 2021/05/24(월) 03:58
```
# About UX/UI Design
> Flask 상에서 index.html 파일을 **"main_page.html"** 로 대체할 예정.
> 현재 추론을 실행하고 리스트조회가 가능한 HTML의 틀만 완성된 상태.
> 맵조회 관련페이지 디자인이 끝나가고 있기때문에, 서둘러서 작업할 예정.
> 나머지 디자인은 천천히 시간을 두고 작업할 예정

> ## 작업예정 (main_page.html)
- ~~맵조회부분에서 **차량검색**을 통해 DB에서부터 불러온 "차량번호"를 통해, 버튼컴포넌트 제작예정~~
- ~~차량번호마다 Marker(인스턴스)의 색깔을 다르게 구현예정~~
- ~~**리스트조회부분**에서 사진을 넣을 DisplayBox 부분과 결과를 반환받을 DisplayBox를 각각 구현할 예정~~
- ~~버튼에 기능도 삽입할 예정~~
- ~~전체차량 조회 기능추가~~
- ~~전체차량 버튼에서 원하는 차량번호로 자동스크롤 및 Blink기능 추가~~
- ~~맵 API에게 차량번호 + 위도 + 경도 정보전달~~
- ~~버튼을 모던하게 디자인~~
- ~~Marker에 Over, Out, Click 시에 다른 이미지 오버래핑~~

- 메인페이지 오른쪽아랫부분에 **Remote Controller** 만들기
- "Marker 클릭 -> (인스턴스조회 실행) -> sql질의" 기능입히기
> ## 지역 or 구역 or 개수제한  에 따라 클러스터링 구현예정
> ## Dynamic View Pointing 구현예정
> ## 시간별로 정렬된 리스트뷰 구현예정


> ## 문제점 (mapPage.html)
- ~~Marker의 **색깔변경 불가능** => <u>색깔대신 다른 망안 검토중</u>~~
- ~~차량검색 직후 DB에서 차량번호를 뽑아옴 (1개 or 전체) 그러나, 인스턴스조회 시에 **DB에 다시 접근** 해야만 한다. => 애초에 모든정보를 데려올까???~~
- ~~리버스지오코딩의 연산시간과 마우스이벤트간의 동기화문제로 인해 인포창이 멈추는 현상발생 => 비동기식구현으로 해결완료~~
