"""
模拟
真实买入
真实止盈
真实止损
而不是 只看未来最高点

假设买入价 300000
规则止盈： +4000
止损： -2000
如果未来先碰 304000算盈利 
如果先碰298000 算亏损
如果60分钟都没碰 就60分钟后收盘退出
"""

import pandas as pd
import xgboost as xgb
from pathlib import Path

# =========================
# 读取数据
# =========================

DATA_PATH = Path("data/samsung_labeled.csv")
MODEL_PATH = Path("models/xgb_strong_buy.json")

df = pd.read_csv(DATA_PATH)

# =========================
# 特征
# =========================

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

# =========================
# 加载模型
# =========================

model = xgb.XGBClassifier()
model.load_model(MODEL_PATH)

# =========================
# 概率预测
# =========================

X = df[FEATURES]

df["buy_probability"] = (
    model.predict_proba(X)[:, 1]
)

# =========================
# 参数
# =========================

threshold = 0.8

# ATR动态止盈止损

atr_tp_multiplier = 3.0
atr_sl_multiplier = 1.2

future_bars = 12

# 手续费 + 税费
fee_cost = 2500

# =========================
# 信号
# =========================

signals = df[
    (
        df["buy_probability"] >= threshold
    )
    &
    (
        df["volume_ratio"] > 1.5
    )
].copy()

# =========================
# 回测
# =========================

results = []

for idx in signals.index:

    entry_price = df.loc[idx, "close"]

    atr = df.loc[idx, "atr14"]

    take_profit = (
        atr * atr_tp_multiplier
    )

    stop_loss = (
        atr * atr_sl_multiplier
    )

    target_price = (
        entry_price + take_profit
    )

    stop_price = (
        entry_price - stop_loss
    )

    future_df = df.loc[
        idx + 1:
        idx + future_bars
    ]

    outcome = "timeout"

    pnl = 0

    for _, row in future_df.iterrows():

        high = row["high"]
        low = row["low"]

        # 先止盈

        if high >= target_price:

            outcome = "win"
            fee_cost = 2500

            pnl = take_profit - fee_cost

            break

        # 再止损

        if low <= stop_price:

            outcome = "loss"
            pnl = -stop_loss - fee_cost

            break

    # 超时退出

    if outcome == "timeout":

        last_close = (
            future_df.iloc[-1]["close"]
        )

        pnl = (
            last_close - entry_price
        ) - fee_cost

    results.append({

        "entry_index": idx,

        "entry_price": entry_price,

        "outcome": outcome,

        "pnl": pnl

    })

# =========================
# 结果统计
# =========================

results_df = pd.DataFrame(results)

win_rate = (
    (results_df["outcome"] == "win")
    .mean()
)

avg_pnl = (
    results_df["pnl"]
    .mean()
)

total_pnl = (
    results_df["pnl"]
    .sum()
)

profit_factor = (
    results_df[
        results_df["pnl"] > 0
    ]["pnl"].sum()
    /
    abs(
        results_df[
            results_df["pnl"] < 0
        ]["pnl"].sum()
    )
)

# =========================
# 输出
# =========================

print("\n========================")
print("Realistic Backtest")
print("========================")

print(
    "\nSignal Count:",
    len(results_df)
)

print(
    "\nWin Rate:",
    round(win_rate, 4)
)

print(
    "\nAverage PnL:",
    round(avg_pnl, 2)
)

print(
    "\nTotal PnL:",
    round(total_pnl, 2)
)

print(
    "\nProfit Factor:",
    round(profit_factor, 2)
)

print(
    "\nOutcome Counts:"
)

print(
    results_df["outcome"]
    .value_counts()
)

# =========================
# 保存
# =========================

SAVE_PATH = Path(
    "reports/realistic_backtest.csv"
)

results_df.to_csv(
    SAVE_PATH,
    index=False
)

print(
    "\nSaved to:",
    SAVE_PATH
)