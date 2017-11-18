import numpy
import pytest
from datetime import datetime

from app import get_longest_interval


def test_get_longest_interval_nan():
    assert get_longest_interval(()) is numpy.NAN
    assert get_longest_interval((datetime(2017, 1, 1),)) is numpy.NAN


@pytest.mark.parametrize("dates, expected", [
    ((datetime(2017, 1, 1), datetime(2017, 1, 1)), 0),
    ((datetime(2017, 1, 1), datetime(2017, 1, 10)), 9),
    ((datetime(2017, 1, 10), datetime(2017, 1, 1)), 9),
    ((datetime(2017, 1, 10), datetime(2017, 1, 1), datetime(2017, 1, 8)), 7),
])
def test_get_longest_interval(dates, expected):
    assert get_longest_interval(dates) == expected
