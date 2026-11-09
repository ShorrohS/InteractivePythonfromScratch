"""
Debugging Challenge 01 — Phase 19: Software Engineering
========================================================

INSTRUCTIONS:
  This file contains 8 code quality issues.
  Some are outright bugs; most are design problems that compile and run
  but violate engineering principles or will cause hard-to-trace failures.

  For each issue:
    1. Read the "# Issue N:" comment to know where to look.
    2. Identify exactly what is wrong and why it matters.
    3. Write the corrected version below the issue.

  DO NOT scroll to the ANSWERS section until you have attempted all 8.

  Hint: not every issue crashes the program — some only cause subtle
  misbehaviour or will bite you the first time a caller passes unexpected input.
"""

# =====================================================================
# The "working" code (but riddled with problems)
# =====================================================================

import smtplib
import sqlite3


# Issue 1: God Object
# This class is responsible for creating orders, processing payment,
# updating inventory, sending confirmation emails, and generating reports.
# All five concerns live in one class with 200+ lines.
class OrderProcessor:

    # Issue 2: Magic numbers
    # The discount thresholds and rates are bare literals scattered through
    # the method. If the business changes the premium threshold from 500 to
    # 750, how many lines need updating?
    def calculate_total(self, subtotal: float, is_premium: bool) -> float:
        if subtotal > 500:
            discount_rate = 0.15
        elif subtotal > 100:
            discount_rate = 0.05
        else:
            discount_rate = 0.0
        tax = subtotal * 0.08
        return subtotal - (subtotal * discount_rate) + tax

    # Issue 3: Mutable default argument
    # This is one of Python's most notorious footguns. Every call that omits
    # `order_history` shares the *same* list across all invocations.
    def record_order(self, order_id: int, order_history: list = []) -> list:
        order_history.append(order_id)
        return order_history

    # Issue 4: Bare except swallowing errors silently
    # Any exception — including KeyboardInterrupt and SystemExit — is caught
    # and discarded. The caller receives None and has no idea why.
    def fetch_product(self, product_id: int):
        try:
            conn = sqlite3.connect("shop.db")
            row = conn.execute(
                "SELECT id, name, price FROM products WHERE id = ?",
                (product_id,)
            ).fetchone()
            conn.close()
            return row
        except:
            pass

    # Issue 5: Deep nesting
    # Four levels of if/else make the logic difficult to follow and test.
    # Guard clauses would flatten this to a single indentation level.
    def get_shipping_cost(self, user, cart) -> float:
        if user is not None:
            if user.get("is_active"):
                if cart.get("weight") is not None:
                    if cart["weight"] > 0:
                        if user.get("is_premium"):
                            return 0.0
                        else:
                            return cart["weight"] * 2.50
                    else:
                        return 0.0
                else:
                    return 0.0
            else:
                return 0.0
        else:
            return 0.0

    # Issue 6: Method with too many parameters (data clump)
    # Seven positional parameters. The caller must remember the exact order.
    # A dataclass or TypedDict would group related data and make calls readable.
    def create_order(
        self,
        customer_name: str,
        customer_email: str,
        customer_address: str,
        product_id: int,
        quantity: int,
        payment_method: str,
        coupon_code: str,
    ) -> dict:
        return {
            "customer": customer_name,
            "email":    customer_email,
            "address":  customer_address,
            "product":  product_id,
            "qty":      quantity,
            "payment":  payment_method,
            "coupon":   coupon_code,
        }

    # Issue 7: Global variable mutation from within a method
    # Mutating a module-level variable inside a method creates hidden,
    # order-dependent state that is invisible to callers and impossible
    # to test in isolation.
    def complete_order(self, order_id: int) -> None:
        global completed_orders_count       # reads and writes a global
        completed_orders_count += 1
        print(f"Order {order_id} completed. Total completed: {completed_orders_count}")

    # Issue 8: No type hints or docstrings on public methods
    # The method below has undocumented parameters, no return type, and no
    # explanation of what "format" means or what the return value looks like.
    def generate_report(self, orders, format, include_tax):
        if format == "csv":
            lines = ["id,total,tax"]
            for o in orders:
                tax = o["total"] * 0.08 if include_tax else 0
                lines.append(f"{o['id']},{o['total']:.2f},{tax:.2f}")
            return "\n".join(lines)
        return str(orders)


# Module-level mutable state (referenced by Issue 7)
completed_orders_count = 0


# =====================================================================
# ANSWERS  (don't read until you've attempted all 8!)
# =====================================================================
#
# Issue 1 — God Object
#   Problem:  One class has five distinct responsibilities (ordering,
#             payment, inventory, email, reporting). Any change to any
#             concern touches the same class.
#   Fix:      Split into focused classes: OrderService, PaymentService,
#             InventoryService, NotificationService, ReportService.
#             Wire them together in a thin orchestrator.
#   Principle: Single Responsibility Principle (SRP)
#
# Issue 2 — Magic numbers
#   Problem:  0.15, 0.05, 500, 100, 0.08 appear as bare literals.
#             To update the premium threshold you must hunt for every 500.
#   Fix:      Define named constants at module level:
#               PREMIUM_THRESHOLD   = 500
#               STANDARD_THRESHOLD  = 100
#               PREMIUM_DISCOUNT    = 0.15
#               STANDARD_DISCOUNT   = 0.05
#               TAX_RATE            = 0.08
#   Principle: Avoid Magic Numbers (Clean Code)
#
# Issue 3 — Mutable default argument
#   Problem:  `order_history=[]` creates ONE list at function definition
#             time. Every call that omits the argument shares it — orders
#             accumulate across completely unrelated calls.
#   Fix:      def record_order(self, order_id: int,
#                              order_history: list | None = None) -> list:
#                 if order_history is None:
#                     order_history = []
#                 order_history.append(order_id)
#                 return order_history
#   Principle: Python gotcha (PEP 20 — explicit is better than implicit)
#
# Issue 4 — Bare except
#   Problem:  `except: pass` silently swallows every exception including
#             KeyboardInterrupt. The method returns None without the caller
#             knowing why. Bugs are completely invisible.
#   Fix:      except sqlite3.Error as e:
#                 logging.error("Failed to fetch product %d: %s", product_id, e)
#                 return None
#             Or re-raise after logging so callers can handle it.
#   Principle: Fail loudly / never swallow exceptions silently
#
# Issue 5 — Deep nesting
#   Problem:  Four levels of if/else require mental stack-tracking.
#             Adding a new condition forces yet another level.
#   Fix:      Use guard clauses — return the default value early:
#               if not user or not user.get("is_active"):   return 0.0
#               if not cart.get("weight") or cart["weight"] <= 0: return 0.0
#               if user.get("is_premium"): return 0.0
#               return cart["weight"] * 2.50
#   Principle: Avoid Deep Nesting / Guard Clauses (Clean Code)
#
# Issue 6 — Too many parameters (data clump)
#   Problem:  Seven positional args are easy to mis-order and hard to read
#             at the call site. Adding an eighth means updating every caller.
#   Fix:      from dataclasses import dataclass
#             @dataclass
#             class OrderRequest:
#                 customer_name: str
#                 customer_email: str
#                 customer_address: str
#                 product_id: int
#                 quantity: int
#                 payment_method: str
#                 coupon_code: str = ""
#
#             def create_order(self, request: OrderRequest) -> dict: ...
#   Principle: Replace Parameter Object / Introduce Parameter Object
#              (Refactoring by Fowler)
#
# Issue 7 — Global variable mutation
#   Problem:  `global completed_orders_count` makes the method's behaviour
#             depend on invisible external state. Tests cannot reset it
#             reliably, and concurrent calls cause race conditions.
#   Fix:      Pass the counter as a dependency or use an instance attribute:
#               class OrderProcessor:
#                   def __init__(self):
#                       self.completed_orders_count = 0
#                   def complete_order(self, order_id: int) -> None:
#                       self.completed_orders_count += 1
#                       print(f"Order {order_id} completed.")
#   Principle: Avoid Global State / Encapsulate State
#
# Issue 8 — No type hints or docstrings
#   Problem:  Callers cannot tell what `format` should be ('csv'? 'json'?
#             an enum?), what `include_tax` means, or what the method returns.
#   Fix:      from typing import Literal
#
#             def generate_report(
#                 self,
#                 orders: list[dict],
#                 format: Literal['csv', 'text'],
#                 include_tax: bool,
#             ) -> str:
#                 """Generate an order report in the requested format.
#
#                 Args:
#                     orders:      List of order dicts with 'id' and 'total' keys.
#                     format:      Output format — 'csv' or 'text'.
#                     include_tax: When True, a tax column is added at 8%.
#
#                 Returns:
#                     A formatted string containing the report.
#                 """
#   Principle: Intentional Documentation / Type Safety
#
# =====================================================================
