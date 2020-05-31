# Wisely 프로젝트 소개 BackEnd

국내 프리미엄 면도 구독 서비스 [와이즐리 Wisely](https://www.wiselyshave.com/) clone project 

<br>

## 개발 인원 및  기간

- 기간 : 2주(5월 11일 ~ 5월 22일)
- 인원 : 프론트엔드 [SSimple Key](https://github.com/skh417), [youngmi14](https://github.com/youngmi14), [Ju-sangha](https://github.com/sangha-ju) 백엔드 [Jeonginbak](https://github.com/Jeonginbak), [sungjun-jin](https://github.com/sungjun-jin)
- [프론트엔드 GitHub](https://github.com/wecode-bootcamp-korea/wisely-frontend)

<br>

## 데모 영상

![Wisely Demo](https://images.velog.io/images/sungjun-jin/post/33991f20-83ea-47b4-82fa-34c066ba8318/image.png)(https://www.youtube.com/watch?v=Lrxk9zgUZl8)

## 목적
- 웹페이지의 구조를 파악하여 modeling 구현
- modeling을 통해 model 및 view 코딩
- 팀프로젝트를 통한 프론트엔드와 백엔드간의 의사소통

<br>

## 적용 기술 및 구현 기능


### 적용 기술

- Python
- Django web framework
- Beautifulsoup
- Selenium
- Bcrypt
- Json Web Token
- AWS EC2, RDS
- CORS headers
- Gunicorn
- Unittest
- Docker

<br>

### DB Modeling with AQuery
![](https://images.velog.io/images/jeongin/post/b39ff8bb-fa6a-4951-a49d-b0273bb1e2f9/image.png)

### 구현 기능

#### User (회원가입 및 로그인)
- 회원가입 및 로그인 (Bcrypt 암호화 및 JWT Access Token 전송) 기능 구현
- 회원가입 유효성 검사 기능 구현

#### Subscription (설문조사)
- 상품 정기구독을 위한 설문조사
- 질문에 따른 답변 출력
- 사용자의 면도기 선호 색상, 면도 주기에 따른 추천 제품 필터링 및 배송 주기 추천

#### Stores (장바구니)
- 색상 옵션 별 장바구니 등록
- 각 상품 별 이미지, 수량 정보 관리

#### 인프라
- Amazon AWS
- EC2 인스턴스에 RDS서버에 설치된 mysql 연동
- Docker

#### requirements.txt
```sh
$ pip install -r requirements.txt
```

#### [API documents(with POSTMAN)](https://documenter.getpostman.com/view/10871584/SzmiYGij?version=latest#ebf689fe-4133-4144-b9ba-bd6acb2da8f0)
