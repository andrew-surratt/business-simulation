from django.db import models

class BusinessType(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)


class Business(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    type = models.ForeignKey(BusinessType, on_delete=models.CASCADE)


class RevenueSource(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)


class ExpenseSource(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
