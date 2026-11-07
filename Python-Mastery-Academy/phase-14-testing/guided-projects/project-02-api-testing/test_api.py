"""
Project 02 - API & Business Logic Testing
Phase 14: Testing

SKILLS PRACTICED:
  - pytest fixtures
  - Parametrize decorator
  - Mocking with unittest.mock
  - Testing with and without real API calls
  - Test coverage

HOW TO RUN:
  pip install pytest pytest-cov
  pytest test_api.py -v
  pytest test_api.py -v --cov=. --cov-report=term-missing
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


# ============================================================
# CODE UNDER TEST (inline for self-contained demo)
# ============================================================

def validate_age(age: int) -> tuple[bool, str]:
    if not isinstance(age, int):
        return False, "Age must be an integer"
    if age < 0 or age > 150:
        return False, f"Age {age} out of valid range (0-150)"
    return True, "Valid"


def calculate_tax(gross: float, rate: float = 0.20) -> float:
    if gross < 0:
        raise ValueError(f"Gross pay cannot be negative: {gross}")
    return round(gross * rate, 2)


def calculate_net_pay(gross: float, tax_rate: float = 0.20) -> dict:
    tax = calculate_tax(gross, tax_rate)
    ni  = round(gross * 0.12, 2)
    net = round(gross - tax - ni, 2)
    return {"gross": gross, "tax": tax, "ni": ni, "net": net}


def fetch_weather(city: str, api_key: str) -> dict:
    """Fetches weather data. In tests, this will be mocked."""
    import requests
    url    = f"https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key}
    r      = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()


def parse_weather_response(data: dict) -> dict:
    """Parse raw API response into clean dict."""
    return {
        "city":        data.get("name", "Unknown"),
        "temp_k":      data["main"]["temp"],
        "temp_c":      round(data["main"]["temp"] - 273.15, 1),
        "humidity":    data["main"]["humidity"],
        "description": data["weather"][0]["description"]
    }


def process_sales_records(records: list[dict]) -> dict:
    """Process sales data and return summary."""
    if not records:
        return {"total": 0, "count": 0, "avg": 0, "max": 0}
    amounts = [r["amount"] for r in records]
    return {
        "total": sum(amounts),
        "count": len(amounts),
        "avg":   round(sum(amounts) / len(amounts), 2),
        "max":   max(amounts)
    }


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def employee_data():
    return {
        "id": "E001",
        "name": "Alice Johnson",
        "gross": 6000.00,   # monthly
        "dept": "Engineering"
    }


@pytest.fixture
def sales_records():
    return [
        {"rep": "Alice", "amount": 5200.0, "region": "North"},
        {"rep": "Bob",   "amount": 3100.0, "region": "South"},
        {"rep": "Carol", "amount": 7800.0, "region": "North"},
        {"rep": "Dave",  "amount": 4500.0, "region": "East"},
    ]


@pytest.fixture
def mock_weather_response():
    """Fake API response — no real API call needed."""
    return {
        "name": "London",
        "main": {"temp": 283.15, "humidity": 78, "pressure": 1013},
        "weather": [{"description": "light rain", "icon": "10d"}]
    }


# ============================================================
# TESTS — VALIDATION
# ============================================================

class TestValidateAge:

    def test_valid_age(self):
        valid, msg = validate_age(25)
        assert valid is True
        assert msg == "Valid"

    def test_zero_age(self):
        valid, _ = validate_age(0)
        assert valid is True

    def test_max_age(self):
        valid, _ = validate_age(150)
        assert valid is True

    def test_negative_age_invalid(self):
        valid, msg = validate_age(-1)
        assert valid is False
        assert "range" in msg

    def test_over_max_invalid(self):
        valid, msg = validate_age(200)
        assert valid is False

    def test_string_input_invalid(self):
        valid, msg = validate_age("thirty")
        assert valid is False
        assert "integer" in msg

    def test_float_input_invalid(self):
        valid, _ = validate_age(25.5)
        assert valid is False

    @pytest.mark.parametrize("age, expected", [
        (0,   True),
        (25,  True),
        (100, True),
        (150, True),
        (-1,  False),
        (151, False),
        (999, False),
    ])
    def test_age_parametrized(self, age, expected):
        valid, _ = validate_age(age)
        assert valid == expected


# ============================================================
# TESTS — PAYROLL CALCULATION
# ============================================================

class TestPayrollCalculations:

    def test_calculate_tax_standard(self):
        assert calculate_tax(10000, 0.20) == 2000.0

    def test_calculate_tax_zero_rate(self):
        assert calculate_tax(10000, 0.0) == 0.0

    def test_calculate_tax_hundred_percent(self):
        assert calculate_tax(10000, 1.0) == 10000.0

    def test_calculate_tax_negative_raises(self):
        with pytest.raises(ValueError, match="negative"):
            calculate_tax(-1000)

    def test_net_pay_returns_dict(self, employee_data):
        result = calculate_net_pay(employee_data["gross"])
        assert isinstance(result, dict)
        assert "net" in result

    def test_net_is_less_than_gross(self, employee_data):
        result = calculate_net_pay(employee_data["gross"])
        assert result["net"] < result["gross"]

    def test_deductions_add_up(self, employee_data):
        result = calculate_net_pay(employee_data["gross"])
        assert abs((result["gross"] - result["tax"] - result["ni"]) - result["net"]) < 0.01

    def test_net_pay_rounding(self):
        result = calculate_net_pay(1000.0, 0.20)
        assert isinstance(result["net"], float)
        # net = 1000 - 200 - 120 = 680
        assert result["net"] == pytest.approx(680.0)

    @pytest.mark.parametrize("gross, rate, expected_tax", [
        (10000, 0.20, 2000.0),
        (5000,  0.15, 750.0),
        (0,     0.20, 0.0),
        (1,     0.20, 0.2),
    ])
    def test_tax_calculations(self, gross, rate, expected_tax):
        assert calculate_tax(gross, rate) == expected_tax


# ============================================================
# TESTS — MOCKING EXTERNAL API
# ============================================================

class TestWeatherAPI:

    @patch("requests.get")
    def test_fetch_weather_success(self, mock_get, mock_weather_response):
        """Test successful API call using a mock."""
        mock_response       = Mock()
        mock_response.json.return_value = mock_weather_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_weather("London", "fake_key")

        assert result["name"] == "London"
        mock_get.assert_called_once()   # verify API was called

    @patch("requests.get")
    def test_fetch_weather_raises_on_error(self, mock_get):
        """Test that HTTP errors propagate."""
        import requests as req_lib
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = req_lib.exceptions.HTTPError("404")
        mock_get.return_value = mock_response

        with pytest.raises(req_lib.exceptions.HTTPError):
            fetch_weather("NonExistentCity123", "fake_key")

    def test_parse_weather_response(self, mock_weather_response):
        """Test parsing without any network call."""
        result = parse_weather_response(mock_weather_response)

        assert result["city"]     == "London"
        assert result["temp_k"]   == 283.15
        assert result["temp_c"]   == pytest.approx(10.0, abs=0.1)
        assert result["humidity"] == 78

    def test_parse_weather_celsius_conversion(self, mock_weather_response):
        """Verify Kelvin to Celsius conversion."""
        result = parse_weather_response(mock_weather_response)
        expected_c = round(mock_weather_response["main"]["temp"] - 273.15, 1)
        assert result["temp_c"] == expected_c


# ============================================================
# TESTS — DATA PROCESSING
# ============================================================

class TestSalesProcessing:

    def test_empty_records(self):
        result = process_sales_records([])
        assert result["total"] == 0
        assert result["count"] == 0

    def test_single_record(self):
        result = process_sales_records([{"rep": "A", "amount": 1000}])
        assert result["total"] == 1000
        assert result["count"] == 1
        assert result["avg"]   == 1000

    def test_multiple_records(self, sales_records):
        result = process_sales_records(sales_records)
        assert result["count"] == 4
        assert result["total"] == pytest.approx(20600.0)
        assert result["max"]   == 7800.0

    def test_result_has_all_keys(self, sales_records):
        result = process_sales_records(sales_records)
        assert all(k in result for k in ("total", "count", "avg", "max"))


# ============================================================
# EDGE CASES
# ============================================================

class TestEdgeCases:

    def test_tax_rounding(self):
        """Verify rounding to 2 decimal places."""
        tax = calculate_tax(3333.33, 0.20)
        assert tax == round(3333.33 * 0.20, 2)

    def test_zero_gross_pay(self):
        result = calculate_net_pay(0.0)
        assert result["net"] == 0.0

    def test_large_gross_pay(self):
        """Should handle large numbers without overflow."""
        result = calculate_net_pay(1_000_000.0)
        assert result["net"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
