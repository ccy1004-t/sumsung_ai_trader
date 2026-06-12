"""实时信号扫描器"""

import time 
from pathlib import Path 

import numpy as np
import pandas as pd
import yfinance as yf
import xgboost as xgb

TICKER = "005930.KS"
MODEL_PATH = Path("models/xgb_strong_buy.json")

FEATURES = [
    "ema8", "ma5", "ma20",
    "vwap", "vwap_distance", "above_vwap",
    "ema8_distance", "above_ema8",
    "atr14",
    "volume_ratio", "volume_spike",
    "body", "upper_shadow", "lower_shadow",
    "day_position"
]

BUY_PROB_THRESHOLD = 0.85
VOLUME_RATIO_THRESHOLD = 1.2
DAY_POSITION_MAX = 0.4

def download_lastest_data():
    df = yf.download(
        TICKER,
        period="5d",
        interval="5m",
        auto_adjust=False,
        progress=False
    )

    if df.empty:
        raise ValueError("No data downloaded.")
    
    if df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()
    return df.dropna()

def make_features(df):
    df["Datetime"] = pd.to_datetime(df["Datetime"])

    df["close"] = df["Close"]
    df["open"] = df["Open"]
    df["high"] = df["High"]
    df["low"] = df["Low"]
    df["volume"] = df["Volume"]

    df["ema8"] = df["close"].ewm(span=8, adjust=False).mean()
    df["above_ema8"] = (df["close"] > df["ema8"]).astype(int)
    df["ema8_distance"] = df["close"] - df["ema8"]

    df["ma5"] = df["close"].rolling(5).mean()
    df["ma20"] = df["close"].rolling(20).mean()

    typical_price = (df["high"] + df["low"] + df["close"]) / 3
    df["tp_volume"] = typical_price * df["volume"]

    df["date"] = df["Datetime"].dt.date
    df["cum_tp_volume"] = df.groupby("date")["tp_volume"].cumsum()
    df["cum_volume"] = df.groupby("date")["volume"].cumsum()
    df["vwap"] = df["cum_tp_volume"] / df["cum_volume"]

    df["above_vwap"] = (df["close"] > df["vwap"]).astype(int)
    df["vwap_distance"] = df["close"] - df["vwap"]

    df["tr1"] = df["high"] - df["low"]
    df["tr2"] = abs(df["high"] - df["close"].shift(1))
    df["tr3"] = abs(df["low"] - df["close"].shift(1))
    df["tr"] = df[["tr1", "tr2", "tr3"]].max(axis=1)
    df["atr14"] = df["tr"].rolling(14).mean()

    df["volume_ma20"] = df["volume"].rolling(20).mean()
    df["volume_ratio"] = df["volume"] / df["volume_ma20"]
    df["volume_spike"] = (df["volume"] > df["volume_ma20"] * 2).astype(int)

    df["body"] = (df["close"] - df["open"]).abs()
    df["upper_shadow"] = df["high"] - df[["open", "close"]].max(axis=1)
    df["lower_shadow"] = df[["open", "close"]].min(axis=1) - df["low"]

    rolling_high = df["high"].rolling(48).max()
    rolling_low = df["low"].rolling(48).min()

    df["day_position"] = (
        (df["close"] - rolling_low) /
        (rolling_high - rolling_low)
    )

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    return df 

def load_model():
    model = xgb.XGBClassifier()
    model.load_model(MODEL_PATH)
    return model

def scan_once(model):
    raw_df = download_lastest_data()
    df = make_features(raw_df)

    latest = df.iloc[-1:].copy()
    X = latest[FEATURES]

    buy_probability = model.predict_proba(X)[0, 1]

    latest_row = latest.iloc[0]

    is_super_signal = (
        buy_probability >= BUY_PROB_THRESHOLD
        and latest_row["volume_ratio"] > VOLUME_RATIO_THRESHOLD
        and latest_row["above_vwap"] == 1
        and latest_row["day_position"] < DAY_POSITION_MAX
    )

    print("\n==============================")
    print("Samsung Live Signal Scanner")
    print("==============================")
    print("Time:", latest_row["Datetime"])
    print("Close:", latest_row["close"])
    print("Buy Probability:", round(buy_probability, 4))
    print("Volume Ratio:", round(latest_row["volume_ratio"], 4))
    print("VWAP Distance:", round(latest_row["vwap_distance"], 2))
    print("EMA8 Distance:", round(latest_row["ema8_distance"], 2))
    print("ATR14:", round(latest_row["atr14"], 2))
    print("Day Position:", round(latest_row["day_position"], 4))
    print("\nConditions:")
    print("Prob OK:",
        buy_probability >= BUY_PROB_THRESHOLD)
    print("Volume OK:",
        latest_row["volume_ratio"] > VOLUME_RATIO_THRESHOLD)
    print("VWAP OK:",
        latest_row["above_vwap"] == 1)
    print("Day Position OK:",
        latest_row["day_position"] < DAY_POSITION_MAX)
    
    if is_super_signal:
        print("\nSIGNAL: SUPER BUY WATCH")
    else:
        print("\nSIGNAL: WAIT")

def main():
    model = load_model()

    for _ in range(3):
        try:
            scan_once(model)
        except Exception as e:
            print("Error:", e)

        print("\nNext scan in 5 minutes...")
        time.sleep(300)

if __name__ == "__main__":
    main()