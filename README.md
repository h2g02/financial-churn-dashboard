# Financial Analytics Dashboard

Streamlit 기반의 금융 데이터 분석 포트폴리오 대시보드입니다.

## 포트폴리오 구성

| # | 보고서 | 핵심 분석 |
|---|--------|-----------|
| 1 | 기업 연체율 시차 분석 | 금리-연체율 간 Time-Lag 상관관계 |
| 2 | 신용카드 고객 이탈 분석 | 거래 패턴 기반 고객군 세분화 |
| 3 | FDS 성능 개선 조치 | 변수 제거 & SMOTE & 임계치 튜닝 |

## 설치 및 실행

```bash
git clone <repository-url>
cd financial-dashboard
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud 배포

1. GitHub에 푸시
2. [share.streamlit.io](https://share.streamlit.io) → New App
3. Main file path: `app.py`
4. Deploy

## 시스템 요구사항

- Python 3.9+
- Ubuntu 20.04+ (Streamlit Cloud)
