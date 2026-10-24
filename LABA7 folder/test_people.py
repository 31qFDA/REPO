import pytest
from people import AnketaError, Person, Student, Teacher


@pytest.mark.parametrize("raw, ozhidanie", [
    ("иванов иван", "Иванов Иван"),
    ("ИВАНОВ ИВАН", "Иванов Иван"),
    ("  иванов   иван  ", "Иванов Иван"),
    ("пЕтРов пЁтР", "Петров Пётр"),
])
def test_fio_privoditsya(raw, ozhidanie):
    assert Person.check_fio(raw) == ozhidanie


def test_fio_iz_odnogo_slova():
    with pytest.raises(AnketaError):
        Person.check_fio("иванов")


@pytest.mark.parametrize("raw, ozhidanie", [
    ("IVAN@MAIL.RU", "ivan@mail.ru"),
    ("  Ivan@Mail.Ru  ", "ivan@mail.ru"),
])
def test_mail_nizhniy_registr(raw, ozhidanie):
    assert Person.check_mail(raw) == ozhidanie


@pytest.mark.parametrize("raw", [
    "ivanmail.ru",
    "ivan@@mail.ru",
    "@mail.ru",
    "ivan@mail",
])
def test_plohaya_pochta(raw):
    with pytest.raises(AnketaError):
        Person.check_mail(raw)


@pytest.mark.parametrize("raw", [
    "+7 (912) 345-67-89",
    "89123456789",
    "8 912 345 67 89",
    "7-912-345-67-89",
])
def test_telefon_privoditsya(raw):
    assert Person.check_phone(raw) == "+7 (912) 345-67-89"


@pytest.mark.parametrize("raw", [
    "123",
    "99123456789",
    "+7 (912) 345-67-8",
    "",
])
def test_plohoy_telefon(raw):
    with pytest.raises(AnketaError):
        Person.check_phone(raw)


def test_telefon_maska():
    p = Person("иванов иван", "ivan@mail.ru", "89123456789")
    assert p.masked_phone() == "+7 (912) ***-**-89"


def test_fio_sokrashchaetsya():
    p = Person("иванов иван петрович", "ivan@mail.ru", "89123456789")
    assert p.short_fio() == "Иванов И. П."


def test_roli_raznye():
    s = Student("иванов иван", "ivan@mail.ru", "89123456789", "иу1")
    t = Teacher("петров петр", "petr@mail.ru", "89123456780", "кафедра")
    assert s.role() == "студент"
    assert t.role() == "преподаватель"


def test_student_bez_gruppy():
    with pytest.raises(AnketaError):
        Student("иванов иван", "ivan@mail.ru", "89123456789", "   ")


def test_stroka_student():
    from registry import Registry
    from unittest.mock import patch
    with patch("builtins.open", create=True):
        pass
    s = Student("иванов иван", "ivan@mail.ru", "89123456789", "иу1")
    assert isinstance(s, Student)


def test_stroka_prepodavatel():
    t = Teacher("петров петр", "petr@mail.ru", "89123456780", "кафедра")
    assert isinstance(t, Teacher)


@pytest.mark.parametrize("stroka", [
    "x;иванов иван;ivan@mail.ru;89123456789;иу1",
    "s;иванов иван;ivan@mail.ru",
    "",
])
def test_plohaya_stroka(stroka, tmp_path):
    from registry import Registry
    f = tmp_path / "a.txt"
    f.write_text(stroka + "\n", encoding="utf-8")
    r = Registry()
    r.load(str(f))
    assert len(r.good) == 0

#Дополнения
def test_dvoynaya_familya():
    assert Person.check_fio("петров-водкин кузьма") == "Петров-Водкин Кузьма"


def test_probel_vnutri_pochty():
    with pytest.raises(AnketaError):
        Person.check_mail("iv anov@mail.ru")
