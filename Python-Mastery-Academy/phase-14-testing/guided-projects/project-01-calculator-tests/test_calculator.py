"""
Calculator Test Suite
Phase 14: Testing

PURPOSE:
  Demonstrates professional pytest testing.
  Tests the calculator engine from Phase 04.

HOW TO RUN:
  pytest test_calculator.py -v
  pytest test_calculator.py -v --cov=. --cov-report=html

INSTALL:
  pip install pytest pytest-cov
"""

import pytest
import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../phase-04-functions/guided-projects/project-01-calculator-engine"))

# ─── Calculator functions (inline for self-contained testing) ─────────────────

def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float | None:
    if b == 0:
        return None
    return a / b

def power(base: float, exponent: float) -> float:
    return base ** exponent

def square_root(n: float) -> float | None:
    if n < 0:
        return None
    return math.sqrt(n)

def simple_interest(principal: float, rate: float, years: int) -> float:
    return principal * (rate / 100) * years

def percentage(value: float, total: float) -> float | None:
    if total == 0:
        return None
    return (value / total) * 100


# ─── FIXTURES ─────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_numbers():
    """Common test numbers."""
    return {"a": 10.0, "b": 4.0, "zero": 0.0, "negative": -5.0}


@pytest.fixture
def financial_params():
    """Sample financial calculation parameters."""
    return {"principal": 10000.0, "rate": 5.0, "years": 3}


# ─── BASIC ARITHMETIC TESTS ───────────────────────────────────────────────────

class TestAddition:
    def test_add_positive(self):
        assert add(3, 5) == 8
    
    def test_add_negative(self):
        assert add(-3, -5) == -8
    
    def test_add_mixed(self):
        assert add(-3, 5) == 2
    
    def test_add_zero(self):
        assert add(10, 0) == 10
        assert add(0, 10) == 10
        assert add(0, 0) == 0
    
    def test_add_floats(self):
        result = add(0.1, 0.2)
        assert math.isclose(result, 0.3, rel_tol=1e-9)
    
    def test_add_large_numbers(self):
        assert add(1_000_000, 2_000_000) == 3_000_000
    
    @pytest.mark.parametrize("a, b, expected", [
        (1, 1, 2),
        (0, 0, 0),
        (-1, 1, 0),
        (100, -100, 0),
        (0.5, 0.5, 1.0),
    ])
    def test_add_parametrized(self, a, b, expected):
        assert add(a, b) == expected


class TestSubtraction:
    def test_subtract_positive(self):
        assert subtract(10, 4) == 6
    
    def test_subtract_result_negative(self):
        assert subtract(4, 10) == -6
    
    def test_subtract_zero(self):
        assert subtract(10, 0) == 10
    
    def test_subtract_same(self):
        assert subtract(10, 10) == 0


class TestMultiplication:
    def test_multiply_positive(self):
        assert multiply(4, 5) == 20
    
    def test_multiply_by_zero(self):
        assert multiply(10, 0) == 0
    
    def test_multiply_by_one(self):
        assert multiply(10, 1) == 10
    
    def test_multiply_negatives(self):
        assert multiply(-4, -5) == 20
    
    def test_multiply_mixed_signs(self):
        assert multiply(-4, 5) == -20


class TestDivision:
    def test_divide_normal(self):
        result = divide(10, 4)
        assert result == 2.5
    
    def test_divide_by_zero_returns_none(self):
        assert divide(10, 0) is None
    
    def test_divide_exact(self):
        assert divide(10, 2) == 5.0
    
    def test_divide_negative(self):
        assert divide(-10, 2) == -5.0
    
    def test_divide_both_negative(self):
        result = divide(-10, -2)
        assert result == 5.0


class TestPower:
    def test_positive_exponent(self):
        assert power(2, 10) == 1024
    
    def test_zero_exponent(self):
        assert power(5, 0) == 1
    
    def test_power_of_one(self):
        assert power(1, 100) == 1
    
    def test_fractional_exponent(self):
        result = power(4, 0.5)
        assert math.isclose(result, 2.0)


class TestSquareRoot:
    def test_perfect_square(self):
        assert square_root(16) == 4.0
        assert square_root(9) == 3.0
        assert square_root(25) == 5.0
    
    def test_square_root_zero(self):
        assert square_root(0) == 0.0
    
    def test_negative_returns_none(self):
        assert square_root(-1) is None
        assert square_root(-100) is None
    
    def test_non_perfect_square(self):
        result = square_root(2)
        assert math.isclose(result, 1.41421356, rel_tol=1e-7)


class TestFinancial:
    def test_simple_interest(self, financial_params):
        p = financial_params
        result = simple_interest(p["principal"], p["rate"], p["years"])
        assert result == 1500.0   # 10000 * 0.05 * 3
    
    def test_simple_interest_zero_rate(self):
        result = simple_interest(10000, 0, 5)
        assert result == 0.0
    
    def test_percentage_calculation(self):
        result = percentage(50, 200)
        assert result == 25.0
    
    def test_percentage_of_zero_returns_none(self):
        assert percentage(50, 0) is None
    
    def test_percentage_100(self):
        assert percentage(100, 100) == 100.0


# ─── EDGE CASE TESTS ──────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_operations_with_infinity(self):
        inf = float("inf")
        assert add(inf, 1) == inf
        assert multiply(inf, 0) != inf  # inf * 0 = nan
    
    def test_very_small_numbers(self):
        result = add(1e-15, 1e-15)
        assert math.isclose(result, 2e-15, rel_tol=1e-10)
    
    def test_type_consistency(self):
        assert isinstance(add(1, 2), (int, float))
        assert isinstance(divide(10, 3), float)
        assert divide(10, 0) is None


# ─── INTEGRATION TEST ─────────────────────────────────────────────────────────

def test_complex_calculation():
    """Test a realistic multi-step calculation."""
    # Calculate: (100 + 50) × 2 ÷ 5 - 10
    step1 = add(100, 50)      # 150
    step2 = multiply(step1, 2)   # 300
    step3 = divide(step2, 5)     # 60
    step4 = subtract(step3, 10)  # 50
    assert step4 == 50.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
