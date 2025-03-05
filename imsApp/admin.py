from django.contrib import admin
from .models import Category, Debt, Expenditure, Employee, Product, Stock, Invoice, Invoice_Item, Payroll,Customer

# Register models here

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'date_created', 'date_updated')
    search_fields = ('name',)

@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('debtor_name', 'amount', 'debt_type', 'status', 'due_date')
    list_filter = ('status', 'debt_type')
    search_fields = ('debtor_name',)

@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ('description', 'category', 'date_spent','income_amount','paid_client')
    list_filter = ('category',)
    search_fields = ('description',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'status', 'salary','job_type','date_of_start','date_of_end')
    list_filter = ('status',)
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'buying_price', 'selling_price', 'status', 'date_created')
    list_filter = ('status',)
    search_fields = ('code', 'name')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'type', 'date_created')
    list_filter = ('type',)
    search_fields = ('product__name',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'customer', 'total', 'date_created')
    search_fields = ('transaction', 'customer')

@admin.register(Invoice_Item)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'product', 'quantity', 'price')
    search_fields = ('invoice__transaction', 'product__name')

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'reg_no', 'designation', 'duty_station','net_salary', 
                    'date_created','working_days','fair_salary','basic_salary','penalty_charges',
                    'mid_month_advance','bank_account','bank_branch')
    search_fields = ('employee__first_name', 'employee__last_name', 'reg_no')

    
@admin.register(Customer)
class CstomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email', 'product_purchased','date_created','price')
    search_fields = ('full_name', 'Phone_number', 'date_created','email','price')
