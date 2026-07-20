from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from business.forms import BusinessForm, ExpenseSourceForm, RevenueSourceForm
from business.models import Business, RevenueSource, ExpenseSource
from business.services import cumulative_profit_by_month, monthly_total


# Create your views here.

def index(request):
    businesses = Business.objects.order_by('-name')

    context = {"businesses": businesses}
    return render(request, "business/index.html", context)

def detail(request, id):
    business = get_object_or_404(Business, pk=id)
    return render(request, "business/detail.html", detail_context(business))


def detail_context(business, *, is_fragment=False):
    revenue_sources = RevenueSource.objects.filter(business=business)
    expense_sources = ExpenseSource.objects.filter(business=business)
    months = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

    revenue_per_month = monthly_total(revenue_sources)
    expense_per_month = monthly_total(expense_sources)

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
        "expense_sources": expense_sources,
        "revenue_per_month": revenue_per_month,
        "expense_per_month": expense_per_month,
        "profit_per_month": revenue_per_month - expense_per_month,
        "is_fragment": is_fragment,
    }
    return context


def business_create(request):
    form = BusinessForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        business = form.save()
        messages.success(request, "Business created.")
        return redirect_response(request, "business:detail", id=business.id)

    return render_form_page(
        request,
        form,
        title="Create business",
        cancel_url="business:index",
        submit_label="Create business",
    )


def business_edit(request, id):
    business = get_object_or_404(Business, pk=id)
    form = BusinessForm(request.POST or None, instance=business)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Business updated.")
        return redirect_response(request, "business:detail", id=business.id)

    return render_form_page(
        request,
        form,
        title="Edit business",
        cancel_url="business:detail",
        cancel_url_kwargs={"id": business.id},
        submit_label="Save changes",
    )


def revenue_source_create(request, business_id):
    business = get_object_or_404(Business, pk=business_id)
    return source_form(request, business, RevenueSourceForm, "Revenue source")


def revenue_source_edit(request, business_id, source_id):
    business = get_object_or_404(Business, pk=business_id)
    source = get_object_or_404(RevenueSource, pk=source_id, business=business)
    return source_form(
        request, business, RevenueSourceForm, "Revenue source", instance=source
    )


def expense_source_create(request, business_id):
    business = get_object_or_404(Business, pk=business_id)
    return source_form(request, business, ExpenseSourceForm, "Expense source")


def expense_source_edit(request, business_id, source_id):
    business = get_object_or_404(Business, pk=business_id)
    source = get_object_or_404(ExpenseSource, pk=source_id, business=business)
    return source_form(
        request, business, ExpenseSourceForm, "Expense source", instance=source
    )


def source_form(request, business, form_class, source_label, instance=None):
    form = form_class(request.POST or None, instance=instance)
    action = "Edit" if instance else "Add"
    if request.method == "POST" and form.is_valid():
        source = form.save(commit=False)
        source.business = business
        source.save()
        messages.success(request, f"{source_label} saved.")
        if is_htmx(request):
            return render_detail_fragment(request, business)
        return redirect("business:detail", id=business.id)

    return render_form_page(
        request,
        form,
        title=f"{action} {source_label.lower()}",
        cancel_url="business:detail",
        cancel_url_kwargs={"id": business.id},
        submit_label="Save source",
        context={"business": business, "form_target": "#detail-content"},
    )


@require_http_methods(["GET", "POST"])
def revenue_source_delete(request, business_id, source_id):
    business = get_object_or_404(Business, pk=business_id)
    source = get_object_or_404(RevenueSource, pk=source_id, business=business)
    return source_delete(request, business, source, "Revenue source")


@require_http_methods(["GET", "POST"])
def expense_source_delete(request, business_id, source_id):
    business = get_object_or_404(Business, pk=business_id)
    source = get_object_or_404(ExpenseSource, pk=source_id, business=business)
    return source_delete(request, business, source, "Expense source")


def source_delete(request, business, source, source_label):
    if request.method == "POST":
        source.delete()
        messages.success(request, f"{source_label} deleted.")
        if is_htmx(request):
            return render_detail_fragment(request, business)
        return redirect("business:detail", id=business.id)

    if is_htmx(request):
        return render(
            request,
            "business/partials/confirmation_modal.html",
            {
                "business": business,
                "source": source,
                "source_label": source_label,
                "is_modal": True,
            },
        )

    return render(
        request,
        "business/source_confirm_delete.html",
        {"business": business, "source": source, "source_label": source_label},
    )


def render_form_page(
    request,
    form,
    *,
    title,
    cancel_url,
    cancel_url_kwargs=None,
    submit_label,
    context=None,
):
    page_context = {
        "form": form,
        "form_title": title,
        "cancel_href": reverse(cancel_url, kwargs=cancel_url_kwargs or {}),
        "submit_label": submit_label,
        "is_modal": is_htmx(request),
        "form_target": "#main-content",
    }
    page_context.update(context or {})
    if is_htmx(request):
        response = render(request, "business/partials/modal_form.html", page_context)
        if request.method == "POST":
            response["HX-Retarget"] = "#modal-content"
            response["HX-Reswap"] = "innerHTML"
        return response
    return render(request, "business/form.html", page_context)


def is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def redirect_response(request, view_name, **kwargs):
    url = reverse(view_name, kwargs=kwargs)
    if is_htmx(request):
        response = HttpResponse(status=204)
        response["HX-Redirect"] = url
        return response
    return redirect(url)


def render_detail_fragment(request, business):
    response = render(
        request,
        "business/partials/detail_content.html",
        detail_context(business, is_fragment=True),
    )
    response["HX-Trigger"] = "uiUpdated"
    return response
