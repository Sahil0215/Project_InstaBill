# Generated by Django 5.1 on 2024-09-01 17:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0034_invoicepurchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicepurchase',
            name='invoice_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billtopurchase', to='bill.customer'),
        ),
    ]
