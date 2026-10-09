def check_fio(raw):
    parts = raw.split()
    if len(parts) < 2:
        return None, "в ФИО меньше двух слов"
    fio = " ".join(parts).title()
    return fio, None


def check_mail(raw):
    mail = raw.strip().lower()
    if mail.count("@") != 1:
        return None, f"почта неверная: {raw.strip()}"
    local, domain = mail.split("@")
    if not local:
        return None, f"почта неверная: {raw.strip()}"
    if not domain:
        return None, f"почта неверная: {raw.strip()}"
    if "." not in domain:
        return None, f"почта неверная: {raw.strip()}"
    if domain.startswith(".") or domain.endswith("."):
        return None, f"почта неверная: {raw.strip()}"
    return mail, None


def check_phone(raw):
    digits = "".join(ch for ch in raw if ch.isdigit())
    if len(digits) != 11:
        return None, f"телефон неверный: {raw.strip()}"
    if digits[0] not in ("7", "8"):
        return None, f"телефон неверный: {raw.strip()}"
    phone = f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    return phone, None


def check_group(raw):
    group = raw.replace(" ", "").lower()
    if not group:
        return None, "пустая группа"
    return group, None


def parse_line(line):
    fields = line.split(";")
    if len(fields) != 4:
        return None, "полей меньше четырёх"
    raw_fio, raw_mail, raw_phone, raw_group = fields

    fio, err = check_fio(raw_fio)
    if err:
        return None, err
    mail, err = check_mail(raw_mail)
    if err:
        return None, err
    phone, err = check_phone(raw_phone)
    if err:
        return None, err
    group, err = check_group(raw_group)
    if err:
        return None, err

    return {"fio": fio, "mail": mail, "phone": phone, "group": group}, None