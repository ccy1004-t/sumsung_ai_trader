"""
给每一根5分钟K线生成未来上涨空间和下跌风险
"""

import pandas as pd 
from pathlib import Path

"""读取特征数据"""
DATA_PATH = Path("data/samsung_features.csv")
df = pd.read_csv(DATA_PATH)

df["Datetime"] = pd.to_datetime(df["Datetime"])

"""参数设置"""

# 5分钟K线：
# 30分钟 = 6根K线
# 60分钟 = 12根K线
HORIZON_30 = 6
HORIZON_60 = 12

"""未来最大上涨 / 最大下跌"""
def future_max_high(series, horizon):
    return(
        series
        .shift(-1)
        .rolling(window=horizon)
        .max()
        .shift(-(horizon - 1))
    )
def future_min_low(series, horizon):
    return(
        series
        .shift(-1)
        .rolling(window=horizon)
        .min()
        .shift(-(horizon -1))
    )

# 未来30分钟最高价 / 最低价
df["future_high_30"] = future_max_high(
    df["high"],
    HORIZON_30
)
df["future_low_30"] = future_min_low(
    df["low"],
    HORIZON_30
)

#未来60分钟最高价 / 最低价
df["future_high_60"] = future_max_high(
    df["high"],
    HORIZON_60
)
df["future_low_60"] = future_min_low(
    df["low"],
    HORIZON_60
)

"""MFE / MAE 空间标签"""
# MFE = 未来最大上涨空间
# MAE = 未来最大下跌风险
df["mfe_30"] = (
    df["future_high_30"] - 
    df["close"]
)
df["mae_30"] = (
    df["close"] -
    df["future_low_30"]
)
df["mfe_60"] = (
    df["future_high_60"] - 
    df["close"]
)
df["mae_60"] = (
    df["close"] - 
    df["future_low_60"]
)

"""买点分类标签"""
# 强买点
# 未来60分钟上涨空间 >= 4000
# 且未来60分钟下跌风险 <= 2000
df["strong_buy_label"] = (
    (df["mfe_60"] >= 2500) &
    (df["mae_60"] <= 2000)
).astype(int)

# 高风险标签
# 未来60分钟下跌风险 >= 2000
df["high_risk_label"] = (
    df["mae_60"] >= 2000
).astype(int)

# 无效买点：
# 未来60分钟上涨空间 < 2000
df["weak_buy_label"] = (
    df["mfe_60"] < 2000
).astype(int)

"""盈亏比标签"""
df["reward_risk_ratio_60"] = (
    df["mfe_60"] /
    df["mae_60"].replace(0, 1)
)
df["good_rr_label"] = (
    df["reward_risk_ratio_60"] >= 2
).astype(int)

"""清理空值"""
df =df.dropna()

"""保存"""
SAVE_PATH = Path("data/samsung_labeled.csv")

df.to_csv(
    SAVE_PATH,
    index=False
)
print(df[[
    "Datetime",
    "close",
    "mfe_30",
    "mae_30",
    "mfe_60",
    "mae_60",
    "reward_risk_ratio_60",
    "strong_buy_label",
    "high_risk_label"
]].tail())

print("\nLabels saved to:", SAVE_PATH)
print("\nHigh Risk Label Count:")
print(df["high_risk_label"].value_counts())

print("\nStrong Buy Label Count:")
print(df["strong_buy_label"].value_counts())