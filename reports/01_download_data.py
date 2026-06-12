"""
下载三星电子 005930.KS 的5分钟数据
保存到 data/samsung_5m.csv
"""

import yfinance as yf 
import pandas as pd 
from pathlib import Path 

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

ticker = "005930.KS"

df = yf.download(
    ticker,
    period="60d",
    interval="5m",
    auto_adjust=False,
    progress=True
)

# 如果是多层表头，拉平
if isinstance(df.columns, type(df.columns)) and hasattr(df.columns, "nlevels"):
    if df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)

df = df.dropna()

# 把时间索引变成 Datetime 列
df = df.reset_index()

df.to_csv(DATA_DIR / "samsung_5m.csv")

print(df.tail())
print("Saved to data/samsung_5m.csv")