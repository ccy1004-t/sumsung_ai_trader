import requests

APP_KEY = "IRTURs5Q2C_a0SD1KONYH_QcK5H2pJWYo7B0o48jezM"
APP_SECRET = "F8dljGykLaozAuedjV_uk5hwY1g-DP5b2fDRiANXh2w"

url = "https://api.kiwoom.com/oauth2/token"

data = {
    "grant_type": "client_credentials",
    "appkey": APP_KEY,
    "secretkey": APP_SECRET
}

res = requests.post(url, json=data)

print("status:", res.status_code)
print(res.text)