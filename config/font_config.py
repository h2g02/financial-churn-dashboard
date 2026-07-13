"""
리눅스 서버 환경에서 한글 폰트를 안전하게 로드합니다.
외부 URL 다운로드 없이 시스템 폰트 경로만 확인합니다.
"""
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

@st.cache_resource
def get_font_path():
    """시스템에 설치된 폰트를 감지하여 첫 번째 유효한 경로를 반환합니다."""
    candidates = [
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "/System/Library/Fonts/AppleGothic.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "c:/Windows/Fonts/malgun.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return "sans-serif"

def _configure_matplotlib():
    """Matplotlib 전역 폰트 설정 (모듈 임포트 시 1회 실행)."""
    font_path = get_font_path()
    if font_path != "sans-serif":
        try:
            fm.fontManager.addfont(font_path)
            prop = fm.FontProperties(fname=font_path)
            plt.rcParams["font.family"] = prop.get_name()
        except Exception:
            plt.rcParams["font.family"] = "sans-serif"
    else:
        plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False

_configure_matplotlib()
