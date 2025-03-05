# Generated by Django 5.1.6 on 2025-03-05 10:17

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('1', 'Active'), ('2', 'Inactive')], default=1, max_length=2)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('job_type', models.CharField(max_length=100)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_of_start', models.DateField()),
                ('date_of_end', models.DateField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('terminated', 'Terminated')], default='active', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('salary', 'Salary Payment'), ('rent', 'Office Rent'), ('utilities', 'Utilities (Water, Electricity, Internet)'), ('supplies', 'Office Supplies'), ('transport', 'Transport & Fuel'), ('marketing', 'Marketing & Advertising'), ('others', 'Other Expenses')], default='others', max_length=20)),
                ('income_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paid_client', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_spent', models.DateField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction', models.CharField(max_length=250)),
                ('customer', models.CharField(max_length=300)),
                ('total', models.FloatField(default=0)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debtor_name', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('debt_type', models.CharField(choices=[('owed_to_me', 'Ninadai'), ('owed_by_me', 'Ninadaiwa')], max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Not Paid'), ('partially_paid', 'Payment Started'), ('paid', 'Full Paid')], default='pending', max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_issued', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_no', models.CharField(max_length=50, unique=True)),
                ('designation', models.CharField(max_length=255)),
                ('duty_station', models.CharField(max_length=255)),
                ('working_days', models.IntegerField(default=0)),
                ('fair_salary', models.FloatField(default=0)),
                ('basic_salary', models.FloatField(default=0)),
                ('penalty_charges', models.FloatField(default=0)),
                ('mid_month_advance', models.FloatField(default=0)),
                ('net_salary', models.FloatField(default=0)),
                ('bank_account', models.CharField(blank=True, max_length=100, null=True)),
                ('bank_branch', models.CharField(blank=True, max_length=100, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imsApp.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('description', models.TextField()),
                ('price', models.FloatField(default=0)),
                ('b_price', models.FloatField(default=0)),
                ('s_price', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('1', 'Active'), ('2', 'Inactive')], default='1', max_length=2)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='imsApp.category')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=300)),
                ('phone_number', models.CharField(max_length=13)),
                ('email', models.EmailField(max_length=254)),
                ('price', models.FloatField(default=0)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('product_purchased', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_purchased', to='imsApp.product')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('type', models.CharField(choices=[('1', 'Stock-in'), ('2', 'Stock-Out')], default=1, max_length=2)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imsApp.product')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('quantity', models.FloatField(default=0)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imsApp.invoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imsApp.product')),
                ('stock', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='imsApp.stock')),
            ],
        ),
    ]
