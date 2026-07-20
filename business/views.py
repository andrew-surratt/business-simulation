from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from business.models import Business, RevenueSource, ExpenseSource
from business.services import cumulative_profit_by_month


# Create your views here.

def index(request):
    businesses = Business.objects.order_by('-name')

    context = {"businesses": businesses}
    return render(request, "business/index.html", context)

def detail(request, id):
    business = get_object_or_404(Business, pk=id)
    revenue_sources = RevenueSource.objects.filter(business=business)
    expense_sources = ExpenseSource.objects.filter(business=business)
    months = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

    profit_by_month = cumulative_profit_by_month(
        revenue_sources,
        expense_sources,
        month_count=len(months),
    )

    context = {
        "labels": months,
        "values": profit_by_month,
        "business": business,
        "revenue_sources": revenue_sources,
        "expense_sources": expense_sources
    }

    return render(request, "business/detail.html", context)
