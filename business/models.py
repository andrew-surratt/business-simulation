from django.db import models

class BusinessType(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self): return self.name

class Business(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    type = models.ForeignKey(BusinessType, on_delete=models.CASCADE)

    def __str__(self): return self.name

class Frequency(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    interval_in_days = models.IntegerField(null=True, blank=True)

    def __str__(self): return self.name

class Currency(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self): return self.name

class RevenueSource(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    business = models.ForeignKey(Business, null=True, on_delete=models.CASCADE)
    frequency = models.ForeignKey(Frequency, null=True, on_delete=models.CASCADE)
    amount = models.FloatField(null=True, blank=True)
    currency = models.ForeignKey(Currency, null=True, on_delete=models.CASCADE)

    def __str__(self): return self.name

class ExpenseSource(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    business = models.ForeignKey(Business, null=True, on_delete=models.CASCADE)
    frequency = models.ForeignKey(Frequency, null=True, on_delete=models.CASCADE)
    amount = models.FloatField(null=True, blank=True)
    currency = models.ForeignKey(Currency, null=True, on_delete=models.CASCADE)

    def __str__(self): return self.name
