#  Copyright (c) 2024.  @Author: Aashish Mahajan
#
#

import pytest
from src.calculator import Calculator


class TestCalculator:
    def setup_method(self):
        self.calculator = Calculator()

    def test_add(self):
        assert self.calculator.add(2, 3) == 5

    def test_subtract(self):
        assert self.calculator.subtract(5, 3) == 2

    def test_multiply(self):
        assert self.calculator.multiply(2, 4) == 8

    def test_divide(self):
        assert self.calculator.divide(6, 2) == 3

    def test_divide_by_zero(self):
        with pytest.raises(ValueError):
            self.calculator.divide(10, 0)
