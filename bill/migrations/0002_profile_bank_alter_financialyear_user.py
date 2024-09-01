# Generated by Django 5.1 on 2024-08-23 07:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('gst', models.CharField(max_length=20)),
                ('adrs', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bill_count', models.IntegerField()),
                ('cash', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=255)),
                ('acno', models.CharField(max_length=20)),
                ('branch', models.TextField()),
                ('ifsc', models.CharField(max_length=15)),
                ('bal', models.DecimalField(decimal_places=2, max_digits=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill.profile')),
            ],
        ),
        migrations.AlterField(
            model_name='financialyear',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill.profile'),
        ),
    ]
