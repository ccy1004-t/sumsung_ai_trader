"""
给三星电子5分钟数据
增加AI学习特征
"""

import pandas as pd 
import numpy as np
from pathlib import Path

"""
读取数据
"""
DATA_PATH = Path("data/samsung_5m.csv")

df = pd.read_csv(DATA_PATH)

if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])
print(df.columns)
"""
时间处理
"""
df["Datetime"] = pd.to_datetime(df["Datetime"])

"""
基础价格
"""
df["close"] = df["Close"]
df["open"] = df["Open"]
df["high"] = df["High"]
df["low"] = df["Low"]
df["volume"] = df["Volume"]

"""
EMA8
"""
df["ema8"] = (
    df["close"]
    .ewm(span=8, adjust=False)
    .mean()
)

# 是否站上EMA8
df["above_ema8"] = (
    df["close"] > df["ema8"]
).astype(int)

# EMA8距离
df["ema8_distance"] = (
    df["close"] - df["ema8"]
)

"""
MA均线
"""
df["ma5"] = (
    df["close"]
    .rolling(5)
    .mean()
)
df["ma20"] = (
    df["close"]
    .rolling(20)
    .mean()
)

"""
VWAP
"""
typical_price = (
    df["high"] + 
    df["low"] + 
    df["close"]
) / 3

df["tp_volume"] = (
    typical_price *
    df["volume"]
)

# 每天重新计算 VWAP
df["date"] = df["Datetime"].dt.date

df["cum_tp_volume"] = (
    df.groupby("date")["tp_volume"]
    .cumsum()
)

df["cum_volume"] = (
    df.groupby("date")["volume"]
    .cumsum()
)

df["vwap"] = (
    df["cum_tp_volume"] /
    df["cum_volume"]
)

df["vwap"] = (
    df["cum_tp_volume"] /
    df["cum_volume"]
)

# 是否站上vwap
df["above_vwap"] = (
    df["close"] > df["vwap"]
).astype(int)

# VWAP距离
df["vwap_distance"] = (
    df["close"] - df["vwap"]
)

"""
ATR波动率
"""
df["tr1"] = (
    df["high"] - df["low"]
)
df["tr2"] = abs(
    df["high"] - 
    df["close"].shift(1)
)
df["tr3"] = abs(
    df["low"] - 
    df["close"].shift(1)
)
df["tr"] = df[
    ["tr1","tr2","tr3"]
].max(axis=1)

df["atr14"] = (
    df["tr"]
    .rolling(14)
    .mean()
)

"""
成交量变化
"""
df["volume_ma20"] = (
    df["volume"]
    .rolling(20)
    .mean()
)
df["volume_ratio"] = (
    df["volume"] / 
    df["volume_ma20"]
)

# 成交量爆发
df["volume_spike"] = (
    df["volume"] > 
    df["volume_ma20"] * 2
).astype(int)

"""K线实体"""
df["body"] = (
    df["close"] - 
    df["open"]
).abs()

"""上影线"""
df["upper_shadow"] = (
    df["high"] - 
    df[["open", "close"]]
    .max(axis=1)
)

"""下影线"""
df["lower_shadow"] = (
    df[["open", "close"]]
    .min(axis=1) - 
    df["low"]
)

"""当日位置"""
rolling_high = (
    df["high"]
    .rolling(48)
    .max()
)

rolling_low = (
    df["low"]
    .rolling(48)
    .min()
)

df["day_position"] = (
    (df["close"] - rolling_low) /
    (rolling_high - rolling_low)
)

"""删除空值"""
df = df.dropna()

"""保存"""
SAVE_PATH = Path(
    "data/samsung_features.csv"
)
df.to_csv(
    SAVE_PATH,
    index=False
)
print(df.tail())
print("\nFeatures saved to:",
      SAVE_PATH
)