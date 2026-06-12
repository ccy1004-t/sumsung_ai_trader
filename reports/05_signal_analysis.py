"""
把模型预测概率最高的买点列出来
看看AI到底什么时候想买
"""

import pandas as pd 
import xgboost as xgb
from pathlib import Path

"""读取数据"""
DATA_PATH = Path("data/samsung_labeled.csv")
MODEL_PATH = Path("models/xgb_strong_buy.json")

df = pd.read_csv(DATA_PATH)
df["Datetime"] = pd.to_datetime(df["Datetime"])

"""特征列"""
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

"""加在模型"""
model = xgb.XGBClassifier()
model.load_model(MODEL_PATH)

"""预测概率"""
X = df[FEATURES]

df["buy_probability"] = model.predict_proba(X)[:, 1]

"""信号筛选"""
threshold = 0.8

signals = df[
    (
        df["buy_probability"] >= threshold
    )
    &
    (
        df["volume_ratio"] > 1.2
    )
    &
    (
        df["above_vwap"] == 1
    )
    &
    (
        df["day_position"] < 0.4
    )
].copy()

"""输出重点字段"""
show_cols = [

    "Datetime",

    "close",

    # AI概率
    "buy_probability",

    # 空间
    "mfe_60",
    "mae_60",
    "reward_risk_ratio_60",

    # VWAP
    "vwap_distance",
    "above_vwap",

    # EMA8
    "ema8_distance",
    "above_ema8",

    # 成交量
    "volume_ratio",
    "volume_spike",

    # 波动率
    "atr14",

    # K线
    "body",
    "upper_shadow",
    "lower_shadow",

    # 日内位置
    "day_position",

    # 标签
    "strong_buy_label"

]
signals = signals[show_cols]

signals = signals.sort_values(
    by="buy_probability",
    ascending=False
)

"""保存结果"""
SAVE_PATH = Path("reports/top_buy_signals.csv")
SAVE_PATH.parent.mkdir(exist_ok=True)

signals.to_csv(SAVE_PATH, index=False)

print("\nTop Buy Signals:")
print(signals.head(30))

print("\nSignal Statistics:\n")

print(
    signals[[
        "buy_probability",
        "volume_ratio",
        "vwap_distance",
        "ema8_distance",
        "atr14",
        "day_position"
    ]].describe()
)

print("\nSignal count:", len(signals))
print("Saved to:", SAVE_PATH)
