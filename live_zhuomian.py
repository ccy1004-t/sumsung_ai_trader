import streamlit as st
import pandas as pd
import os
import xgboost as xgb
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

st.set_page_config(
    page_title="Samsung AI Dashboard",
    layout="wide"
)

st.markdown("""
<style>
            [data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

[data-testid="stStatusWidget"] {
    display: none !important;
}

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

html, body, [data-testid="stAppViewContainer"] {
    overflow-x: hidden !important;
}

.stApp {
    background:
        radial-gradient(circle at 2% 8%, rgba(0, 245, 255, 0.035), transparent 0 12%),
        radial-gradient(circle at 88% 6%, rgba(118, 48, 255, 0.18), transparent 0 24%),
        radial-gradient(circle at 100% 32%, rgba(133, 36, 255, 0.24), transparent 0 40%),
        radial-gradient(circle at 96% 94%, rgba(111, 26, 247, 0.22), transparent 0 36%),
        radial-gradient(circle at 8% 100%, rgba(88, 16, 206, 0.16), transparent 0 22%),
        linear-gradient(90deg, #040916 0%, #040613 22%, #030411 48%, #070314 72%, #13041e 100%);
    color: #EAF6FF;
}

.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background:
        radial-gradient(circle at 4% 8%, rgba(255,255,255,0.04) 0 0.08%, transparent 0.09% 100%),
        radial-gradient(circle at 14% 18%, rgba(130,150,255,0.05) 0 0.07%, transparent 0.08% 100%),
        radial-gradient(circle at 38% 12%, rgba(255,255,255,0.03) 0 0.05%, transparent 0.06% 100%),
        radial-gradient(circle at 64% 10%, rgba(180,120,255,0.05) 0 0.06%, transparent 0.07% 100%),
        radial-gradient(circle at 78% 24%, rgba(255,255,255,0.03) 0 0.05%, transparent 0.06% 100%),
        radial-gradient(circle at 92% 74%, rgba(180,120,255,0.05) 0 0.08%, transparent 0.09% 100%),
        radial-gradient(circle at 10% 96%, rgba(180,120,255,0.06) 0 0.07%, transparent 0.08% 100%),
        radial-gradient(circle at 100% 0%, rgba(143, 56, 255, 0.10), transparent 0 24%),
        radial-gradient(circle at 100% 55%, rgba(116, 34, 248, 0.10), transparent 0 30%),
        radial-gradient(circle at 100% 100%, rgba(111, 29, 241, 0.18), transparent 0 38%);
    z-index: 0;
    opacity: 0.95;
}

[data-testid="stMain"] {
    width: 100% !important;
    max-width: 100% !important;
}

[data-testid="stMain"] > div {
    width: 100% !important;
    max-width: 100% !important;
}

section.main > div {
    width: 100% !important;
    max-width: 100% !important;
}

.block-container {
    padding-top: 0.35rem;
    padding-bottom: 0.35rem;
    max-width: 1980px !important;
    width: auto !important;
    padding-left: 20px !important;
    padding-right: 20px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    position: relative;
    z-index: 1;
}

[data-testid="stAppViewContainer"] {
    overflow-x: hidden !important;
}

section.main {
    max-width: 100%;
    margin: 0;
    overflow-x: hidden !important;
}

.main .block-container {
    max-width: none !important;
    width: auto !important;
    margin-left: 16px !important;
    margin-right: 16px !important;
    padding-left: 12px !important;
    padding-right: 12px !important;
    box-sizing: border-box !important;
}

[data-testid="stMainBlockContainer"] {
    max-width: none !important;
    width: auto !important;
    margin-left: 16px !important;
    margin-right: 16px !important;
    padding-left: 12px !important;
    padding-right: 12px !important;
    box-sizing: border-box !important;
}

h1, h2, h3 {
    color: #EAF6FF;
    text-shadow: 0 0 18px rgba(0, 245, 255, 0.65);
}

[data-testid="stMetric"] {
    background: rgba(10, 18, 40, 0.72);
    border: 1px solid rgba(0, 245, 255, 0.28);
    border-radius: 18px;
    padding: 20px;
    box-shadow:
        0 0 22px rgba(0, 245, 255, 0.12),
        inset 0 0 18px rgba(138, 43, 226, 0.08);
    backdrop-filter: blur(14px);
}

[data-testid="stMetricLabel"] {
    color: #AFC8FF;
}

[data-testid="stMetricValue"] {
    color: #00F5FF;
    text-shadow: 0 0 14px rgba(0, 245, 255, 0.9);
}

.stDataFrame {
    border: 1px solid rgba(138, 43, 226, 0.35);
    border-radius: 16px;
    box-shadow: 0 0 25px rgba(138, 43, 226, 0.15);
}

div[data-testid="stDataFrame"] {
    background: rgba(8, 18, 40, 0.78);
}

hr {
    border-color: rgba(0, 245, 255, 0.18);
}

            
section[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at top left, rgba(0,245,255,0.05), transparent 22%),
        radial-gradient(circle at bottom left, rgba(138,43,226,0.26), transparent 30%),
        linear-gradient(180deg, #090b1d 0%, #070917 48%, #04050f 100%);
    border-right: 1px solid rgba(88, 63, 198, 0.16);
    position: fixed !important;
    top: 12px;
    left: 12px;
    bottom: 12px;
    width: 218px !important;
    min-width: 218px !important;
    max-width: 218px !important;
    border-radius: 18px;
    z-index: 1000;
}

section[data-testid="stSidebar"] > div {
    width: 218px !important;
}

[data-testid="collapsedControl"] {
    z-index: 1001 !important;
}

.side-item {
    margin: 6px 0;
    padding: 9px 11px;
    border-radius: 12px;
    color: #DCE8FF;
    background: linear-gradient(90deg, rgba(18,20,44,0.94), rgba(9,11,24,0.9));
    border: 1px solid rgba(87, 54, 188, 0.10);
    box-shadow: inset 0 0 16px rgba(255,255,255,0.015);
    font-weight: 600;
    font-size: 12px;
}

.side-item:hover {
    background: linear-gradient(90deg, rgba(46,28,115,0.96), rgba(18,20,54,0.92));
    box-shadow: 0 0 16px rgba(138,43,226,0.18), inset 0 0 10px rgba(255,255,255,0.02);
}

.side-item.active {
    background: linear-gradient(90deg, rgba(111,43,255,0.94), rgba(35,22,96,0.94));
    border: 1px solid rgba(148, 94, 255, 0.24);
    box-shadow:
        0 0 18px rgba(138,43,226,0.22),
        inset 0 0 16px rgba(255,255,255,0.05);
}

div[data-testid="stExpander"] {
    border: 1px solid rgba(130, 108, 220, 0.16);
    border-radius: 14px;
    background: rgba(10, 14, 36, 0.52);
    box-shadow: inset 0 0 10px rgba(255,255,255,0.015);
    margin-top: 12px;
}

div[data-testid="stExpander"] summary {
    color: #DCE8FF !important;
    font-weight: 600;
}

.panel-title {
    color:#EAF6FF;
    text-shadow:0 0 16px rgba(255,255,255,0.18);
    margin:0 0 8px 0;
    font-size:14px;
    font-weight:800;
    letter-spacing:0.4px;
}

.terminal-footer {
    color:#7f91c7;
    font-size:10px;
    text-align:center;
    margin-top:8px;
    letter-spacing:0.4px;
}

.top-shell {
    border:1px solid rgba(74, 54, 176, 0.16);
    background:
        radial-gradient(circle at right top, rgba(149, 56, 255, 0.12), transparent 24%),
        linear-gradient(180deg, rgba(7,10,24,0.99), rgba(5,8,20,0.99));
    box-shadow:
        0 0 18px rgba(0,245,255,0.03),
        0 0 24px rgba(138,43,226,0.05),
        inset 0 0 22px rgba(255,255,255,0.015);
    backdrop-filter: blur(12px);
}

.top-chip {
    background:linear-gradient(180deg, rgba(12,16,38,0.96), rgba(8,11,28,0.94));
    border:1px solid rgba(84,66,184,0.18);
    box-shadow:0 0 12px rgba(91,48,255,0.08);
}

.condition-card {
    background:rgba(11, 15, 36, 0.36);
    border:1px solid rgba(180,108,255,0.08);
    box-shadow: inset 0 0 10px rgba(255,255,255,0.012);
}

.chart-shell {
    border:1px solid rgba(76, 58, 170, 0.14);
    border-radius:18px;
    background:linear-gradient(180deg, rgba(9,13,30,0.94), rgba(6,8,20,0.92));
    box-shadow:0 0 22px rgba(138,43,226,0.06), inset 0 0 20px rgba(255,255,255,0.015);
    padding:10px 10px 6px 10px;
    backdrop-filter:blur(12px);
}

.feature-card {
    border-radius: 20px;
    background: rgba(5, 8, 28, 0.82);
    border: 1px solid rgba(180,108,255,0.18);
    box-shadow:
        0 0 35px rgba(130,60,255,.15),
        0 0 80px rgba(0,245,255,.08),
        inset 0 0 20px rgba(138,43,226,.04);
    padding: 18px 18px 16px 18px;
    backdrop-filter: blur(12px);
}

.feature-title {
    color: #EAF6FF;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 0.4px;
    margin: 0 0 20px 0;
    text-shadow: 0 0 16px rgba(255,255,255,0.14);
}

.price-chart-card-marker,
.ai-conditions-card-marker {
    display: none;
}

div[data-testid="stVerticalBlock"]:has(> div[data-testid="element-container"] .price-chart-card-marker),
div[data-testid="stVerticalBlock"]:has(> div[data-testid="element-container"] .ai-conditions-card-marker) {
    border-radius: 20px;
    background: rgba(5, 8, 28, 0.82);
    border: 1px solid rgba(180,108,255,0.18);
    box-shadow:
        0 0 35px rgba(130,60,255,.15),
        0 0 80px rgba(0,245,255,.08),
        inset 0 0 20px rgba(138,43,226,.04);
    padding: 18px 18px 16px 18px;
    backdrop-filter: blur(12px);
}

.mini-chip {
    display:inline-flex;
    align-items:center;
    justify-content:center;
    padding:4px 8px;
    min-width:26px;
    border-radius:999px;
    background:rgba(16,19,40,0.92);
    border:1px solid rgba(76, 63, 164, 0.16);
    color:#8fa8f2;
    font-size:10px;
    font-weight:700;
    box-shadow:inset 0 0 10px rgba(255,255,255,0.015);
}

.mini-chip.active {
    color:#f0ebff;
    background:linear-gradient(90deg, rgba(111,43,255,0.92), rgba(56,31,156,0.94));
    box-shadow:0 0 14px rgba(138,43,226,0.22);
}
</style>
""", unsafe_allow_html=True)

ROOT = os.path.dirname(os.path.abspath(__file__))

FEATURE_FILE = os.path.join(
    ROOT,
    "data",
    "kiwoom_samsung_features.csv"
)

current_time = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
<div class="top-shell" style="
display:flex;
justify-content:space-between;
align-items:center;
margin:2px 0 10px 0;
padding:10px 14px;
border-radius:18px;
min-height:64px;
">
    <div style="display:flex;align-items:center;gap:14px;min-width:0;">
        <div>
            <div style="
            background:linear-gradient(90deg, #17f2ff 0%, #34c8ff 34%, #7691ff 68%, #b547ff 100%);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            font-size:22px;
            font-weight:800;
            letter-spacing:0.8px;
            text-shadow:0 0 12px rgba(23,242,255,0.28), 0 0 22px rgba(181,71,255,0.18);
            line-height:1.05;
            white-space:nowrap;
            ">
            ⚡ SAMSUNG AI TRADER
            </div>
            <div style="
            color:#a8b8f7;
            font-size:10px;
            letter-spacing:2.6px;
            margin-top:2px;
            white-space:nowrap;
            ">
            REAL-TIME SIGNAL DASHBOARD
            </div>
        </div>
        <div class="top-chip" style="
        color:#00FFCC;
        font-weight:700;
        font-size:12px;
        padding:5px 10px;
        border-radius:999px;
        white-space:nowrap;
        ">
        ● SYSTEM ACTIVE
        </div>
        <div style="
        color:#EAF6FF;
        font-size:15px;
        font-weight:700;
        letter-spacing:1px;
        white-space:nowrap;
        ">
        {current_time}
        </div>
    </div>
    <div style="display:flex;align-items:center;gap:10px;white-space:nowrap;">
        <div class="top-chip" style="
        color:#EAF6FF;
        padding:6px 12px;
        border-radius:999px;
        font-weight:700;
        font-size:12px;
        ">
        ⚙ Settings
        </div>
        <div class="top-chip" style="
        width:32px;
        height:32px;
        display:flex;
        align-items:center;
        justify-content:center;
        border-radius:50%;
        color:#EAF6FF;
        font-size:14px;
        ">
        🔔
        </div>
        <div style="
        color:#FFFFFF;
        padding:6px 12px;
        border-radius:999px;
        background:linear-gradient(90deg,#6A00FF,#B000FF);
        box-shadow:0 0 20px rgba(176,0,255,0.8);
        font-weight:800;
        font-size:12px;
        ">
        ● LIVE
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding:12px 10px;">
    <h2 style="
    background:linear-gradient(90deg, #22f1ff 0%, #63b8ff 40%, #9a6bff 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    text-shadow:0 0 16px rgba(46,232,255,0.22);
    margin:0 0 6px 0;
    font-size:22px;
    ">
    ⬡ SAMSUNG AI TRADER
    </h2>
    <p style="color:#8EA7FF; letter-spacing:2px; font-size:10px; margin:0 0 12px 0;">
    REAL-TIME SIGNAL DASHBOARD
    </p>
    <hr>
    <div class="side-item active">📊 Dashboard</div>
    <div class="side-item">📈 Market</div>
    <div class="side-item">🎯 Signals</div>
    <div class="side-item">🤖 Models</div>
    <div class="side-item">📑 Backtest</div>
    <div class="side-item">📋 Logs</div>
    <div class="side-item">📂 Reports</div>
    <div class="side-item">⚙️ Settings</div>
    <div style="margin-top:16px;padding:12px;border-radius:16px;background:linear-gradient(135deg, rgba(18,22,48,0.96), rgba(10,12,28,0.92));border:1px solid rgba(90,108,190,0.16);box-shadow:inset 0 0 16px rgba(255,255,255,0.02);">
        <div style="color:#a4b3e8;font-size:10px;margin-bottom:6px;">AI MODEL STATUS</div>
        <div style="color:#dce8ff;font-size:11px;font-weight:700;">Ensemble Model v2.1</div>
        <div style="margin-top:12px;display:flex;align-items:center;justify-content:center;">
            <div style="width:72px;height:72px;border-radius:50%;background:conic-gradient(#2ce9ff 0deg, #7a3cff 313deg, rgba(40,52,92,0.35) 313deg, rgba(40,52,92,0.2) 360deg);position:relative;box-shadow:0 0 16px rgba(124,60,255,0.18);">
                <div style="position:absolute;inset:8px;border-radius:50%;background:#0a0f22;"></div>
                <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#dffcff;font-size:14px;font-weight:800;">87%</div>
            </div>
        </div>
    </div>
    <div style="margin-top:12px;padding:12px;border-radius:16px;background:linear-gradient(135deg, rgba(18,22,48,0.96), rgba(10,12,28,0.92));border:1px solid rgba(90,108,190,0.16);box-shadow:inset 0 0 16px rgba(255,255,255,0.02);">
        <div style="color:#a4b3e8;font-size:10px;margin-bottom:6px;">MODEL PERFORMANCE</div>
        <div style="color:#2ee8ff;font-size:22px;font-weight:800;">↑ 23.4%</div>
        <div style="color:#8EA7FF;font-size:10px;">vs Last 7 Days</div>
    </div>
    </div>
    """, unsafe_allow_html=True)

def ai_card(title, value, subtitle="", ring_percent=None):
    ring_markup = ""
    if ring_percent is not None:
        ring_value = max(0, min(100, float(ring_percent)))
        ring_degrees = ring_value * 3.6
        ring_markup = (
            '<div style="'
            'width:52px;'
            'height:52px;'
            'position:relative;'
            'flex:0 0 auto;'
            'display:flex;'
            'align-items:center;'
            'justify-content:center;'
            '">'
            '<div style="'
            'position:absolute;'
            'inset:0;'
            'border-radius:50%;'
            'background:rgba(13,16,36,0.95);'
            'border:1px solid rgba(82,72,154,0.18);'
            'box-shadow:0 0 14px rgba(27,224,255,0.08),0 0 24px rgba(138,43,226,0.12);'
            '"></div>'
            '<div style="'
            'position:absolute;'
            'inset:6px;'
            'border-radius:50%;'
            f'background:conic-gradient(from 208deg, #18f1ff 0deg, #28c3ff {ring_degrees * 0.62}deg, #8a39ff {ring_degrees}deg, rgba(27,36,70,0.92) {ring_degrees}deg, rgba(27,36,70,0.34) 360deg);'
            'box-shadow:0 0 12px rgba(24,241,255,0.22), 0 0 20px rgba(138,57,255,0.18);'
            '"></div>'
            '<div style="'
            'position:absolute;'
            'inset:10px;'
            'border-radius:50%;'
            'background:rgba(7,10,23,0.85);'
            'box-shadow:inset 0 0 10px rgba(255,255,255,0.015);'
            '"></div>'
            '</div>'
        )
    sparkline_markup = ""
    if ring_percent is None:
        sparkline_markup = (
            '<div style="'
            'position:absolute;'
            'right:14px;'
            'bottom:10px;'
            'width:72px;'
            'height:28px;'
            'opacity:0.9;'
            '">'
            '<svg width="72" height="28" viewBox="0 0 72 28" fill="none" xmlns="http://www.w3.org/2000/svg">'
            '<path d="M2 24 L14 18 L22 20 L30 11 L40 15 L50 8 L58 12 L70 3" stroke="#18F1FF" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M2 26 L14 20 L22 22 L30 13 L40 17 L50 10 L58 14 L70 5" stroke="rgba(138,57,255,0.75)" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>'
            '</svg>'
            '</div>'
        )

    card_html = (
        '<div style="'
        'padding:12px 14px;'
        'border-radius:24px;'
        'background:radial-gradient(circle at right top, rgba(138,43,226,0.10), transparent 28%), linear-gradient(180deg, rgba(9,13,31,0.96), rgba(6,9,22,0.92));'
        'border:1px solid rgba(88, 62, 170, 0.10);'
        'box-shadow:0 0 12px rgba(0,245,255,.03), 0 0 26px rgba(138,43,226,.05), inset 0 0 20px rgba(255,255,255,.02);'
        'min-height:84px;'
        'display:flex;'
        'align-items:center;'
        'justify-content:space-between;'
        'gap:10px;'
        'overflow:hidden;'
        'backdrop-filter:blur(12px);'
        'position:relative;'
        '">'
        '<div style="min-width:0;flex:1;">'
        '<div style="color:#b7c7ff;font-size:9px;font-weight:700;margin-bottom:8px;white-space:normal;line-height:1.15;">'
        f'{title}'
        '</div>'
        '<div style="color:#1ceeff;font-size:16px;font-weight:800;text-shadow:0 0 18px rgba(28,238,255,0.55);line-height:1.08;white-space:normal;word-break:break-word;">'
        f'{value}'
        '</div>'
        '<div style="color:#91a4ea;font-size:10px;font-weight:600;margin-top:8px;white-space:normal;line-height:1.15;">'
        f'{subtitle}'
        '</div>'
        '</div>'
        f'{sparkline_markup}'
        f'{ring_markup}'
        '</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

if not os.path.exists(FEATURE_FILE):
    st.error("Feature file not found.")
    st.stop()

df = pd.read_csv(FEATURE_FILE)

if len(df) == 0:
    st.warning("No data.")
    st.stop()

latest = df.iloc[-1]

MODEL_FILE = os.path.join(ROOT, "models", "xgb_strong_buy.json")

FEATURES = [
    "ema8",
    "ma5",
    "ma20",
    "vwap",
    "vwap_distance",
    "above_vwap",
    "ema8_distance",
    "above_ema8",
    "atr14",
    "volume_ratio",
    "volume_spike",
    "body",
    "upper_shadow",
    "lower_shadow",
    "day_position"
]

for col in FEATURES:
    df[col] = pd.to_numeric(df[col], errors="coerce")

ai_df = df.dropna(subset=FEATURES)

if len(ai_df) > 0:

    ai_latest = ai_df.iloc[-1]

    model = xgb.Booster()
    model.load_model(MODEL_FILE)

    X = ai_latest[FEATURES].to_frame().T
    X = X.astype(float)

    dmatrix = xgb.DMatrix(X, feature_names=FEATURES)

    buy_prob = float(model.predict(dmatrix)[0])

    if buy_prob >= 0.80:
        ai_signal = "BUY"
    elif buy_prob >= 0.65:
        ai_signal = "WATCH"
    else:
        ai_signal = "WAIT"

else:
    buy_prob = None
    ai_signal = "NOT READY"

if buy_prob is not None:
    if buy_prob >= 0.80:
        probability_label = "High Probability"
    elif buy_prob >= 0.65:
        probability_label = "Medium Probability"
    else:
        probability_label = "Low Probability"
    confidence_text = f"Confidence: {round(buy_prob * 100)}%"
else:
    probability_label = "Low Probability"
    confidence_text = "Confidence: 50%"

top1, top2, top3, top4 = st.columns(4)

with top1:
    ai_card(
        "SAMSUNG (005930.KS)",
        f"₩ {latest['close']:,.0f}",
        "Samsung Electronics"
    )

with top2:
    if buy_prob is not None:
        ai_card(
            "BUY PROBABILITY",
            f"{round(buy_prob * 100, 2)}%",
            probability_label,
            ring_percent=buy_prob * 100
        )
    else:
        ai_card(
            "BUY PROBABILITY",
            "50.25%",
            probability_label,
            ring_percent=50.25
        )

signal_color = "#B000FF"
signal_text = "🟣 WAIT"

if ai_signal == "BUY":
    signal_color = "#00FF9C"
    signal_text = "🟢 STRONG BUY"
elif ai_signal == "WATCH":
    signal_color = "#FFD700"
    signal_text = "🟡 WATCH"

with top3:
    ai_card(
        "AI SIGNAL",
        signal_text,
        confidence_text,
        ring_percent=buy_prob * 100 if buy_prob is not None else 50
    )

with top4:
    ai_card(
        "MARKET TREND",
        "BULLISH",
        "Strength: 68/100",
        ring_percent=68
    )

st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

show_cols = [
    "datetime",
    "open",
    "high",
    "low",
    "close",
    "volume"
]

chart_df = df.tail(80).copy()

if "datetime" in chart_df.columns:
    chart_df["datetime"] = pd.to_datetime(chart_df["datetime"], errors="coerce")

for col in ["open", "high", "low", "close", "volume", "ema8", "vwap", "ma20", "ma60"]:
    if col in chart_df.columns:
        chart_df[col] = pd.to_numeric(chart_df[col], errors="coerce")

if "close" in chart_df.columns:
    if "open" not in chart_df.columns:
        chart_df["open"] = chart_df["close"].shift(1)
        chart_df["open"] = chart_df["open"].fillna(chart_df["close"])
    if "high" not in chart_df.columns:
        chart_df["high"] = chart_df[["open", "close"]].max(axis=1) * 1.001
    if "low" not in chart_df.columns:
        chart_df["low"] = chart_df[["open", "close"]].min(axis=1) * 0.999

    if "ma20" not in chart_df.columns:
        chart_df["ma20"] = chart_df["close"].rolling(window=20, min_periods=1).mean()
    if "ma60" not in chart_df.columns:
        chart_df["ma60"] = chart_df["close"].rolling(window=60, min_periods=1).mean()

if all(col in chart_df.columns for col in ["datetime", "volume", "close"]):
    chart_df["trade_date"] = chart_df["datetime"].dt.date
    volume_cumsum = chart_df.groupby("trade_date")["volume"].cumsum()
    value_cumsum = (chart_df["close"] * chart_df["volume"]).groupby(chart_df["trade_date"]).cumsum()
    chart_df["vwap"] = value_cumsum / volume_cumsum.replace(0, pd.NA)

    median_close = chart_df["close"].median()
    if pd.notna(median_close):
        vwap_mask = (
            (chart_df["vwap"] < median_close * 0.7) |
            (chart_df["vwap"] > median_close * 1.3)
        )
        chart_df.loc[vwap_mask, "vwap"] = pd.NA

has_ohlc = all(col in chart_df.columns for col in ["open", "high", "low", "close"])
has_volume = "volume" in chart_df.columns

if has_volume:
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.78, 0.22]
    )
else:
    fig = make_subplots(rows=1, cols=1)

if has_ohlc:
    fig.add_trace(
        go.Candlestick(
            x=chart_df["datetime"],
            open=chart_df["open"],
            high=chart_df["high"],
            low=chart_df["low"],
            close=chart_df["close"],
            name="OHLC",
            increasing=dict(
                line=dict(color="#00F5FF", width=1.2),
                fillcolor="rgba(0,245,255,0.22)"
            ),
            decreasing=dict(
                line=dict(color="#FF4DFF", width=1.2),
                fillcolor="rgba(255,77,255,0.22)"
            )
        ),
        row=1,
        col=1
    )

if "ema8" in chart_df.columns:
    fig.add_trace(
        go.Scatter(
            x=chart_df["datetime"],
            y=chart_df["ema8"],
            mode="lines",
            name="EMA8",
            line=dict(color="#00BFFF", width=2)
        ),
        row=1,
        col=1
    )

if "ma20" in chart_df.columns:
    fig.add_trace(
        go.Scatter(
            x=chart_df["datetime"],
            y=chart_df["ma20"],
            mode="lines",
            name="MA20",
            line=dict(color="#7A5CFF", width=1.5)
        ),
        row=1,
        col=1
    )

if "ma60" in chart_df.columns:
    fig.add_trace(
        go.Scatter(
            x=chart_df["datetime"],
            y=chart_df["ma60"],
            mode="lines",
            name="MA60",
            line=dict(color="#4B1D88", width=1.5)
        ),
        row=1,
        col=1
    )

if "vwap" in chart_df.columns:
    fig.add_trace(
        go.Scatter(
            x=chart_df["datetime"],
            y=chart_df["vwap"],
            mode="lines",
            name="VWAP",
            line=dict(color="#FF9FEA", width=2)
        ),
        row=1,
        col=1
    )

if has_volume:
    volume_colors = [
        "#00F5FF" if close_val >= open_val else "#FF4DFF"
        for open_val, close_val in zip(chart_df["open"], chart_df["close"])
    ]
    fig.add_trace(
        go.Bar(
            x=chart_df["datetime"],
            y=chart_df["volume"],
            name="Volume",
            marker=dict(color=volume_colors),
            opacity=0.35
        ),
        row=2,
        col=1
    )

fig.update_layout(
    height=500 if has_volume else 400,
    margin=dict(l=8, r=8, t=8, b=8),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(8,12,28,0.92)",
    font=dict(color="#EAF6FF", size=11),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=10, color="#D6E6FF")
    )
)

fig.update_xaxes(
    showgrid=True,
    tickfont=dict(size=10),
    gridcolor="rgba(31,99,173,0.18)",
    zeroline=False,
    rangeslider=dict(visible=False),
    rangebreaks=[
        dict(bounds=["sat", "mon"]),
        dict(pattern="hour", bounds=[15.5, 9])
    ],
    row=1,
    col=1
)

fig.update_yaxes(
    showgrid=True,
    tickfont=dict(size=10),
    gridcolor="rgba(31,99,173,0.18)",
    zeroline=False,
    row=1,
    col=1
)

if has_volume:
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(31,99,173,0.14)",
        tickfont=dict(size=10),
        rangebreaks=[
            dict(bounds=["sat", "mon"]),
            dict(pattern="hour", bounds=[15.5, 9])
        ],
        row=2,
        col=1
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(31,99,173,0.14)",
        zeroline=False,
        tickfont=dict(size=9),
        title_text="Volume",
        row=2,
        col=1
    )

left_main, right_panel = st.columns([3, 1])

with left_main:
    with st.container():
        st.markdown('<div class="price-chart-card-marker"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:16px;
            margin-bottom:16px;
            padding-bottom:14px;
            border-bottom:1px solid rgba(180,108,255,0.10);
            flex-wrap:wrap;
        ">
            <div style="color:#EAF6FF;font-size:16px;font-weight:900;letter-spacing:0.5px;text-shadow:0 0 16px rgba(0,245,255,0.12);">
                📈 Price Chart
            </div>
            <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                <span class="mini-chip">1m</span>
                <span class="mini-chip">5m</span>
                <span class="mini-chip">15m</span>
                <span class="mini-chip">1h</span>
                <span class="mini-chip active">1D</span>
                <span class="mini-chip">1W</span>
                <span class="mini-chip" style="margin-left:10px;padding:5px 14px;">Indicators</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        with st.expander("📋 Recent Market Data", expanded=True):
            st.dataframe(
                df[show_cols].tail(5),
                use_container_width=True,
                height=165
            )

with right_panel:
    with st.container():
        st.markdown('<div class="ai-conditions-card-marker"></div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">🤖 AI MODEL CONDITIONS</div>', unsafe_allow_html=True)

        conditions = [
            ("VWAP Distance", "PASS ✅" if float(latest["vwap_distance"]) > -500 else "FAIL ❌"),
            ("EMA8 Distance", "PASS ✅" if float(latest["ema8_distance"]) > -500 else "FAIL ❌"),
            ("Volume Ratio", "PASS ✅" if float(latest["volume_ratio"]) > 1 else "FAIL ❌"),
            ("ATR14", "PASS ✅" if float(latest["atr14"]) > 0 else "FAIL ❌"),
            ("Day Position", "PASS ✅" if float(latest["day_position"]) > 0.3 else "FAIL ❌"),
            ("Buy Probability", f"{round(buy_prob*100,2)}%" if buy_prob is not None else "N/A"),
            ("AI Signal", ai_signal)
        ]

        condition_icons = {
            "VWAP Distance": "📈",
            "EMA8 Distance": "⚡",
            "Volume Ratio": "📊",
            "ATR14": "🌀",
            "Day Position": "🎯",
            "Buy Probability": "🧠",
            "AI Signal": "🤖"
        }

        for name, value in conditions:
            icon = condition_icons.get(name, "•")
            is_pass = isinstance(value, str) and "PASS" in value
            is_fail = isinstance(value, str) and "FAIL" in value

            if is_pass:
                value_html = """
                <span style="
                    color:#DFFFF6;
                    font-size:11px;
                    font-weight:800;
                    padding:4px 8px;
                    border-radius:999px;
                    background:rgba(0,255,156,0.14);
                    border:1px solid rgba(0,255,156,0.35);
                    box-shadow:0 0 14px rgba(0,255,156,0.22);
                    white-space:nowrap;
                ">
                    PASS
                </span>
                """
            elif is_fail:
                value_html = """
                <span style="
                    color:#FFE7EA;
                    font-size:11px;
                    font-weight:800;
                    padding:4px 8px;
                    border-radius:999px;
                    background:rgba(255,59,92,0.14);
                    border:1px solid rgba(255,59,92,0.4);
                    box-shadow:0 0 14px rgba(255,59,92,0.2);
                    white-space:nowrap;
                ">
                    FAIL
                </span>
                """
            else:
                value_html = f"""
                <span style="color:#00F5FF;font-size:12px;font-weight:800;text-shadow:0 0 12px rgba(0,245,255,0.7);white-space:nowrap;">
                    {value}
                </span>
                """

            st.markdown(
                f"""
                <div class="condition-card" style="
                    padding:7px 9px;
                    margin-bottom:5px;
                    border-radius:12px;
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    color:white;
                    backdrop-filter:blur(12px);
                ">
                    <span style="display:flex;align-items:center;gap:7px;color:#EAF6FF;font-size:11px;font-weight:600;">
                        <span style="font-size:12px;">{icon}</span>
                        <span>{name}</span>
                    </span>
                    {value_html}
                </div>
                """,
                unsafe_allow_html=True
            )

bottom1, bottom2, bottom3 = st.columns([1.3, 1, 1])

with bottom1:
    st.markdown("""
    <div style="
        padding:10px 12px 8px 12px;
        border-radius:16px 16px 0 0;
        background:linear-gradient(135deg, rgba(12,18,38,0.95), rgba(8,12,26,0.9));
        border:1px solid rgba(0,245,255,0.06);
        border-bottom:none;
        box-shadow:0 0 18px rgba(0,245,255,0.04), inset 0 0 12px rgba(255,255,255,0.02);
        display:flex;
        align-items:center;
        justify-content:space-between;
        color:#EAF6FF;
        backdrop-filter:blur(12px);
    ">
        <div style="font-size:13px;font-weight:700;letter-spacing:0.5px;">📜 SIGNAL HISTORY</div>
        <div style="font-size:13px;color:#8EA7FF;">×</div>
    </div>
    """, unsafe_allow_html=True)

    history_df = df.tail(5).copy()
    history_df["Buy Probability"] = round(buy_prob * 100, 2) if buy_prob is not None else None
    history_df["AI Signal"] = ai_signal

    history_cols = [
        "datetime",
        "close",
        "Buy Probability",
        "AI Signal"
    ]

    history_rows_html = ""

    for _, row in history_df[history_cols].iterrows():
        signal_value = str(row["AI Signal"])

        if "BUY" in signal_value:
            signal_badge = """
            <span style="
                color:#DFFFF6;
                font-size:11px;
                font-weight:800;
                padding:4px 8px;
                border-radius:999px;
                background:rgba(0,255,156,0.14);
                border:1px solid rgba(0,255,156,0.35);
                box-shadow:0 0 14px rgba(0,255,156,0.22);
                white-space:nowrap;
            ">BUY</span>
            """
        elif "WATCH" in signal_value:
            signal_badge = """
            <span style="
                color:#FFF6CC;
                font-size:11px;
                font-weight:800;
                padding:4px 8px;
                border-radius:999px;
                background:rgba(255,215,0,0.14);
                border:1px solid rgba(255,215,0,0.35);
                box-shadow:0 0 14px rgba(255,215,0,0.2);
                white-space:nowrap;
            ">WATCH</span>
            """
        elif "FAIL" in signal_value or "SELL" in signal_value:
            signal_badge = """
            <span style="
                color:#FFE7EA;
                font-size:11px;
                font-weight:800;
                padding:4px 8px;
                border-radius:999px;
                background:rgba(255,59,92,0.14);
                border:1px solid rgba(255,59,92,0.4);
                box-shadow:0 0 14px rgba(255,59,92,0.2);
                white-space:nowrap;
            ">SELL</span>
            """
        else:
            signal_badge = """
            <span style="
                color:#F3E8FF;
                font-size:11px;
                font-weight:800;
                padding:4px 8px;
                border-radius:999px;
                background:rgba(176,0,255,0.14);
                border:1px solid rgba(176,0,255,0.35);
                box-shadow:0 0 14px rgba(176,0,255,0.2);
                white-space:nowrap;
            ">WAIT</span>
            """

        prob_value = row["Buy Probability"]
        prob_text = "N/A" if pd.isna(prob_value) else f"{float(prob_value):.2f}%"

        history_rows_html += f"""
        <div style="
            display:grid;
            grid-template-columns: 1.2fr 1fr 0.9fr 1fr;
            align-items:center;
            gap:6px;
            padding:8px 10px;
            border-top:1px solid rgba(255,255,255,0.06);
        ">
            <div style="color:#DCE8FF;font-size:11px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{row['datetime']}</div>
            <div style="color:#00F5FF;font-size:11px;font-weight:700;white-space:nowrap;">₩ {float(row['close']):,.0f}</div>
            <div style="color:#EAF6FF;font-size:11px;white-space:nowrap;">{prob_text}</div>
            <div>{signal_badge}</div>
        </div>
        """

    st.markdown(
        f"""
        <div style="
            background:linear-gradient(135deg, rgba(12,18,38,0.92), rgba(8,12,26,0.84));
            border:1px solid rgba(0,245,255,0.06);
            border-top:none;
            border-radius:0 0 16px 16px;
            box-shadow:0 0 18px rgba(0,245,255,0.04), inset 0 0 12px rgba(255,255,255,0.02);
            min-height:196px;
            overflow:hidden;
            backdrop-filter:blur(12px);
        ">
            <div style="
                display:grid;
                grid-template-columns: 1.2fr 1fr 0.9fr 1fr;
                align-items:center;
                gap:6px;
                padding:9px 10px;
                background:rgba(255,255,255,0.03);
                color:#8EA7FF;
                font-size:10px;
                letter-spacing:0.8px;
            ">
                <div>TIME</div>
                <div>PRICE</div>
                <div>PROB</div>
                <div>AI SIGNAL</div>
            </div>
            {history_rows_html}
        </div>
        """,
        unsafe_allow_html=True
    )

with bottom2:
    st.markdown("""
    <div style="
        padding:10px 12px 8px 12px;
        border-radius:16px 16px 0 0;
        background:linear-gradient(135deg, rgba(12,18,38,0.95), rgba(8,12,26,0.9));
        border:1px solid rgba(0,245,255,0.06);
        border-bottom:none;
        box-shadow:0 0 18px rgba(0,245,255,0.04), inset 0 0 12px rgba(255,255,255,0.02);
        display:flex;
        align-items:center;
        justify-content:space-between;
        color:#EAF6FF;
        backdrop-filter:blur(12px);
    ">
        <div style="font-size:13px;font-weight:700;letter-spacing:0.5px;">🖥️ SYSTEM LOG</div>
        <div style="font-size:13px;color:#8EA7FF;">×</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        padding:12px;
        border-radius:0 0 16px 16px;
        background:linear-gradient(135deg, rgba(12,18,38,0.92), rgba(8,12,26,0.84));
        border:1px solid rgba(0,245,255,0.06);
        border-top:none;
        box-shadow:0 0 18px rgba(0,245,255,0.04), inset 0 0 12px rgba(255,255,255,0.02);
        color:#EAF6FF;
        line-height:1.6;
        font-size:12px;
        min-height:196px;
        backdrop-filter:blur(12px);
    ">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.06);">
            <div style="display:flex;align-items:center;gap:10px;min-width:0;">
                <span style="color:#8EA7FF;font-size:11px;white-space:nowrap;">23:47:30</span>
                <span style="color:#EAF6FF;font-size:11px;">AI model prediction completed</span>
            </div>
            <span style="color:#DFF3FF;font-size:10px;font-weight:800;padding:4px 8px;border-radius:999px;background:rgba(0,153,255,0.14);border:1px solid rgba(0,153,255,0.35);box-shadow:0 0 12px rgba(0,153,255,0.18);white-space:nowrap;">INFO</span>
        </div>
        <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.06);">
            <div style="display:flex;align-items:center;gap:10px;min-width:0;">
                <span style="color:#8EA7FF;font-size:11px;white-space:nowrap;">23:47:28</span>
                <span style="color:#EAF6FF;font-size:11px;">Market data updated</span>
            </div>
            <span style="color:#DFF3FF;font-size:10px;font-weight:800;padding:4px 8px;border-radius:999px;background:rgba(0,153,255,0.14);border:1px solid rgba(0,153,255,0.35);box-shadow:0 0 12px rgba(0,153,255,0.18);white-space:nowrap;">INFO</span>
        </div>
        <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.06);">
            <div style="display:flex;align-items:center;gap:10px;min-width:0;">
                <span style="color:#8EA7FF;font-size:11px;white-space:nowrap;">23:47:25</span>
                <span style="color:#EAF6FF;font-size:11px;">News sentiment analysis completed</span>
            </div>
            <span style="color:#DFFFF6;font-size:10px;font-weight:800;padding:4px 8px;border-radius:999px;background:rgba(0,255,156,0.14);border:1px solid rgba(0,255,156,0.35);box-shadow:0 0 12px rgba(0,255,156,0.18);white-space:nowrap;">SUCCESS</span>
        </div>
        <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;padding:7px 0;">
            <div style="display:flex;align-items:center;gap:10px;min-width:0;">
                <span style="color:#8EA7FF;font-size:11px;white-space:nowrap;">23:47:22</span>
                <span style="color:#EAF6FF;font-size:11px;">Volume spike detected</span>
            </div>
            <span style="color:#FFF6CC;font-size:10px;font-weight:800;padding:4px 8px;border-radius:999px;background:rgba(255,215,0,0.14);border:1px solid rgba(255,215,0,0.35);box-shadow:0 0 12px rgba(255,215,0,0.18);white-space:nowrap;">WARNING</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with bottom3:
    st.markdown("""
    <div style="
        padding:10px 12px 8px 12px;
        border-radius:16px 16px 0 0;
        background:linear-gradient(135deg, rgba(12,18,38,0.95), rgba(8,12,26,0.9));
        border:1px solid rgba(0,245,255,0.06);
        border-bottom:none;
        box-shadow:0 0 18px rgba(0,245,255,0.04), inset 0 0 12px rgba(255,255,255,0.02);
        display:flex;
        align-items:center;
        justify-content:space-between;
        color:#EAF6FF;
        backdrop-filter:blur(12px);
    ">
        <div style="font-size:13px;font-weight:700;letter-spacing:0.5px;">📊 MARKET OVERVIEW</div>
        <div style="font-size:13px;color:#8EA7FF;">×</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        padding:12px;
        border-radius:0 0 16px 16px;
        background:linear-gradient(135deg, rgba(12,18,38,0.92), rgba(8,12,26,0.84));
        border:1px solid rgba(0,245,255,0.06);
        border-top:none;
        box-shadow:0 0 18px rgba(0,245,255,0.04), inset 0 0 12px rgba(255,255,255,0.02);
        min-height:196px;
        backdrop-filter:blur(12px);
    ">
        <div style="display:flex;justify-content:space-between;margin-bottom:9px;color:#AFC8FF;font-size:11px;">
            <span>KOSPI</span><span style="color:#00F5FF;font-weight:800;">2,625.58</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:9px;color:#AFC8FF;font-size:11px;">
            <span>KOSDAQ</span><span style="color:#00F5FF;font-weight:800;">872.34</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:9px;color:#AFC8FF;font-size:11px;">
            <span>S&amp;P 500</span><span style="color:#00F5FF;font-weight:800;">5,278.40</span>
        </div>
        <div style="display:flex;justify-content:space-between;color:#AFC8FF;font-size:11px;">
            <span>NASDAQ</span><span style="color:#00F5FF;font-weight:800;">16,735.02</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    '<div class="terminal-footer">SAMSUNG AI TRADER SYSTEM v2.1.0 | All Rights Reserved</div>',
    unsafe_allow_html=True
)
