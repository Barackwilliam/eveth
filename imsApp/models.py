from re import I
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from more_itertools import quantify
from django.db.models import Sum
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


    

class Invoice(models.Model):
    transaction = models.CharField(max_length = 250)
    customer = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Add this field
    email = models.EmailField(null=True, blank=True)


    total = models.FloatField(default= 0)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction

    def item_count(self):
        return Invoice_Item.objects.filter(invoice = self).aggregate(Sum('quantity'))['quantity__sum']




# my mod

class Debt(models.Model):
    DEBT_TYPE_CHOICES = [
        ('owed_to_me', 'Ninadai'),  # Madeni unayodai
        ('owed_by_me', 'Ninadaiwa') # Madeni unayodaiwa
    ]

    STATUS_CHOICES = [
        ('pending', 'Not Paid'),
        ('partially_paid', 'Payment Started'),
        ('paid', 'Full Paid')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='debts')  # Mtumiaji anayehusika na deni
    debtor_name = models.CharField(max_length=255)  # Jina la anayehusika na deni (ikiwa si mtumiaji wa mfumo)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Kiasi cha deni
    debt_type = models.CharField(max_length=20, choices=DEBT_TYPE_CHOICES)  # Aina ya deni
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Hali ya deni
    description = models.TextField(blank=True, null=True)  # Maelezo kuhusu deni
    date_issued = models.DateField(auto_now_add=True)  # Tarehe deni lilipoingizwa
    due_date = models.DateField(null=True, blank=True)  # Tarehe ya mwisho wa kulipa

    def __str__(self):
        return f"{self.debtor_name} - {self.amount} ({self.get_debt_type_display()})"



class Expenditure(models.Model):
    CATEGORY_CHOICES = [
        ('salary', 'Salary Payment'),
        ('rent', 'Office Rent'),
        ('utilities', 'Utilities (Water, Electricity, Internet)'),
        ('supplies', 'Office Supplies'),
        ('transport', 'Transport & Fuel'),
        ('marketing', 'Marketing & Advertising'),
        ('others', 'Other Expenses'),
    ]

    description = models.CharField(max_length=255)  # Short description of the expense
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='others')  # Expense category
    income_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Expense amount
    paid_client = models.DecimalField(max_digits=10, decimal_places=2)
    date_spent = models.DateField(auto_now_add=True)  # Date of expenditure
    created_at = models.DateTimeField(auto_now_add=True)  # Record creation time
    updated_at = models.DateTimeField(auto_now=True)  # Last updated time

    def __str__(self):
        return f"{self.description} - {self.income_amount} TZS"



class Employee(models.Model):
    EMPLOYMENT_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('terminated', 'Terminated'),
    ]

    first_name = models.CharField(max_length=100)  # Jina la kwanza
    last_name = models.CharField(max_length=100)  # Jina la mwisho
    phone_number = models.CharField(max_length=15, unique=True)  # Namba ya simu
    email = models.EmailField(unique=True)  # Barua pepe
    job_type = models.CharField(max_length=100)  # Cheo / Kazi
    salary = models.DecimalField(max_digits=10, decimal_places=2)  # Mshahara
    date_of_start = models.DateField()  # Tarehe ya kuajiriwa
    date_of_end = models.DateField()  # Tarehe ya kuajiriwa

    status = models.CharField(max_length=10, choices=EMPLOYMENT_STATUS, default='active')  # Hali ya kazi

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_type}"



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    code=models.CharField(max_length=100,blank=True, null=True)
    name=models.CharField(max_length=250,blank=True, null=True)
    description = models.TextField()
    buying_price = models.FloatField(default=0)
    selling_price = models.FloatField(default=0)
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default='1')

    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code or 'N/A'} - {self.name or 'Unnamed'}"

    def count_inventory(self):
        stocks = Stock.objects.filter(product = self)
        stockIn = 0
        stockOut = 0
        for stock in stocks:
            if stock.type == '1':
                stockIn = int(stockIn) + int(stock.quantity)
            else:
                stockOut = int(stockOut) + int(stock.quantity)
        available  = stockIn - stockOut
        return available
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    type = models.CharField(max_length=2, choices=(('1', 'Stock-in'), ('2', 'Stock-Out')), default='1')
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        product_code = self.product.code if self.product and self.product.code else "NoCode"
        product_name = self.product.name if self.product and self.product.name else "NoName"
        return f"{product_code} - {product_name}"

class Invoice_Item(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, blank= True, null= True)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)

    def __str__(self):
        return self.invoice.transaction


@receiver(models.signals.post_save, sender=Invoice_Item)
def stock_update(sender, instance, **kwargs):
    stock = Stock(product = instance.product, quantity = instance.quantity, type = 2)
    stock.save()
    # stockID = Stock.objects.last().id
    Invoice_Item.objects.filter(id= instance.id).update(stock=stock)

@receiver(models.signals.post_delete, sender=Invoice_Item)
def delete_stock(sender, instance, **kwargs):
    try:
        stock = Stock.objects.get(id=instance.stock.id).delete()
    except:
        return instance.stock.id




#payroll

from django.db import models
from django.db import models
from django.utils import timezone

class Payroll(models.Model):
    employee = models.CharField(max_length=255)
    reg_no = models.CharField(max_length=50, unique=True)  # Namba ya Usajili
    designation = models.CharField(max_length=255)  # Cheo
    duty_station = models.CharField(max_length=255)  # Kituo cha Kazi
    working_days = models.IntegerField(default=0)  # Siku za Kazi
    fair_salary = models.FloatField(default=0)  # Malipo ya Haki
    basic_salary = models.FloatField(default=0)  # Mshahara wa Msingi
    penalty_charges = models.FloatField(default=0)  # Makato ya Adhabu
    mid_month_advance = models.FloatField(default=0)  # Mkopo wa Mwezi
    net_salary = models.FloatField(default=0)  # Mshahara Halisi
    bank_account = models.CharField(max_length=100, blank=True, null=True)  # Akaunti ya Benki
    bank_branch = models.CharField(max_length=100, blank=True, null=True)  # Tawi la Benki
    date_created = models.DateTimeField(default=timezone.now)  # Tarehe ya Kuongezwa

    
    def __str__(self):
        return self.employee

    
class Customer(models.Model):
    full_name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=13)
    email = models.EmailField()
    product_purchased = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_purchased')
    price = models.FloatField(default=0)
    date_created = models.DateTimeField(default=timezone.now)  # Tarehe ya Kuongezwa


    def get_product_price(self):
        return self.product_purchased.selling_price

    def __str__(self):
        return f"{self.full_name} - {self.product_purchased.selling_price}"
    
