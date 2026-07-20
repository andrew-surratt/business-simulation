"""Pure business calculations shared by views and unit tests."""


def monthly_total(sources, days_in_month=30):
    """Return the normalized monthly total for a collection of sources."""
    return sum(
        source.amount / (source.frequency.interval_in_days / days_in_month)
        for source in sources
    )


def cumulative_profit_by_month(revenue_sources, expense_sources, month_count=12):
    """Return cumulative profit for each month in the requested period."""
    monthly_profit = monthly_total(revenue_sources) - monthly_total(expense_sources)
    return [monthly_profit * month for month in range(1, month_count + 1)]

