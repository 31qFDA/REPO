"""#Задание 1
from calc import summa


def test_summa_dva_polozhitelnyh():
    assert summa(2, 3) == 5


def test_summa_s_nulyom():
    assert summa(0, 5) == 5
#Задание 2
from calc import skidka
def test_skidka_10_ot_1000():
    assert skidka(1000, 10) == 900.0

#Задание 3
import pytest
from calc import skidka, srednee


def test_skidka_slishkom_bolshaya():
    with pytest.raises(ValueError):
        skidka(1000, 95)


def test_srednee_pustoy_spisok():
    with pytest.raises(ValueError):
        srednee([])

#Задание 4
import pytest
from calc import srednee


@pytest.mark.parametrize("chisla, ozhidaemoe", [
    ([5], 5),
    ([2, 4], 3),
    ([1, 2, 3, 4], 2.5),
    ([-2, 2], 0),
])
def test_srednee_parametrizaciya(chisla, ozhidaemoe):
    assert srednee(chisla) == ozhidaemoe
"""
#Задание 5
import pytest
from wordcount import chastota


@pytest.fixture
def fayl_s_tekstom(tmp_path):
    put = tmp_path / "text.txt"
    put.write_text("Мама мыла раму. Рама, мама, рама!", encoding="utf-8")
    return put


def test_slova_mama_i_rama(fayl_s_tekstom):
    slovar = chastota(fayl_s_tekstom)
    assert slovar["мама"] == 2
    assert slovar["рама"] == 2


def test_net_kluchey_so_znakami(fayl_s_tekstom):
    slovar = chastota(fayl_s_tekstom)
    assert "рама," not in slovar
    assert "раму." not in slovar


def test_chetyre_raznyh_slova(fayl_s_tekstom):
    slovar = chastota(fayl_s_tekstom)
    assert len(slovar) == 4