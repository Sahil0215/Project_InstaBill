# Generated by Django 5.1 on 2024-09-02 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0037_profile_cash_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='invoice_to',
            new_name='payment_of',
        ),
    ]
