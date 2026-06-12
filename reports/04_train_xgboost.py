"""
strong_buy_label
什么位置属于高质量买点
"""

import pandas as pd 
import xgboost as xgb
from pathlib import Path
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)
from sklearn.model_selection import train_test_split

"""读取数据"""
DATA_PATH = Path(
    "data/samsung_labeled.csv"
)
df = pd.read_csv(DATA_PATH)

"""特征列"""
FEATURES = [
    #趋势
    "ema8",
    "ma5",
    "ma20",

    # VWAP
    "vwap",
    "vwap_distance",
    "above_vwap",

    # EMA
    "ema8_distance",
    "above_ema8",

    # 波动率
    "atr14",

    # 成交量
    "volume_ratio",
    "volume_spike",

    # K线
    "body",
    "upper_shadow",
    "lower_shadow",

    # 日内位置
    "day_position"
]

"""标签"""
TARGET = "strong_buy_label"

"""删除空值"""
df = df.dropna()

"""X / y"""
X = df[FEATURES]
y = df[TARGET]

"""时间切分(不要shuffle)"""
split_idx = int(len(df) * 0.8)

X_train= X.iloc[:split_idx]
X_test = X.iloc[split_idx:]

y_train = y.iloc[:split_idx]
y_test = y.iloc[split_idx:]

"""XGBoost 模型"""
positive_weight = (
    len(y_train[y_train == 0]) /
    len(y_train[y_train == 1])
)

model = xgb.XGBClassifier(

    n_estimators=300,
    max_depth=6,
    learning_rate=0.03,

    subsample=0.8,
    colsample_bytree=0.8,

    scale_pos_weight=positive_weight,

    random_state=42,

    eval_metric="logloss"
)

"""训练"""
model.fit(
    X_train,
    y_train
)
"""预测"""
"""预测类别"""
y_pred = model.predict(X_test)

"""概率"""
y_prob = model.predict_proba(X_test)[:, 1]

"""自定义阀值"""
threshold = 0.7

# 概率 > 0.8 才算强买点

y_pred = (
    y_prob > threshold
).astype(int)

"""结果"""
print("\nAccuracy:")
print(
    accuracy_score(y_test, y_pred)
)
print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred
    )
)
print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        y_pred
    )
)

"""特征重要性"""
importance_df = pd.DataFrame({
    "feature": FEATURES,
    "importance": model.feature_importances_
})
importance_df = (
    importance_df
    .sort_values(
        by="importance",
        ascending=False
    )
)
print("\nFeature Importance:")

"""保存模型"""
MODEL_PATH = Path(
    "models/xgb_strong_buy.json"
)
MODEL_PATH.parent.mkdir(
    exist_ok=True
)
model.save_model(MODEL_PATH)

print(
    "\nModel saved to:",
    MODEL_PATH
)