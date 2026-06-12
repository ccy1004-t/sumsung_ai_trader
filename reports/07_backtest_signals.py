"""
如果模型发出买点
真实历史能赚多少
"""

import pandas as pd
import xgboost as xgb 
from pathlib import Path

"""读取数据"""
DATA_PATH = Path("data/samsung_labeled.csv")
MODEL_PATH = Path("models/xgb_strong_buy.json")

df = pd.read_csv(DATA_PATH)

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

"""加载模型"""
model = xgb.XGBClassifier()
model.load_model(MODEL_PATH)

"""预测概率"""
X = df[FEATURES]
df["buy_probability"] = (
    model.predict_proba(X)[:, 1]
)

"""信号条件"""
threshold = 0.7

signals = df[
    (
        df["buy_probability"] >= threshold
    )
    &
    (
        df["volume_ratio"] > 1.5
    )
].copy()

"""回测统计"""
signals["expected_profit"] = (
    signals["mfe_60"]
)
signals["expected_loss"] = (
    signals["mae_60"]
)
signals["rr"] = (
    signals["expected_profit"] /
    signals["expected_loss"]
    .replace(0, 1)
)

"""胜率"""
signals["win"] = (
    signals["mfe_60"] >
    signals["mae_60"]
).astype(int)

win_rate = (
    signals["win"]
    .mean()
)

"""Profit Factor"""
total_profit = (
    signals["expected_profit"]
    .sum()
)
total_loss = (
    signals["expected_loss"]
    .sum()
)
profit_factor = (
    total_profit / 
    total_loss
)

"""平均值"""
avg_profit = (
    signals["expected_profit"]
    .mean()
)
avg_loss = (
    signals["expected_loss"]
    .mean()
)
avg_rr = (
    signals["rr"]
    .mean()
)

"""输出"""
print("\n========================")

print("Backtest Result")

print("========================")

print(

    "\nSignal Count:",

    len(signals)

)

print(

    "\nWin Rate:",

    round(win_rate, 4)

)

print(

    "\nAverage Profit:",

    round(avg_profit, 2)

)

print(

    "\nAverage Loss:",

    round(avg_loss, 2)

)

print(

    "\nAverage RR:",

    round(avg_rr, 2)

)

print(

    "\nProfit Factor:",

    round(profit_factor, 2)

)

"""保存信号"""

SAVE_PATH = Path(

    "reports/backtest_signals.csv"

)

signals.to_csv(

    SAVE_PATH,

    index=False

)

print(

    "\nSaved to:",

    SAVE_PATH

)