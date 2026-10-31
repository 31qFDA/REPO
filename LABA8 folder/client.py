import requests

BASE = "http://127.0.0.1:5000"
TIMEOUT = 5  # секунды


class ServerNedostupen(Exception):
    pass


def _zapros(method, path, **kwargs):
    try:
        r = requests.request(method, BASE + path, timeout=TIMEOUT, **kwargs)
    except (requests.ConnectionError, requests.Timeout) as e:
        raise ServerNedostupen(f"сервер недоступен: {e}")

    if r.status_code >= 500:
        raise ServerNedostupen(f"сервер ответил кодом {r.status_code}")

    return r


def poluchit_ankety():
    r = _zapros("GET", "/anketi")
    return r.json()


def poluchit_anketu(nomer):
    r = _zapros("GET", f"/anketi/{nomer}")
    if r.status_code == 404:
        return None
    return r.json()


def proverit_pochty(mail):
    r = _zapros("POST", "/proverka", json={"mail": mail})
    try:
        return bool(r.json().get("prinyato"))
    except ValueError:
        return False


def poluchit_statistiku():
    r = _zapros("GET", "/statistika")
    return r.json()