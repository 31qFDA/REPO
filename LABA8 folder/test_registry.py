import pytest
from registry import Registry


@pytest.fixture
def zhurnal(tmp_path):
    f = tmp_path / "ankety.txt"
    f.write_text(
        "s;иванов иван;ivan@mail.ru;89123456789;иу1\n"
        "t;петров петр;petr@mail.ru;89123456780;кафедра\n"
        "s;сидоров сидор;sid@mail.ru;89123456781;иу2\n"
        "x;плохой тип;bad@mail.ru;89123456782;extra\n"
        "s;мало полей;bad@mail.ru\n"
        "s;иванов иван;badmail;89123456789;иу1\n",
        encoding="utf-8",
    )
    r = Registry()
    r.load(str(f))
    return r


def test_pustoy_zhurnal():
    assert len(Registry()) == 0


def test_posle_zagruzki_tri(zhurnal):
    assert len(zhurnal) == 3


def test_brak_tri(zhurnal):
    assert len(zhurnal.bad) == 3


def test_nomera_strok_braka(zhurnal):
    nomera = [n for n, _, _ in zhurnal.bad]
    assert nomera == [4, 5, 6]


def test_net_fayla():
    r = Registry()
    assert r.load("net_takogo_fayla.txt") is False


def test_stat_po_rolyam(zhurnal):
    assert zhurnal.stats_by_role() == {"студент": 2, "преподаватель": 1}


def test_stat_po_gruppam(zhurnal):
    assert zhurnal.stats_by_group() == {"иу1": 1, "иу2": 1}


def test_perebor_ciklom(zhurnal):
    names = [p.fio for p in zhurnal.good]
    assert len(names) == 3


def test_sortirovka(zhurnal):
    fio = [p.fio for p in zhurnal.good]
    assert fio == sorted(fio)


def test_save_ok(zhurnal, tmp_path, monkeypatch):
    import registry
    monkeypatch.setattr(registry, "OK_FILE", str(tmp_path / "ok.txt"))
    zhurnal.save_ok()
    lines = (tmp_path / "ok.txt").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3


def test_save_errors(zhurnal, tmp_path, monkeypatch):
    import registry
    monkeypatch.setattr(registry, "ERRORS_FILE", str(tmp_path / "errors.txt"))
    zhurnal.save_errors()
    text = (tmp_path / "errors.txt").read_text(encoding="utf-8")
    assert "неизвестный тип" in text

#Дополнение (выдаёт ошибку)
def test_familya_na_yo(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text(
        "s;яковлева анна;ya@mail.ru;89123456789;иу1\n"
        "s;ёлкина елена;el@mail.ru;89123456780;иу1\n"
        "s;абрамова алла;al@mail.ru;89123456781;иу1\n",
        encoding="utf-8",
    )
    r = Registry()
    r.load(str(f))
    familii = [p.fio.split()[0] for p in r.good]
    assert familii == ["Абрамова", "Ёлкина", "Яковлева"]