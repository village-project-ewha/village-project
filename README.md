<h1>
  <img src="/static/resource/Logo/006-1.png" width="100" style="vertical-align: middle;">
</h1>
이화여대 물품 대여 및 판매 플랫폼 빌리지(Village)입니다.  

## 1. 만든이 CodeVilly
| 이름      | 역할               |
| ------- | ---------------- |
| **김미리** | 팀장 · 프론트엔드 |
| **신지민** | 프론트엔드         |
| **박린**  | 백엔드           |
| **이영윤** | 백엔드           |
| **김예교** | 디자인           |

## 2. 주요 기능

### ① 사용자 등록 및 관리  
- 회원가입  
- 로그인  
- 로그아웃  
- 내 거래 내역 확인  

### ② 상품 관련 기능  
- 전체 상품 조회  
- 상품 상세 조회  
- 상품 대여 및 구매  
- 상품 등록  
- 위시리스트(좋아요)에 상품 추가  
- 내 위시리스트 조회  

### ③ 리뷰 기능  
- 전체 리뷰 조회  
- 리뷰 상세 조회  
- 내가 거래한 상품 선택 후 리뷰 작성  

### ④ 구해 드림 (요청 게시판)  
- 필요한 상품을 찾는 글 게시  
- 게시글에 댓글 작성

## 3. 디렉토리 구조
```
village-project/
├── LICENSE
│
├── app.py
├── database.py
│
├── authentication/
│   └── firebase_auth.json
│
├── static/
│   ├── css/
│   ├── images/
│   ├── js/
│   └── resource/
│
└── templates/
    ├── detail.html
    ├── heart_list.html
    ├── home.html
    ├── index.html
    ├── login.html
    ├── product_detail.html
    ├── products.html
    ├── reg_items.html
    ├── reg_reviews.html
    ├── request_board.html
    ├── request_view.html
    ├── request_write.html
    ├── result.html
    ├── review_detail.html
    ├── review.html
    ├── select_review.html
    ├── signup.html
    ├── transactions.html
    └── view_review_detail.html
```


## 4. 개발 환경

### **디자인**
<p align="left">
  <img src="https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white"/>
</p>

### **프론트엔드**

<p align="left">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"/>
</p>

### **백엔드**

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/Anaconda-44A833?style=for-the-badge&logo=anaconda&logoColor=white"/>
</p>

### **Database / Infra**

<p align="left">
  <img src="https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black"/>
  <img src="https://img.shields.io/badge/Realtime%20DB-039BE5?style=for-the-badge&logo=firebase&logoColor=white"/>
</p>

## 5. 기타 url
**기술블로그** >> https://velog.io/@mill2kko/series/2025-2-osp

