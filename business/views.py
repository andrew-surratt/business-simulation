from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from business.models import Business, RevenueSource, ExpenseSource


# Create your views here.

def index(request):
    businesses = Business.objects.order_by('-name')

    print(", ".join([f"{b.name} ({b.location})" for b in businesses]))

    context = {"businesses": businesses}
    return render(request, "business/index.html", context)

def detail(request, id):
    business = get_object_or_404(Business, pk=id)
    revenue_sources = RevenueSource.objects.filter(business=business)
    expense_sources = ExpenseSource.objects.filter(business=business)
    months = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

    revenue_per_month = 0
    for source in revenue_sources:
        days_in_month = 30
        mult = source.frequency.interval_in_days / days_in_month
        revenue_per_month += (source.amount / mult)

    expense_per_month = 0
    for source in expense_sources:
        days_in_month = 30
        mult = source.frequency.interval_in_days / days_in_month
        expense_per_month += (source.amount / mult)

    profit_per_month = revenue_per_month - expense_per_month

    profit_by_month = [profit_per_month*m for m in range(1, len(months)+1)]

    context = {
        "labels": months,
        "values": profit_by_month,
        "business": business,
        "revenue_sources": revenue_sources,
        "expense_sources": expense_sources
    }

    print(", ".join([f"{r.name} ({r.business.name})" for r in revenue_sources]))
    print(", ".join([f"{e.name} ({e.business.name})" for e in expense_sources]))


    return render(request, "business/detail.html", context)