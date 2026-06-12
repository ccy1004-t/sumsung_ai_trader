import sys
import os
import time
import requests
import pandas as pd
from datetime import datetime, time as dt_time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from config import APP_KEY, APP_SECRET

OUT_FILE = os.path.join(ROOT, "data", "kiwoom_samsung_live.csv")


def get_token():
    url = "https://api.kiwoom.com/oauth2/token"

    data = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "secretkey": APP_SECRET
    }

    res = requests.post(url, json=data)
    res.raise_for_status()
    return res.json()["token"]


def get_samsung_price(token):
    url = "https://api.kiwoom.com/api/dostk/stkinfo"

    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "authorization": f"Bearer {token}",
        "cont-yn": "N",
        "next-key": "",
        "api-id": "ka10001"
    }

    data = {
        "stk_cd": "005930"
    }

    res = requests.post(url, headers=headers, json=data)
    res.raise_for_status()
    return res.json()


def clean_number(x):
    return int(str(x).replace("+", "").replace("-", "").replace(",", ""))


token = get_token()
print("TOKEN OK")
print("Start Samsung live scanner... Ctrl+C to stop")

while True:

    now = datetime.now().time()

    START_TIME = dt_time(8, 30)
    END_TIME = dt_time(15, 30)

    if not (START_TIME <= now <= END_TIME):
        print("Market Closed - Waiting...")
        time.sleep(300)
        continue

    try:
        data = get_samsung_price(token)

        row = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "code": data["stk_cd"],
            "name": data["stk_nm"],
            "price": clean_number(data["cur_prc"]),
            "change_rate": float(str(data["flu_rt"]).replace("+", "")),
            "volume": clean_number(data["trde_qty"]),
        }

        df = pd.DataFrame([row])

        if not os.path.exists(OUT_FILE):
            df.to_csv(OUT_FILE, index=False)
        else:
            df.to_csv(OUT_FILE, mode="a", header=False, index=False)

        print(row)

        time.sleep(60)

    except KeyboardInterrupt:
        print("Stopped.")
        break

    except Exception as e:
        print("ERROR:", e)
        time.sleep(5)