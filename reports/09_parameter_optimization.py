"""
自动测试不同止盈 / 止损组合
找出三星电子最适合的参数
"""

import pandas as pd
import xgboost as xgb
from pathlib import Path

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

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

X = df[FEATURES]

df["buy_probability"] = model.predict_proba(X)[:, 1]

# =========================
# 参数组合
# =========================

threshold_list = [0.6, 0.7, 0.8]
take_profit_list = [2500, 3000, 3500, 4000, 4500, 5000]
stop_loss_list = [1000, 1500, 2000, 2500]
future_bars = 12  # 60分钟
fee_cost = 2500

results = []

# =========================
# 回测函数
# =========================

def run_backtest(data, threshold, take_profit, stop_loss):

    signals = data[
    (
        data["buy_probability"] >= threshold
    )
    &
    (
        data["volume_ratio"] > 1.5
    )
    &
    (
        data["above_vwap"] == 1
    )
].copy()

    trade_results = []

    for idx in signals.index:

        entry_price = data.loc[idx, "close"]
        target_price = entry_price + take_profit
        stop_price = entry_price - stop_loss

        future_df = data.loc[
            idx + 1:
            idx + future_bars
        ]

        if len(future_df) == 0:
            continue

        outcome = "timeout"
        pnl = 0

        for _, row in future_df.iterrows():

            high = row["high"]
            low = row["low"]

            if high >= target_price:
                outcome = "win"
                pnl = take_profit - fee_cost
                break

            if low <= stop_price:
                outcome = "loss"
                pnl = -stop_loss - fee_cost
                break

        if outcome == "timeout":
            last_close = future_df.iloc[-1]["close"]
            pnl = (last_close - entry_price) - fee_cost

        trade_results.append({
            "outcome": outcome,
            "pnl": pnl
        })

    if len(trade_results) == 0:
        return None

    result_df = pd.DataFrame(trade_results)

    signal_count = len(result_df)

    win_rate = (
        (result_df["outcome"] == "win").mean()
    )

    avg_pnl = result_df["pnl"].mean()
    total_pnl = result_df["pnl"].sum()

    total_profit = result_df[
        result_df["pnl"] > 0
    ]["pnl"].sum()

    total_loss = abs(
        result_df[
            result_df["pnl"] < 0
        ]["pnl"].sum()
    )

    if total_loss == 0:
        profit_factor = 999
    else:
        profit_factor = total_profit / total_loss

    loss_count = (
        result_df["outcome"] == "loss"
    ).sum()

    timeout_count = (
        result_df["outcome"] == "timeout"
    ).sum()

    return {
        "threshold": threshold,
        "take_profit": take_profit,
        "stop_loss": stop_loss,
        "signal_count": signal_count,
        "win_rate": win_rate,
        "avg_pnl": avg_pnl,
        "total_pnl": total_pnl,
        "profit_factor": profit_factor,
        "loss_count": loss_count,
        "timeout_count": timeout_count
    }

# =========================
# 参数循环
# =========================

for threshold in threshold_list:
    for take_profit in take_profit_list:
        for stop_loss in stop_loss_list:

            result = run_backtest(
                df,
                threshold,
                take_profit,
                stop_loss
            )

            if result is not None:
                results.append(result)

# =========================
# 保存结果
# =========================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by=["profit_factor", "avg_pnl"],
    ascending=False
)

SAVE_PATH = Path(
    "reports/parameter_optimization.csv"
)

SAVE_PATH.parent.mkdir(exist_ok=True)

results_df.to_csv(
    SAVE_PATH,
    index=False
)

print("\n========================")
print("Top Parameter Results")
print("========================\n")

print(results_df.head(20))

print("\nSaved to:", SAVE_PATH)