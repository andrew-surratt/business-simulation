# Generated by Django 5.2 on 2025-04-19 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_currency_frequency_expensesource_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='symbol',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
