# Slay the Spire 분석기 (Slay the Spire Analyzer)

슬레이 더 스파이어(Slay the Spire) 게임 데이터를 수집, 처리 및 분석하는 프로젝트입니다. 게임 플레이 로그를 크롤링하여 전투 데이터를 추출하고, 딥러닝 모델을 통해 게임 내 의사결정을 분석합니다.

## 대상 데이터

![runs_filtering](https://github.com/user-attachments/assets/83113ddf-87e7-492a-9341-2c0dc3292a2b)

## 프로젝트 구조

```
spirestar_run_crawler/
├── battles/               # 전투 데이터 처리 및 저장
│   ├── battle_count.py    # 전투 데이터 카운팅 유틸리티
│   └── filter_battles.py  # 전투 데이터 필터링 로직
├── data/                  # 데이터 처리 및 관리
│   ├── data_filtering.py  # 데이터 필터링 유틸리티
│   ├── data_preview.py    # 데이터 미리보기 유틸리티
│   └── parquet_loader.py  # Parquet 파일 로딩 유틸리티
├── deep_learning/         # 딥러닝 모델 관련 모듈
│   ├── scale.py           # 데이터 스케일링 유틸리티
│   ├── train.py           # 모델 학습 스크립트
│   └── train_emb.py       # 임베딩 모델 학습 스크립트
├── sample/                # 샘플 데이터 및 테스트 케이스
└── script/                # 주요 실행 스크립트
    ├── feature_inspection.py    # 특성 검사 유틸리티
    ├── main_simulator.py        # 메인 시뮬레이션 로직
    ├── mismatch_handler.py      # 불일치 처리 유틸리티
    ├── run_handler.py           # 실행 처리 유틸리티
    └── simulation_processor.py  # 시뮬레이션 처리 로직

```

## 주요 기능

### 데이터 수집 및 처리
- Parquet 형식의 게임 로그 파일 로딩 및 처리
- 특정 빌드 버전(2019-01-23 ~ 2020-11-30) 데이터 필터링
- 전투 데이터 추출 및 정제

### 게임 시뮬레이션
- 게임 플레이 로그 기반 전투 시뮬레이션
- 덱 구성, 유물, 이벤트 선택 등의 게임 내 의사결정 추적
- 층별 게임 진행 상황 분석

### 딥러닝 모델
- 카드, 유물, 적 정보에 대한 임베딩 모델
- 전투 결과 예측 모델
- 데이터 캐싱 및 전처리 파이프라인

### 데이터 분석 및 시각화
- 게임 데이터 통계 분석
- 그래프 기반 데이터 시각화
- 전투 결과 요약 및 인사이트 도출

## 기술 스택

- **언어**: Python
- **데이터 처리**: Pandas, NumPy
- **머신러닝/딥러닝**: TensorFlow, Keras, Scikit-learn
- **데이터 저장**: Parquet, JSON

## 캐릭터 지원

현재 다음 캐릭터들에 대한 분석을 지원합니다:
- 아이언클래드 (IRONCLAD)
- 사일런트 (THE_SILENT)
- 디펙트 (DEFECT)
- 와쳐 (WATCHER)