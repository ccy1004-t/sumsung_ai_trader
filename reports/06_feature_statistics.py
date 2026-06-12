"""
AI到底在学什么
"""

import pandas as pd 
from pathlib import Path 

"""读取数据"""
DATA_PATH = Path(
    "data/samsung_labeled.csv"
)
df = pd.read_csv(DATA_PATH)

"""强买点/普通点"""
strong_df = df[
    df["strong_buy_label"] == 1
]
normal_df = df[
    df["strong_buy_label"] == 0
]

"""要统计的特征"""
FEATURES = [
    "vwap_distance",
    "ema8_distance",

    "volume_ratio",

    "upper_shadow",
    "lower_shadow",

    "atr14",
    
    "day_position"
]

"""输出统计"""
print("\n===================")
print("Strong Buy Statistics")
print("====================")

for feature in FEATURES:
    print(f"\n{feature}")
    print(
        "Strong Buy Mean:",
        round(
            strong_df[feature].mean(),
            4
        )
    )
    print(
        "Normal Mean:",
        round(
            normal_df[feature].mean(),
            4
        )
    )

    """保存统计结果"""
stats = []

for feature in FEATURES:

    stats.append({

        "feature": feature,

        "strong_buy_mean":

            strong_df[feature].mean(),

        "normal_mean":

            normal_df[feature].mean(),

        "difference":

            strong_df[feature].mean()

            -

            normal_df[feature].mean()

    })

stats_df = pd.DataFrame(stats)

SAVE_PATH = Path(

    "reports/feature_statistics.csv"

)

SAVE_PATH.parent.mkdir(

    exist_ok=True

)

stats_df.to_csv(

    SAVE_PATH,

    index=False

)

print("\nSaved to:", SAVE_PATH)