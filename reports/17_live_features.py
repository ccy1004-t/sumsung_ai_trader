import os
import sys
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

IN_FILE = os.path.join(ROOT, "data", "kiwoom_samsung_5min.csv")
OUT_FILE = os.path.join(ROOT, "data", "kiwoom_samsung_features.csv")

df = pd.read_csv(IN_FILE)
df["datetime"] = pd.to_datetime(df["datetime"])

df = df.sort_values("datetime")

# EMA8
df["ema8"] = df["close"].ewm(span=8, adjust=False).mean()
df["ema8_distance"] = df["close"] - df["ema8"]

# VWAP
df["typical_price"] = (df["high"] + df["low"] + df["close"]) / 3
df["vwap"] = (df["typical_price"] * df["volume_diff"]).cumsum() / df["volume_diff"].replace(0, pd.NA).cumsum()
df["vwap"] = df["vwap"].fillna(df["close"])
df["vwap_distance"] = df["close"] - df["vwap"]

# Volume Ratio
df["volume_ma5"] = df["volume_diff"].rolling(5).mean()
df["volume_ratio"] = df["volume_diff"] / df["volume_ma5"]

# ATR14
df["prev_close"] = df["close"].shift(1)
df["tr1"] = df["high"] - df["low"]
df["tr2"] = (df["high"] - df["prev_close"]).abs()
df["tr3"] = (df["low"] - df["prev_close"]).abs()
df["tr"] = df[["tr1", "tr2", "tr3"]].max(axis=1)
df["atr14"] = df["tr"].rolling(14).mean()

# MA
df["ma5"] = df["close"].rolling(5).mean()
df["ma20"] = df["close"].rolling(20).mean()

# Above VWAP
df["above_vwap"] = (df["close"] > df["vwap"]).astype(int)

# Above EMA8
df["above_ema8"] = (df["close"] > df["ema8"]).astype(int)

# Volume Spike
df["volume_spike"] = (
    df["volume_diff"] >
    df["volume_diff"].rolling(5).mean() * 1.5
).astype(int)

# Candle
df["body"] = (df["close"] - df["open"]).abs()

df["upper_shadow"] = (
    df["high"]
    - df[["open", "close"]].max(axis=1)
)

df["lower_shadow"] = (
    df[["open", "close"]].min(axis=1)
    - df["low"]
)

# Day Position
day_high = df["high"].max()
day_low = df["low"].min()
df["day_position"] = (df["close"] - day_low) / (day_high - day_low)

df.to_csv(OUT_FILE, index=False)

print("features saved:", OUT_FILE)
print(df.tail(10)[[
    "datetime", "close", "vwap_distance",
    "ema8_distance", "volume_ratio",
    "atr14", "day_position"
]])