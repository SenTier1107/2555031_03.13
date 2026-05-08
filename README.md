# 🚀 Appprogramming 2026 - 주차별 실습 및 과제 기록
이 저장소는 '앱프로그래밍' 수업의 학습 기록과 과제물을 관리하는 공간입니다.
커밋 기록을 바탕으로 주차별 실습 내용과 주요 과제를 정리하였습니다.

---

## 📅 실습 및 과제 로드맵

| 구분 | 주요 실습 및 과제 | 상세 내용 |
| :--- | :--- | :--- |
| **1주차**<br>2026.03.13 | `모듈,패키지 실습파일`<br>`과제01_Rocket,Titanic.ipynb` | - 파이썬 모듈 시스템 및 패키지 구조화 실습<br>- 외부 API 호출을 통한 ETL 프로세스 구현 기초 |
| **2주차**<br>2026.03.20 | `python_class_faker,tom_jerry.ipynb`<br>`seaborntips.ipynb` | - 클래스(Class) 설계 및 객체지향 프로그래밍 실습<br>- Seaborn 라이브러리를 활용한 데이터 샘플링 실습 |
| **3월 과제**<br>2026.03 | [`EDA-Project_Blood-Donation-Analysis`](https://github.com/SenTier1107/EDA-Project_Blood-Donation-Analysis_2026) | - 헌혈 데이터 EDA 프로젝트<br>- 🔗 링크를 클릭하면 해당 프로젝트 저장소로 이동합니다 |
| **3주차**<br>2026.03.27 | `0327_REST_API_DataFrame_Gradio_Gemini.py` | - REST API를 활용한 웹 데이터 수집 및 서버 헤더 분석<br>- JSON 데이터 → Pandas DataFrame 변환 및 가공<br>- Gradio UI를 활용한 실시간 데이터 필터링 및 통계분석 대시보드 구현<br>- 서울시 공공자전거(따릉이) 3개월 데이터 병합 및 시각화<br>- Gemini AI(google.colab.ai)를 활용한 영→한 번역 서비스 구현 |
| **4주차**<br>2026.04.03 | `AppDev1_Web_Crawling_Scraping_Lab.ipynb` | - BeautifulSoup를 활용한 정적 웹사이트 크롤링 및 스크래핑<br>- Python I/O 유형(Text/Binary/Raw) 및 with 구문 실습<br>- Books to Scrape 사이트에서 카테고리별 도서 데이터 수집 및 정규분포 검정(Q-Q Plot, Shapiro-Wilk)<br>- quotes.toscrape 사이트 텍스트 마이닝 및 CountVectorizer 인코딩 실습 |
| **5주차**<br>2026.04.10 | `NaverWebtoon_Scraping.ipynb` | - 정적 크롤링(BeautifulSoup) vs 동적 크롤링(Selenium) 비교 실험<br>- React 기반 SPA(네이버 웹툰) 동적 크롤링 실습<br>- Selenium + headless Chrome을 활용한 "이달의 신규 웹툰" 제목·작가·내용 스크래핑<br>- WebDriverWait를 활용한 명시적 대기 및 CSS 부분 매칭 셀렉터 활용 |
| **6주차**<br>2026.04.17 | [`0417_FastAPI_Prerequisites`](./0417_FastAPI_Prerequisites) | - 데코레이터(`@`) 패턴 및 함수 레지스트리 구현<br>- 타입 힌트(Type Hints) — `list[T]`, `Optional`, `Union`<br>- Pydantic `BaseModel`을 활용한 런타임 데이터 유효성 검사<br>- SQLite3 CRUD 실습 및 CSV 데이터 DB 연동<br>- SQLite3 + Pydantic 연동으로 Row 데이터 모델 객체 변환<br>- 동기(Sync) vs 비동기(Async) 파일 다운로드 성능 비교 (`asyncio`, `aiohttp`)<br>- Gradio UI 구현 및 ngrok을 통한 외부 URL 공개 |
| **7주차**<br>2026.04.22 | [`FastAPI_SyncAsync`](./FastAPI_SyncAsync) | - 동기(Sync) vs 비동기(Async) 심화 실습 — `threading`, `asyncio`, `aiohttp`, `Semaphore`<br>- CSV 파일 다운로드 성능 비교 (순차 처리 vs 동시 처리)<br>- FastAPI 기초 — 엔드포인트 정의, Path/Query Parameter, Pydantic 유효성 검사<br>- CRUD API 구현 — GET / POST / PUT / DELETE / CSV 다운로드<br>- `requests` vs `httpx` 클라이언트 비교 실습<br>- Swagger UI(`/docs`)를 통한 API 테스트 |
| **8주차**<br>2026.04.29 | [`FastAPI_Learn`](https://github.com/SenTier1107/FastAPI_Learn) | - FastAPI 공식 문서 기반 단계별 학습 및 실습<br>- Path Parameters, Query Parameters, Request Body 개념 학습<br>- Pydantic `BaseModel`을 활용한 요청 데이터 검증<br>- `Annotated`와 `Query()`를 활용한 문자열 검증 및 별칭 선언<br>- 쿼리 매개변수를 Pydantic 모델로 그룹화하여 관리 |
| **중간고사**<br>2026.05.08 | [`quote_analytics_dashboard`](https://github.com/SenTier1107/quote_analytics_dashboard) | - FastAPI + Gradio 기반 명언 분석 · 추천 대시보드 구축<br>- BeautifulSoup4 + httpx로 quotes.toscrape.com 크롤링<br>- SQLite3 CRUD API 및 Swagger UI 구현<br>- TF-IDF 시그니처 단어, 임베딩 기반 추천, 태그 네트워크 분석<br>- Docker + Hugging Face Spaces 배포<br>- 🔗 [배포 URL](https://sentier2006-quote-analytics-dashboard.hf.space/dashboard) |
| **분석 실습** | `customer_data_preprocessing.ipynb`<br>`Preprocessing_Skewed_Data_Transformation.ipynb`<br>`Standardization_Analysis_of_human_data.ipynb` | - 실무 데이터 클렌징 및 전처리 기법 학습<br>- 데이터 표준화 및 왜곡 데이터 변환 분석 |

---

## 🛠 Tech Stack

### Languages & Environments
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/) [![Google Colab](https://img.shields.io/badge/Google%20Colab-F9AB00?style=flat-square&logo=googlecolab&logoColor=white)](https://colab.research.google.com/) [![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)](https://jupyter.org/)

### Data Analysis & Visualization
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/) [![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org/) [![Seaborn](https://img.shields.io/badge/Seaborn-444444?style=flat-square)](https://seaborn.pydata.org/) [![Matplotlib](https://img.shields.io/badge/Matplotlib-ffffff?style=flat-square&logo=matplotlib&logoColor=black)](https://matplotlib.org/) [![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)

### Web & AI
[![Gradio](https://img.shields.io/badge/Gradio-FF7C00?style=flat-square&logo=gradio&logoColor=white)](https://www.gradio.app/) [![Gemini](https://img.shields.io/badge/Gemini%20AI-8E75B2?style=flat-square&logo=google&logoColor=white)](https://gemini.google.com/) [![Claude](https://img.shields.io/badge/Claude%20AI-D97757?style=flat-square&logo=anthropic&logoColor=white)](https://claude.ai/) [![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/) [![Requests](https://img.shields.io/badge/Requests-2B5B84?style=flat-square&logo=python&logoColor=white)](https://docs.python-requests.org/) [![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-444444?style=flat-square&logo=python&logoColor=white)](https://www.crummy.com/software/BeautifulSoup/) [![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat-square&logo=selenium&logoColor=white)](https://www.selenium.dev/) [![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/) [![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/) [![aiohttp](https://img.shields.io/badge/aiohttp-2C5BB4?style=flat-square&logo=aiohttp&logoColor=white)](https://docs.aiohttp.org/) [![uvicorn](https://img.shields.io/badge/uvicorn-499848?style=flat-square&logo=gunicorn&logoColor=white)](https://www.uvicorn.org/)

---

## 👤 Profile
* **이름**: 이지원 (Jiwon Lee)
* **전공**: 빅데이터과

---

© 2026 Jiwon Lee. All rights reserved.
