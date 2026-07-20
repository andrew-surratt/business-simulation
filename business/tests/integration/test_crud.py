from django.test import Client, TestCase
from django.urls import reverse

from business.forms import RevenueSourceForm
from business.models import (
    Business,
    BusinessType,
    Currency,
    ExpenseSource,
    Frequency,
    RevenueSource,
)


class PublicCrudTest(TestCase):
    def setUp(self):
        self.business_type = BusinessType.objects.create(name="Retail")
        self.currency = Currency.objects.create(name="US Dollar", symbol="$")
        self.frequency = Frequency.objects.create(name="Monthly", interval_in_days=30)
        self.business = Business.objects.create(
            name="Corner Shop",
            location="Chicago",
            type=self.business_type,
            currency=self.currency,
        )

    def business_data(self, **overrides):
        data = {
            "name": "New Shop",
            "location": "Austin",
            "type": self.business_type.id,
            "currency": self.currency.id,
        }
        data.update(overrides)
        return data

    def source_data(self, **overrides):
        data = {
            "name": "Subscriptions",
            "amount": "1250.50",
            "frequency": self.frequency.id,
            "currency": self.currency.id,
        }
        data.update(overrides)
        return data

    def test_business_create_renders_and_saves(self):
        url = reverse("business:business_create")
        self.assertTemplateUsed(self.client.get(url), "business/form.html")

        response = self.client.post(url, self.business_data())

        created = Business.objects.get(name="New Shop")
        self.assertRedirects(response, reverse("business:detail", args=[created.id]))

    def test_business_edit_updates_existing_business(self):
        response = self.client.post(
            reverse("business:business_edit", args=[self.business.id]),
            self.business_data(name="Updated Shop"),
        )

        self.business.refresh_from_db()
        self.assertEqual(self.business.name, "Updated Shop")
        self.assertRedirects(response, reverse("business:detail", args=[self.business.id]))

    def test_revenue_source_create_assigns_business(self):
        response = self.client.post(
            reverse("business:revenue_source_create", args=[self.business.id]),
            self.source_data(),
        )

        source = RevenueSource.objects.get(name="Subscriptions")
        self.assertEqual(source.business, self.business)
        self.assertRedirects(response, reverse("business:detail", args=[self.business.id]))

    def test_expense_source_create_assigns_business(self):
        response = self.client.post(
            reverse("business:expense_source_create", args=[self.business.id]),
            self.source_data(name="Rent"),
        )

        source = ExpenseSource.objects.get(name="Rent")
        self.assertEqual(source.business, self.business)
        self.assertRedirects(response, reverse("business:detail", args=[self.business.id]))

    def test_source_edit_cannot_cross_business_boundary(self):
        other_business = Business.objects.create(
            name="Other",
            type=self.business_type,
            currency=self.currency,
        )
        source = RevenueSource.objects.create(
            business=other_business,
            frequency=self.frequency,
            currency=self.currency,
            name="Other revenue",
            amount=100,
        )

        response = self.client.get(
            reverse(
                "business:revenue_source_edit",
                args=[self.business.id, source.id],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_source_delete_requires_confirmation_then_deletes(self):
        source = ExpenseSource.objects.create(
            business=self.business,
            frequency=self.frequency,
            currency=self.currency,
            name="Rent",
            amount=1000,
        )
        url = reverse(
            "business:expense_source_delete", args=[self.business.id, source.id]
        )

        self.assertTemplateUsed(self.client.get(url), "business/source_confirm_delete.html")
        response = self.client.post(url)

        self.assertFalse(ExpenseSource.objects.filter(id=source.id).exists())
        self.assertRedirects(response, reverse("business:detail", args=[self.business.id]))

    def test_negative_source_amount_is_rejected(self):
        form = RevenueSourceForm(data=self.source_data(amount="-1"))

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["amount"], ["Enter an amount of zero or more."])

    def test_htmx_get_renders_form_as_modal_fragment(self):
        response = self.client.get(
            reverse("business:revenue_source_create", args=[self.business.id]),
            headers={"HX-Request": "true"},
        )

        self.assertTemplateUsed(response, "business/partials/modal_form.html")
        self.assertTemplateNotUsed(response, "base_generic.html")
        self.assertContains(response, 'class="modal-dialog')

    def test_invalid_htmx_form_stays_in_modal(self):
        response = self.client.post(
            reverse("business:revenue_source_create", args=[self.business.id]),
            self.source_data(amount="-1"),
            headers={"HX-Request": "true"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["HX-Retarget"], "#modal-content")
        self.assertContains(response, "Enter an amount of zero or more.")
        self.assertFalse(RevenueSource.objects.exists())

    def test_valid_htmx_source_form_refreshes_dashboard(self):
        response = self.client.post(
            reverse("business:revenue_source_create", args=[self.business.id]),
            self.source_data(),
            headers={"HX-Request": "true"},
        )

        self.assertTemplateUsed(response, "business/partials/detail_content.html")
        self.assertEqual(response.headers["HX-Trigger"], "uiUpdated")
        self.assertContains(response, 'id="detail-content"')
        self.assertContains(response, "Subscriptions")
        self.assertContains(response, "$1250.50")

    def test_htmx_delete_refreshes_dashboard(self):
        source = RevenueSource.objects.create(
            business=self.business,
            frequency=self.frequency,
            currency=self.currency,
            name="Sales",
            amount=500,
        )
        url = reverse(
            "business:revenue_source_delete", args=[self.business.id, source.id]
        )

        confirmation = self.client.get(url, headers={"HX-Request": "true"})
        response = self.client.post(url, headers={"HX-Request": "true"})

        self.assertTemplateUsed(
            confirmation, "business/partials/confirmation_modal.html"
        )
        self.assertEqual(response.headers["HX-Trigger"], "uiUpdated")
        self.assertFalse(RevenueSource.objects.filter(id=source.id).exists())

    def test_htmx_business_save_redirects_to_canonical_detail_page(self):
        response = self.client.post(
            reverse("business:business_edit", args=[self.business.id]),
            self.business_data(name="Updated Shop"),
            headers={"HX-Request": "true"},
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            response.headers["HX-Redirect"],
            reverse("business:detail", args=[self.business.id]),
        )

    def test_detail_displays_monthly_summary_and_accessible_tables(self):
        RevenueSource.objects.create(
            business=self.business,
            frequency=self.frequency,
            currency=self.currency,
            name="Sales",
            amount=2000,
        )
        ExpenseSource.objects.create(
            business=self.business,
            frequency=self.frequency,
            currency=self.currency,
            name="Rent",
            amount=750,
        )

        response = self.client.get(
            reverse("business:detail", args=[self.business.id])
        )

        self.assertContains(response, "Monthly revenue")
        self.assertContains(response, "$2000.00")
        self.assertContains(response, "Monthly expenses")
        self.assertContains(response, "$750.00")
        self.assertContains(response, "Monthly profit")
        self.assertContains(response, "$1250.00")
        self.assertContains(response, 'scope="col"')

    def test_public_updates_require_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post(
            reverse("business:business_edit", args=[self.business.id]),
            self.business_data(name="Unprotected change"),
        )

        self.assertEqual(response.status_code, 403)
        self.business.refresh_from_db()
        self.assertEqual(self.business.name, "Corner Shop")
