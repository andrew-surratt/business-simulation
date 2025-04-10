from django.contrib import admin

from .models import Business, BusinessType, ExpenseSource, RevenueSource

admin.site.register(Business)
admin.site.register(BusinessType)
admin.site.register(ExpenseSource)
admin.site.register(RevenueSource)