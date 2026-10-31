class AnketaError(Exception):
    pass

class Person:
    def __init__(self, fio, mail, phone):
        self.fio = self.check_fio(fio)
        self.mail = self.check_mail(mail)
        self.phone = self.check_phone(phone)

    @staticmethod
    def check_fio(raw):
        parts = raw.split()
        if len(parts) < 2:
            raise AnketaError("в ФИО меньше двух слов")
        result = []
        for part in parts:
            result.append("-".join(chast.title() for chast in part.split("-")))
        return " ".join(result)

    @staticmethod
    def check_mail(raw):
        mail = raw.strip().lower()
        if " " in mail:
            raise AnketaError(f"почта неверная: {raw.strip()}")
        if mail.count("@") != 1:
            raise AnketaError(f"почта неверная: {raw.strip()}")
        local, domain = mail.split("@")
        if not local:
            raise AnketaError(f"почта неверная: {raw.strip()}")
        if not domain:
            raise AnketaError(f"почта неверная: {raw.strip()}")
        if "." not in domain:
            raise AnketaError(f"почта неверная: {raw.strip()}")
        if domain.startswith(".") or domain.endswith("."):
            raise AnketaError(f"почта неверная: {raw.strip()}")
        return mail

    def sort_key(self):
        return self.fio.replace("ё", "е").replace("Ё", "Е")

    def __lt__(self, other):
        return self.sort_key() < other.sort_key()

    @staticmethod
    def check_phone(raw):
        digits = "".join(ch for ch in raw if ch.isdigit())
        if len(digits) != 11:
            raise AnketaError(f"телефон неверный: {raw.strip()}")
        if digits[0] not in ("7", "8"):
            raise AnketaError(f"телефон неверный: {raw.strip()}")
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"

    def masked_phone(self):
        return self.phone[:9] + "***-**-" + self.phone[-2:]

    def short_fio(self):
        parts = self.fio.split()
        if len(parts) >= 3:
            return f"{parts[0]} {parts[1][0]}. {parts[2][0]}."
        return f"{parts[0]} {parts[1][0]}."

    def role(self):
        return "человек"

    def extra(self):
        return ""

    def __str__(self):
        return f"{self.fio}"

    def __lt__(self, other):
        return self.fio < other.fio


class Student(Person):
    def __init__(self, fio, mail, phone, gruppa):
        super().__init__(fio, mail, phone)
        self.gruppa = self.check_gruppa(gruppa)

    @staticmethod
    def check_gruppa(raw):
        gruppa = raw.replace(" ", "").lower()
        if not gruppa:
            raise AnketaError("пустая группа")
        return gruppa

    def role(self):
        return "студент"

    def extra(self):
        return self.gruppa


class Teacher(Person):
    def __init__(self, fio, mail, phone, kafedra):
        super().__init__(fio, mail, phone)
        self.kafedra = self.check_kafedra(kafedra)

    @staticmethod
    def check_kafedra(raw):
        kafedra = " ".join(raw.split())
        if not kafedra:
            raise AnketaError("пустая кафедра")
        return kafedra

    def role(self):
        return "преподаватель"

    def extra(self):
        return self.kafedra