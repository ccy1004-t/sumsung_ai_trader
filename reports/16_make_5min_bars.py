import os
import sys
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

IN_FILE = os.path.join(ROOT, "data", "kiwoom_samsung_live.csv")
OUT_FILE = os.path.join(ROOT, "data", "kiwoom_samsung_5min.csv")

df = pd.read_csv(IN_FILE)

df["datetime"] = pd.to_datetime(df["datetime"])
df = df.sort_values("datetime")

# 5分钟K线
bars = (
    df.set_index("datetime")
    .resample("5min")
    .agg({
        "price": ["first", "max", "min", "last"],
        "volume": "last",
        "change_rate": "last",
    })
)

bars.columns = ["open", "high", "low", "close", "volume", "change_rate"]
bars = bars.dropna().reset_index()

# 计算这一根5分钟内新增成交量
bars["volume_diff"] = bars["volume"].diff()
bars["volume_diff"] = bars["volume_diff"].fillna(0)

bars.to_csv(OUT_FILE, index=False)

print("5min bars saved:", OUT_FILE)
print(bars.tail(10))