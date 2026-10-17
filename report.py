W_NO = 3
W_FIO = 28
W_MAIL = 22
W_PHONE = 22
W_GROUP = 8
W_DOMAIN = 22

OK_FILE = "ok.txt"
ERRORS_FILE = "errors.txt"


def mask_phone(phone):
    return phone[:9] + "***-**-" + phone[-2:]


def cut(text, width):
    if len(text) > width:
        return text[:width - 3] + "..."
    return text


def print_table(good):
    header = (
        f"{'№':<{W_NO}}"
        f"{'ФИО':<{W_FIO}}"
        f"{'Почта':<{W_MAIL}}"
        f"{'Телефон':<{W_PHONE}}"
        f"{'Группа':<{W_GROUP}}"
    )
    print(header)
    print("-" * (W_NO + W_FIO + W_MAIL + W_PHONE + W_GROUP))
    for i, a in enumerate(good, 1):
        print(
            f"{i:<{W_NO}}"
            f"{cut(a['fio'], W_FIO):<{W_FIO}}"
            f"{cut(a['mail'], W_MAIL):<{W_MAIL}}"
            f"{mask_phone(a['phone']):<{W_PHONE}}"
            f"{a['group']:<{W_GROUP}}"
        )
    print("-" * (W_NO + W_FIO + W_MAIL + W_PHONE + W_GROUP))


def print_errors(bad):
    print(f"\nОтклонено строк: {len(bad)}")
    for line_no, line, reason in bad:
        print(f"  строка {line_no}: {reason}")
        print(f"      {line}")


def print_stats(good, total_lines):
    print(f"\nВсего строк в файле: {total_lines}")
    print(f"Принято: {len(good)} | Отклонено: {len(good) and 0 or 0}", end="")
    print()

    stat = {}
    for a in good:
        stat[a["group"]] = stat.get(a["group"], 0) + 1
    print("\nПо группам:")
    for group in sorted(stat):
        print(f"  {group}   {stat[group]}")


def save_files(good, bad):
    with open(OK_FILE, "w", encoding="utf-8") as f:
        for a in good:
            f.write(f"{a['fio']};{a['mail']};{a['phone']};{a['group']}\n")
    with open(ERRORS_FILE, "w", encoding="utf-8") as f:
        for line_no, line, reason in bad:
            f.write(f"строка {line_no}: {reason}\n{line}\n\n")