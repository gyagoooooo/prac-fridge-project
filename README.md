# Refrigerator Inventory Management

## 프로젝트 소개

냉장고 재고 관리 서비스를 구현하며 웹 애플리케이션의 발전 과정을 비교한 프로젝트입니다.

동일한 기능과 동일한 SQLite 데이터베이스를 유지한 상태에서 다음 세 가지 방식으로 구현하였습니다.

1. Flask Template
2. Flask REST API + jQuery
3. FastAPI REST API

이를 통해 서버 사이드 렌더링(Server Side Rendering) 방식과 REST API 기반 구조의 차이를 비교하고, FastAPI의 실무적인 장점을 학습하는 것을 목표로 하였습니다.

---

## 기술 스택

### Backend

* Flask
* FastAPI
* SQLAlchemy
* SQLite

### Frontend

* HTML
* CSS
* JavaScript
* jQuery

### Database

* SQLite

---

## 프로젝트 구조

```text
fridge-project/

├── refrigerator.db

├── 01_flask_template/
│   ├── app.py
│   ├── templates/
│   └── static/

├── 02_flask_rest_jquery/
│   ├── app.py
│   ├── templates/
│   └── static/

└── 03_fastapi_rest/
    ├── main.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    ├── templates/
    └── static/
```

---

## 주요 기능

### 식재료 관리

* 식재료 등록
* 식재료 조회
* 식재료 수정
* 식재료 삭제

### 재고 관리

* 수량 감소(소비)
* 유통기한 관리
* 냉장 / 냉동 / 실온 구분

---

## 데이터베이스 구조

### ingredients

| 컬럼명          | 타입      |
| ------------ | ------- |
| id           | INTEGER |
| name         | TEXT    |
| category     | TEXT    |
| storage_type | TEXT    |
| quantity     | INTEGER |
| unit         | TEXT    |
| expire_date  | TEXT    |
| memo         | TEXT    |
| created_at   | TEXT    |

---

# 1. Flask Template

## 구조

```text
Browser
 ↓
Flask
 ↓
SQLite
 ↓
Jinja2 Template
 ↓
HTML
```

## 특징

* 서버가 HTML 생성
* Form 기반 요청 처리
* 페이지 전체 새로고침
* Jinja2 Template 사용

### 학습 내용

* Flask Routing
* Form 처리
* Redirect
* Jinja2 Template
* SQLite 연동

---

# 2. Flask REST API + jQuery

## 구조

```text
Browser
 ↓
Ajax
 ↓
Flask REST API
 ↓
SQLite
 ↓
JSON
 ↓
DOM 갱신
```

## 특징

* JSON 기반 통신
* Ajax 활용
* 페이지 새로고침 없이 화면 갱신
* REST API 설계 적용

### API

| Method | URL                           | 기능 |
| ------ | ----------------------------- | -- |
| GET    | /api/ingredients              | 조회 |
| POST   | /api/ingredients              | 등록 |
| PUT    | /api/ingredients/{id}         | 수정 |
| PATCH  | /api/ingredients/{id}/consume | 소비 |
| DELETE | /api/ingredients/{id}         | 삭제 |

### 학습 내용

* REST API
* Ajax
* JSON
* DOM Manipulation
* HTTP Method 활용

---

# 3. FastAPI REST API

## 구조

```text
Browser
 ↓
fetch
 ↓
FastAPI
 ↓
SQLAlchemy
 ↓
SQLite
 ↓
JSON
```

## 특징

* FastAPI 사용
* SQLAlchemy ORM 적용
* Pydantic Validation
* Swagger 자동 문서 생성

### API 문서

```text
http://localhost:5000/docs
```

### 학습 내용

* FastAPI
* SQLAlchemy ORM
* Pydantic
* Swagger
* 타입 힌트 기반 개발

---

## 구현 방식 비교

| 항목         | Flask Template | Flask REST API | FastAPI REST API |
| ---------- | -------------- | -------------- | ---------------- |
| 응답         | HTML           | JSON           | JSON             |
| 페이지 새로고침   | O              | X              | X                |
| Ajax       | X              | O              | fetch            |
| REST API   | X              | O              | O                |
| Validation | 직접 구현          | 직접 구현          | 자동               |
| Swagger    | X              | X              | O                |
| ORM        | X              | X              | O                |
| 실무 활용도     | 낮음             | 보통             | 높음               |
