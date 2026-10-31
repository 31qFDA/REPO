import requests

BASE = "http://127.0.0.1:5000"
#Задание 1
r = requests.get(BASE + "/")
print("Код:", r.status_code)
print("Тип r.text:", type(r.text))
print("Тип r.json():", type(r.json()))
print("Название сервиса:", r.json().get("servis"))
print("\n\n")
#Задание 2
r = requests.get(BASE + "/anketi")
data = r.json()
print("Пришло анкет:", len(data))
print("ФИО первой:", data[0]["fio"])
print("\n\n")
#Задание 3
r = requests.get(BASE + "/anketi/99")
print("Код:", r.status_code)
print("r.ok:", r.ok)
print("Текст ошибки:", r.json().get("oshibka"))
print("\n\n")
#Задание 4
r = requests.get(BASE + "/anketi", params={"tip": "t"})
print("URL запроса:", r.url)
for p in r.json():
    print(p["fio"], "-", p["kafedra"])
print("\n\n")
#Задание 5
for mail in ["ivanov@mail.ru", "kuznetsov.mail.ru"]:
    r = requests.post(BASE + "/proverka", json={"mail": mail})
    print("Почта:", mail, "| Код:", r.status_code, "| Принято:", r.json().get("prinyato"))