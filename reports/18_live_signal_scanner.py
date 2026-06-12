print("START")
import os
import sys
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

FEATURE_FILE = os.path.join(ROOT, "data", "kiwoom_samsung_features.csv")

df = pd.read_csv(FEATURE_FILE)

latest = df.iloc[-1]

close = latest["close"]
vwap_distance = latest["vwap_distance"]
ema8_distance = latest["ema8_distance"]
volume_ratio = latest["volume_ratio"]
atr14 = latest["atr14"]
day_position = latest["day_position"]

print("==============================")
print("Samsung Live Signal Scanner")
print("==============================")
print("Time:", latest["datetime"])
print("Close:", close)
print("VWAP Distance:", vwap_distance)
print("EMA8 Distance:", ema8_distance)
print("Volume Ratio:", volume_ratio)
print("ATR14:", atr14)
print("Day Position:", day_position)

conditions = {
    "VWAP OK": vwap_distance > 0,
    "EMA8 OK": ema8_distance > 0,
    "Volume OK": volume_ratio >= 1.2,
    "Day Position OK": 0.25 <= day_position <= 0.85,
}

print("\nConditions:")
for k, v in conditions.items():
    print(k + ":", v)

score = sum(conditions.values())

print("\nScore:", score, "/ 4")

if score >= 4:
    signal = "BUY"
elif score == 3:
    signal = "WATCH"
else:
    signal = "WAIT"

if pd.isna(atr14):
    signal = "WAIT"
    print("\nNote: ATR14 not ready yet. Need at least 14 bars.")

print("\nSIGNAL:", signal)