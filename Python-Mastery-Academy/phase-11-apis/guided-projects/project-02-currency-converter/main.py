"""
Project 02 - Currency Converter
Phase 11: APIs

SKILLS PRACTICED:
  - REST API consumption
  - JSON parsing
  - Environment variables for API keys
  - Error handling for network requests
  - Caching API responses

API: Open Exchange Rates (free tier) or ExchangeRate-API
Get free key at: https://www.exchangerate-api.com

HOW TO RUN:
  python main.py
"""

import os
import json
from datetime import datetime, date
from pathlib import Path

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

API_KEY  = os.environ.get("EXCHANGE_API_KEY", "demo")
BASE_URL = "https://v6.exchangerate-api.com/v6"
CACHE_FILE = "exchange_rates_cache.json"

# Demo rates when no API key
DEMO_RATES = {
    "USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 149.5,
    "AUD": 1.53, "CAD": 1.36, "CHF": 0.89, "INR": 83.1,
    "CNY": 7.25, "MXN": 17.2, "BRL": 4.97, "SGD": 1.34,
    "HKD": 7.82, "NOK": 10.7, "SEK": 10.5, "DKK": 6.89,
    "NZD": 1.63, "ZAR": 18.8, "AED": 3.67, "SAR": 3.75
}


def load_cache() -> dict | None:
    """Load cached exchange rates (valid for today)."""
    if not Path(CACHE_FILE).exists():
        return None
    try:
        with open(CACHE_FILE) as f:
            cache = json.load(f)
        if cache.get("date") == date.today().isoformat():
            return cache["rates"]
    except (json.JSONDecodeError, KeyError):
        pass
    return None


def save_cache(rates: dict, base: str = "USD") -> None:
    with open(CACHE_FILE, "w") as f:
        json.dump({"date": date.today().isoformat(),
                   "base": base, "rates": rates}, f, indent=2)


def fetch_rates(base: str = "USD") -> dict:
    """Fetch live exchange rates. Falls back to cache or demo data."""
    # Try cache first
    cached = load_cache()
    if cached:
        print("  (Using today's cached rates)")
        return cached

    if not REQUESTS_AVAILABLE:
        print("  requests not installed — using demo rates")
        return DEMO_RATES

    if API_KEY == "demo":
        print("  No API key — using demo rates")
        print("  Get free key at: https://www.exchangerate-api.com")
        return DEMO_RATES

    try:
        url = f"{BASE_URL}/{API_KEY}/latest/{base}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("result") == "success":
                rates = data["conversion_rates"]
                save_cache(rates, base)
                print("  Live rates fetched successfully.")
                return rates
    except requests.exceptions.RequestException as e:
        print(f"  API error: {e}. Using demo rates.")

    return DEMO_RATES


def convert(amount: float, from_currency: str,
            to_currency: str, rates: dict) -> float:
    """Convert amount between currencies."""
    from_cur = from_currency.upper()
    to_cur   = to_currency.upper()

    if from_cur not in rates:
        raise ValueError(f"Unknown currency: {from_cur}")
    if to_cur not in rates:
        raise ValueError(f"Unknown currency: {to_cur}")

    # Convert to USD base, then to target
    in_usd = amount / rates[from_cur]
    result = in_usd * rates[to_cur]
    return round(result, 4)


def format_rate_table(rates: dict, base: str = "USD") -> None:
    """Display exchange rates table."""
    common = ["EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "INR", "CNY", "MXN"]
    print(f"\n  Exchange rates vs {base}")
    print(f"  {'Currency':<10} {'Rate':>12}")
    print("  " + "-" * 25)
    for cur in common:
        if cur in rates and cur != base:
            print(f"  {cur:<10} {rates[cur]:>12.4f}")


def main():
    print("=" * 55)
    print("  CURRENCY CONVERTER")
    print("=" * 55)

    print("\n  Loading exchange rates...")
    rates = fetch_rates("USD")
    print(f"  {len(rates)} currencies available.")

    while True:
        print("\n  [1] Convert Amount    [2] Rate Table")
        print("  [3] Multi-Convert     [0] Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            try:
                amount = float(input("  Amount: "))
                from_c = input("  From currency (e.g. USD): ").strip().upper()
                to_c   = input("  To currency (e.g. EUR): ").strip().upper()
                result = convert(amount, from_c, to_c, rates)
                rate   = convert(1, from_c, to_c, rates)
                print(f"\n  {amount:,.2f} {from_c} = {result:,.4f} {to_c}")
                print(f"  (Rate: 1 {from_c} = {rate:.4f} {to_c})")
            except (ValueError, KeyError) as e:
                print(f"  Error: {e}")

        elif choice == "2":
            base = input("  Base currency [USD]: ").strip().upper() or "USD"
            format_rate_table(rates, base)

        elif choice == "3":
            try:
                amount = float(input("  Amount in USD: "))
                targets = ["EUR", "GBP", "JPY", "AUD", "CAD", "INR"]
                print(f"\n  {amount:,.2f} USD equals:")
                for cur in targets:
                    if cur in rates:
                        result = convert(amount, "USD", cur, rates)
                        print(f"  {cur}:  {result:>12,.4f}")
            except ValueError:
                print("  Invalid amount.")

        elif choice == "0":
            print("  Goodbye!")
            break


if __name__ == "__main__":
    main()
