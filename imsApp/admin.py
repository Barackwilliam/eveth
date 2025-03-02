from django.contrib import admin
from imsApp.models import Category, Product, Stock, Invoice, Invoice_Item
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(Invoice)
admin.site.register(Invoice_Item)

from .models import Debt

@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('debtor_name', 'amount', 'debt_type', 'status', 'due_date')
    list_filter = ('status', 'debt_type')
    search_fields = ('debtor_name',)

from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'phone_number', 'salary', 'status', 'date_hired')
    list_filter = ('status', 'position')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')

from .models import Expenditure

@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ('description', 'category', 'amount', 'date_spent', 'created_at')
    list_filter = ('category', 'date_spent')
    search_fields = ('description',)


