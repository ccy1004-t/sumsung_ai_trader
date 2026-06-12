import sys
import os
import requests

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from config import APP_KEY, APP_SECRET

url = "https://api.kiwoom.com/oauth2/token"

data = {
    "grant_type": "client_credentials",
    "appkey": APP_KEY,
    "secretkey": APP_SECRET
}

res = requests.post(url, json=data)

print(res.status_code)
print(res.text)