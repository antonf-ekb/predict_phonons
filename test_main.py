from main import calculate_values
from main import get_models


def test_calculate_values():
    values = calculate_values("Mn2CoCrP2", get_models())
    result = [6.07, 163, 95]
    assert values[0]*0.5 <= result[0] <= values[0]*1.5
    assert values[1] * 0.7 <= result[1] <= values[1] * 1.3
    assert values[2] * 0.5 <= result[2] <= values[2] * 1.5


def test_calculate_values_bad():
    assert calculate_values("m", get_models()) == [0]


def test_calculate_values_empty():
    assert calculate_values("", get_models()) == [0]
