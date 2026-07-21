from types import SimpleNamespace

from django.test import SimpleTestCase

from business.services import cumulative_profit_by_month, monthly_total


def source(amount, interval_in_days):
    return SimpleNamespace(
        amount=amount,
        frequency=SimpleNamespace(interval_in_days=interval_in_days),
    )


class MonthlyTotalTest(SimpleTestCase):
    databases = set()

    def test_empty_sources_total_zero(self):
        self.assertEqual(monthly_total([]), 0)

    def test_normalizes_sources_to_thirty_days(self):
        sources = [source(100, 1), source(300, 30)]

        self.assertEqual(monthly_total(sources), 3300)


class CumulativeProfitTest(SimpleTestCase):
    databases = set()

    def test_returns_cumulative_profit_for_requested_months(self):
        revenue = [source(30000, 30)]
        expenses = [source(20000, 30)]

        self.assertEqual(
            cumulative_profit_by_month(revenue, expenses, month_count=3),
            [10000, 20000, 30000],
        )

    def test_supports_negative_profit(self):
        revenue = [source(1000, 30)]
        expenses = [source(1500, 30)]

        self.assertEqual(
            cumulative_profit_by_month(revenue, expenses, month_count=2),
            [-500, -1000],
        )

