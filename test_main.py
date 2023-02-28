from main import calculate_values
from main import get_models


def test_calculate_values():
    assert calculate_values("Mn2CoCrP2", get_models()) == [6.07, 163, 95]


def test_calculate_values_bad():
    assert calculate_values("M", get_models()) == [0]


def test_calculate_values_empty():
    assert calculate_values("", get_models()) == [0]
