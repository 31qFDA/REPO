import os
from people import AnketaError, Student, Teacher

OK_FILE = "ok.txt"
ERRORS_FILE = "errors.txt"
W_NO = 3
W_FIO = 28
W_ROLE = 15
W_EXTRA = 16
W_PHONE = 22


class Registry:
    def __init__(self):
        self.good = []
        self.bad = []

    def add(self, person):
        self.good.append(person)

    def load(self, filename):
        if not os.path.exists(filename):
            return False
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line_no, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped:
                continue
            fields = stripped.split(";")
            if len(fields) != 5:
                self.bad.append((line_no, stripped, "полей не пять"))
                continue
            tip, fio, mail, phone, extra = fields
            tip = tip.strip().lower()
            try:
                if tip == "s":
                    person = Student(fio, mail, phone, extra)
                elif tip == "t":
                    person = Teacher(fio, mail, phone, extra)
                else:
                    raise AnketaError(f"неизвестный тип: {tip}")
                self.add(person)
            except AnketaError as e:
                self.bad.append((line_no, stripped, str(e)))
        self.good.sort()
        return True

    def stats_by_role(self):
        stat = {}
        for p in self.good:
            stat[p.role()] = stat.get(p.role(), 0) + 1
        return stat

    def stats_by_group(self):
        stat = {}
        for p in self.good:
            if p.role() == "студент":
                g = p.extra()
                stat[g] = stat.get(g, 0) + 1
        return stat

    def save_ok(self):
        with open(OK_FILE, "w", encoding="utf-8") as f:
            for p in self.good:
                f.write(f"{p.fio};{p.mail};{p.phone};{p.role()};{p.extra()}\n")

    def save_errors(self):
        with open(ERRORS_FILE, "w", encoding="utf-8") as f:
            for line_no, line, reason in self.bad:
                f.write(f"строка {line_no}: {reason}\n{line}\n\n")

    def print_table(self):
        header = (
            f"{'№':<{W_NO}}"
            f"{'ФИО':<{W_FIO}}"
            f"{'Роль':<{W_ROLE}}"
            f"{'Группа/кафедра':<{W_EXTRA}}"
            f"{'Телефон':<{W_PHONE}}"
        )
        print(header)
        print("-" * (W_NO + W_FIO + W_ROLE + W_EXTRA + W_PHONE))
        for i, p in enumerate(self.good, 1):
            fio = p.fio
            if len(fio) > W_FIO:
                fio = fio[:W_FIO - 3] + "..."
            print(
                f"{i:<{W_NO}}"
                f"{fio:<{W_FIO}}"
                f"{p.role():<{W_ROLE}}"
                f"{p.extra():<{W_EXTRA}}"
                f"{p.masked_phone():<{W_PHONE}}"
            )
        print("-" * (W_NO + W_FIO + W_ROLE + W_EXTRA + W_PHONE))

    def print_errors(self):
        print(f"\nОтклонено строк: {len(self.bad)}")
        for line_no, line, reason in self.bad:
            print(f"  строка {line_no}: {reason}")
            print(f"      {line}")

    def __len__(self):
        return len(self.good)