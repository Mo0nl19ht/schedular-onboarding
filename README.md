# 스케줄링 서버 구축
- Spring Boot & JPA로 백엔드 개발하다가 온 내가 Fastapi에 익숙해지기 위한 회사 온보딩 프로젝트
- 온갖 삽질을 했음

# 계획 및 목표

- 프로젝트 설계(3일)
- 개발(5일)
    - 회원 관리 및 조회
        - admin
        - user
    - 로그인
    - 일정 관리 및 조회
    - 일정 알림
    - validation

## 실제 일정

## 설계

### 1일차

1. 요구사항 분석
2. 컨벤션 설정
3. 설계
4. 클래스 다이어그램
5. 인증, 인가 방법
    1. JWT

### 2일차

1. member 시나리오
2. 인증, 인가 시나리오

### 3일차

- schedule 시나리오
- 알림 설계
    1. APSchedule
- 스케줄러 시나리오

## 개발

### 1일

- 프로그램 구조 설정
    - 3 layer 아키텍처 , 도메인 패키지 구조
- 각 service, controller, repository를 어떻게 관리할까?
    - spring 에서는 bean으로 등록해서 싱글톤으로 만들어지고 컨테이너에서 ioc로  알아서 관리해줬는데 fastapi는 어떻게 해야하나?
    - di를 Depends로 활용하라는데 이게 Controller단 외에는 어떻게 사용 가능한가?
        - MemberController( member_service = Depends(MemberService))
        - 이렇게 등록하고 하나만 만들어서 사용이 가능한가?
- singleton, di 관련해서 fastapi repo의 issue 찾아봄
    - https://github.com/tiangolo/fastapi/issues/504
    - 그 외에도 다른 여러 글 찾아보았으나 fastapi내의 명확한 해결책은 없음

### 2일차

- [여러 래퍼런스를 가지고 있는 라이브러리를 찾음](https://www.humphreyahn.dev/blog/dependency-injector#9b987463-025c-43ba-a521-90fccd0b959b)
    - [관련 글](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html)
    - 래퍼런스
        - socar
        - bentoml
        - …
    - 하지만 지금 이 framework 까지 공부해서 적용하면 시간이 부족하다고 판단하여 기존 AIP에서 활용하는 방식 차용
        - main.py에서 service, controller, repository 호출
- mariadb 생성 후 연결

### 3일차

- BaseEntity 설정
    - 자동으로 created_at, updated_at 갱신
- user, admin이 member를 상속하는 클래스 생성
- 상속구조를 db로 매핑하기 위한 방법 찾음
    - __mapper_args__ 를 이용한 설정

### 4일차

- 만든 model을 db가 인식하지 못하는 문제 발생

`Base.metadata.create_all(bind=self.engine)` 을 하는 곳에서 model의 정보를 인식해야하는데

model정보를 담은 member.py와 위 메소드를 실행하는 곳이 달라서 인식을 못했음

→ 위 메소드를 실행하는곳에서 모델을 import해주었다

### 5일차

- Member CRUD API 생성
- validation 로직 작성
    - 피드백도 받았지만 나도 service에서 error를 raise하는게 맞나 싶었다
    - 하지만 service에서 검출한 오류를 어떻게 controller로 넘겨서 반환하는지 몰라서 일단은 냅뒀다
    - 전에 springboot에서는 `ExceptionController` 를 따로 만들어서 에러를 반환했기에 이렇게 하고 싶었지만 시간이 부족하여 찾아보지는 못했다.

### 6일차

- JWT를 이용한 인증, 인가

### 7일차

- Schedule CUD API 생성

### 8일차

- Schedule 조회 API 생성
    - datetime을 이용한 sqlalchemy 조회
- 전체적인 코드 정리

# 느낀점

- Fastapi, sqlalchemy, pydantic을 처음 접해 작동 방식, 문법, 사용방법을 공부하면서 진행하느라 예정보다 늦춰짐
- 아직 만들어진지 얼마 되지 않은 framework이다보니 많은 기능을 제공하고 있지 않아 직접 구현하거나 다른 라이브러리를 추가로 사용해야되서 아쉬웠다
- framework 자체는 쉽고 document는 잘 되어있는 편이나, 관련 자료 및 실 사용 사례가 많지 않아 실질적으로 적용하여 사용하는데에 어려움을 느낌
- fastapi와 관련된 새로운 프레임워크가 빠르게 업데이트 되고 있어서 재밌었다
    - **SQLAlchemy + Pydantic인 SQLModel이라는 라이브러리를 fastapi의 창시자가 만들었음**
    - 추후에 이 라이브러리를 적용하면 조금 더 편할 것 같다
- 빠르게 개발하기 위해 넘어간 fastapi, sqlalchemy의 작동 원리를 다음에 개발하면서 더 공부해야겠다
- 모르는것이 많아 공부하고 개발하는데에 시간을 많이 쓰다보니 문서를 제대로 작성하지 못했다
    - 다른 사람과 협업하기 위해 문서의 중요성을 인지하자
- domain 주도 개발을 위해 domain으로 서비스 로직을 넣을 수 있도록 더 노력하자


# 대략적 설계
<details>
<summary>설계 내용</summary>
**[회원 관리]**

- 회원 가입 및 로그인 기능
- 사용자, 관리자로 구분
- 일반은 조회만, 관리자는 모든 데이터에 대한 CRUD가 가능합니다.

### 일정 관리

- 사용자는 본인의 일정 CRUD
    - yyyymmddhhmm 으로 일정 관리
    - 30분 단위로 관리
        - 알림 스케줄링할 때 너무 짧은 시간이면 자주 검사해야함
- 관리자는 모든 사람의 일정 CRUD
- 일정 조회
    - 해당 달
    - 해당 주
    - 모든 일정
- 완료 / 예정 으로 상태 분류
### 일정 관리

- 사용자는 본인의 일정 CRUD
    - yyyymmddhhmm 으로 일정 관리
    - 30분 단위로 관리
- 관리자는 모든 사람의 일정 CRUD
- 일정 조회
    - 해당 달
    - 해당 주
    - 모든 일정
- 일정 알림 기능
    - 하루 전 알림 서비스
- 완료 / 예정 으로 상태 분류

### 시나리오

- [ ]  user는 자신의 schedule을 생성할 수 있다
    - yyyymmddhhmm ~ yyyymmddhhmm
    - 30분 단위로 관리
    - start
    - end
    - memo
    - status (closed / open)

- [ ]  user는 자신의 schedule을 수정할 수 있다
- [ ]  user는 자신의 schedule을 삭제할 수 있다
- [ ]  user는 자신의 schedule을 조회할 수 있다
    - closed / open으로 구분하여 조회 가능
    - 1달 단위 조회
    - 주 단위 조회
    - 모든 일정 조회
        - 시작일자로 정렬
        - 페이징?
    - schedule id 기반 조회

- [ ]  admin은 어떤 user의 schedule을 생성할 수 있다
- [ ]  admin은 어떤 user의 schedule을 조회할 수 있다
- [ ]  admin은 어떤 user의 schedule을 수정할 수 있다
- [ ]  admin은 어떤 user의 schedule을 삭제할 수 있다
- [ ]  admin은 모든 user의 schedule을 조회할 수 있다
    - offset , limit


## 회원가입 시퀀스

### 회원가입

1. id, password, email, name입력
2. id, email 중복검사
    1. 있으면 에러 발생
3. user 인스턴스 생성
4. db commit
5. 완료
    1. 201 created

### 로그인

1. id, password 입력
2. 맞는 정보인지 확인
    1. id로 user 불러오기
    2. 입력 받은 password 암호화 하여 저장된 password와 비교
    3. 틀리다면 401 Unauthorized
3. access token 생성
    1. member_id
    2. role
4. 사용자 정보와 함께 반환

### 인가

1. 클라이언트에서 api에 필요한 정보와 access token을 함께 보냄
2. access token에서 member_id, role 꺼냄
3. role로 검증
    1. admin 이라면 모두 허용
        1. (schdule, member)모든 정보 조회는 admin만 가능
    2. user면 본인꺼만 가능
    3. 권한 없으면 403 Forbidden
4. 원하는 정보 반환

### 탈퇴

1. 클라이언트에서 access token 보냄
2. access token에서 member_id, role 꺼냄
3. 검증
    1. 권한 없으면 403 Forbidden
4. db에서 해당 member, member의 schedule 삭제
5. db commit

</details>