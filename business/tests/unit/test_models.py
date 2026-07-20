from django.test import SimpleTestCase

from business.models import Business, BusinessType, Currency, ExpenseSource, Frequency, RevenueSource


class ModelStringTest(SimpleTestCase):
    databases = set()

    def test_model_names_are_used_as_string_representations(self):
        models = [
            BusinessType(name="Retail"),
            Currency(name="US Dollar", symbol="$"),
            Business(name="TechCorp"),
            Frequency(name="Monthly", interval_in_days=30),
            RevenueSource(name="Software Sales"),
            ExpenseSource(name="Salaries"),
        ]

        self.assertEqual(
            [str(instance) for instance in models],
            ["Retail", "US Dollar", "TechCorp", "Monthly", "Software Sales", "Salaries"],
        )

