from django.test import TestCase, Client
from django.urls import reverse
from business.models import (
    BusinessType, Currency, Business, Frequency, 
    RevenueSource, ExpenseSource
)


# ============================================================================
# MODEL TESTS
# ============================================================================

class BusinessTypeModelTest(TestCase):
    """Test BusinessType model"""
    
    def setUp(self):
        """Create test data"""
        self.business_type = BusinessType.objects.create(name="Retail")
    
    def test_business_type_creation(self):
        """Test that a BusinessType can be created"""
        self.assertEqual(self.business_type.name, "Retail")
        self.assertTrue(isinstance(self.business_type, BusinessType))
    
    def test_business_type_str(self):
        """Test the string representation of BusinessType"""
        self.assertEqual(str(self.business_type), "Retail")


class CurrencyModelTest(TestCase):
    """Test Currency model"""
    
    def setUp(self):
        self.currency = Currency.objects.create(
            name="US Dollar",
            symbol="$"
        )
    
    def test_currency_creation(self):
        """Test that a Currency can be created"""
        self.assertEqual(self.currency.name, "US Dollar")
        self.assertEqual(self.currency.symbol, "$")
    
    def test_currency_str(self):
        """Test the string representation of Currency"""
        self.assertEqual(str(self.currency), "US Dollar")


class BusinessModelTest(TestCase):
    """Test Business model"""
    
    def setUp(self):
        self.business_type = BusinessType.objects.create(name="Tech")
        self.currency = Currency.objects.create(name="USD", symbol="$")
        self.business = Business.objects.create(
            name="TechCorp",
            location="San Francisco",
            type=self.business_type,
            currency=self.currency
        )
    
    def test_business_creation(self):
        """Test that a Business can be created"""
        self.assertEqual(self.business.name, "TechCorp")
        self.assertEqual(self.business.location, "San Francisco")
        self.assertEqual(self.business.type.name, "Tech")
        self.assertEqual(self.business.currency.name, "USD")
    
    def test_business_str(self):
        """Test the string representation of Business"""
        self.assertEqual(str(self.business), "TechCorp")


class FrequencyModelTest(TestCase):
    """Test Frequency model"""
    
    def setUp(self):
        self.frequency = Frequency.objects.create(
            name="Monthly",
            interval_in_days=30
        )
    
    def test_frequency_creation(self):
        """Test that a Frequency can be created"""
        self.assertEqual(self.frequency.name, "Monthly")
        self.assertEqual(self.frequency.interval_in_days, 30)
    
    def test_frequency_str(self):
        """Test the string representation of Frequency"""
        self.assertEqual(str(self.frequency), "Monthly")


class RevenueSourceModelTest(TestCase):
    """Test RevenueSource model"""
    
    def setUp(self):
        self.business_type = BusinessType.objects.create(name="Tech")
        self.currency = Currency.objects.create(name="USD", symbol="$")
        self.business = Business.objects.create(
            name="TechCorp",
            type=self.business_type,
            currency=self.currency
        )
        self.frequency = Frequency.objects.create(
            name="Monthly",
            interval_in_days=30
        )
        self.revenue = RevenueSource.objects.create(
            name="Software Sales",
            business=self.business,
            frequency=self.frequency,
            amount=10000,
            currency=self.currency
        )
    
    def test_revenue_source_creation(self):
        """Test that a RevenueSource can be created"""
        self.assertEqual(self.revenue.name, "Software Sales")
        self.assertEqual(self.revenue.amount, 10000)
        self.assertEqual(self.revenue.business.name, "TechCorp")
    
    def test_revenue_source_str(self):
        """Test the string representation of RevenueSource"""
        self.assertEqual(str(self.revenue), "Software Sales")


class ExpenseSourceModelTest(TestCase):
    """Test ExpenseSource model"""
    
    def setUp(self):
        self.business_type = BusinessType.objects.create(name="Tech")
        self.currency = Currency.objects.create(name="USD", symbol="$")
        self.business = Business.objects.create(
            name="TechCorp",
            type=self.business_type,
            currency=self.currency
        )
        self.frequency = Frequency.objects.create(
            name="Monthly",
            interval_in_days=30
        )
        self.expense = ExpenseSource.objects.create(
            name="Salaries",
            business=self.business,
            frequency=self.frequency,
            amount=50000,
            currency=self.currency
        )
    
    def test_expense_source_creation(self):
        """Test that an ExpenseSource can be created"""
        self.assertEqual(self.expense.name, "Salaries")
        self.assertEqual(self.expense.amount, 50000)
        self.assertEqual(self.expense.business.name, "TechCorp")
    
    def test_expense_source_str(self):
        """Test the string representation of ExpenseSource"""
        self.assertEqual(str(self.expense), "Salaries")


# ============================================================================
# TEMPLATE TESTS - INDEX
# ============================================================================

class IndexTemplateTest(TestCase):
    """Test the index.html template rendering"""
    
    def setUp(self):
        self.client = Client()
        self.business_type = BusinessType.objects.create(name="Tech")
        self.currency = Currency.objects.create(name="USD", symbol="$")
    
    def test_index_template_renders_welcome_message(self):
        """Test that index template displays welcome message"""
        response = self.client.get(reverse('business:index'))
        self.assertContains(response, "Welcome to the Business Simulator")
    
    def test_index_template_empty_businesses_message(self):
        """Test that index template shows 'no businesses' message when empty"""
        response = self.client.get(reverse('business:index'))
        self.assertContains(response, "No businesses created.")
    
    def test_index_template_displays_business_count(self):
        """Test that index template displays correct count of businesses"""
        Business.objects.create(
            name="Company A",
            location="NYC",
            type=self.business_type,
            currency=self.currency
        )
        Business.objects.create(
            name="Company B",
            location="LA",
            type=self.business_type,
            currency=self.currency
        )
        
        response = self.client.get(reverse('business:index'))
        self.assertContains(response, "Check out any of the following 2 business(es)")
    
    def test_index_template_displays_business_links(self):
        """Test that index template displays business names as links"""
        business = Business.objects.create(
            name="TechCorp",
            location="SF",
            type=self.business_type,
            currency=self.currency
        )
        
        response = self.client.get(reverse('business:index'))
        self.assertContains(response, "TechCorp")
        self.assertContains(response, f'/business/{business.id}/')
    
    def test_index_template_business_links_are_clickable(self):
        """Test that business links have proper href attributes"""
        business = Business.objects.create(
            name="MyBusiness",
            location="Boston",
            type=self.business_type,
            currency=self.currency
        )
        
        response = self.client.get(reverse('business:index'))
        self.assertContains(
            response,
            f'<a href="/business/{business.id}/">MyBusiness</a>'
        )
    
    def test_index_template_displays_all_businesses(self):
        """Test that all businesses are displayed"""
        for i in range(5):
            Business.objects.create(
                name=f"Business {i}",
                location=f"Location {i}",
                type=self.business_type,
                currency=self.currency
            )
        
        response = self.client.get(reverse('business:index'))
        for i in range(5):
            self.assertContains(response, f"Business {i}")
    
    def test_index_template_includes_base_template_elements(self):
        """Test that index template extends base template properly"""
        response = self.client.get(reverse('business:index'))
        # Check for elements from base_generic.html
        self.assertContains(response, "Business Simulator")
        self.assertContains(response, "Home")


# ============================================================================
# TEMPLATE TESTS - DETAIL
# ============================================================================

class DetailTemplateTest(TestCase):
    """Test the detail.html template rendering"""
    
    def setUp(self):
        self.client = Client()
        self.business_type = BusinessType.objects.create(name="Tech")
        self.currency = Currency.objects.create(name="USD", symbol="$")
        self.business = Business.objects.create(
            name="TechCorp",
            location="San Francisco",
            type=self.business_type,
            currency=self.currency
        )
        self.frequency = Frequency.objects.create(
            name="Monthly",
            interval_in_days=30
        )
    
    def test_detail_template_displays_business_name(self):
        """Test that detail template displays business name"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertContains(response, "TechCorp")
    
    def test_detail_template_displays_business_type(self):
        """Test that detail template displays business type"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertContains(response, "Type:")
        self.assertContains(response, "Tech")
    
    def test_detail_template_displays_business_location(self):
        """Test that detail template displays business location"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertContains(response, "Location:")
        self.assertContains(response, "San Francisco")
    
    def test_detail_template_displays_revenue_sources_heading(self):
        """Test that detail template displays revenue sources heading"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertContains(response, "Revenue Sources")
    
    def test_detail_template_displays_revenue_sources(self):
        """Test that detail template displays revenue sources"""
        revenue = RevenueSource.objects.create(
            name="Software Sales",
            business=self.business,
            frequency=self.frequency,
            amount=10000.50,
            currency=self.currency
        )
        
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertContains(response, "Software Sales")
        self.assertContains(response, "$10000.50")
        self.assertContains(response, "Monthly")
    
    def test_detail_template_displays_multiple_revenue_sources(self):
        """Test that detail template displays multiple revenue sources"""
        RevenueSource.objects.create(
            name="Software Sales",
            business=self.business,
            frequency=self.frequency,
            amount=10000,
            currency=self.currency
        )
        RevenueSource.objects.create(
            name="Consulting",
            business=self.business,
            frequency=self.frequency,
            amount=5000,
            currency=self.currency
        )
        
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertContains(response, "Software Sales")
        self.assertContains(response, "Consulting")
    
    def test_detail_template_displays_expense_sources_heading(self):
        """Test that detail template displays expense sources heading"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertContains(response, "Expense Sources")
    
    def test_detail_template_displays_expense_sources(self):
        """Test that detail template displays expense sources"""
        expense = ExpenseSource.objects.create(
            name="Salaries",
            business=self.business,
            frequency=self.frequency,
            amount=50000.75,
            currency=self.currency
        )
        
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertContains(response, "Salaries")
        self.assertContains(response, "$50000.75")
        self.assertContains(response, "Monthly")
    
    def test_detail_template_displays_multiple_expense_sources(self):
        """Test that detail template displays multiple expense sources"""
        ExpenseSource.objects.create(
            name="Salaries",
            business=self.business,
            frequency=self.frequency,
            amount=50000,
            currency=self.currency
        )
        ExpenseSource.objects.create(
            name="Rent",
            business=self.business,
            frequency=self.frequency,
            amount=10000,
            currency=self.currency
        )
        
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertContains(response, "Salaries")
        self.assertContains(response, "Rent")
    
    def test_detail_template_displays_currency_symbol(self):
        """Test that detail template displays currency symbol"""
        RevenueSource.objects.create(
            name="Sales",
            business=self.business,
            frequency=self.frequency,
            amount=5000,
            currency=self.currency
        )
        
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertContains(response, "$")
    
    def test_detail_template_has_chart_canvas(self):
        """Test that detail template includes chart canvas element"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertContains(response, '<canvas id="chart">')
    
    def test_detail_template_includes_chart_js_library(self):
        """Test that detail template includes Chart.js library"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertContains(response, "chart.js")
    
    def test_detail_template_includes_base_template_elements(self):
        """Test that detail template extends base template properly"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertContains(response, "Business Simulator")
    
    def test_detail_template_empty_revenue_sources(self):
        """Test that detail template handles no revenue sources"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        # Should have the heading but no list items
        self.assertContains(response, "Revenue Sources")
    
    def test_detail_template_empty_expense_sources(self):
        """Test that detail template handles no expense sources"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        # Should have the heading but no list items
        self.assertContains(response, "Expense Sources")
    
    def test_detail_template_formats_floats_correctly(self):
        """Test that detail template formats floats with 2 decimal places"""
        RevenueSource.objects.create(
            name="Sales",
            business=self.business,
            frequency=self.frequency,
            amount=1234.5,  # Should display as 1234.50
            currency=self.currency
        )
        
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertContains(response, "1234.50")


# ============================================================================
# VIEW TESTS
# ============================================================================

class IndexViewTest(TestCase):
    """Test the index view"""
    
    def setUp(self):
        self.client = Client()
        self.business_type = BusinessType.objects.create(name="Tech")
        self.currency = Currency.objects.create(name="USD", symbol="$")
        
        Business.objects.create(
            name="Company A",
            location="NYC",
            type=self.business_type,
            currency=self.currency
        )
        Business.objects.create(
            name="Company B",
            location="LA",
            type=self.business_type,
            currency=self.currency
        )
    
    def test_index_view_status_code(self):
        """Test that index view returns 200"""
        response = self.client.get(reverse('business:index'))
        self.assertEqual(response.status_code, 200)
    
    def test_index_view_uses_correct_template(self):
        """Test that index view uses the correct template"""
        response = self.client.get(reverse('business:index'))
        self.assertTemplateUsed(response, 'business/index.html')
    
    def test_index_view_context_contains_businesses(self):
        """Test that context contains businesses"""
        response = self.client.get(reverse('business:index'))
        self.assertIn('businesses', response.context)
        businesses = response.context['businesses']
        self.assertEqual(len(businesses), 2)
    
    def test_index_view_businesses_ordered_by_name(self):
        """Test that businesses are ordered by name descending"""
        response = self.client.get(reverse('business:index'))
        businesses = response.context['businesses']
        self.assertEqual(businesses[0].name, "Company B")
        self.assertEqual(businesses[1].name, "Company A")


class DetailViewTest(TestCase):
    """Test the detail view"""
    
    def setUp(self):
        self.client = Client()
        self.business_type = BusinessType.objects.create(name="Tech")
        self.currency = Currency.objects.create(name="USD", symbol="$")
        self.business = Business.objects.create(
            name="TechCorp",
            location="SF",
            type=self.business_type,
            currency=self.currency
        )
        
        self.frequency_monthly = Frequency.objects.create(
            name="Monthly",
            interval_in_days=30
        )
        
        self.revenue = RevenueSource.objects.create(
            name="Sales",
            business=self.business,
            frequency=self.frequency_monthly,
            amount=30000,
            currency=self.currency
        )
        
        self.expense = ExpenseSource.objects.create(
            name="Salaries",
            business=self.business,
            frequency=self.frequency_monthly,
            amount=20000,
            currency=self.currency
        )
    
    def test_detail_view_status_code(self):
        """Test that detail view returns 200 for valid business"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertEqual(response.status_code, 200)
    
    def test_detail_view_invalid_business_returns_404(self):
        """Test that detail view returns 404 for invalid business"""
        response = self.client.get(reverse('business:detail', args=[999]))
        self.assertEqual(response.status_code, 404)
    
    def test_detail_view_uses_correct_template(self):
        """Test that detail view uses the correct template"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertTemplateUsed(response, 'business/detail.html')
    
    def test_detail_view_context_contains_business(self):
        """Test that context contains the correct business"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        self.assertEqual(response.context['business'].id, self.business.id)
    
    def test_detail_view_context_contains_revenue_sources(self):
        """Test that context contains revenue sources"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        revenue_sources = response.context['revenue_sources']
        self.assertEqual(len(revenue_sources), 1)
        self.assertEqual(revenue_sources[0].name, "Sales")
    
    def test_detail_view_context_contains_expense_sources(self):
        """Test that context contains expense sources"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        expense_sources = response.context['expense_sources']
        self.assertEqual(len(expense_sources), 1)
        self.assertEqual(expense_sources[0].name, "Salaries")
    
    def test_detail_view_calculates_profit_correctly(self):
        """Test that profit is calculated correctly"""
        response = self.client.get(
            reverse('business:detail', args=[self.business.id])
        )
        # Monthly profit should be 30000 - 20000 = 10000
        values = response.context['values']
        expected_profit_month_1 = 10000 * 1
        self.assertEqual(values[0], expected_profit_month_1)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class BusinessWorkflowTest(TestCase):
    """Test complete workflows"""
    
    def setUp(self):
        self.client = Client()
        self.business_type = BusinessType.objects.create(name="E-commerce")
        self.currency = Currency.objects.create(name="USD", symbol="$")
    
    def test_create_business_and_view_details(self):
        """Test creating a business and viewing its details"""
        business = Business.objects.create(
            name="Online Store",
            location="Remote",
            type=self.business_type,
            currency=self.currency
        )
        
        frequency = Frequency.objects.create(
            name="Daily",
            interval_in_days=1
        )
        
        RevenueSource.objects.create(
            name="Online Sales",
            business=business,
            frequency=frequency,
            amount=500,
            currency=self.currency
        )
        
        # Test viewing the detail page
        response = self.client.get(reverse('business:detail', args=[business.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['business'].name, "Online Store")
    
    def test_business_appears_in_index_and_detail_views(self):
        """Test that business appears in both index and detail pages"""
        business = Business.objects.create(
            name="My Business",
            location="Somewhere",
            type=self.business_type,
            currency=self.currency
        )
        
        # Check index page
        index_response = self.client.get(reverse('business:index'))
        self.assertContains(index_response, "My Business")
        
        # Check detail page
        detail_response = self.client.get(
            reverse('business:detail', args=[business.id])
        )
        self.assertContains(detail_response, "My Business")
