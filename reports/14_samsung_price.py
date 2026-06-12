import sys
import os
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from config import APP_KEY, APP_SECRET

# 1. 获取 token
token_url = "https://api.kiwoom.com/oauth2/token"

token_data = {
    "grant_type": "client_credentials",
    "appkey": APP_KEY,
    "secretkey": APP_SECRET
}

token_res = requests.post(token_url, json=token_data)
token_json = token_res.json()

access_token = token_json["token"]
print("TOKEN OK")

# 2. 查询 삼성전자 기본정보
url = "https://api.kiwoom.com/api/dostk/stkinfo"

headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "authorization": f"Bearer {access_token}",
    "cont-yn": "N",
    "next-key": "",
    "api-id": "ka10001"
}

data = {
    "stk_cd": "005930"
}

res = requests.post(url, headers=headers, json=data)

result = res.json()

print("==== Samsung Price ====")
print("Code:", result["stk_cd"])
print("Name:", result["stk_nm"])
print("Current Price:", result["cur_prc"])
print("Change Rate:", result["flu_rt"])
print("Volume:", result["trde_qty"])
print("Return Code:", result["return_code"])
print("Message:", result["return_msg"])