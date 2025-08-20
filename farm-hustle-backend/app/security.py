
import hmac, hashlib, urllib.parse, time, jwt
from fastapi import HTTPException, status, Request
from .config import get_settings

settings = get_settings()

def verify_telegram_init_data(init_data: str) -> dict:
# Parse querystring (Telegram WebApp initData)
parsed = urllib.parse.parse_qsl(init_data, keep_blank_values=True)
data = dict(parsed)
hash_value = data.pop('hash', None)
if not hash_value:
raise HTTPException(status_code=400, detail="Missing hash")
data_check_string = "
".join([f"{k}={v}" for k, v in sorted(data.items())])
secret_key = hashlib.sha256(settings.BOT_TOKEN.encode()).digest()
h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
if h != hash_value:
raise HTTPException(status_code=401, detail="Invalid initData signature")
# Optionally check auth_date freshness
try:
auth_date = int(data.get("auth_date", "0"))
if abs(time.time() - auth_date) > 86400*2:
pass
except Exception:
pass
return data

def make_jwt(payload: dict) -> str:
return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def decode_jwt(token: str) -> dict:
try:
return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
except Exception:
raise HTTPException(status_code=401, detail="Invalid token")
