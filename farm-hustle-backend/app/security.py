# app/security.py
import hmac, hashlib, urllib.parse, time
from fastapi import HTTPException
import jwt  # PyJWT
from .config import get_settings

settings = get_settings()

def verify_telegram_init_data(init_data: str) -> dict:
    if not init_data:
        raise HTTPException(status_code=400, detail="Empty initData")

    # 1) Парсим query-string (URL-decoded значения)
    pairs = urllib.parse.parse_qsl(init_data, keep_blank_values=True)

    data = {}
    hash_value = None
    for k, v in pairs:
        if k == "hash":
            hash_value = v
        else:
            # ВАЖНО: signature НЕ исключаем — она должна входить в проверку
            data[k] = v
    if not hash_value:
        raise HTTPException(status_code=400, detail="Missing hash")

    # 2) data_check_string: "k=v" по возрастанию ключей, разделитель — '\n'
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))

    # 3) Секрет для Mini Apps: HMAC-SHA256('WebAppData', BOT_TOKEN)
    bot_token = (settings.BOT_TOKEN or "").strip()
    if not bot_token:
        raise HTTPException(status_code=500, detail="BOT_TOKEN not set")

    secret_key = hmac.new(
        key=b"WebAppData",
        msg=bot_token.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()

    # 4) Ожидаемый hash
    expected_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_hash, hash_value):
        # — временные логи на случай странных кейсов (можно убрать после отладки) —
        # print("CHECK_KEYS", list(sorted(data.keys())))
        # print("CHECK_STR", data_check_string[:400])
        raise HTTPException(status_code=401, detail="Invalid initData signature")

    # (опц.) свежесть
    try:
        auth_date = int(data.get("auth_date", "0"))
        if auth_date and time.time() - auth_date > 172800:
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
