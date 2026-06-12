import os
import sys
import pandas as pd
import xgboost as xgb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

FEATURE_FILE = os.path.join(ROOT, "data", "kiwoom_samsung_features.csv")
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

df = pd.read_csv(FEATURE_FILE)

for col in FEATURES:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=FEATURES)

if df.empty:
    print("Not enough data yet. Need more 5min bars.")
    sys.exit()

latest = df.iloc[-1]

model = xgb.Booster()
model.load_model(MODEL_FILE)

X = latest[FEATURES].to_frame().T
X = X.apply(pd.to_numeric, errors="coerce")
X = X.astype(float)

dmatrix = xgb.DMatrix(X, feature_names=FEATURES)
buy_prob = float(model.predict(dmatrix)[0])

print("==============================")
print("Samsung AI Signal")
print("==============================")
print("Time:", latest["datetime"])
print("Close:", latest["close"])
print("Buy Probability:", round(buy_prob, 4))
print("VWAP Distance:", round(latest["vwap_distance"], 2))
print("EMA8 Distance:", round(latest["ema8_distance"], 2))
print("Volume Ratio:", round(latest["volume_ratio"], 4))
print("ATR14:", round(latest["atr14"], 2))
print("Day Position:", round(latest["day_position"], 4))

if buy_prob >= 0.80:
    signal = "BUY"
elif buy_prob >= 0.65:
    signal = "WATCH"
else:
    signal = "WAIT"

print("\nAI SIGNAL:", signal)