import pandas as pd

df = pd.read_csv("data/kiwoom_samsung_live.csv")

df["datetime"] = pd.to_datetime(df["datetime"])

market_df = df[
    (df["datetime"].dt.time >= pd.to_datetime("08:30").time()) &
    (df["datetime"].dt.time <= pd.to_datetime("15:30").time())
]

market_df.to_csv(
    "data/kiwoom_samsung_live_clean.csv",
    index=False
)

print("Rows left:", len(market_df))
print("Market hours only saved.")