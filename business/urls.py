from django.urls import path

from . import views

app_name = 'business'

urlpatterns = [
    path('', views.index, name='index'),
    path("new/", views.business_create, name="business_create"),
    path("<int:id>/", views.detail, name="detail"),
    path("<int:id>/edit/", views.business_edit, name="business_edit"),
    path(
        "<int:business_id>/revenue/new/",
        views.revenue_source_create,
        name="revenue_source_create",
    ),
    path(
        "<int:business_id>/revenue/<int:source_id>/edit/",
        views.revenue_source_edit,
        name="revenue_source_edit",
    ),
    path(
        "<int:business_id>/revenue/<int:source_id>/delete/",
        views.revenue_source_delete,
        name="revenue_source_delete",
    ),
    path(
        "<int:business_id>/expense/new/",
        views.expense_source_create,
        name="expense_source_create",
    ),
    path(
        "<int:business_id>/expense/<int:source_id>/edit/",
        views.expense_source_edit,
        name="expense_source_edit",
    ),
    path(
        "<int:business_id>/expense/<int:source_id>/delete/",
        views.expense_source_delete,
        name="expense_source_delete",
    ),
]
