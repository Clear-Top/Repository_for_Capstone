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

# Flask 기반의 SR-LPR 어플리케이션 구현
Baseline모델은 LPSR-Recognition 구조를 Keras로 구현 및 훈련 진행
웹 디자인 + 모델 훈련 + 나온 결과를 통해 추가적인 기능 구현을 최우선 목표로 진행

# Input [Image,Video] 에 따라 다르게 구현해야하는지 의문.
SISR을 이용하여 의도적인 Down Sampling을 통한 모델 훈련, SRGAN을 사용해보는것도 괜찮아보임.

# Dataset
https://sejonguniversity-my.sharepoint.com/personal/minhdl_sju_ac_kr/_layouts/15/onedrive.aspx?originalPath=aHR0cHM6Ly9zZWpvbmd1bml2ZXJzaXR5LW15LnNoYXJlcG9pbnQuY29tLzpmOi9nL3BlcnNvbmFsL21pbmhkbF9zanVfYWNfa3IvRXJSTXE4MjNWbkJLdlNrbHB0bjJXYklCLUp4TDdwS3QzaE91aVk4RTNvV2tyUT9ydGltZT1iNXlXOVNMNDJFZw&id=%2Fpersonal%2Fminhdl%5Fsju%5Fac%5Fkr%2FDocuments%2Fradish%20project%20dataset%2FCapstone%5Fdataset%2Flicense%20plate%20dataset <br/>

