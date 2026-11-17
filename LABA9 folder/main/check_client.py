import requests

BASE = "http://127.0.0.1:5000"

r = requests.post(BASE + "/api/anketi", json={
    "tip": "s", "fio": "новиков иван",
    "mail": "nov@mail.ru", "phone": "89213334455", "gruppa": "09c33",
})
print(r.status_code, r.json())

r = requests.post(BASE + "/api/anketi", json={
    "tip": "s", "fio": "плохов петр",
    "mail": "plohovmail.ru", "phone": "89213334455", "gruppa": "09c33",
})
print(r.status_code, r.json())

print(requests.get(BASE + "/api/anketi").json())
print(requests.get(BASE + "/api/anketi?rol=студент").json())
print(requests.get(BASE + "/api/statistika").json())
print(requests.get(BASE + "/api/brak").json())
print(requests.get(BASE + "/api/anketi/99").status_code)