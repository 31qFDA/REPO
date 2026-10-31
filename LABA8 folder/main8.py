import json

import client
from people import AnketaError, Student, Teacher
from registry import Registry


def sdelat_obekt(d):
    tip = d.get("tip")
    if tip == "s":
        return Student(d["fio"], d["mail"], d["phone"], d["gruppa"])
    if tip == "t":
        return Teacher(d["fio"], d["mail"], d["phone"], d["kafedra"])
    raise AnketaError(f"неизвестный тип: {tip}")


def zagruzit_s_servera():
    dannyе = client.poluchit_ankety()
    good, bad = [], []
    for d in dannyе:
        nomer = d.get("nomer")
        try:
            good.append(sdelat_obekt(d))
        except (AnketaError, KeyError) as e:
            bad.append((nomer, d, str(e)))
    good.sort()
    return good, bad


def zagruzit_iz_fayla():
    r = Registry()
    if not r.load("anketa.txt"):
        return None, None
    return r.good, r.bad


def pechatat_tablitsu(good):
    print(f"{'№':<3} {'ФИО':<30} {'Роль':<15} {'Телефон':<20} {'Доп.'}")
    print("-" * 90)
    for i, p in enumerate(good, 1):
        print(f"{i:<3} {p.fio:<30} {p.role():<15} {p.phone:<20} {p.extra()}")
    print(f"Принято: {len(good)}")


def main():
    try:
        good, bad = zagruzit_s_servera()
        istochnik = "сервер"
    except client.ServerNedostupen as e:
        print(f"Сервер недоступен: {e}")
        print("Переключаюсь на запасной источник — anketa.txt")
        good, bad = zagruzit_iz_fayla()
        if good is None:
            print("Нет ни сервера, ни файла anketa.txt. Работа завершена.")
            return
        istochnik = "файл anketa.txt"

    print(f"Источник данных: {istochnik}\n")

    pechatat_tablitsu(good)
    print(f"Отклонено: {len(bad)}\n")

    if bad:
        print("Отклонённые записи:")
        for nomer, d, prichina in bad:
            print(f"  №{nomer}: {prichina}")
        print()

    print("Сводка по ролям (своя):")
    svoya = {}
    for p in good:
        svoya[p.role()] = svoya.get(p.role(), 0) + 1
    for rol, kol in svoya.items():
        print(f"  {rol}: {kol}")

    try:
        stat = client.poluchit_statistiku()
        print("\nСтатистика сервера:", stat)
    except client.ServerNedostupen as e:
        print(f"\nСтатистику получить не удалось: {e}")

    print("\nПроверка почт принятых анкет:")
    rezultaty = []
    for p in good:
        try:
            ok = client.proverit_pochty(p.mail)
            print(f"  {p.mail}: {'принята' if ok else 'отклонена'}")
            rezultaty.append({"mail": p.mail, "prinyato": ok})
        except client.ServerNedostupen as e:
            print(f"  {p.mail}: проверить не удалось ({e})")
            rezultaty.append({"mail": p.mail, "prinyato": None})

    otchet = {
        "istochnik": istochnik,
        "prinyato": len(good),
        "otkloneno": len(bad),
        "svodka_po_rolyam": svoya,
        "otklonennye": [{"nomer": n, "prichina": pr} for n, _, pr in bad],
        "proverka_pochty": rezultaty,
    }
    with open("otchet.json", "w", encoding="utf-8") as f:
        json.dump(otchet, f, ensure_ascii=False, indent=2)
    print("\nИтог сохранён в otchet.json")


main()