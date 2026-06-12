"""Excel实时_Python_AI判断"""

import time
from datetime import datetime

import pandas as pd

EXCEL_PATH = "realtime.xlsx"
SAVE_PATH = "data/hts_realtime_log.csv"

print("KB HTS Excel Live Reader Started...\n")

history = []

while True:

    try:

        # 读取Excel
        df = pd.read_excel(EXCEL_PATH)

        # 取第一行
        row = df.iloc[0]

        # 这里改成你的Excel列名
        price = row["현재가"]
        volume = row["체결량"]
        strength = row["체결강도"]

        now = datetime.now()

        new_row = {
            "time": now,
            "price": price,
            "volume": volume,
            "strength": strength
        }

        history.append(new_row)

        log_df = pd.DataFrame(history)

        # 保存历史
        log_df.to_csv(
            SAVE_PATH,
            index=False
        )

        print("======================")
        print("Time:", now)
        print("Price:", price)
        print("Volume:", volume)
        print("Strength:", strength)
        print("======================\n")

    except Exception as e:

        print("Error:", e)

    # 每5秒读取一次
    time.sleep(5)